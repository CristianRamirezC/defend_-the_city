from imports import *
pygame.mixer.init()

if not pygame.display.get_init():
    pygame.display.init()
if not pygame.font.get_init():
    pygame.font.init()
global ANCHO,ALTO,pantalla
ANCHO=800
ALTO=600
pantalla = pygame.display.set_mode((ANCHO,ALTO))
pantalla.fill((51,51,51))
m =Menu(pantalla)
m.draw_menu()

while 1:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                sys.exit()
