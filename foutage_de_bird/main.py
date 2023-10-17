import pygame
from sys import exit
import random

import Pipe
from Bird import Bird, bird_images
from Ground import Ground, ground_image, skyline_image
from Ground import win_height, win_width
from Pipe import Pipe, bottom_pipe_image, top_pipe_image, score_update


pygame.init()
pygame.display.set_caption("Foutage de bird")
clock = pygame.time.Clock()


# Window
window = pygame.display.set_mode((win_width, win_height))

# Images
game_over_image = pygame.image.load("assets/game_over.png")
start_image = pygame.image.load("assets/start.png")

# Game
font = pygame.font.SysFont('Segoe', 26)
game_stopped = True


def quit_game():
    # Exit Game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()


# Game Main Method
def main():
    # Instantiate Bird
    bird = pygame.sprite.GroupSingle()
    bird.add(Bird())

    # Setup Pipes
    pipe_timer = 0
    score = 0
    pipes = pygame.sprite.Group()

    # Instantiate Initial Ground
    x_pos_ground, y_pos_ground = 0, 520
    ground = pygame.sprite.Group()
    ground.add(Ground(x_pos_ground, y_pos_ground))

    run = True
    while run:
        # Quit
        quit_game()

        # Reset Frame
        window.fill((0, 0, 0))

        # User Input
        user_input = pygame.key.get_pressed()

        # Draw Background
        window.blit(skyline_image, (0, 0))

        # Spawn Ground
        if len(ground) <= 2:
            ground.add(Ground(win_width, y_pos_ground))

        # Draw - Pipes, Ground and Bird
        pipes.draw(window)
        ground.draw(window)
        bird.draw(window)

        # Show Score
        score = score_update(score)
        score_text = font.render('Score: ' + str(score), True, pygame.Color(255, 255, 255))
        window.blit(score_text, (20, 20))

        # Update - Pipes, Ground and Bird
        if bird.sprite.alive:
            pipes.update()
            ground.update()
        bird.update(user_input)

        # Collision Detection
        collision_pipes = pygame.sprite.spritecollide(bird.sprites()[0], pipes, False)
        collision_ground = pygame.sprite.spritecollide(bird.sprites()[0], ground, False)
        if collision_pipes or collision_ground:
            bird.sprite.alive = False
            if collision_ground:
                window.blit(game_over_image, (win_width // 2 - game_over_image.get_width() // 2,
                                              win_height // 2 - game_over_image.get_height() // 2))
                if user_input[pygame.K_r]:
                    score = 0
                    break

        # Spawn Pipes
        if pipe_timer <= 0 and bird.sprite.alive:
            x_top, x_bottom = 550, 550
            y_top = random.randint(-600, -480)
            y_bottom = y_top + random.randint(90, 130) + bottom_pipe_image.get_height()
            pipes.add(Pipe(x_top, y_top, top_pipe_image, 'top'))
            pipes.add(Pipe(x_bottom, y_bottom, bottom_pipe_image, 'bottom'))
            pipe_timer = random.randint(90, 250)
        pipe_timer -= 1

        clock.tick(60)
        pygame.display.update()


# Menu
def menu():
    global game_stopped

    while game_stopped:
        quit_game()

        # Draw Menu
        window.fill((0, 0, 0))
        window.blit(skyline_image, (0, 0))
        window.blit(ground_image, Ground(0, 520))
        window.blit(bird_images[0], (100, 250))
        window.blit(start_image, (win_width // 2 - start_image.get_width() // 2,
                                  win_height // 2 - start_image.get_height() // 2))

        # User Input
        user_input = pygame.key.get_pressed()
        if user_input[pygame.K_SPACE]:
            main()

        pygame.display.update()


menu()