import pygame
from pygame.locals import *
import sys
import random
import pygame.freetype

#SetUp
pygame.init()
pygame.display.set_caption('RetroSnake v0.1')

FPS = 60
FPS_CLOCK =  pygame.time.Clock()

#Fonts
GAME_FONT = pygame.freetype.Font("./Fonts/PressStart2P.ttf", 24)
GAME_FONT2 = pygame.freetype.Font("./Fonts/PressStart2P.ttf", 30)
GAME_FONT3 = pygame.freetype.Font("./Fonts/PressStart2P.ttf", 70)

#Screen Setup
height = 550
width = 750
surface = pygame.display.set_mode((width, height))
walls = [(0, 0, 550, 20),(0, 530, 550, 20),(0, 0, 20, 550),(530, 0, 20, 550)]

#Snake (Player Character)
class Snake():
    def __init__(self):
        self.snakes = []
        self.dirList = []
        self.oldList = []
        self.direction = ["east"]
        self.counter = 0
        self.food = None
        self.lastSnake = []
        self.lastDir = []
        self.score = 0
        
        self.set_up()
        
    #setups the game's initial parameters    
    def set_up(self):
        self.makeFood()
        self.lastDir = "east"   
        self.snakes = [[110, 110, 30, 30]]
        self.dirList = ["east"]
        self.oldList = []
        self.direction = ["east"]
        self.counter = 0
        self.food = None
        self.lastSnake = []
        self.lastDir = []
        self.score = 0
        self.makeFood() 
        
    #Moves each snake piece in the correct direction    
    def move(self):
        count = 0
        self.oldList = self.dirList
        self.dirList = self.direction + self.oldList
        self.dirList.pop()
        self.lastSnake = tuple(self.snakes[len(self.snakes)-1])
        self.lastDir = tuple(self.dirList[len(self.dirList)-1])
        for items in self.dirList:
            if items == "east":
                temp = self.snakes[count]
                temp[0] += 30
                self.snakes[count] = temp
            if items == "west":
                temp = self.snakes[count]
                temp[0] -= 30
                self.snakes[count] = temp
            if items == "north":
                temp = self.snakes[count]
                temp[1] -= 30
                self.snakes[count] = temp
            if items == "south":
                temp = self.snakes[count]
                temp[1] += 30
                self.snakes[count] = temp
            count += 1   
            
    #Sets direction of the snake head (player input)                 
    def make_direction(self, num):
        if num == 1:
            self.direction[0] = "east"
        elif num == 2:
            self.direction[0] = "south"
        elif num == 3:
            self.direction[0] = "north"
        elif num == 4:
            self.direction[0] = "west"
            
    #Snake collision detections with walls and itself    
    def collisionCheck(self):
        for items in walls:
            if Rect(items).colliderect(Rect(self.snakes[0])):
                game_over(self.score)
        for item in self.snakes[1:]:
            if Rect(item).colliderect(Rect(self.snakes[0])):
                game_over(self.score)
    
    #Spawns food pieces            
    def makeFood(self):
        do = True
        xCord = random.randrange(30, 520, 30)
        yCord = random.randrange(30, 520, 30)
        for i in range(0, len(self.snakes)):
            temp = self.snakes[i]
            if xCord == temp[0]:
                do = False
            if yCord == temp[1]:
                do = False
        if do:
            self.food = (xCord-5, yCord-5, 20, 20)
        else:
            self.makeFood()
    
    #The snake grows (and score is incremented) when the snake collides with food
    def eatFood(self):
        self.snakes.append(list(self.lastSnake))
        self.dirList.append(list(self.lastDir))
        self.score += 1
        self.makeFood()

#Change to a pause screen game loop        
def pauseScreen():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                if pygame.Rect((580, 350, 150, 50)).collidepoint(pygame.mouse.get_pos()):
                    main()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    main()
        if pygame.Rect((580, 350, 150, 50)).collidepoint(pygame.mouse.get_pos()):
             GAME_FONT.render_to(surface, (595, 365), "Pause", (200, 200, 200))
        else:
             GAME_FONT.render_to(surface, (595, 365), "Pause", (0, 0, 0))
            
                   
        GAME_FONT2.render_to(surface, (200, 250), "PAUSED", (0, 0, 0))      
                
        pygame.display.update()
        FPS_CLOCK.tick(FPS)

