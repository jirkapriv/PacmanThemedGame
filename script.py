import pygame
import sys
import pytmx

pygame.init()

screen_size = [800, 800]
screen = pygame.display.set_mode((screen_size[0], screen_size[1]))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
game_name = "PacMan"  # zatim
left = False
right = False
down = False
up = False
run = True
action = None
tmx_map = pytmx.load_pygame("level1Map.tmx")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SPEED = 4

SCALE = 2
MSCALE = 5
player = pygame.image.load("pacman.png").convert()
player.set_colorkey((255,255,255))
player = pygame.transform.scale(player, (player.get_width() * SCALE, player.get_height() * SCALE))
player_rect = player.get_rect(topleft=(screen.get_width() / 2, screen.get_height() / 2))
playerFliped = player
playerRight = player
playerFliped = pygame.transform.flip(playerFliped, True, False)
playerDown = pygame.transform.rotate(player,270)
playerUp = pygame.transform.rotate(player,90)

pygame.display.set_caption(game_name)

while run:
    screen.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
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
                player = playerUp


    #teleport na druhou stranu
    if player_rect.x < 0-player.get_width():
        player_rect.x = screen.get_width()
    elif player_rect.x > screen.get_width()+player.get_width():
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


    if action == "left":
        player_rect.x -= SPEED
    if action == "right":
        player_rect.x += SPEED

        
    for layerX in tmx_map.visible_layers:
        if isinstance(layerX, pytmx.TiledTileLayer) and layerX.name == "Vrstva1":
            for x, y, tile in layerX.tiles():
                platformX = pygame.Rect(x * 8 * MSCALE, y * 8 * MSCALE,
                                        8 * MSCALE, 8 * MSCALE)
                if player_rect.colliderect(platformX):
                    if action == "right":
                        player_rect.right = platformX.left
                        
                    elif action == "left":
                        player_rect.left = platformX.right
                        
    if action == "down":
        player_rect.y += SPEED
    if action == "up":
        player_rect.y -= SPEED
        

    for layerY in tmx_map.visible_layers:
        if isinstance(layerY, pytmx.TiledTileLayer) and layerY.name == "Vrstva1":
            for n, m, tile in layerY.tiles():
                platformY = pygame.Rect(n * 8 * MSCALE, m * 8 * MSCALE,
                                        8 * MSCALE, 8 * MSCALE)
                if player_rect.colliderect(platformY):
                    if action == "down":
                        player_rect.bottom = platformY.top
                    elif action == "up":
                        player_rect.top = platformY.bottom




    screen.blit(player, player_rect)
    
    pygame.display.flip()
    clock.tick(60)
