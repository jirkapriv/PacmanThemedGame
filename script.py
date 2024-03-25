import pygame
import sys
import pytmx
import random
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

pygame.init()

screen_size = [840, 840]            #zkusim jsem random number (odhad)
screen = pygame.display.set_mode((screen_size[0], screen_size[1]))
clock = pygame.time.Clock()

font = pygame.font.Font(None, 36)   #velikost pisma
game_name = "PacMan"                #nazev hry
pygame.display.set_caption(game_name)
actionX = None
actionY = None
mainAction = None
positionX = 0
positionY = 0

tmx_map = pytmx.load_pygame("level1Map.tmx")
eatSound = pygame.mixer.Sound("eatSoundPacMan.mp3")
eatSound.set_volume(0.3)
pygame.mixer.music.load("introPacMan.mp3")
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(1)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SPEED = 4
SCALE = 2.5                         #aby nemel misto
MSCALE = 5
enemySPEED = 1
havePowerUp = False
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
timer = 100
pointList = []
powerUpsList = []

for layer in tmx_map.visible_layers:
    if isinstance(layer, pytmx.TiledTileLayer) and layer.name == "Jidlo":
        for x, y, image in layer.tiles():
            pointList.append([x * 8 * MSCALE + (8 * MSCALE)/2 , y * 8 * MSCALE + (8 * MSCALE)/2])

for layer in tmx_map.visible_layers:
    if isinstance(layer, pytmx.TiledTileLayer) and layer.name == "powerUp":
        for x, y, image in layer.tiles():
            powerUpsList.append([x * 8 * MSCALE + (8 * MSCALE)/2 , y * 8 * MSCALE + (8 * MSCALE)/2])  

with open("name.txt", "r") as file:
    first_line = file.readline().strip()
    if not first_line:
        name = input("Enter Your Name: ")
        with open("name.txt", "w") as file_write:
            file_write.write(name)
    else:
        name = first_line

uri = "mongodb+srv://jiriprivratsky:8kp9pwcPtvazMCe3@cluster0.gvsfodh.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
mydb = client["mydatabase"]
mycol = mydb["players"]


# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)




while True:
    if not havePowerUp:
        textik = str(f"invisibility: {0}")
    else:
        textik = f"invisibility: {round(max(timer,0))}"
    
    if timer <= 0 and havePowerUp == True:
        havePowerUp = False
        timer = 100
    else:
        timer -= 0.25
    screen.fill(BLACK)
    pressed = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT or pressed[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()

    if enemySPEED == 1:
        levelDifficulty = "Easy"
    if enemySPEED == 2:
        levelDifficulty = "Normal"
    if enemySPEED == 3:
        levelDifficulty = "Hard"
    if enemySPEED == 4:
        levelDifficulty = "Impossible"



    text = font.render(f"Score: {pointsCount}", True, WHITE)
    text2 = font.render(textik, True, WHITE)
    text3 = font.render(levelDifficulty, True, WHITE)

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

        #Pokud hrac nesnedl powerup tak si ho nepratele mohou najit
        if havePowerUp != True:
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
        else:
            enemies_close[a] = False
            
    if havePowerUp:
        player.set_alpha(50)
        playerFliped.set_alpha(50)
        playerRight.set_alpha(50)
        playerUp.set_alpha(50)
        playerDown.set_alpha(50)
    else:
        player.set_alpha(255)
        playerFliped.set_alpha(255)
        playerRight.set_alpha(255)
        playerUp.set_alpha(255)
        playerDown.set_alpha(255)

    for layer in tmx_map.visible_layers :
        if isinstance(layer, pytmx.TiledTileLayer) and layer.name == "Colides":
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
            pointsCount+=10
            pygame.mixer.Sound.play(eatSound)
            
    if pointList == []:
        if enemySPEED < 4:
            enemySPEED += 1
        for layer in tmx_map.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer) and layer.name == "Jidlo":
                for x, y, image in layer.tiles():
                    pointList.append([x * 8 * MSCALE + (8 * MSCALE)/2 , y * 8 * MSCALE + (8 * MSCALE)/2])
     
     
        for layer in tmx_map.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer) and layer.name == "powerUp":
                for x, y, image in layer.tiles():
                    powerUpsList.append([x * 8 * MSCALE + (8 * MSCALE)/2 , y * 8 * MSCALE + (8 * MSCALE)/2])  
        player_rect = player.get_rect(topleft=(screen.get_width() / 2 - 220, screen.get_height() / 2 ))
        for a in range(len(enemies)):
            enemies_rect[a].x = 440
            enemies_rect[a].y = 200    
            
    for x, y in enumerate(powerUpsList):
        pygame.draw.circle(screen, (255,255,255), (y[0], y[1]), 10)
        if player_rect.colliderect((y[0], y[1], 2, 2)):
            powerUpsList.pop(x)
            pygame.mixer.Sound.play(eatSound)
            havePowerUp = True
            timer = 100
            pointsCount+=50
            

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
        if isinstance(layer, pytmx.TiledTileLayer) and layer.name == "Colides":
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
        if isinstance(layerY, pytmx.TiledTileLayer) and layerY.name == "Colides":
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
        if actionY == "up":
            player = playerUp
        elif actionY == "down":
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
        if actionX == "left":
            player = playerFliped
        elif actionX == "right":
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
    screen.blit(text2, (screen.get_width()- 200, 10))
    screen.blit(text3, (screen.get_width()/2 - text3.get_width()/2, 10))

    if gameOver:                     #zatim se na hre pracuje takze to bude v komentu
        
        listDat = [
            {
                "name":name, "score":pointsCount
            }
            
        ]
        mycol.insert_many(listDat)
        break

    
    pygame.display.flip()
    clock.tick(60)