import pygame
import math as m
import random
from pygame import mixer


class SpaceDeltaForce:
    def __init__(self):
        # Initialize pygame
        pygame.init()

        # Creating Screen
        self.screen = pygame.display.set_mode((800, 600))

        # background
        self.bgImg = pygame.image.load("Resources/img/bgimg.png")

        # Background Music
        mixer.music.load("Resources/sound/background.wav")
        mixer.music.play(-1)

        # Adding title and icon
        pygame.display.set_caption("Space Delta Force")
        self.icon = pygame.image.load("Resources/img/icon.png")
        pygame.display.set_icon(self.icon)

        # Player Score
        self.score = 0

        # Sound effects
        self.bullet_sound = pygame.mixer.Sound("Resources/sound/laser.wav")
        self.collision_sound = pygame.mixer.Sound("Resources/sound/collision.wav")

        # Fonts
        self.score_font = pygame.font.Font("freesansbold.ttf", 24)
        self.game_over_font = pygame.font.Font("freesansbold.ttf", 64)
        self.replay_font = pygame.font.Font("freesansbold.ttf", 16)

        # Creating Player
        self.playerImg = pygame.image.load("Resources/img/player.png")
        self.playerX = 370
        self.playerY = 500
        self.playerX_change = 0

        # Creating Enemies
        self.enemyImg = []
        self.enemyX = []
        self.enemyY = []
        self.enemyX_change = []
        self.enemyY_change = []
        self.no_of_enemies = 7
        self.create_enemies()

        # Creating Bullets
        self.bulletImg = pygame.image.load("Resources/img/bullets.png")
        self.bulletX = 0
        self.bulletY = 480
        self.bulletX_change = 0
        self.bulletY_change = 2
        self.bullet_state = "ready"

        # Game Loop
        self.running = True
        self.game_over = False

    def create_enemies(self):
        for i in range(self.no_of_enemies):
            self.enemyImg.append(pygame.image.load("Resources/img/enemy.png"))
            self.enemyX.append(random.randint(0, 736))
            self.enemyY.append(random.randint(50, 150))
            self.enemyX_change.append(1)
            self.enemyY_change.append(64)

    def is_collision(self, bulletX, bulletY, enemyX, enemyY):
        distance = m.sqrt((m.pow(bulletX - enemyX, 2)) + (m.pow(bulletY - enemyY, 2)))
        if distance <= 27:
            return True
        return False

    def end_game(self):
        game_over = self.game_over_font.render("GAME OVER", True, (255, 0, 0))
        self.screen.blit(game_over, (200, 200))
        replay_message = self.replay_font.render("[Press SPACE To Replay or ESC to Quit]", True, (225, 191, 0))
        self.screen.blit(replay_message, (245, 270))

    # Reset Game
    def reset(self):
        self.playerX = 370
        self.playerY = 500
        self.playerX_change = 0
        self.enemyImg = []
        self.enemyX.clear()
        self.enemyY.clear()
        self.enemyX_change.clear()
        self.enemyY_change.clear()
        self.create_enemies()
        self.bulletX = 0
        self.bulletY = 480
        self.bullet_state = "ready"
        self.score = 0
        self.game_over = False

    # Draw Player
    def player(self, x, y):
        self.screen.blit(self.playerImg, (x, y))

    # Draw enemy
    def enemy(self, x, y, i):
        self.screen.blit(self.enemyImg[i], (x, y))

    # Fire Bullet
    def fire_bullet(self, x, y):
        self.bullet_state = "fire"
        self.screen.blit(self.bulletImg, (x + 16, y + 10))

    def run(self):
        while self.running:
            self.screen.fill((0, 0, 0))

            # Draw Background
            self.screen.blit(self.bgImg, (0, 0))
            total_score = self.score_font.render("Score : " + str(self.score), True, (255, 91, 0))
            self.screen.blit(total_score, (15, 10))

            # Event Listener
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    if event.key == pygame.K_LEFT:
                        self.playerX_change = -1.7
                        print("Left Shift.")
                    if event.key == pygame.K_RIGHT:
                        self.playerX_change = 1.7
                        print("Right Shift.")
                    if event.key == pygame.K_LCTRL:
                        if self.bullet_state == "ready":
                            self.bulletX = self.playerX
                            self.bullet_sound.play()
                            self.fire_bullet(self.bulletX, self.bulletY)
                            print("Bullet is Fired")
                    if self.game_over and event.key == pygame.K_SPACE:
                        self.reset()

                if event.type == pygame.KEYUP:
                    self.playerX_change = 0

            if not self.game_over:

                # Player Movement Control
                self.playerX += self.playerX_change
                if self.playerX <= 0:
                    self.playerX = 0
                elif self.playerX >= 736:
                    self.playerX = 736

                self.player(self.playerX, self.playerY)

                # Enemy Movement Control
                for i in range(self.no_of_enemies):
                    self.enemyX[i] += self.enemyX_change[i]
                    if self.enemyX[i] >= 736:
                        self.enemyX_change[i] = -1
                        self.enemyY[i] += self.enemyY_change[i]
                    elif self.enemyX[i] <= 0:
                        self.enemyX_change[i] = 1
                        self.enemyY[i] += self.enemyY_change[i]
                    self.enemy(self.enemyX[i], self.enemyY[i], i)

                    if self.enemyY[i] >= 450:
                        for j in range(self.no_of_enemies):
                            self.enemyY[j] = 900
                        self.game_over = True
                        break

                    # Target Abolishment
                    collision = self.is_collision(self.bulletX, self.bulletY, self.enemyX[i], self.enemyY[i])
                    if collision:
                        self.collision_sound.play()
                        self.score += 1
                        self.bullet_state = "ready"
                        self.bulletY = 480
                        self.enemyX[i] = random.randint(0, 736)
                        self.enemyY[i] = random.randint(50, 150)

                # Bullet Movement Control
                if self.bulletY <= 0:
                    self.bulletY = 480
                    self.bullet_state = "ready"
                if self.bullet_state == "fire":
                    self.fire_bullet(self.bulletX, self.bulletY)
                    self.bulletY -= self.bulletY_change

            # Game Over Message
            if self.game_over:
                self.end_game()
            # Update (refresh) screen
            pygame.display.update()


if __name__ == '__main__':
    game = SpaceDeltaForce()
    game.run()
