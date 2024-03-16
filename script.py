import pygame
import sys
import pytmx

from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

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
x = 0



pohybDelta1 = 0
pohybDelta2 = 0

tmx_map = pytmx.load_pygame("level1Map.tmx")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SPEED = 4

SCALE = 2.5                   #aby nemel misto
MSCALE = 5
#hrac
player = pygame.image.load("pacman2.png").convert()
player.set_colorkey((255,255,255))
player = pygame.transform.scale(player, (player.get_width() * SCALE, player.get_height() * SCALE))
player_rect = player.get_rect(topleft=(screen.get_width() / 2 -10, screen.get_height() / 2))
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
enemy1_plan_moveX = None
enemy1_plan_moveY = None
enemy1_move_done = True


player_grid_x = player_rect.x // 40
player_grid_y = player_rect.y // 40
enemy1_grid_x = enemy1_rect.x // 40
enemy1_grid_y = enemy1_rect.y // 40

#mapa hry
game_map = [
      [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
      [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
      [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
      [1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1],
      [1,0,1,0,0,0,1,0,0,0,0,0,1,0,0,0,1,0,1,1],
      [1,0,1,1,1,1,1,0,1,1,1,0,1,1,1,1,1,0,1,1],
      [1,0,0,0,0,1,0,0,1,1,1,0,0,1,0,0,0,0,1,1],
      [1,1,1,1,0,1,0,0,0,0,0,0,0,1,0,1,1,1,1,1],
      [1,1,1,1,0,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1],
      [0,0,0,0,0,1,0,0,1,0,1,0,0,1,0,0,0,0,0,1],
      [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
      [0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,1],
      [1,1,1,1,0,1,0,1,1,1,1,1,0,1,0,1,1,1,1,1],
      [1,1,1,1,0,1,0,1,0,1,0,1,0,1,0,1,1,1,1,1],
      [1,0,0,0,0,1,0,1,0,1,0,1,0,1,0,0,0,0,0,1],
      [1,0,1,1,1,1,1,1,0,1,0,1,1,1,1,1,1,1,0,1],
      [1,0,1,0,0,0,0,1,0,1,0,1,0,0,0,0,0,1,0,1],
      [1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1],
      [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
      [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
      [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]
# vytvoreni gridu
grid = Grid(matrix = game_map)

# vytvoreni startu a konce
start = grid.node(enemy1_grid_x, enemy1_grid_y)
end = grid.node(player_grid_x, player_grid_y)

# vytvoreni hledaciho pohybu
finder = AStarFinder()

# pouziti hledani na cestu
path,runs = finder.find_path(start,end,grid)

#print(path)
#idk 
path_with_ones = [[1 if cell == 0 else cell for cell in row] for row in path]

print(path_with_ones)


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
    player_grid_x = player_rect.x // 40
    player_grid_y = player_rect.y // 40
    enemy1_grid_x = enemy1_rect.x // 40
    enemy1_grid_y = enemy1_rect.y // 40

    #print(player_grid_x, player_grid_y, enemy1_grid_x, enemy1_grid_y)

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

    # Zacne to zjistovat pozice po 4s
    # Aktualizace pozice 1 každé dvě sekundy
    if pygame.time.get_ticks() % 1000 == 0:
        pohybDelta1 = [enemy1_rect.x, enemy1_rect.y]
    # Aktualizace pozice 2 každé dvě sekundy
    if pygame.time.get_ticks() % 2000 == 0:
        pohybDelta2 = [enemy1_rect.x, enemy1_rect.y]

    #print(pohybDelta1, pohybDelta2, enemy1_rect)

    """if (pohybDelta1 == pohybDelta2) or (enemy1_actionX == None or enemy1_actionY == None):
        if (enemy1_rect.right != player_rect.left and enemy1_rect.top != player_rect.bottom and enemy1_rect.bottom != player_rect.top and enemy1_rect.left != player_rect.right):
            check_pos = [enemy1_rect.x, enemy1_rect.y]
            if(check_pos == pohybDelta1 or check_pos == pohybDelta2):
                print(695584462436)
                if player_rect.y > enemy1_rect.y:
                    enemy1_plan_moveY = "down"
                    print("down")
                elif player_rect.y < enemy1_rect.y:
                    enemy1_plan_moveY = "up"
                    print("up")
                if player_rect.x > enemy1_rect.x:
                    enemy1_plan_moveX = "right"
                    print("right")
                elif player_rect.x < enemy1_rect.x:
                    enemy1_plan_moveX = "left"
                    print("left")"""
        


        #urceni smeru #5                        dfsghdfghdfgbrddhbgdgfhbdfghbdfghbfgdhbdfghbdfghbdfghb      (malem jsem rozbil klavesu kvuli teto podmince)

    # problem s velikosti postavicky nejak se proste hejbne a bum spusti se podminka, ale neni tam ulicka treba idk
    #   pokud se zmeni pozice           pokud jsou dva povely                       pokud jeho plan je jit nahoru ci dolu
    if positionY != player_rect.y:
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
    if positionX != player_rect.x:
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

        #teleport na druhou stranu
    if (player_rect.x < 0-player.get_width()//2) and actionX == "left":
        player_rect.x = screen.get_width()
        #print(player_rect.x,player_rect.y )
        #player_rect.y = 400
    elif player_rect.x > (screen.get_width()+player.get_width()//2+player.get_width()//2) :
        player_rect.x = 0
        #player_rect.y = 400
        #print(player_rect.x,player_rect.y )


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

    # if enemy1_actionX == None:
    #     enemy1_check_plan = "down"
    #     if enemy1_check_plan == "down" and enemy1_move_done == True:
    #         enemy1_move_done = False
    #         enemy1_plan_move = "down"
    # elif enemy1_actionY == None:
    #     enemy1_check_plan = "left"
    #     if enemy1_check_plan == "left" and enemy1_move_done == True:
    #         enemy1_move_done = False
    #         enemy1_plan_move = "left"
    # else:
    #     enemy1_check_plan = None


    #print(enemy1_check_plan, enemy1_actionX, enemy1_actionY)
    


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


    screen.blit(player, player_rect)
    screen.blit(enemy1, enemy1_rect)
    
    pygame.display.flip()
    clock.tick(60)