try:
    import pygame,sys,random,threading,time,ConfigParser
    from pygame.locals import *
except (KeyboardInterrupt, SystemExit):
        raise
except:
    print("Error: No se lograron importar las librerias correctamente")
    raise


class Elemento(pygame.sprite.Sprite):
    def __init__(self, x, y, archivo):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(archivo).convert()
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        self.tipo = "ninguno"
        self.bloqueo = "no"
        self.actualizable = "no"

    def update_rect(self,x,y):
        self.rect = self.image.get_rect()
        self.rect.x= x
        self.rect.y= y

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

def checkCollision(sprite1, sprite2):
    col = pygame.sprite.collide_rect(sprite1, sprite2)
    if col == True:
        return True
    else:
        return False

def cargar_fondo(archivo, ancho, alto):
    imagen = pygame.image.load(archivo).convert_alpha()
    imagen_ancho, imagen_alto = imagen.get_size()
    tabla_fondos = []
    for fondo_x in range(0, imagen_ancho/ancho):
       linea = []
       tabla_fondos.append(linea)
       for fondo_y in range(0, imagen_alto/alto):
            cuadro = (fondo_x * ancho, fondo_y * alto, ancho, alto)
            linea.append(imagen.subsurface(cuadro))
    return tabla_fondos

def dibujarmapa(archivo,seccion,vxi,vyi):
    global images
    interprete = ConfigParser.ConfigParser()
    interprete.read(archivo)
    try:
        imagen = interprete.get(seccion, "origen")
        mapa = interprete.get(seccion, "mapa").split("\n")
        images = cargar_fondo(imagen, vxi,vyi)
    except:
        print("Error en la lectura de la seccion")
        sys.exit(0)
    try:
        for ey, punto in enumerate(mapa):
            for ex,cd in enumerate(punto):
                ls_valid.append((ex*vxi,ey*vyi))
                if((interprete.get(cd, "nombre") == "cesped_claro")):
                    vx = interprete.get(cd, "vx")
                    vy = interprete.get(cd, "vy")
                    m = Elemento(ex*vxi,ey*vyi,imagen)
                    m.image=images[int(vx)][int(vy)]
                    m.tipo=interprete.get(cd, "nombre")
                    m.bloqueo=interprete.get(cd, "muro")
                    m.actualizable=interprete.get(cd, "actualizable")
                    m.update_rect(ex*vxi,ey*vyi)

                    ls_todos.add(m)

                if((interprete.get(cd, "nombre") == "cesped_oscuro")):
                    vx = interprete.get(cd, "vx")
                    vy = interprete.get(cd, "vy")
                    m = Elemento(ex*vxi,ey*vyi,imagen)
                    m.image=images[int(vx)][int(vy)]
                    m.tipo=interprete.get(cd, "nombre")
                    m.bloqueo=interprete.get(cd, "muro")
                    m.actualizable=interprete.get(cd, "actualizable")
                    m.update_rect(ex*vxi,ey*vyi)

                    ls_todos.add(m)

    except:
        print("Archivo de configuracion corrupto reinstale el juego o contacte al soporte")
        sys.exit(0)


class Enemigo(pygame.sprite.Sprite):
    image_arriba = []
    image_abajo =  []
    image_derecha = []
    image_izquierda=[]
    def __init__(self, x,y, sp1,sp2):
        pygame.sprite.Sprite.__init__(self)

        matrizimg = cargar_fondo("data/images/ZombieSheet.png", 21,21)
        for i in range(sp1,sp2):
            self.image_abajo.append(matrizimg[i][0])
        for i in range(sp1,sp2):
            self.image_izquierda.append(matrizimg[i][1])
        for i in range(sp1,sp2):
            self.image_derecha.append(matrizimg[i][2])
        for i in range(sp1,sp2):
            self.image_arriba.append(matrizimg[i][3])

        self.image = self.image_derecha[0]
        self.rect = self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        self.vida=100

class Boton(pygame.sprite.Sprite):
	def __init__(self,archivo,xi,yi,nombre):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(archivo).convert_alpha()
		self.rect = self.image.get_rect()
		self.nombre = nombre
		self.rect.x = xi
		self.rect.y = yi

class Juego:
    nivel=1
    surface=None

    def __init__(self,nivel,surface):
        self.nivel = nivel
        self.surface = surface


    def gestor(self):
        if(self.nivel==1):
            self.nivel_1()


    def nivel_1(self):
        global ls_todos, ls_valid
        ALTO = 600
        ANCHO = 800
        pygame.init()
        reloj = pygame.time.Clock()
        pantalla = pygame.display.set_mode((ANCHO, ALTO+30))
        pygame.display.set_caption('%s  %.2f' % ("Defend the city - LVL 1       FPS:", reloj.get_fps()), 'Spine Runtime')
        pygame.display.set_icon(pygame.image.load("data/images/ico.png").convert_alpha())
        pantalla.fill((0,0,0))
        sub = pantalla.subsurface([0,ALTO, ANCHO, 30]) #Dibuja una surface sobre la pantalla
        tipo = pygame.font.SysFont("monospace", 15)
        tipo.set_bold(True)
        sub.fill((0,0,0))

        ls_valid = []
        ls_todos=pygame.sprite.Group()
        m = dibujarmapa("mapa.404","nivel1", 40,40)
        print ls_valid
        ls_todos.draw(self.surface)
        pygame.display.flip()
        while 1:
            next
