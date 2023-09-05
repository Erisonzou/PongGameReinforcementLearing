import pygame,sys, random

pygame.init()

font20 = pygame.font.Font('freesansbold.ttf', 20)
sWidth, sHeight = 1000,600
screen = pygame.display.set_mode((sWidth,sHeight))
pygame.display.set_caption("Pong")
clock = pygame.time.Clock()
FPS = 90

class Ball:

    BLUE = (0, 0, 255)
    WHITE = (255, 255, 255)
    
    def __init__(self,ScreenWidth, ScreenHeight, radius):
        self.ScreenHeight = ScreenHeight
        self.ScreenWidth = ScreenWidth
        self.x_pos = ScreenWidth/2 - radius
        self.y_pos = ScreenHeight/2 - radius
        self.radius = radius
        self.Velx = 3 * random.randint(-1,1)
        self.Vely = 3 * random.choice((-1,1))
        self.ball = pygame.draw.circle(screen, self.BLUE ,(self.x_pos, self.y_pos),self.radius)
        self.firstTime = 1
    
    def display(self,screen):
        self.ball = pygame.draw.circle(screen, self.BLUE ,(self.x_pos, self.y_pos),self.radius)


    def update(self):
        self.x_pos += self.Velx 
        self.y_pos += self.Vely
        
        if self.y_pos + self.radius >= 0:
            self.Vely *= -1
        
        if self.y_pos - self.radius <= sHeight:
            self.Vely *= -1
        
        if self.x_pos <= 0 and self.firstTime:
            self.firstTime = 0
            return 1
        elif self.x_pos >= self.ScreenWidth and self.firstTime:
            self.firstTime = 0
            return -1
        else:
            return 0


    def hit(self):
        self.Velx *= -1
        self.Vely *= -1

    def getRect(self):
        return self.ball
    
    def reset(self):
        self.x_pos = self.ScreenWidth/2 - self.radius
        self.y_pos = self.ScreenHeight/2 - self.radius
        self.Velx = 3 * random.randint(-1,1)
        self.Vely = 3 * random.choice((-1,1))
        self.firstTime = 1

class Paddle:

    def __init__(self, paddleWidth,paddleLength,color,ScreenHeight,ScreenWidth,decision):

        self.ScreenWidth = ScreenWidth
        self.ScreenHeight = ScreenHeight
        self.width = paddleWidth
        self.length = paddleLength
        self.color = color
        self.left_paddle = ScreenHeight/2 - paddleLength/2
        self.right_paddle = ScreenHeight/2 + paddleLength/2
        self.y = ScreenHeight/2 - self.length/2
        self.Velocity = 0

        if decision == 'Player':
            self.x = 100 - self.width/2
        else:
            self.x = self.ScreenWidth - (100 - self.width/2)
        
        self.paddle = pygame.draw.rect(screen, self.color,pygame.Rect(self.x, self.y, self.width, self.length))
    
    
    def draw_paddle(self,screen):
        self.paddle = pygame.draw.rect(screen, self.color,pygame.Rect(self.x, self.y, self.width, self.length))
    
    def Movement_input(self, direction):
        if direction == 'Right':
            self.Velocity = 3
        if direction == 'Left':
            self.Velocity = -3
    
    def Move(self):
        self.y += self.Velocity
        self.left_paddle += self.Velocity
        self.right_paddle += self.Velocity

        if self.left_paddle <= 0:
            self.Velocity = 0
        
        if self.right_paddle >= self.ScreenHeight:
            self.Velocity = 0
    
    def getRect(self):
        return self.paddle

    def displayScore(self, text, score, x, y, color):
        text = font20.render(text+str(score), True, color)
        textRect = text.get_rect()
        textRect.center = (x, y)
 
        screen.blit(text, textRect)

ball = Ball(sWidth,sHeight,15)
Player = Paddle(20, 120, (130,0,0), sHeight, sWidth,'Player')
Enemy = Paddle(20, 120, (130,0,0), sHeight, sWidth,'Enemy')

PlayerScore = 0
Player2Score = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                Player.Movement_input('Right')     
            if event.key == pygame.K_LEFT:
                Player.Movement_input('Left')
                
        
    if pygame.Rect.colliderect(ball.getRect(),Player.getRect()):
        ball.hit()

    point = ball.update()   
    if point == -1:
        PlayerScore += 1
    elif point == 1:
        Player2Score += 1

    if point:
        ball.reset()

    Player.Move()
    screen.fill((0,0,0))   
    Player.draw_paddle(screen)
    Enemy.draw_paddle(screen)
    ball.display(screen)
    
    Player.displayScore("Player : ", PlayerScore, 100, 20, (255, 255, 255))
    Player.displayScore("Enemy : ", PlayerScore, sWidth - 100, 20, (255, 255, 255))
    pygame.display.update()
    clock.tick(FPS)