import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Super Mario Clone"

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (135, 206, 235)  # Sky blue
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BROWN = (139, 69, 19)
GOLD = (255, 215, 0)

# Player settings
PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60
PLAYER_COLOR = RED
PLAYER_SPEED = 5
JUMP_FORCE = 15
GRAVITY = 0.8

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Goal(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(GOLD)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, distance):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(BROWN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.start_x = x
        self.distance = distance
        self.speed = 2
        self.direction = 1

    def update(self):
        self.rect.x += self.speed * self.direction
        if abs(self.rect.x - self.start_x) > self.distance:
            self.direction *= -1

class Player(pygame.sprite.Sprite):
    def __init__(self, platforms, enemies, goal):
        super().__init__()
        self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        self.image.fill(PLAYER_COLOR)
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = SCREEN_HEIGHT - PLAYER_HEIGHT - 100
        self.velocity_y = 0
        self.on_ground = False
        self.platforms = platforms
        self.enemies = enemies
        self.goal = goal
        self.is_alive = True

    def update(self):
        if not self.is_alive:
            return

        keys = pygame.key.get_pressed()
        
        # Horizontal movement
        if keys[pygame.K_LEFT]:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.rect.x += PLAYER_SPEED

        # Keep within screen bounds
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > SCREEN_WIDTH - PLAYER_WIDTH:
            self.rect.x = SCREEN_WIDTH - PLAYER_WIDTH

        # Jumping
        if keys[pygame.K_SPACE] and self.on_ground:
            self.velocity_y = -JUMP_FORCE
            self.on_ground = False

        # Apply gravity
        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y

        # Collision with platforms
        self.on_ground = False
        hits = pygame.sprite.spritecollide(self, self.platforms, False)
        if hits:
            for platform in hits:
                # Falling down onto a platform
                if self.velocity_y > 0 and self.rect.bottom <= platform.rect.bottom + self.velocity_y:
                    self.rect.bottom = platform.rect.top
                    self.velocity_y = 0
                    self.on_ground = True
                # Jumping up into a platform
                elif self.velocity_y < 0 and self.rect.top >= platform.rect.top + self.velocity_y:
                    self.rect.top = platform.rect.bottom
                    self.velocity_y = 0

        # Ground collision (bottom of screen)
        if self.rect.y >= SCREEN_HEIGHT - PLAYER_HEIGHT:
            self.rect.y = SCREEN_HEIGHT - PLAYER_HEIGHT
            self.velocity_y = 0
            self.on_ground = True

        # Collision with enemies
        enemy_hits = pygame.sprite.spritecollide(self, self.enemies, False)
        if enemy_hits:
            for enemy in enemy_hits:
                # Jump on top of enemy to kill it
                if self.velocity_y > 0 and self.rect.bottom <= enemy.rect.bottom:
                    enemy.kill()
                    self.velocity_y = -JUMP_FORCE / 2 # Bounce off
                else:
                    # Hit by enemy
                    self.is_alive = False
                    print("Game Over!")
                    pygame.quit()
                    sys.exit()
        
        # Collision with goal
        if pygame.sprite.collide_rect(self, self.goal):
            print("You Win!")
            pygame.quit()
            sys.exit()

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(SCREEN_TITLE)

# Clock for controlling frame rate
clock = pygame.time.Clock()
FPS = 60

def main():
    # Create sprite groups
    all_sprites = pygame.sprite.Group()
    platforms = pygame.sprite.Group()
    enemies = pygame.sprite.Group()

    # Create platforms
    # Ground platform
    ground = Platform(0, SCREEN_HEIGHT - 20, SCREEN_WIDTH, 20)
    platforms.add(ground)
    all_sprites.add(ground)

    # Floating platforms
    p1 = Platform(200, 450, 200, 20)
    p2 = Platform(500, 350, 200, 20)
    p3 = Platform(100, 250, 150, 20)
    
    platforms.add(p1, p2, p3)
    all_sprites.add(p1, p2, p3)

    # Create enemies
    e1 = Enemy(250, 420, 100)
    e2 = Enemy(550, 320, 100)
    enemies.add(e1, e2)
    all_sprites.add(e1, e2)

    # Create goal
    goal = Goal(700, 310)
    all_sprites.add(goal)

    player = Player(platforms, enemies, goal)
    all_sprites.add(player)

    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update
        all_sprites.update()

        # Drawing
        screen.fill(BLUE)
        all_sprites.draw(screen)

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
