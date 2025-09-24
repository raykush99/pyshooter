import pygame
import time
import math
import random

pygame.init()

# Setup screen
WIDTH, HEIGHT = 750, 750
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PyShooter")

clock = pygame.time.Clock()

# Define Variables
score = 0
speed = 5
health = 10
number_enemies = 2
timer_speed = 0
timer_fire = 0
time_heart = pygame.time.get_ticks() + random.randint(30000, 60000)

projectiles = []
enemies = []
# Define sprites
player = {
    "name": "user",
    "health": health,
    "position": [WIDTH / 2, HEIGHT / 2],
    "speed": speed,
    "sprite": pygame.image.load("sprites/player.png").convert_alpha()
}
projectile = {
    "name": "bullet",
    "speed": speed * 2,
    "color": [255, 0, 0],
    "rect": [50, 50, 10, 10], # x, y, width, height
}
enemy = {
    "name": "enemy",
    "position": [50, 50],
    "color": [0, 255, 100],
    "radius": 20,
    "speed": 1,
}
heart = {
    "name": "heart",
    "position": [50, 50],
    "sprite": pygame.image.load("sprites/heart.png").convert_alpha(),
    "rect": [0, 0, 0, 0]
}
enemy["position"][0] = random.randint(0 + enemy["radius"], WIDTH - enemy["radius"])
enemy["position"][1] = random.randint(0 + enemy["radius"], HEIGHT - enemy["radius"])
score_font = pygame.font.Font(None, 200)
end_font = pygame.font.Font(None, 100)
end_score_font = pygame.font.Font(None, 50)
score_color = (50, 50, 50)
health_color = (255, 0, 0)
black = (0, 0, 0)
health_active = False
running = True
launch = False
# Game loop
while running:
    screen.fill((30, 30, 30))

