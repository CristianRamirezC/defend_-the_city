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
        self.click = False

    def update_rect(self,x,y):
        self.rect = self.image.get_rect()
        self.rect.x= x
        self.rect.y= y
    def update(self,surface):
		if self.click :
			self.rect.center = pygame.mouse.get_pos()
		surface.blit(self.image,self.rect)

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
    def __init__(self, x,y, sp1,sp2, y1):
        pygame.sprite.Sprite.__init__(self)
        self.sp1=sp1
        self.sp2=sp2
        matrizimg = cargar_fondo("data/images/ZombieSheet.png", 32,32)
        for i in range(self.sp1,self.sp2):
            self.image_abajo.append(matrizimg[i][y1])
        for i in range(self.sp1,self.sp2):
            self.image_izquierda.append(matrizimg[i][y1+1])
        for i in range(self.sp1,self.sp2):
            self.image_derecha.append(matrizimg[i][y1+2])
        for i in range(self.sp1,self.sp2):
            self.image_arriba.append(matrizimg[i][y1+3])

        self.image = self.image_izquierda[0]
        self.rect = self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        self.vida=100
        self.velocidad=200
        self.control_velocidad = 0
        self.i = self.sp1

    def update(self):
        if(self.control_velocidad == 0):
            self.control_velocidad+=1
            self.rect.x -= 2
            if(self.i < self.sp2):
                #print len(self.image_izquierda)
                self.image = self.image_izquierda[self.i]
                self.i+=1
            else:
                self.i=self.sp1

        else:
            if(self.control_velocidad > self.velocidad):
                self.control_velocidad=0
            else:
                self.control_velocidad+=1


