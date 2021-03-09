import pygame

pygame.init()
win = pygame.display.set_mode((500, 500))
pygame.display.set_caption('pong.py')

speed = 2
ballvel = 2
ballImage = None
paddleImage1 = None
paddleImage2 = None

player1score = 0
player2score = 0

running = True


class Text:
    def newText(self, font, text):
        return font.render(text, 1, pygame.Color('white'))


class Paddle:
    def __init__(self, x, y, name):
        self.visual = {
            'x': x,
            'y': y
        }
        self.name = name

    def move(self, x, y):
        self.visual['x'] += x
        self.visual['y'] += y

    def render(self):
        global paddleImage1, paddleImage2
        render = pygame.draw.rect(win, (255, 255, 255), (self.visual['x'], self.visual['y'], 20, 150))
        if self.name == 'Paddle1':
            paddleImage1 = render
        elif self.name == 'Paddle2':
            paddleImage2 = render


class Ball:
    def __init__(self, x, y):
        self.visual = {
            'x': x,
            'y': y
        }
        self.velx = 0
        self.vely = 0

    def render(self):
        global ballImage
        ballImage = pygame.draw.rect(win, (255, 255, 255), (self.visual['x'], self.visual['y'], 20, 20))

    def move(self):
        self.visual['x'] += self.velx
        self.visual['y'] += self.vely

    def set_vel(self, x, y):
        self.velx = x
        self.vely = y

    def set_pos(self, x, y):
        self.visual['x'] = x
        self.visual['y'] = y

    def bounce(self):
        if ballImage and paddleImage1 and paddleImage2:
            collider = None
            if ballImage.colliderect(paddleImage1):
                collider = paddleImage1
            elif ballImage.colliderect(paddleImage2):
                collider = paddleImage2

            if collider:
                ball.set_vel(self.velx * -1, self.vely)
                if collider == paddleImage1:
                    self.visual['x'] += 5
                else:
                    self.visual['x'] -= 5
            elif self.visual['y'] < 0 or self.visual['y'] > 480:
                self.set_vel(self.velx, self.vely * -1)
        return 0

    def scorecheck(self):
        global player1score, player2score
        if self.visual['x'] < 0:
            # Player 2 scored
            ball.set_pos(240, 240)
            ball.set_vel(ballvel, ballvel)
            player2score += 1
        elif self.visual['x'] > 480:
            # Player 1 scored
            ball.set_pos(240, 240)
            ball.set_vel(-ballvel, ballvel)
            player1score += 1


paddle1 = Paddle(20, 175, 'Paddle1')
paddle2 = Paddle(460, 175, 'Paddle2')
ball = Ball(230, 230)
texthandler = Text()

ball.set_vel(ballvel, ballvel)
while running:
    pygame.time.delay(10)
    win.fill((0, 0, 0))
    scoreText = texthandler.newText(pygame.font.SysFont('Roboto Slab', 75), f'{player1score}-{player2score}')
    scoreTextRect = scoreText.get_rect(center=(250, 50))
    win.blit(scoreText, scoreTextRect)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and paddle1.visual['y'] > 0:
        paddle1.move(0, -speed)
    if keys[pygame.K_s] and paddle1.visual['y'] < 350:
        paddle1.move(0, speed)
    if keys[pygame.K_UP] and paddle2.visual['y'] > 0:
        paddle2.move(0, -speed)
    if keys[pygame.K_DOWN] and paddle2.visual['y'] < 350:
        paddle2.move(0, speed)

    ball.move()
    ball.bounce()
    ball.scorecheck()

    paddle1.render()
    paddle2.render()
    ball.render()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()

pygame.quit()
