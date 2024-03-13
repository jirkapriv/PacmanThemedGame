import pygame
import sys
import pytmx
pygame.init()

screen_size = [755, 800]            #zkusim jsem random number (odhad)
screen = pygame.display.set_mode((screen_size[0], screen_size[1]))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)   #velikost pisma
game_name = "PacMan"                #nazev hry
actionX = None
actionY = None
mainAction = None

positionX = 0
positionY = 0


tmx_map = pytmx.load_pygame("level1Map.tmx")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SPEED = 4

SCALE = 2.5                         #aby nemel misto
MSCALE = 5
#hrac
player = pygame.image.load("pacman2.png").convert()
player.set_colorkey((255,255,255))
player = pygame.transform.scale(player, (player.get_width() * SCALE, player.get_height() * SCALE))
player_rect = player.get_rect(topleft=(screen.get_width() / 2, screen.get_height() / 2))
playerFliped = player
playerRight = player
playerFliped = pygame.transform.flip(playerFliped, True, False)
playerDown = pygame.transform.rotate(player,270)
playerUp = pygame.transform.rotate(player,90)

#nepratele
enemy1 = pygame.image.load("pinky.png").convert()
enemy1.set_colorkey((255,255,255))
enemy1 = pygame.transform.scale(enemy1, (enemy1.get_width() * SCALE, enemy1.get_height() * SCALE))
enemy1_rect = enemy1.get_rect(topleft=(screen.get_width() / 2, screen.get_width() / 2))
enemy1_actionX = None        #pro osu x
enemy1_actionY = None        #pro osu y
enemy1_check_plan = None
enemy1_plan_move = None
enemy1_move_done = True


pygame.display.set_caption(game_name)

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


    #teleport na druhou stranu
    if (player_rect.x < 0-player.get_width()//2) and actionX == "left":
        player_rect.x = screen.get_width()
        #player_rect.y = positionY
    elif player_rect.x > ((screen.get_width()-player.get_width())+player.get_width()//2) and actionX == "right":
        player_rect.x = 0
        #player_rect.y = positionY

    #prikaz kam ma jit nepritel                 #potrebovalo by to lepsi logiku
    #pro osu x
    if (enemy1_rect.x > player_rect.x):
        enemy1_actionX = "left"
    elif (enemy1_rect.x < player_rect.x):
        enemy1_actionX = "right"
    else:
        enemy1_actionX = None
    #pro osu y
    if (enemy1_rect.y > player_rect.y):
        enemy1_actionY = "up"
    elif (enemy1_rect.y < player_rect.y):
        enemy1_actionY = "down"
    else:
        enemy1_actionY = None

    if enemy1_actionX == None:
        enemy1_check_plan = "down"
        if enemy1_check_plan == "down" and enemy1_move_done == True:
            enemy1_move_done = False
            enemy1_plan_move = "down"
    elif enemy1_actionY == None:
        enemy1_check_plan = "left"
        if enemy1_check_plan == "left" and enemy1_move_done == True:
            enemy1_move_done = False
            enemy1_plan_move = "left"
    else:
        enemy1_check_plan = None


    print(enemy1_check_plan, enemy1_actionX, enemy1_actionY)
    


    for layer in tmx_map.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for x, y, image in layer.tiles():
                image.convert()
                image.set_colorkey(WHITE)
                scaled_image = pygame.transform.scale(
                    image, (8 * MSCALE, 8 * MSCALE))
                screen.blit(scaled_image, (x * 8 *
                            MSCALE, y * 8 * MSCALE))


    if actionX == "left":
        player_rect.x -= SPEED
    if actionX == "right":
        player_rect.x += SPEED

    if enemy1_actionX == "left":
        enemy1_rect.x -= SPEED
    if enemy1_actionX == "right":
        enemy1_rect.x += SPEED

        
    for layerX in tmx_map.visible_layers:
        if isinstance(layerX, pytmx.TiledTileLayer) and layerX.name == "Vrstva1":
            for x, y, tile in layerX.tiles():
                platformX = pygame.Rect(x * 8 * MSCALE, y * 8 * MSCALE,
                                        8 * MSCALE, 8 * MSCALE)
                if player_rect.colliderect(platformX):
                    if actionX == "right":
                        player_rect.right = platformX.left
                        
                    elif actionX == "left":
                        player_rect.left = platformX.right

                if enemy1_rect.colliderect(platformX):
                    if enemy1_actionX == "right":
                        enemy1_rect.right = platformX.left
                    
                    elif enemy1_actionX == "left":
                        enemy1_rect.left = platformX.right
                        
    if actionY == "down":
        player_rect.y += SPEED
    if actionY == "up":
        player_rect.y -= SPEED

    if enemy1_actionY == "down":
        enemy1_rect.y += SPEED
    if enemy1_actionY == "up":
        enemy1_rect.y -= SPEED
        

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
                
                if enemy1_rect.colliderect(platformY):
                    if enemy1_actionY == "down":
                        enemy1_rect.bottom = platformY.top
                    
                    elif enemy1_actionY == "up":
                        enemy1_rect.top = platformY.bottom


    #///////////////pohyb///////////////
    if pressed[pygame.K_w] or pressed[pygame.K_UP]:         #pokud jde nahoru
        if(actionY != "up"):
            positionX = player_rect.x
        actionY = "up"
        mainAction = actionY
    if pressed[pygame.K_s] or pressed[pygame.K_DOWN]:			#pokud jde dolu
        if(actionY != "down"):
            positionX = player_rect.x
        actionY = "down"
        mainAction = actionY
	
    if pressed[pygame.K_a] or pressed[pygame.K_LEFT]:			#pokud jde do leva
        if(actionX != "left"):
            positionY = player_rect.y
        actionX = "left"
        mainAction = actionX
    if pressed[pygame.K_d] or pressed[pygame.K_RIGHT]:			#pokud jde do prava
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
            if (mainAction == "up"):
                player = playerUp
            elif(mainAction == "Down"):
                player = playerDown
            #print("Y",positionY, player_rect.y, "True", "1")
            #print("MainAction", mainAction)
            actionX = None
    #       pokud se zmeni pozice               pokud jsou dva povely                 pokud jeho plan je jit do leva ci do prava
    elif (positionX > player_rect.x or positionX < player_rect.x) or positionX != player_rect.x:
        if mainAction == "left":
            player = playerFliped
        elif mainAction == "right":
            player = playerRight
        if ((actionX != None and actionY != None) and mainAction == "left" or mainAction == "right"):
            if (mainAction == "left"):
                player = playerFliped
            elif(mainAction == "right"):
                player = playerRight
            #print("X", positionX, player_rect.x, "True", "2")
            #print("MainAction", mainAction)
            actionY = None
    if mainAction == "left" or mainAction == "right":
        positionY = player_rect.y
    elif mainAction == "down" or mainAction == "up":
        positionX = player_rect.x
    #///////////////pohyb///////////////


    screen.blit(player, player_rect)
    screen.blit(enemy1, enemy1_rect)
    
    pygame.display.flip()
    clock.tick(60)