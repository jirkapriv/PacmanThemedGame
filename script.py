import pygame
import sys
import pytmx
import random

pygame.init()

screen_size = [840, 840]            #zkusim jsem random number (odhad)
screen = pygame.display.set_mode((screen_size[0], screen_size[1]))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)   #velikost pisma
game_name = "PacMan"                #nazev hry
"""left = False
right = False
down = False
up = Falsed
run = True"""
actionX = None
actionY = None
mainAction = None

positionX = 0
positionY = 0

tmx_map = pytmx.load_pygame("level1Map.tmx")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SPEED = 4
enemySPEED = 3

SCALE = 2.5                         #aby nemel misto
MSCALE = 5
#hrac
player = pygame.image.load("pacman2.png").convert()
player.set_colorkey((255,255,255))
player = pygame.transform.scale(player, (player.get_width() * SCALE, player.get_height() * SCALE))
player_rect = player.get_rect(topleft=(screen.get_width() / 2 - 220, screen.get_height() / 2 ))
playerFliped = player
playerRight = player
playerFliped = pygame.transform.flip(playerFliped, True, False)
playerDown = pygame.transform.rotate(player,270)
playerUp = pygame.transform.rotate(player,90)
pointsCount = 0

#nepratele
enemies = [pygame.image.load("Pinky.png").convert(), pygame.image.load("Blinky.png").convert(), pygame.image.load("Clyde.png").convert(), pygame.image.load("Inky.png").convert()]
enemies_rect = []
"""enemy1 = pygame.image.load("Pinky.png").convert()
enemy2 = pygame.image.load("Blinky.png").convert()
enemy3 = pygame.image.load("Clyde.png").convert()
enemy4 = pygame.image.load("Inky.png").convert()"""
for a in range(len(enemies)):
    enemies[a].set_colorkey((255,255,255))
    enemies[a] = pygame.transform.scale(enemies[a], (enemies[a].get_width() * SCALE, enemies[a].get_height() * SCALE))
    enemies_rect.append(enemies[a].get_rect(topleft=(440, 200)))

#enemy1_rect = enemy1.get_rect(topleft=(screen.get_width() / 2, screen.get_width() / 2))            #spawn do klece
#enemy1_rect = enemy1.get_rect(topleft=(440, 200))                                                  #spawn mimo klec

enemies_actionX = ["left", "right", "left", "right"]        #pro osu x
enemies_actionY = ["down", "up", "down", "up"]        #pro osu y
enemy_random_moveX = ["left", "right"]
enemy_random_moveY = ["up", "down"]
enemies_osaX = []
enemies_osaY = []
for a in range(len(enemies_rect)):
    enemies_osaX.append(enemies_rect[a].x)
    enemies_osaY.append(enemies_rect[a].y)
enemies_close = [False, False, False, False]

enemies_rangeOfSeeing = 4

gameOver = False

pointList = []


pygame.display.set_caption(game_name)
for layer in tmx_map.visible_layers:
    if isinstance(layer, pytmx.TiledTileLayer) and layer.name == "Vrstva2":
        for x, y, image in layer.tiles():
            pointList.append([x * 8 * MSCALE + (8 * MSCALE)/2 , y * 8 * MSCALE + (8 * MSCALE)/2])
        