class Boton(pygame.sprite.Sprite):
	def __init__(self,archivo,x,y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(archivo).convert_alpha()
		self.rect = self.image.get_rect()
		self.nombre = nombre
		self.rect.x = xi
		self.rect.y = yi


class Bullet(pygame.sprite.Sprite): #Hereda de la clase sprite

    def __init__(self, img_name, x,y, direccion): #img para cargar, y su padre(de donde debe salir la bala)
    	pygame.sprite.Sprite.__init__(self)
    	self.image = pygame.image.load(img_name).convert_alpha()
    	self.rect = self.image.get_rect()
    	self.rect.x = x
    	self.rect.y = y
        self.speed = 3
        self.direccion = "derecha"
    def update(self):
            if(self.direccion == "derecha"): #derecha
                self.rect.x += self.speed
            if(self.direccion == "izquierda"):#izquierda
                self.rect.x -= self.speed
            if(self.direccion == "arriba"):#arriba
                self.rect.y -= self.speed
            if(self.direccion == "abajo"):#abajo
                self.rect.y += self.speed

class Soldado1(pygame.sprite.Sprite):
    def __init__(self, x,y):
        pygame.sprite.Sprite.__init__(self)
        matrizimg = cargar_fondo("data/images/soldados.png", 32,32)
        self.activado=False
        self.image=matrizimg[0][2]
        self.click=False
        self.bloqueo=False
        self.rect = self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        self.vida = 50
        self.fire_rate=0
        self.control_vida = 0

    def update_rect(self,x,y):
        self.rect = self.image.get_rect()
        self.rect.x= x
        self.rect.y= y
    def updatex(self,surface):
		if self.click :
			self.rect.center = pygame.mouse.get_pos()
		surface.blit(self.image,self.rect)

    def update(self):
        for e in ls_enemigos:
            if(checkCollision(self,e)):
                if(self.bloqueo):
                    e.rect.left = self.rect.right-1
                #e.rect.x += 1
                if(self.control_vida == 0):
                    self.control_vida+=1
                    self.vida -= 5
                else:
                    if(self.control_vida > 500):
                        self.control_vida=0
                    else:
                        self.control_vida+=1
        if(self.fire_rate==0):
            if(self.bloqueo and self.fire_rate==0):
                self.fire_rate+=1
                b = Bullet("data/images/bala.png", self.rect.x, self.rect.y, "derecha")
                ls_balas.add(b)
        else:
            if(self.fire_rate > 700):
                self.fire_rate=0
            else:
                self.fire_rate+=1

class Soldado2(pygame.sprite.Sprite):
    def __init__(self, x,y):
        pygame.sprite.Sprite.__init__(self)
        matrizimg = cargar_fondo("data/images/soldados.png", 32,32)
        self.activado=False
        self.image=matrizimg[3][6]
        self.click=False
        self.bloqueo=False
        self.rect = self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        self.vida = 20
        self.fire_rate=0
        self.control_vida = 0

    def update_rect(self,x,y):
        self.rect = self.image.get_rect()
        self.rect.x= x
        self.rect.y= y
    def updatex(self,surface):
		if self.click :
			self.rect.center = pygame.mouse.get_pos()
		surface.blit(self.image,self.rect)

    def update(self):
        for e in ls_enemigos:
            if(checkCollision(self,e)):
                if(self.bloqueo):
                    e.rect.left = self.rect.right-1
                #e.rect.x += 1
                if(self.control_vida == 0):
                    self.control_vida+=1
                    self.vida -= 5
                else:
                    if(self.control_vida > 500):
                        self.control_vida=0
                    else:
                        self.control_vida+=1
        if(self.fire_rate==0):
            if(self.bloqueo and self.fire_rate==0):
                self.fire_rate+=1
                b = Bullet("data/images/bala.png", self.rect.x, self.rect.y, "derecha")
                ls_balas.add(b)
        else:
            if(self.fire_rate > 500):
                self.fire_rate=0
            else:
                self.fire_rate+=1

class Soldado3(pygame.sprite.Sprite):
    def __init__(self, x,y):
        pygame.sprite.Sprite.__init__(self)
        matrizimg = cargar_fondo("data/images/soldados.png", 32,32)
        self.activado=False
        self.image=matrizimg[3][2]
        self.click=False
        self.bloqueo=False
        self.rect = self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        self.vida = 200
        self.fire_rate=0
        self.control_vida = 0

    def update_rect(self,x,y):
        self.rect = self.image.get_rect()
        self.rect.x= x
        self.rect.y= y
    def updatex(self,surface):
		if self.click :
			self.rect.center = pygame.mouse.get_pos()
		surface.blit(self.image,self.rect)

    def update(self):
        for e in ls_enemigos:
            if(checkCollision(self,e)):
                if(self.bloqueo):
                    e.rect.left = self.rect.right-1
                #e.rect.x += 1
                if(self.control_vida == 0):
                    self.control_vida+=1
                    self.vida -= 5
                else:
                    if(self.control_vida > 500):
                        self.control_vida=0
                    else:
                        self.control_vida+=1
        if(self.fire_rate==0):
            if(self.bloqueo and self.fire_rate==0):
                self.fire_rate+=1
                b = Bullet("data/images/bala.png", self.rect.x, self.rect.y, "derecha")
                ls_balas.add(b)
        else:
            if(self.fire_rate > 1000):
                self.fire_rate=0
            else:
                self.fire_rate+=1




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
        global ls_todos, ls_valid, ANCHO, ALTO, ls_enemigos, ls_arrastrable, ls_balas
        vidaf=100
        ALTO = 600
        ANCHO = 800
        pygame.init()
        reloj = pygame.time.Clock()
        pantalla = pygame.display.set_mode((ANCHO, ALTO+80))
        pygame.display.set_caption('%s  %.2f' % ("Defend the city - LVL 1       FPS:", reloj.get_fps()), 'Spine Runtime')
        pygame.display.set_icon(pygame.image.load("data/images/ico.png").convert_alpha())
        pantalla.fill((255,0,0))
        sub = pantalla.subsurface([0,ALTO, ANCHO, 50]) #Dibuja una surface sobre la pantalla
        tipo = pygame.font.SysFont("monospace", 15)
        tipo.set_bold(True)
        sub.fill((255,255,255))

        ls_valid = []

        ls_todos=pygame.sprite.Group()
        ls_enemigos=pygame.sprite.Group()
        ls_arrastrable=pygame.sprite.Group()
        ls_balas = pygame.sprite.Group()
        ls_soldados = pygame.sprite.Group()

        m = dibujarmapa("mapa.404","nivel1", 40,40)

        m = Soldado1(40*0,ALTO)
        ls_arrastrable.add(m)
        m=Soldado2(40*1,ALTO)
        ls_arrastrable.add(m)
        m=Soldado3(40*2,ALTO)
        ls_arrastrable.add(m)

        ls_todos.draw(self.surface)
        pygame.display.flip()
        presionado = False
        cont_waves=0
        muerto = False
        terminar=False
        while not terminar:
            if(vidaf <= 0):
                tipo2 = pygame.font.Font("data/fonts/Pixeled.ttf", 20)
                global picture
                picture = pygame.image.load("data/images/gameover.jpeg")
                picture = pygame.transform.scale(picture, (ANCHO, ALTO+10))
                rect = picture.get_rect()
                muerto = True
                sub.fill((0,0,0))
                tipo.set_bold(True)
                teclas1 = tipo2.render("Presione ESC para ir al menu" , 1 , (255,0,0))

            for event in pygame.event.get():
                if event.type==pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pantalla = pygame.display.set_mode((ANCHO, ALTO))
                        terminar=True
                        #sys.exit(0)

            P=pygame.mouse.get_pressed()
            if(P[0] == 1):
                for bloque in ls_arrastrable:
                    if(not bloque.click):
                        if bloque.rect.collidepoint(event.pos):
                            bloque.updatex(pantalla)
                            if(not bloque.bloqueo):
                                bloque.click = True
                                m = Soldado1(40*0,ALTO)
                                ls_arrastrable.add(m)
                                m=Soldado2(40*1,ALTO)
                                ls_arrastrable.add(m)
                                m=Soldado3(40*2,ALTO)
                                ls_arrastrable.add(m)
            else:
                for bloque in ls_arrastrable:
                    if(bloque.click):
                        bloque.updatex(pantalla)
                        if(bloque.click):
                            bloque.click = False
                            bloque.bloqueo = True


            if(cont_waves==0):
                cont_waves+=1
                ls_valid_en = []
                for i in xrange(15):
                    ls_valid_en.append(40*i)

                tipos = [(0,3,0),(3,6,0), (6,9,0)]
                velocidad =[100, 130, 400]
                vida= [100, 130, 400]

                for zombie in range(10):
                    index=random.randrange(0,len(tipos))
                    en=Enemigo(ANCHO, ls_valid_en[random.randrange(14)], tipos[index][0],tipos[index][1],tipos[index][2])
                    en.vida=vida[index]
                    en.velocidad=velocidad[index]
                    ls_enemigos.add(en)
            else:
                if(cont_waves > 100000):
                    cont_waves=0
                else:
                    cont_waves+=1

            for e in ls_enemigos:
                if(e.vida <= 0):
                    ls_enemigos.remove(e)

                for bulletx in ls_balas:
                    if(checkCollision(bulletx,e)):
                        print en.vida
                        e.vida-=random.randrange(10,15)
                        ls_balas.remove(bulletx)
                if(en.rect.x <= 0):
                    vidaf-=30


            for bloque in ls_arrastrable:
                if(bloque.click):
                    bloque.updatex(pantalla)
                if(bloque.vida <= 0):
                    ls_arrastrable.remove(ele)

            if(not muerto):
                pantalla.fill((255,0,0))
                sub.fill((255,255,255))
                ls_enemigos.update()
                ls_balas.update()
                ls_arrastrable.update()
                ls_todos.draw(pantalla)
                ls_arrastrable.draw(pantalla)
                ls_soldados.draw(pantalla)
                ls_balas.draw(pantalla)
                ls_enemigos.draw(pantalla)
            else:
                pantalla.blit(picture, rect)
                pantalla.blit(teclas1, [ANCHO/2-220,ALTO/2+300])
            pygame.display.flip()
