try:
    import pygame,sys,random,threading,time,ConfigParser
    from pygame.locals import *
except (KeyboardInterrupt, SystemExit):
        raise
except:
    print("Error: No se lograron importar las librerias correctamente")
    raise

class Menu:
    lista = []
    tam_font = 32
    font_path1 = 'data/fonts/Pixeled.ttf'
    font_path2 = 'data/fonts/Paskowy.ttf'
    font = pygame.font.Font
    dest_surface = pygame.Surface
    start=(0,0)
    intro = True
    filepath_s = 'data/sounds/intr.ogg'
    def __init__(self, dest_surface):
        self.intro = True
        self.reloj = pygame.time.Clock()
        self.tipo1 = self.font(self.font_path1, self.tam_font)
        self.tipo2 = self.font(self.font_path2, self.tam_font+30)
        self.dest_surface = dest_surface
        self.imagem = pygame.image.load("data/images/city.jpeg")
        self.imagem = pygame.transform.scale(self.imagem, (800, 600))

    #def get_color(self):
    def draw_menu(self):
        pygame.display.set_caption("sisas")
        if(self.intro):
            pygame.mixer.music.load(self.filepath_s)
            pygame.mixer.music.play(-1)
            ls_2 = "Defend the city v1.0 "
            ls_3 = "Computacion grafica UTP"
            ls_4 = "Cristian Camilo Ramirez"
            i=0
            p=0
            z=0
            cad=''
            cad2=''
            cad3=''
            segundo=False
            tercero=False
            while self.intro:
                if(i < len(ls_2)):
                    cad += ls_2[i]
                else:
                    segundo=True
                if(segundo):
                    if(p < len(ls_3)):
                        cad2 += ls_3[p]
                        p+=1
                        tercero=True
                    else:
                        self.dest_surface.blit(self.imagem, [0,120])
                        if(tercero):
                            if(z < len(ls_4)):
                                cad3 += ls_4[z]
                                z+=1
                            else:
                                pygame.time.delay(2000)
                                pygame.mixer.music.stop()
                                break
                text = self.tipo1.render(cad , 1 , (random.randrange(100,255),0,0))
                self.dest_surface.blit(text, (100,0))
                text = self.tipo1.render(cad2 , 1 , (random.randrange(100,255),0,0))
                self.dest_surface.blit(text, (30,60))
                text = self.tipo2.render(cad3 , 1 , (random.randrange(100,255),0,0))
                self.dest_surface.blit(text, (430,500))
                pygame.display.flip()
                i+=1
                self.reloj.tick(2)
