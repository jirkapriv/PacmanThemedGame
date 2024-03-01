import pygame
import sys
import pytmx
pygame.init()

screen_size = [760, 800]            #zkusim jsem random number (odhad)
screen = pygame.display.set_mode((screen_size[0], screen_size[1]))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)   #velikost pisma
game_name = "PacMan"                #nazev hry
left = False
right = False
down = False
up = False
run = True
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
player = pygame.image.load("pacman2.png").convert()
player.set_colorkey((255,255,255))
player = pygame.transform.scale(player, (player.get_width() * SCALE, player.get_height() * SCALE))
player_rect = player.get_rect(topleft=(screen.get_width() / 2, screen.get_height() / 2))
playerFliped = player
playerRight = player
playerFliped = pygame.transform.flip(playerFliped, True, False)
playerDown = pygame.transform.rotate(player,270)
playerUp = pygame.transform.rotate(player,90)

pygame.display.set_caption(game_name)

while True:
    screen.fill(BLACK)
    pressed = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT or pressed[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()
        """if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                action = "left"
                player = playerFliped
            if event.key == pygame.K_d:
                action = "right"
                player = playerRight
            if event.key == pygame.K_s:
                action = "down"
                player = playerDown
            if event.key == pygame.K_w:
                action = "up"
                player = playerUp"""


    #teleport na druhou stranu
    if player_rect.x < 0-(player.get_width()//2):						#HUH
        player_rect.x = screen.get_width()
    elif player_rect.x > screen.get_width()-(player.get_width()//4):	#HUH vubec nevim proc tady je deleno 4, ale kdyz tam bude ta 2 tak zmizi z mapy takze to musi byt nesymetricke
        player_rect.x = 0


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
                        
    if actionY == "down":
        player_rect.y += SPEED
    if actionY == "up":
        player_rect.y -= SPEED
        

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


    #pohyb
    if pressed[pygame.K_w]:         #pokud jde nahoru
        if(actionY != "up"):
            positionX = player_rect.x
        actionY = "up"
        mainAction = actionY
        """print(positionX)
        print(player_rect.x)
        print("--------------")"""
    if pressed[pygame.K_s]:			#pokud jde dolu
        if(actionY != "down"):
            positionX = player_rect.x
        actionY = "down"
        mainAction = actionY
        """print(positionX)
        print(player_rect.x)
        print("--------------")"""
	
    if pressed[pygame.K_a]:			#pokud jde do leva
        if(actionX != "left"):
            positionY = player_rect.y
        actionX = "left"
        mainAction = actionX
    if pressed[pygame.K_d]:			#pokud jde do prava
        if(actionX != "right"):
            positionY = player_rect.y
        actionX = "right"
        mainAction = actionX
    
    #urceni smeru #3                              #potreba zjistit zda muze projit pri mainPohybu
    if actionX != None or actionY != None:
        if actionX == "right" or actionX == "left" and actionY == "up" or actionY == "down":
            if positionY != player_rect.y and mainAction == "up" or mainAction == "down":
                    #if     tady bude tedy podminka s collision zda muze projit 
                    actionX = None
            """elif positionX != player_rect.x and mainAction == "right" or mainAction == "left":
                actionY = None"""


    #urceni smeru #2
    """if positionY != player_rect.y and actionY != None:
        print("X",positionX, player_rect.x)
        if actionX != None:
                if player_rect.top != platformY.bottom or player_rect.bottom != platformY.top:
                    actionX = None
                    print("neni rovno1")
    if positionX != player_rect.x and actionX != None:
        print("Y",positionY, player_rect.y)
        if actionY != None:
                if player_rect.left != platformX.right or player_rect.right != platformX.left:
                    actionY = None
                    print("neni rovno2")"""


    screen.blit(player, player_rect)
    
    pygame.display.flip()
    clock.tick(60)