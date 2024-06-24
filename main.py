import pygame
import math as m
import random
from pygame import mixer
import time

class SpaceDeltaForce:
    def __init__(self):
        # Initialize pygame
        pygame.init()

        # Creating Screen
        self.screen = pygame.display.set_mode((800, 600))

        # Resources --- Images
        self.bgImg = pygame.image.load("Resources/img/bgimg.png")
        self.playerImg = pygame.image.load("Resources/img/player.png")
        self.bulletImg = pygame.image.load("Resources/img/bullets.png")
        self.enemyImg = pygame.image.load("Resources/img/enemy.png")
        self.icon = pygame.image.load("Resources/img/icon.png")
        self.welcomeImg = pygame.transform.scale(pygame.image.load("Resources/img/welcome.png"), (800, 600))

        # Resources --- Sounds
        # mixer.music.load("Resources/sound/background.wav")

        # Background Music
        mixer.music.load("Resources/sound/background.wav")
        mixer.music.play(-1)

        # Adding title and icon
        pygame.display.set_caption("Space Delta Force")
        pygame.display.set_icon(self.icon)

        # Player Score
        self.score = 0

        # Sound effects
        self.bullet_sound = pygame.mixer.Sound("Resources/sound/laser.wav")
        self.collision_sound = pygame.mixer.Sound("Resources/sound/collision.wav")

        # Fonts
        # self.welcome_font = pygame.font.SysFont
        self.welcome_font = pygame.font.Font("freesansbold.ttf", 64)
        self.score_font = pygame.font.Font("freesansbold.ttf", 24)
        self.game_over_font = pygame.font.Font("freesansbold.ttf", 64)
        self.normal_font = pygame.font.Font("freesansbold.ttf", 16)

        # Creating Player
        self.player_init = 375
        self.player_vel = 1
        self.playerX = 370
        self.playerY = 500
        self.playerX_change = 0

        # Creating Enemies
        self.enemy_img = []
        self.enemyX = []
        self.enemyY = []
        self.enemyX_change = []
        self.enemyY_change = []
        self.no_of_enemies = 7
        self.create_enemies()

        # Creating Bullets
        self.bulletX = 0
        self.bulletY = 480
        self.bulletX_change = 0
        self.bulletY_change = 2
        self.bullet_state = "ready"

        # High Score
        with open("Resources/high_score.txt", "r") as f:
            self.high_score = int(f.read())

        # Game Loop
        self.running = False
        self.game_over = False

    def create_enemies(self):
        for i in range(self.no_of_enemies):
            self.enemy_img.append(self.enemyImg)
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
        replay_message = self.normal_font.render("[Press SPACE To Replay or ESC to Quit]", True, (225, 191, 0))
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
        self.screen.blit(self.enemy_img[i], (x, y))

    # Fire Bullet
    def fire_bullet(self, x, y):
        self.bullet_state = "fire"
        self.screen.blit(self.bulletImg, (x + 16, y + 10))

    def welcome(self):
        while not self.running:
            self.screen.fill((0, 0, 0))

            # Draw Background
            self.screen.blit(self.welcomeImg, (0, 0))
            welcome_msg = self.welcome_font.render("SPACE DELTA FORCE", True, (225, 0, 0))
            self.screen.blit(welcome_msg, (60, 50))
            for i in range(8):
                self.enemy_img.append(self.enemyImg)
                self.enemyX.append(75 + i*64)
                self.enemyY.append(134)
                self.enemyX_change.append(0.4)
                self.enemyY_change.append(0)

            # Enemy Movement Control
            for i in range(8):
                self.enemyX[i] += self.enemyX_change[i]
                if self.enemyX[i] >= 700:
                    self.enemyX_change[i] = -1.5
                elif self.enemyX[i] <= 100:
                    self.enemyX_change[i] = 1.5
                self.enemy(self.enemyX[i], 134, i)

            # Player Movement Control
            player_img = pygame.transform.scale(self.playerImg, (72, 72))
            self.player_init += self.player_vel
            if self.player_init >= 600:
                self.player_vel = -1.5
            elif self.player_init <= 200:
                self.player_vel = 1.5
            self.screen.blit(player_img, (self.player_init, 410))

            play_message = self.normal_font.render("[Press ENTER To play or ESC to Quit]", True, (225, 191, 0))
            self.screen.blit(play_message, (245, 550))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.running = True
                        self.reset()
                        game.run()

            pygame.display.update()

    def run(self):
        while self.running:
            self.screen.fill((0, 0, 0))

            # Draw Background
            self.screen.blit(self.bgImg, (0, 0))
            hiscore = self.normal_font.render(f"High Score : {self.high_score}", True, (255, 51, 0))
            self.screen.blit(hiscore, (15, 10))
            total_score = self.score_font.render("Score : " + str(self.score), True, (255, 91, 0))
            self.screen.blit(total_score, (15, 25))

            # Event Listener
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                        quit()
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
                if self.playerX >= 736:
                    self.playerX = 736

                self.player(self.playerX, self.playerY)

                # Enemy Movement Control
                for i in range(self.no_of_enemies):
                    self.enemyX[i] += self.enemyX_change[i]
                    if self.enemyX[i] >= 736:
                        self.enemyX_change[i] = -0.9
                        self.enemyY[i] += self.enemyY_change[i]
                    elif self.enemyX[i] <= 0:
                        self.enemyX_change[i] = 0.9
                        self.enemyY[i] += self.enemyY_change[i]
                    self.enemy(self.enemyX[i], self.enemyY[i], i)

                    if self.enemyY[i] >= 450:
                        if self.score > self.high_score:
                            with open("Resources/high_score.txt", "w") as f:
                                self.high_score = self.score
                                f.write(str(self.high_score))
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
    game.welcome()
