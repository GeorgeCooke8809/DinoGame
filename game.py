import functions
import pygame
import random
import math as maths

pygame.init()

dino = pygame.transform.scale(pygame.image.load("Sprites/dino.png"), (50, 50))

obstacle_1 = pygame.transform.scale(pygame.image.load("Sprites/obs1.png"), (50, 50))
obstacle_2 = pygame.transform.scale(pygame.image.load("Sprites/obs2.png"), (50, 75))
flyer = pygame.transform.scale(pygame.image.load("Sprites/fly.png"), (50, 50))

root = pygame.display.set_mode((1000,400))

running = True

clock = pygame.time.Clock()
delta_time = 0.1
score = 0

obstacles = [] # [type, x]
last_obstacle = -30

def get_speed(score):
    return (maths.sqrt(score+1)*25)+50

def get_dino_height(last_jump, score): # TODO: this is very wrong
    x = score - last_jump
    y = (((6.5*x)-11.2)**2)+75
    y = max(75, min(200, y))

    return y

collided = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    last_jump = -50

    #collided = False

    while collided == False:
        score += 3 * delta_time
        root.fill((0,0,0))

        dino_y = get_dino_height(last_jump, score)

        root.blit(dino, (150, dino_y))
        dino_hitbox = pygame.Rect(150, dino_y, dino.get_width(), dino.get_height())

        if score >= last_obstacle + (1200 / get_speed(score)):
            spawn = random.randint(0, 100)
            if spawn <= 60:
                if score >= 400:
                    obstacle_type = random.randint(0,150)
                else:
                    obstacle_type = random.randint(0,100)
                
                if obstacle_type <= 50:
                    obstacles.append(["OBS1", 1000])
                elif obstacle_type <= 100:
                    obstacles.append(["OBS1", 1000])
                elif obstacle_type <= 150:
                    obstacles.append(["FLY", 1000])


                last_obstacle = score
            else:
                last_obstacle += (90 / get_speed(score)) * delta_time

        index = 0

        for obstacle in obstacles:
            if obstacle[0] == "OBS1":
                root.blit(obstacle_1, (obstacle[1], 200))
                if obstacle[1]<=200 and obstacle[1]+50>=150 and dino_y+50 >= 200:
                    collided = True
            elif obstacle[0] == "OBS2":
                root.blit(obstacle_2, (obstacle[1], 175))
                if obstacle[1]<=200 and obstacle[1]+50>=150 and dino_y+50 >= 175:
                    collided = True
            elif obstacle[0] == "FLY":
                root.blit(flyer, (obstacle[1], 125))
                if obstacle[1]<=200 and obstacle[1]+50>=150 and 125 >= dino_y+50 and 75 <= dino_y + 50: # TODO: might need fixing at higher scores
                    collided = True

            obstacles[index][1] -= get_speed(score) * delta_time
            index += 1



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    last_jump = score

        pygame.display.flip()

        delta_time = clock.tick(75) / 1000
        delta_time = max(0.001, min(0.5, delta_time))

pygame.quit()