#Change to a GameOver screen game loop        
def game_over(score):
    time1 = pygame.time.get_ticks()
    yCond = True
    nCond = False
    show = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and nCond:
                    yCond = True
                    nCond = False
                if event.key == pygame.K_RIGHT and yCond:
                    yCond = False
                    nCond = True
                if event.key == pygame.K_RETURN:
                    if yCond:
                        main()
                    elif nCond:
                        pygame.quit()
                        sys.exit()
                        
        #FADEOUT ANIMATION TO GAME OVER SCREEN                      
        time2 = pygame.time.get_ticks()
        if time2 > 500 + time1:       
            surface.fill((170, 170, 170)) 
        if time2 > 1000 + time1:
            surface.fill((130, 130, 130))  
        if time2 > 1500 + time1:
            surface.fill((80, 80, 80)) 
        if time2 > 2000 + time1:
            surface.fill((30, 30, 30)) 
        if time2 > 2500 + time1:
            surface.fill((0, 0, 0))
            GAME_FONT3.render_to(surface, (60, 120), "GAME OVER", (255, 255, 255))   
            show = True 
        if show and time2 > 3000 + time1:  #Game Over Screen
            surface.fill((0, 0, 0))    
            GAME_FONT3.render_to(surface, (60, 120), "GAME OVER", (255, 255, 255))   
            GAME_FONT2.render_to(surface, (220, 230), "PLAY AGAIN?", (255, 255, 255)) 
            GAME_FONT2.render_to(surface, (310, 300), "Y", (255, 255, 255)) 
            GAME_FONT2.render_to(surface, (380, 300), "N", (255, 255, 255)) 
            GAME_FONT2.render_to(surface, (140, 400), f"YOUR SCORE WAS {score}!", (255, 255, 255)) 
            
            if yCond:
                pygame.draw.rect(surface, (255, 255, 255), (308, 333, 28, 10))
            elif nCond:
                pygame.draw.rect(surface, (255, 255, 255), (378, 333, 28, 10))
        #        
    
        pygame.display.update()
        FPS_CLOCK.tick(FPS)
    
#MAIN LOOP                
def main():  
    #SET UP
    snake = Snake()  
    lastDir = "east"                       
    time1 = pygame.time.get_ticks()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            #MOVEMENT WITH ARROW KEYS
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT and lastDir != "west":
                    lastDir = "east"
                    snake.make_direction(1)

                elif event.key == pygame.K_DOWN and lastDir != "north":
                    lastDir = "south"
                    snake.make_direction(2)

                elif event.key == pygame.K_UP and lastDir != "south":
                    lastDir = "north"
                    snake.make_direction(3)

                elif event.key == pygame.K_LEFT and lastDir != "east":
                    lastDir = "west"
                    snake.make_direction(4)
                    
                if event.key == pygame.K_SPACE:
                    pauseScreen()
            #PAUSE SCREEN BUTTON        
            if event.type == pygame.MOUSEBUTTONUP:
                if pygame.Rect((580, 350, 150, 50)).collidepoint(pygame.mouse.get_pos()):
                    pauseScreen()
                    
        snake.collisionCheck()
        surface.fill((255, 255, 255))
        
        pygame.draw.rect(surface, (0,0,0), snake.food)
        if Rect(snake.food).colliderect(Rect(snake.snakes[0])):
            snake.eatFood()
    
    
        time2 = pygame.time.get_ticks()
        if time2 > time1 + 150:
            snake.move()
            time1 = pygame.time.get_ticks()
    
        #VISUALS
        pygame.draw.rect(surface, (155, 155, 155), (550, 0, 200, 550))
        pygame.draw.rect(surface, (105, 105, 105), (580, 350, 150, 50))
    
        GAME_FONT.render_to(surface, (590, 50), "Snake", (0, 0, 0))
        GAME_FONT.render_to(surface, (600, 80), "v0.1", (0, 0, 0))
        GAME_FONT.render_to(surface, (590, 150), "Score", (0, 0, 0))
        if pygame.Rect((580, 350, 150, 50)).collidepoint(pygame.mouse.get_pos()):
             GAME_FONT.render_to(surface, (595, 365), "Pause", (200, 200, 200))
        else:
             GAME_FONT.render_to(surface, (595, 365), "Pause", (0, 0, 0))
        GAME_FONT2.render_to(surface, (635, 187), f"{snake.score}", (0, 0, 0))
    
        for item in snake.snakes:
            pygame.draw.rect(surface, (0, 0, 0), item)
    
        for things in walls:
            pygame.draw.rect(surface, (0, 0, 0), things)
        #
        pygame.display.update()
        FPS_CLOCK.tick(FPS)

main()