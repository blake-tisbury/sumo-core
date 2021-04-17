import pygame
import time
import sys


screenh = 800
screenw = 1200

pygame.init()



clock = pygame.time.Clock()
bullets = []


class MainRun(object):
    def __init__(self, screenw, screenh):
        self.dw = screenw 
        self.dh = screenh
        print('SumoGame Loaded')
        self.mainloop()


    def mainloop(self):
        # Put all variables up here
        run = True
        shoot = True

        class Player(object):
            def __init__(self, dim, x, y):
                self.dim = dim
                self.x = x
                self.y = y
                self.width = self.dim
                self.height = self.dim
                self.vel = 5
                self.lvl = 0
                self.isJump = False
                self.jumpCount = 10
                self.bg = pygame.image.load('venv/SumoGame/background.jpg')
                self.bg1 = pygame.image.load('venv/SumoGame/sewerbg.png')
                self.right = True
                self.left = False
                self.tel = False
                self.hitbox = ()
                self.sumoLeft = pygame.image.load('venv/SumoGame/Sumo.png')
                self.sumoRight = pygame.image.load('venv/SumoGame/Sumoright.png')

            def draw(self, win):

                sumoLeft = pygame.transform.smoothscale(self.sumoLeft, (self.dim, self.dim))
                sumoRight = pygame.transform.smoothscale(self.sumoRight, (self.dim, self.dim))

                global starttime
                if self.lvl == 0:
                    win.blit(self.bg, (0, 0))
                elif self.lvl == 1:
                    win.blit(self.bg1, (0, 0))

                if self.x > screenw:
                    self.x = screenw - screenw
                    self.lvl += 1
                    self.tel = True
                    starttime = pygame.time.get_ticks()

                if self.x < 0 - self.width and self.lvl >= 1:
                    self.x = screenw
                    self.lvl -= 1
                    self.tel = True
                    starttime = pygame.time.get_ticks()

                if self.tel == True and pygame.time.get_ticks() - starttime >= 100:
                    self.tel = False

                if self.left:
                    win.blit(sumoLeft, (self.x, self.y))
                elif self.right:
                    win.blit(sumoRight, (self.x, self.y))

                if self.lvl != 0 and self.x < 0 - self.width:
                    self.lvl -= 1
                if self.left == True:
                    self.hitbox = self.hitbox = (
                        self.x + self.dim / 3.3 - self.dim / 40, self.y + self.height / 11, self.width - self.dim / 2,
                        self.height - self.height / 9)

                else:
                    self.hitbox = self.hitbox = (
                        self.x + self.dim / 4 - self.dim / 40, self.y + self.height / 11, self.width - self.dim / 2,
                        self.height - self.height / 9)

                self.rect = self.sumoLeft.get_rect(center=(self.x + self.width / 2, self.y + self.height / 2))

        class Projectile(object):

            def __init__(self, x, y, radius, color, facing):
                self.x = x
                self.y = y
                self.radius = radius
                self.color = color
                self.facing = facing
                self.vel = 8 * facing

            def draw(self, win):
                pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

        sumoMan = Player(600, 0, 145)

        def redrawWin():
            sumoMan.draw(win)

        while run:
            global shootTime
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            for bullet in bullets:
                if screenw > bullet.x > 0 and sumoMan.tel == False:
                    bullet.x += bullet.vel
                else:
                    bullets.pop(bullets.index(bullet))

            keys = pygame.key.get_pressed()

            if keys[pygame.K_f]:

                if shoot == False and pygame.time.get_ticks() - shootTime >= 100:
                    shoot = True

                if sumoMan.left:
                    facing = -1
                else:
                    facing = 1

                if len(bullets) < 100 and shoot == True:
                    shootTime = pygame.time.get_ticks()
                    bullets.append(
                        Projectile(round(sumoMan.x + sumoMan.width // 2), round(sumoMan.y + sumoMan.height // 2), 6,
                                   (255, 30, 10), facing))
                    shoot = False

            # Left and Right

            if keys[pygame.K_d] and sumoMan.x < screenw - sumoMan.width / 2 - 50 or keys[
                pygame.K_d] and sumoMan.lvl < 1:
                sumoMan.x += sumoMan.vel
                sumoMan.right = True
                sumoMan.left = False
            elif keys[pygame.K_a] and sumoMan.x > sumoMan.vel - (sumoMan.width / 3 - sumoMan.width / 4) or keys[
                pygame.K_a] and sumoMan.lvl > 0:
                sumoMan.x -= sumoMan.vel
                sumoMan.right = False
                sumoMan.left = True

            if not sumoMan.isJump:

                # Up and Down
                if keys[pygame.K_w] and sumoMan.lvl == 1 and 855 > (sumoMan.x + sumoMan.width / 4) > 760:
                    sumoMan.y -= sumoMan.vel
                else:
                    if sumoMan.y < screenh - sumoMan.dim - (sumoMan.dim / 10) and not 855 > sumoMan.x > 760:
                        sumoMan.vel = 20
                        sumoMan.y += sumoMan.vel

                if keys[pygame.K_s] and sumoMan.y < screenh - sumoMan.dim - (sumoMan.dim / 10):
                    sumoMan.y += sumoMan.vel

                # Run and Jump
                if keys[pygame.K_LSHIFT]:
                    sumoMan.vel = 10
                else:
                    sumoMan.vel = 5
                if keys[pygame.K_SPACE]:  # and sumoMan.jumpCount >= 10:
                    sumoMan.isJump = True
            else:
                if sumoMan.jumpCount >= -10:
                    neg = 1
                    if sumoMan.jumpCount < 0:
                        neg = -1

                    sumoMan.y -= ((sumoMan.jumpCount ** 2) / 2) * neg
                    sumoMan.jumpCount -= 1
                else:
                    sumoMan.isJump = False
                    sumoMan.jumpCount = 10
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    run = False
            redrawWin()
            pygame.display.update()

def main():  # Packs the GUI class into a main function and sets program basics
    program = pygame
    global icon
    global win
    icon = program.image.load('venv/UI/tizzycrypt.ico')
    win = program.display.set_mode((screenw, screenh))
    program.display.set_icon(icon)
    program.display.set_caption("Sumo Man: Consume All")



    app = MainRun(screenh, screenw)



if __name__ == '__main__':
    main()