while True:
    screen.fill(BLACK)
    pressed = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT or pressed[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()
        """if event.type == pygame.KEYDOWN:                     #funkce na pohyb je dole
            if event.key == pygame.K_a:
                actionX = "left"
                #player = playerFliped
            if event.key == pygame.K_d:
                actionX = "right"
                #player = playerRight
            if event.key == pygame.K_s:
                actionY = "down"
                #player = playerDown
            if event.key == pygame.K_w:
                actionY = "up"
                #player = playerUp"""


    text = font.render(f"Score: {pointsCount}", True, WHITE)

    #teleport na druhou stranu
    if (player_rect.x < 0-player.get_width()//2) and actionX == "left":
        player_rect.x = screen.get_width()
        #player_rect.y = positionY
    elif player_rect.x > ((screen.get_width()-player.get_width())+player.get_width()//2) and actionX == "right":
        player_rect.x = 0
        #player_rect.y = positionY

    #teleport na druhou stranu pro enemy
    for a in range(len(enemies)):
        if (enemies_rect[a].x < 0-enemies[a].get_width()//2) and enemies_actionX[a] == "left":
            enemies_rect[a].x = screen.get_width()
        elif enemies_rect[a].x > ((screen.get_width()-enemies[a].get_width())+enemies[a].get_width()//2) and enemies_actionX[a] == "right":
            enemies_rect[a].x = 0

        #prikaz kam ma jit nepritel                 #potrebovalo by to lepsi logiku
        if (enemies_rect[a].x > player_rect.x and enemies_close[a]):
            enemies_actionX[a] = "left"
        elif (enemies_rect[a].x < player_rect.x and enemies_close[a]):
            enemies_actionX[a] = "right"
        if (enemies_rect[a].y > player_rect.y and enemies_close[a]):
            enemies_actionY[a] = "up"
        elif (enemies_rect[a].y < player_rect.y and enemies_close[a]):
            enemies_actionY[a] = "down"

        #nepritel je blizko "I can smell him!!!!"
        if player_rect.y <= enemies_rect[a].y+enemies[a].get_height()*enemies_rangeOfSeeing and player_rect.y+player.get_height()*enemies_rangeOfSeeing >= enemies_rect[a].y and player_rect.x <= enemies_rect[a].x+enemies[a].get_width()*enemies_rangeOfSeeing and player_rect.x+player.get_width()*enemies_rangeOfSeeing >= enemies_rect[a].x:
            #print("I see him!!!")
            enemies_close[a] = True
        else:
            #print("I can't see him :,(")
            enemies_close[a] = False

        #pokud se player dotkne nepritele tak skonci hra
        if player_rect.y <= enemies_rect[a].y+enemies[a].get_height()//2 and player_rect.y+player.get_height()//2 >= enemies_rect[a].y and player_rect.x <= enemies_rect[a].x+enemies[a].get_width()//2 and player_rect.x+player.get_width()//2 >= enemies_rect[a].x:
            gameOver = True

    for layer in tmx_map.visible_layers :
        if isinstance(layer, pytmx.TiledTileLayer) and layer.name == "Vrstva1":
            for x, y, image in layer.tiles():
                image.convert()
                image.set_colorkey(WHITE)
                scaled_image = pygame.transform.scale(
                    image, (8 * MSCALE, 8 * MSCALE))
                screen.blit(scaled_image, (x * 8 *
                            MSCALE, y * 8 * MSCALE))
    
    for x, y in enumerate(pointList):
        pygame.draw.circle(screen, (255,255,255), (y[0], y[1]), 3)
        if player_rect.colliderect((y[0], y[1], 2, 2)):
            pointList.pop(x)
            pointsCount+=1
        
        

    if actionX == "left":
        player_rect.x -= SPEED
    if actionX == "right":
        player_rect.x += SPEED

    for a in range(len(enemies)):
        if enemies_actionX[a] == "left":
            enemies_rect[a].x -= enemySPEED
        if enemies_actionX[a] == "right":
            enemies_rect[a].x += enemySPEED

        
    for layer in tmx_map.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer) and layer.name == "Vrstva1":
            for x, y, tile in layer.tiles():
                platformX = pygame.Rect(x * 8 * MSCALE, y * 8 * MSCALE,
                                        8 * MSCALE, 8 * MSCALE)
                if player_rect.colliderect(platformX):
                    if actionX == "right":
                        player_rect.right = platformX.left
                        
                    elif actionX == "left":
                        player_rect.left = platformX.right

                for a in range(len(enemies)):
                    if enemies_rect[a].colliderect(platformX):
                        randomNumberX = random.randrange(0,len(enemy_random_moveX))
                        #randomNumberY = random.randrange(0,len(enemy1_random_moveY))
                        #print(randomNumberX)
                        if enemies_actionX[a] == "right":
                            enemies_rect[a].right = platformX.left

                            if enemies_close[a] != True:    
                                if enemies_osaY[a] != enemies_rect[a].y:
                                    enemies_osaY[a] = enemies_rect[a].y
                                    #enemy1_actionX = "left"
                                    enemies_actionX[a] = enemy_random_moveX[randomNumberX]
                                    #enemy1_actionY = enemy1_random_moveY[randomNumberY]
                                else:
                                    #print(f'Detekce X: {enemies_actionX[a]}')
                                    enemies_actionX[a] = enemy_random_moveX[randomNumberX]

                        elif enemies_actionX[a] == "left":
                            enemies_rect[a].left = platformX.right

                            if enemies_close[a] != True:
                                if enemies_osaY[a] != enemies_rect[a].y:
                                    enemies_osaY[a] = enemies_rect[a].y
                                    #enemy1_actionX = "right"
                                    enemies_actionX[a] = enemy_random_moveX[randomNumberX]
                                    #enemy1_actionY = enemy1_random_moveY[randomNumberY]
                                else:
                                    #print(f'Detekce X: {enemies_actionX[a]}')
                                    enemies_actionX[a] = enemy_random_moveX[randomNumberX]
                        
    if actionY == "down":
        player_rect.y += SPEED
    if actionY == "up":
        player_rect.y -= SPEED

    for a in range(len(enemies)):
        if enemies_actionY[a] == "down":
            enemies_rect[a].y += enemySPEED
        if enemies_actionY[a] == "up":
            enemies_rect[a].y -= enemySPEED
        

    for layerY in tmx_map.visible_layers:
        if isinstance(layerY, pytmx.TiledTileLayer) and layerY.name == "Vrstva1":
            for n, m, tile in layerY.tiles():
                platformY = pygame.Rect(n * 8 * MSCALE, m * 8 * MSCALE,
                                        8 * MSCALE, 8 * MSCALE)
                if player_rect.colliderect(platformY):
                    if actionY == "down":
                        player_rect.bottom = platformY.top
                    elif actionY == "up":
                        player_rect.top = platformY.bottom
                for a in range(len(enemies)):
                    if enemies_rect[a].colliderect(platformY):
                        #randomNumberX = random.randrange(0,len(enemy1_random_moveX))
                        randomNumberY = random.randrange(0,len(enemy_random_moveY))
                        #print(randomNumberY)
                        if enemies_actionY[a] == "down":
                            enemies_rect[a].bottom = platformY.top

                            if enemies_close[a] != True:
                                if enemies_osaX[a] != enemies_rect[a].x:
                                    enemies_osaX[a] = enemies_rect[a].x
                                    #enemy1_actionY = "up"
                                    #enemy1_actionX = enemy1_random_moveX[randomNumberX]
                                    enemies_actionY[a] = enemy_random_moveY[randomNumberY]
                                else:
                                    #print(f'Detekce Y: {enemies_osaY[a]}')
                                    enemies_actionY[a] = enemy_random_moveY[randomNumberY]

                        elif enemies_actionY[a] == "up":
                            enemies_rect[a].top = platformY.bottom

                            if enemies_close[a] != True:
                                if enemies_osaX[a] != enemies_rect[a].x:
                                    enemies_osaX[a] = enemies_rect[a].x
                                    #enemy1_actionY = "down"
                                    #enemy1_actionX = enemy1_random_moveX[randomNumberX]
                                    enemies_actionY[a] = enemy_random_moveY[randomNumberY]
                                else:
                                    #print(f'Detekce Y: {enemies_osaY[a]}')
                                    enemies_actionY[a] = enemy_random_moveY[randomNumberY]


    #///////////////pohyb///////////////
    if pressed[pygame.K_w] or pressed[pygame.K_UP]:         #pokud jde nahoru
        if(actionY != "up"):
            positionX = player_rect.x
        actionY = "up"
        mainAction = actionY
    elif pressed[pygame.K_s] or pressed[pygame.K_DOWN]:			#pokud jde dolu
        if(actionY != "down"):
            positionX = player_rect.x
        actionY = "down"
        mainAction = actionY
	
    elif pressed[pygame.K_a] or pressed[pygame.K_LEFT]:			#pokud jde do leva
        if(actionX != "left"):
            positionY = player_rect.y
        actionX = "left"
        mainAction = actionX
    elif pressed[pygame.K_d] or pressed[pygame.K_RIGHT]:			#pokud jde do prava
        if(actionX != "right"):
            positionY = player_rect.y
        actionX = "right"
        mainAction = actionX
    
    #urceni smeru #5                        dfsghdfghdfgbrddhbgdgfhbdfghbdfghbfgdhbdfghbdfghbdfghb      (malem jsem rozbil klavesu kvuli teto podmince)

    #problem s velikosti postavicky nejak se proste hejbne a bum spusti se podminka, ale neni tam ulicka treba idk
    #   pokud se zmeni pozice           pokud jsou dva povely                       pokud jeho plan je jit nahoru ci dolu
    if ((positionY > player_rect.y and positionY < player_rect.y) or positionY != player_rect.y):
        if mainAction == "up":
            player = playerUp
        elif mainAction == "down":
            player = playerDown
        if ((actionX != None and actionY != None) and mainAction == "up" or mainAction == "down"):
            #print("Y",positionY, player_rect.y, "True", "1")
            #print("MainAction", mainAction)
            actionX = None
            if (actionY == "up"):
                player = playerUp
            elif(actionY == "Down"):
                player = playerDown
    #       pokud se zmeni pozice               pokud jsou dva povely                 pokud jeho plan je jit do leva ci do prava
    elif (positionX > player_rect.x or positionX < player_rect.x) or positionX != player_rect.x:
        if mainAction == "left":
            player = playerFliped
        elif mainAction == "right":
            player = playerRight
        if ((actionX != None and actionY != None) and mainAction == "left" or mainAction == "right"):
            #print("X", positionX, player_rect.x, "True", "2")
            #print("MainAction", mainAction)
            actionY = None
            if (actionX == "left"):
                player = playerFliped
            elif(actionX == "right"):
                player = playerRight
    if mainAction == "left" or mainAction == "right":
        positionY = player_rect.y
    elif mainAction == "down" or mainAction == "up":
        positionX = player_rect.x
    #///////////////pohyb///////////////

    screen.blit(player, player_rect)
    for a in range(len(enemies)):
        screen.blit(enemies[a], enemies_rect[a])
    #screen.blit(enemy1, enemy1_rect)
    screen.blit(text, (10, 10))

    if gameOver:                     #zatim se na hre pracuje takze to bude v komentu
        break

    
    pygame.display.flip()
    clock.tick(60)