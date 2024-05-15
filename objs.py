import pygame
from random import randint
import copy
import os
import datetime

class Bird(pygame.Rect):
 
    TERMINAL_VELOCITY = 15
    gravity = 0.5
    r = 25

    def __init__(self, x, y, screen: pygame.Surface):
        self.pos = pygame.Vector2(x,y)
        self.orginal_pos = pygame.Vector2(x,y)

        self.hitbox = pygame.Rect(self.pos.x-self.r, self.pos.y-self.r, self.r*2, self.r*2)
        self.draw_hitbox = False

        self.velocity = 0
        self.screen = screen

    def show(self):
        pygame.draw.circle(self.screen, "darkgoldenrod2", self.pos, self.r)
        if self.draw_hitbox:
            pygame.draw.rect(self.screen, "red", self.hitbox, width=3)
    
    def update(self):
        if self.velocity < self.TERMINAL_VELOCITY:
            self.velocity += self.gravity
        self.pos.y += self.velocity

        if self.pos.y > self.screen.get_height() - self.r:
            self.pos.y = self.screen.get_height() - self.r
            self.velocity = 0
        
        if self.pos.y - self.r < 0:
            self.pos.y = 0 + self.r
            self.velocity = 0
        
        self.update_hitbox()
    
    def update_hitbox(self):
        self.hitbox = pygame.Rect(self.pos.x-self.r, self.pos.y-self.r, self.r*2, self.r*2)
    
    def up(self):
        self.velocity -= self.TERMINAL_VELOCITY*0.7
    
    def reset(self):
        self.velocity = 0
        self.pos = copy.deepcopy(self.orginal_pos)

class Pipe():

    w = 60
    speed = 5

    def __init__(self, x, y, gap_size, screen:pygame.Surface):
        self.screen = screen
        
        self.x = x - self.w/2
        self.y = y

        self.gap = randint(int(Bird.r*2*gap_size[0]), int(Bird.r*2*gap_size[1]))
        #print(self.gap)

        self.top_pipe = pygame.Rect(self.x, 0, self.w, self.y - (self.gap/2))
        self.bottom_pipe = pygame.Rect(self.x, self.y + self.gap/2, self.w, self.screen.get_height() - self.y + self.gap/2)
        self.rect_colour = "darkolivegreen3"
        
        self.scored = False
    
    def show(self):

        pygame.draw.rect(self.screen, self.rect_colour, self.top_pipe)
        pygame.draw.rect(self.screen, self.rect_colour, self.bottom_pipe)
    
    def update(self):
        self.x -= self.speed
        self.top_pipe.x -= self.speed
        self.bottom_pipe.x -= self.speed
    
    def hit(self, bird: Bird):
        if self.bottom_pipe.colliderect(bird.hitbox) or self.top_pipe.colliderect(bird.hitbox):
            self.rect_colour = "red"
            return True
    
class Score():

    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 50)
        self.score = 0
        self.x = self.screen.get_width()/2
        self.y = 10
    
    def show(self):
        text = self.font.render(f"{self.score}", True, "black")
        self.screen.blit(text, (self.x, self.y))
    
    def score_up(self):
        self.score += 1
    
    def reset(self):
        self.score = 0


    def render_leaderboard(self):
        """
        Structured as Name - Score - Date and time
        """
        self.screen.fill("white")

        leaderboard = self.read_leaderboard()
        if not leaderboard:
            leaderboard.append(["No Scores Recorded", ""])

        leaderboard_font = pygame.font.SysFont("Arial", 40)
        leaderboard_font_date = pygame.font.SysFont("Arial", 10)

        for i in range(min(10, len(leaderboard))):
            text = leaderboard_font.render(f"{i+1}. {leaderboard[i][0]} - {leaderboard[i][1]}", True, "black")
            date_text = leaderboard_font_date.render(f"{leaderboard[i][2]}", True, "black")
            self.screen.blit(text, (self.screen.get_width()/2 - text.get_width()/2, self.y + (i+1)*60))
            self.screen.blit(date_text, (self.screen.get_width()/2 - date_text.get_width()/2, self.y + (i+1)*60 + 50))
        
        restart_text = leaderboard_font.render("Press R to Restart", True, "black")
        self.screen.blit(restart_text, (self.screen.get_width()/2 - restart_text.get_width()/2, self.y + (i+4)*60))

        pygame.display.flip()

        self.write_leaderboard(leaderboard)

        waiting_for_input = True
        while waiting_for_input:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        waiting_for_input = False
                    if event.key == pygame.K_q:
                        pygame.quit()
                        exit()
    
    def update_leaderboard(self, name):
        if self.score > 0:
            with open("resources\leaderboard.txt", "a") as f:
                f.write(f"{name} - {self.score} - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    @staticmethod
    def write_leaderboard(leaderboard):
        with open("resources\leaderboard.txt", "w") as f:
            for name, score, date in leaderboard:
                f.write(f"{name} - {score} - {date}\n")
        
    @staticmethod
    def read_leaderboard():
        """
        Structured as Name - Score - Date and time
        """
        leaderboard = []
        if os.path.exists("resources\leaderboard.txt"):
            with open("resources\leaderboard.txt", "r") as f:
                lines = f.readlines()
                for line in lines:
                    leaderboard.append([x.strip() for x in line.split(" - ")])
        else:
            return []

        leaderboard.sort(key=lambda x: (-int(x[1]), datetime.datetime.strptime(x[2], '%Y-%m-%d %H:%M:%S')))
        return leaderboard