#heart
    heart["rect"] = heart["sprite"].get_rect(center=heart["position"])

    if pygame.time.get_ticks() >= time_heart and health_active == False:
        heart["position"] = [random.randint(0 + heart["sprite"].get_width() // 2, WIDTH - heart["sprite"].get_width() // 2), random.randint(0 + heart["sprite"].get_height() // 2, HEIGHT - heart["sprite"].get_height() // 2)]
        health_active = True
    if health_active == True:
        screen.blit(heart["sprite"], (heart["position"][0], heart["position"][1]))
        if heart["rect"].colliderect(player["sprite"].get_rect(center=player["position"])):
            print("Heart collected!")
            health += 1
            time_heart = pygame.time.get_ticks() + random.randint(30000, 60000)
            health_active = False

    screen.blit(score_font.render(f"{score}", True, score_color), score_font.render(f"{score}", True, score_color).get_rect(center=(WIDTH // 2, HEIGHT // 2)))  # Draw at top-left corner

    if score > 5:
        number_enemies = 3
    if score >= 15:
        number_enemies = 4
    if score >= 30:
        number_enemies = 5
    if score >= 60:
        number_enemies = 6
    if score >= 100:
        number_enemies = 8
    if score >= 200:
        number_enemies = 10

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Launch projectile
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            bullet = {
                "name": "bullet",
                "speed": projectile["speed"],
                "color": projectile["color"],
                "rect": [player["position"][0], player["position"][1], 10, 10],
                "angle": angle,
            }
            projectiles.append(bullet)

    for bullet in projectiles[:]:
            pygame.draw.ellipse(screen, bullet["color"], bullet["rect"])
            bullet["rect"][0] += bullet["speed"] * math.cos(math.radians(bullet["angle"]))
            bullet["rect"][1] -= bullet["speed"] * math.sin(math.radians(bullet["angle"]))
            pygame.draw.ellipse(screen, bullet["color"], bullet["rect"])
            if bullet["rect"][0] > WIDTH or bullet["rect"][0] < 0 or bullet["rect"][1] > HEIGHT or bullet["rect"][1] < 0:
                projectiles.remove(bullet)
            for enemy_clone in enemies[:]:
                rect_bullet = pygame.Rect(bullet["rect"])
                rect_enemy = pygame.Rect(enemy_clone["position"][0], enemy_clone["position"][1], enemy["radius"]*2, enemy["radius"]*2)
                if rect_bullet.colliderect(rect_enemy):
                    score += 1
                    try:
                        projectiles.remove(bullet)
                        enemies.remove(enemy_clone)
                    except ValueError:
                        pass
    keys = pygame.key.get_pressed()
# Movement controls
    if keys[pygame.K_w]:
        player["position"][1] -= player["speed"]
    if keys[pygame.K_s]:
        player["position"][1] += player["speed"]
    if keys[pygame.K_a]:
        player["position"][0] -= player["speed"]
    if keys[pygame.K_d]:
        player["position"][0] += player["speed"]
# Speed boost control
    if keys[pygame.K_q]:
        player["speed"] = 20
        timer_speed = pygame.time.get_ticks() + 5000
    if pygame.time.get_ticks() >= timer_speed:
        player["speed"] = 5  # Reset to normal
#Rapid fire
    if keys[pygame.K_1]:
        timer_fire = pygame.time.get_ticks() + 5000
    if pygame.time.get_ticks() <= timer_fire:
        bullet = {
                "name": "bullet",
                "speed": projectile["speed"],
                "color": projectile["color"],
                "rect": [player["position"][0], player["position"][1], 10, 10],
                "angle": angle,
            }
        projectiles.append(bullet)

    
    sprite_width = player["sprite"].get_width()
    sprite_height = player["sprite"].get_height()

    player["position"][0] = max(sprite_width / 2, min(WIDTH - sprite_width / 2, player["position"][0]))
    player["position"][1] = max(sprite_height / 2, min(HEIGHT - sprite_height / 2, player["position"][1]))
    
    sprite_rect = player["sprite"].get_rect(center=player["position"])
    #screen.blit(player["sprite"], sprite_rect)

        # Get mouse position
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Calculate angle between player and mouse
    dx = mouse_x - player["position"][0]
    dy = mouse_y - player["position"][1]
    angle = -math.degrees(math.atan2(dy, dx))  # Negative to rotate correctly

    # Rotate sprite
    rotated_sprite = pygame.transform.rotate(player["sprite"], angle - 90)

    # Get new rect and center it on the player
    rotated_rect = rotated_sprite.get_rect(center=player["position"])
    
    #enemy movement

    if len(enemies) < number_enemies:
        enemy_clone = {
            "name": "enemy_clone",
            "position": [random.randint(0 + enemy["radius"], WIDTH - enemy["radius"]), random.randint(0 + enemy["radius"], HEIGHT - enemy["radius"])],
            "color": enemy["color"],
            "radius": enemy["radius"],
            "speed": enemy["speed"],
        }
        enemies.append(enemy_clone)
    for enemy_clone in enemies[:]:
        if enemy_clone["position"][0] < player["position"][0]:
            enemy_clone["position"][0] += enemy_clone["speed"]
        elif enemy_clone["position"][0] > player["position"][0]:
            enemy_clone["position"][0] -= enemy_clone["speed"]
        else:
            enemy_clone["position"][0] += 0

        if enemy_clone["position"][1] < player["position"][1]:
            enemy_clone["position"][1] += enemy_clone["speed"]
        elif enemy_clone["position"][1] > player["position"][1]:
            enemy_clone["position"][1] -= enemy_clone ["speed"]
        else:
            enemy_clone["position"][1] += 0
        pygame.draw.circle(screen, enemy_clone["color"], enemy_clone["position"], enemy_clone["radius"])
        rect_enemy = pygame.Rect(enemy_clone["position"][0], enemy_clone["position"][1], enemy["radius"]*2, enemy["radius"]*2)
        if rect_enemy.colliderect(sprite_rect):
                    print("Got attacked!")
                    health -= 1
                    try:
                        enemies.remove(enemy_clone)
                    except ValueError:
                        pass

    # Draw it
    screen.blit(rotated_sprite, rotated_rect)
    if health < 10:
        pygame.draw.rect(screen, health_color, (player["position"][0] - sprite_width / 4, player["position"][1] - sprite_height / 2, health * 5, 5))
    if health <= 0:
        screen.fill((100, 0, 0))
        screen.blit(end_font.render(f"GAME OVER!", True, black), end_font.render(f"GAME OVER!", True, black).get_rect(center=(WIDTH // 2, HEIGHT // 2)))
        screen.blit(end_score_font.render(f"Final Score: {score}", True, black), end_score_font.render(f"Final Score: {score}", True, black).get_rect(center=(WIDTH // 2, HEIGHT // 2 + 200)))
    pygame.display.flip()  
    print(health_active)       
    clock.tick(60)

pygame.quit()