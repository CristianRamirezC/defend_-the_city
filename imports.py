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
    font_path3 = 'data/fonts/cubic.ttf'
    font = pygame.font.Font
    dest_surface = pygame.Surface
    start=(0,0)
    intro = True
    filepath_s = 'data/sounds/intr.ogg'
    def __init__(self, datos, dest_surface, position):
        self.intro = True
        self.reloj = pygame.time.Clock()
        self.tipo1 = self.font(self.font_path1, self.tam_font)
        self.tipo2 = self.font(self.font_path2, self.tam_font+30)
        self.tipo3 = self.font(self.font_path3, self.tam_font+15)

        self.dest_surface = dest_surface
        self.imagem = pygame.image.load("data/images/city.jpeg")
        self.imagem = pygame.transform.scale(self.imagem, (800, 600))

        self.lista = datos
        self.start = position
        self.color_n = (255,0,0)
        self.color_s = (0,255,0)
        self.cursor = 0
        self.imagem = pygame.image.load("data/images/city.jpeg")
        self.imagem = pygame.transform.scale(self.imagem, (800, 600))

    def get_color(self):
        l_colores=[]
        for i in range(len(self.lista)):
            l_colores.append(self.color_n)
        l_colores[self.cursor] = self.color_s
        return l_colores

    def draw_menu(self):
        pygame.display.set_caption('%s  %.2f' % ("Defend the city - Main       FPS:", self.reloj.get_fps()), 'Spine Runtime')
        pygame.display.set_icon(pygame.image.load("data/images/ico.png").convert_alpha())
        while 1:
            self.dest_surface.fill((51,51,51))
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
                                    self.intro=False
                    text = self.tipo1.render(cad , 1 , (random.randrange(100,255),0,0))
                    self.dest_surface.blit(text, (100,0))
                    text = self.tipo1.render(cad2 , 1 , (random.randrange(100,255),0,0))
                    self.dest_surface.blit(text, (30,60))
                    text = self.tipo2.render(cad3 , 1 , (random.randrange(100,255),0,0))
                    self.dest_surface.blit(text, (430,500))
                    pygame.display.flip()
                    i+=1
                    self.reloj.tick(2)
            else:
                y=self.start[1]
                self.dest_surface.blit(self.imagem, [0,0])
                l = self.get_color()
                for i in range(len(self.lista)):
                    text = self.tipo3.render(self.lista[i] , 1 , l[i])
                    self.dest_surface.blit(text, (self.start[0],y))
                    y+=70
                pygame.display.flip()
                break
