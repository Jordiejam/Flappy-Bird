import pygame
import sys
from objs import Bird, Pipe, Score
from random import randint

def reset(b:Bird, s:Score):
    b.reset()
    s.reset()
    Pipe.speed = 5

def game_over(screen:pygame.Surface, scoreboard:Score):
    h = screen.get_height()*0.2
    
    font = pygame.font.SysFont(None, 55)
    text = font.render("Game Over", True, (255, 0, 0))
    screen.blit(text, (width // 2 - text.get_width()/2, h))

    score_text = font.render(f"Score: {scoreboard.score}", True, (255, 255, 255))
    screen.blit(score_text, (width // 2 - score_text.get_width()/2, h + text.get_height() + 10))

    restart_text = font.render("Press R to Restart", True, (255, 255, 255))
    screen.blit(restart_text, (width // 2 - restart_text.get_width()/2, h + score_text.get_height() * 2 + 20))

    leaderboard_text = font.render("Press L to View Leaderboard", True, (255, 255, 255))
    screen.blit(leaderboard_text, (width // 2 - leaderboard_text.get_width()/2, h + score_text.get_height() * 3 + 30))

    pygame.display.flip()

    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting_for_input = False
                if event.key == pygame.K_l:
                    waiting_for_input = False
                    scoreboard.render_leaderboard()
                if event.key == pygame.K_q:
                    pygame.quit()
                    exit()
                
# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode([1200/2.2, 1920/2.2])
clock = pygame.time.Clock()
width = screen.get_width()
height = screen.get_height()
center = pygame.Vector2(width/2, height/2)

# Setup
bird = Bird(width/5, height/2, screen)
scoreboard = Score(screen)
pipes:list[Pipe] = []

PLAYER_NAME = "Jordiejam"

# Game Loop
running = True
iteration = 0
difficulty_increased = False
difficulty_modifier = 0
pipe_gap_size = (4, 7)
pipe_gap_variation = 0.5
while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird.up()
            if event.key == pygame.K_F2:
                bird.draw_hitbox = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_F2:
                bird.draw_hitbox = False

    screen.fill("cyan4")

    bird.update()
    bird.show()
    
    if iteration % (100-difficulty_modifier) == 0:
        if pipes:
            last_y = pipes[-1].y
            pipe_y = min(max(height*0.20,randint(int(last_y - height*pipe_gap_variation), int(last_y + height*pipe_gap_variation))), height*0.80)
        else:
            pipe_y = randint(int(height*0.2), int(height*0.8))
        pipes.append(Pipe(width+Pipe.w, pipe_y, pipe_gap_size, screen))
    
    if scoreboard.score and scoreboard.score % 3 == 0:
        if not difficulty_increased:
            if difficulty_modifier < 5:
                difficulty_modifier += 1
            elif difficulty_modifier < 10:
                pipe_gap_size = (3.5, 6.5)
                difficulty_modifier += 2
            elif difficulty_modifier < 20:
                pipe_gap_size = (3, 6)
                pipe_gap_variation = 0.3
                difficulty_modifier += 3
            elif difficulty_modifier < 40:
                pipe_gap_size = (2.75, 5.5)
                pipe_gap_variation = 0.4
                difficulty_modifier += 4
            elif difficulty_modifier < 70:
                pipe_gap_size = (2.5, 5 )
                pipe_gap_variation = 0.5
                difficulty_modifier += 5
            
            iteration -= 20

            if Pipe.speed <= 7:
                Pipe.speed += 0.1
            
            difficulty_increased = True
    else:
        difficulty_increased = False

    
    for i in range(len(pipes)-1, -1, -1):

        pipes[i].update()
        pipes[i].show()

        if not pipes[i].scored:
            if bird.pos.x-bird.r > pipes[i].x:
                pipes[i].scored = True
                scoreboard.score += 1

        if pipes[i].hit(bird):
            scoreboard.update_leaderboard(PLAYER_NAME)
            game_over(screen, scoreboard)
            reset(bird, scoreboard)
            difficulty_modifier = 0
            difficulty_increased = False
            pipes = []
            break

        if pipes[i].x < -pipes[i].w:
            pipes.pop(i)

    scoreboard.show()
    # Flip the display
    pygame.display.flip()
    # Cap the frame rate to 60 fps
    clock.tick(60)
    iteration += 1

# Done! Time to quit.
pygame.quit()
sys.exit()
