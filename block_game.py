import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shooting Soldier Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

# Clock for controlling frame rate
clock = pygame.time.Clock()
FPS = 60

# Load soldier image for the player
soldier_image = pygame.image.load("soldier.png")  # Replace with your soldier image file
soldier_image = pygame.transform.scale(soldier_image, (150, 100))

# Load enemy image
enemy_image = pygame.image.load("enemy.png")  # Replace with your enemy image file
enemy_image = pygame.transform.scale(enemy_image, (150, 100))

# Player properties
player_size = soldier_image.get_width()
player_pos = [WIDTH // 2 - player_size // 2, HEIGHT - 100]
player_speed = 7
bullets_left = 6  # Initial bullets

# Enemy properties
enemy_size = enemy_image.get_width()
enemies = [{"pos": [random.randint(0, WIDTH - enemy_size), 0], "health": 2}]
enemy_speed = 2

# Bullet properties
bullet_width, bullet_height = 6, 12
bullets = []
bullet_speed = 10

# Score
score = 0
font = pygame.font.Font(None, 36)

# Function to check collision
def detect_collision(obj1_pos, obj2_pos, obj1_size, obj2_size):
    """Check if two rectangles are colliding."""
    x1, y1 = obj1_pos
    x2, y2 = obj2_pos

    return (
        x1 < x2 + obj2_size and x1 + obj1_size > x2 and
        y1 < y2 + obj2_size and y1 + obj1_size > y2
    )

# Main game loop
running = True
while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and bullets_left > 0:
                # Fire a bullet centered on the soldier
                bullet_x = player_pos[0] + player_size // 2 - bullet_width // 2
                bullet_y = player_pos[1]
                bullets.append([bullet_x, bullet_y])
                bullets_left -= 1  # Decrease bullets when shooting

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_pos[0] -= player_speed
    if keys[pygame.K_RIGHT]:
        player_pos[0] += player_speed

    # Wrap player around the screen
    if player_pos[0] < -player_size:  # If the soldier moves off the left side
        player_pos[0] = WIDTH
    if player_pos[0] > WIDTH:  # If the soldier moves off the right side
        player_pos[0] = -player_size

    # Update bullet positions
    for bullet in bullets[:]:
        bullet[1] -= bullet_speed
        if bullet[1] < 0:  # Remove bullet if it goes off-screen
            bullets.remove(bullet)

    # Update enemy positions
    for enemy in enemies[:]:
        enemy["pos"][1] += enemy_speed

        # Check if enemy goes off-screen
        if enemy["pos"][1] > HEIGHT:
            running = False  # Game over

        # Check for bullet collision
        for bullet in bullets[:]:
            if detect_collision(bullet, enemy["pos"], bullet_width, enemy_size):
                bullets.remove(bullet)
                enemy["health"] -= 1

                # If health is 0, remove the enemy
                if enemy["health"] == 0:
                    enemies.remove(enemy)
                    score += 1
                    bullets_left += 3  # Reward: Gain 3 bullets after killing an enemy

                    # Spawn a new enemy
                    enemies.append({"pos": [random.randint(0, WIDTH - enemy_size), 0], "health": 2})

    # Draw player (soldier character)
    screen.blit(soldier_image, (player_pos[0], player_pos[1]))

    # Draw enemies
    for enemy in enemies:
        screen.blit(enemy_image, (enemy["pos"][0], enemy["pos"][1]))

    # Draw bullets
    for bullet in bullets:
        pygame.draw.rect(screen, YELLOW, (bullet[0], bullet[1], bullet_width, bullet_height))

    # Draw score and bullets left
    score_text = font.render(f"Score: {score}", True, WHITE)
    bullets_text = font.render(f"Bullets: {bullets_left}", True, RED)
    screen.blit(score_text, (10, 10))
    screen.blit(bullets_text, (10, 50))

    pygame.display.flip()
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
sys.exit()
