import pygame
import random

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Enhanced Dino Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Load images
try:
    dino_image = pygame.image.load("dino.png").convert_alpha()
    dino_image = pygame.transform.scale(dino_image, (50, 50))
    cactus_images = [
        pygame.transform.scale(pygame.image.load("cactus1.png").convert_alpha(), (30, 50)),
        pygame.transform.scale(pygame.image.load("cactus2.png").convert_alpha(), (30, 60))
    ]
    ground_image = pygame.image.load("ground.png").convert_alpha()
    ground_image = pygame.transform.scale(ground_image, (WIDTH, 20))
except:
    print("Image files not found. Make sure to have 'dino.png', 'cactus1.png', 'cactus2.png', and 'ground.png' in the same folder.")
    dino_image = pygame.Surface((50, 50))
    dino_image.fill((0, 0, 255))  # Blue color for dino if image not found
    cactus_images = [pygame.Surface((30, 50)), pygame.Surface((30, 60))]
    cactus_images[0].fill((255, 0, 0))  # Red for cactus1 if image not found
    cactus_images[1].fill((0, 255, 0))  # Green for cactus2 if image not found
    ground_image = pygame.Surface((WIDTH, 20))
    ground_image.fill((139, 69, 19))  # Brown color for ground if image not found

# Dino settings
dino_x, dino_y = 40, HEIGHT - 100
dino_vel_y = 0
gravity = 1
jump_height = -15
is_jumping = False

# Obstacle settings
obstacle_x = WIDTH
obstacle_speed = 8
obstacle_image = random.choice(cactus_images)

# Ground settings
ground_y = HEIGHT - 20
ground_x = 0

# Game variables
score = 0
font = pygame.font.Font(None, 66)
clock = pygame.time.Clock()

# Main game loop
running = True
while running:
    screen.fill(WHITE)
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:  # Check for screen tap
            if not is_jumping:
                dino_vel_y = jump_height
                is_jumping = True

    # Dino movement and gravity
    dino_y += dino_vel_y
    dino_vel_y += gravity

    # Check if dino is on the ground
    if dino_y >= HEIGHT - 70:
        dino_y = HEIGHT - 70
        dino_vel_y = 0
        is_jumping = False

    # Obstacle movement and reset
    obstacle_x -= obstacle_speed
    if obstacle_x < -50:
        obstacle_x = WIDTH
        obstacle_image = random.choice(cactus_images)  # Randomize cactus
        score += 1

    # Ground movement
    ground_x -= obstacle_speed
    if ground_x <= -WIDTH:
        ground_x = 0

    # Collision detection
    dino_rect = dino_image.get_rect(topleft=(dino_x, dino_y))
    cactus_rect = obstacle_image.get_rect(topleft=(obstacle_x, HEIGHT - obstacle_image.get_height() - 20))
    if dino_rect.colliderect(cactus_rect):
        print("Game Over")
        running = False

    # Drawing
    screen.blit(ground_image, (ground_x, ground_y))
    screen.blit(ground_image, (ground_x + WIDTH, ground_y))
    screen.blit(dino_image, (dino_x, dino_y))
    screen.blit(obstacle_image, (obstacle_x, HEIGHT - obstacle_image.get_height() - 20))

    # Display score
    score_text = font.render("Score: " + str(score), True, BLACK)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()