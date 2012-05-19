"Escenas del juego."

from random import randrange
import pygame as p
from pygame.locals import K_F5
from comun import cargar_imagen, WIDTH, HEIGHT, Texto
import MySQLdb

class Serpiente(p.sprite.Sprite):
    "Define el comportamiento y caracteristicas de la serpiente."
    def __init__(self):
        "Inicializa la serpiente"
        p.sprite.Sprite.__init__(self)
        self.image = cargar_imagen("cuadro.png", True)
        self.rect = self.image.get_rect()
        self.direccion = 2
        self.cuerpo = []
        self.pos_x = 0
        self.pos_y = 0
        self.init_cuerpo()

    def init_cuerpo(self):
        "Crea el cuerpo de la serpiente y lo posiciona."
        pos_x = WIDTH / 2
        pos_y = HEIGHT / 2
        for i in range(0, 4):
            self.cuerpo.append(self.rect)
            self.cuerpo[i] = self.cuerpo[i].move(pos_x, pos_y)
            pos_y -= self.rect.h
        self.pos_x = pos_x
        self.pos_y = pos_y
            
    def teclado(self, evento):
        "Detecta los eventos del teclado para mover a la serpiente."
        if evento:
            tecla = evento[0].key - 272
            if 7 > (tecla + self.direccion) > 3:
                self.direccion = tecla

    def actualizar(self):
        "Actualiza la posicion de la serpiente en base a la direccion."
        if self.direccion == 2:
            self.pos_y += self.rect.h
        elif self.direccion == 1:
            self.pos_y -= self.rect.h
        elif self.direccion == 3:
            self.pos_x += self.rect.w
        elif self.direccion == 4:
            self.pos_x -= self.rect.w
        #Agregar nuevo elemento hacia la direccion indicada.
        self.cuerpo.insert(0, self.rect)
        self.cuerpo[0] = self.cuerpo[0].move(self.pos_x, self.pos_y)
        
    def se_alimento(self, comida):
        "Detecta si llego al alimento."
        if self.pos_x == comida.rect.x and self.pos_y == comida.rect.y:
            return True
        self.cuerpo.pop()
        return False
        
    def colisiona(self):
        "Verifica si hubo colision con alguna pared o consigo misma."
        if (self.cuerpo[0].left< 0 or self.cuerpo[0].right> WIDTH or
                self.cuerpo[0].top< 0 or self.cuerpo[0].bottom> HEIGHT or
                self.cuerpo[0] in self.cuerpo[1:]):
            return True
        return False



class Comida(p.sprite.Sprite):
    "Define la imagen de la comida y los lugares donde se encontrara."
    def __init__(self, serpiente):
        "Inicializa la comida."
        p.sprite.Sprite.__init__(self)
        #Cargar la imagen de la comida.
        self.image = cargar_imagen("comida.png", True)
        #Obtener las dimensiones de la comida.
        self.rect = self.image.get_rect()
        #Generar una comida.
        self.generar(serpiente)
        
    def generar(self, serpiente):
        "Genera nuevo alimento."
        while self.rect in serpiente.cuerpo:
            self.rect.left = randrange(0, WIDTH, self.rect.w)
            self.rect.top = randrange(0, HEIGHT, self.rect.h)
        
    def mostrar(self):
        "Sirve para regresar las coordenadas de la comida."
        return self.rect



class EscenaJuego():
    "Escena del juego."
    def __init__(self, nombre):
		"Nombre del jugador"
		self.nombre=nombre
		"Creamos los objetos del juego"
		self.serpiente = Serpiente()
		self.comida = Comida(self.serpiente)
		"Variables de control y puntuacion"
		self.puntos = 0
		self.haComido=False	
		self.insertar=False	
		self.termino = False
		"Texto"
		self.puntuacion = Texto("Puntos: ")
		self.fondo = cargar_imagen("terminado.jpg")
		self.terminado = Texto("Juego Terminado", tamano= 50) 
		
    "Mover la Serpiente"    
    def eventos(self, teclado = None):
        self.serpiente.teclado(teclado)

    "Comprobamos si la serpiente ha comido o colisiona"  
    def actualizar(self):
		self.serpiente.actualizar()
		if self.serpiente.se_alimento(self.comida):
			self.haComido=True
			self.comida.generar(self.serpiente)
			self.puntos += 10
		else:
			self.haComido=False
		if self.serpiente.colisiona():
			return True
		return False

    def comer(self):
        return self.haComido
    


    "Dibujamos la serpiente y la comida, tambien controla el final de la partida en el else"	
    def dibujar(self, pantalla, value):
		if value==False:
		    "Muestra los objetos en pantalla."
		    pantalla.fill( (0x11, 0x11, 0x11) )        
		    #Dibujar objetos en la interfaz.
		    pantalla.blit(self.comida.image, self.comida.mostrar())
		    pantalla.blit(self.puntuacion.mostrar(str(self.puntos)), 
		        self.puntuacion.pos(horz= 0, vert= 0))
		    #Dibujar la serpiente.
		    for i in range(0, len(self.serpiente.cuerpo)):
		        pantalla.blit(self.serpiente.image, self.serpiente.cuerpo[i])
		else:
			puntosTotales = Texto("Puntos: " + str(self.puntos), tamano= 32)  
			pantalla.blit(self.fondo, (0, 0))
			pantalla.blit(self.terminado.mostrar(),self.terminado.pos(1, 1, 0, -24))
			pantalla.blit(puntosTotales.mostrar(), puntosTotales.pos(1, 1, 0, 24))
			self.rankin(pantalla)

    "Insertamos la puntuacion e imprimimos el rankin"
    def rankin(self, pantalla):
		#Comprobamos que es la primera vez que entra para insertar la puntuacion
		if self.insertar==False and self.puntos!=0:
			self.insertarPuntos()
		self.imprimirRankin(pantalla)
		
		
    def imprimirRankin(self, pantalla):
		# Establecemos la conexion
		Conexion = MySQLdb.connect(host='localhost', user='root',passwd='root', db='serpiente')
		# Creamos el cursor
		cursor = Conexion.cursor()
		cursor.execute("SELECT * FROM Puntos ORDER BY Puntuacion DESC")
		score_data = cursor.fetchall()
		rows = len (score_data)
		puntosTotales = Texto("Nombre        Puntos", tamano= 30)
		pantalla.blit(puntosTotales.mostrar(), puntosTotales.pos(0,0,200,320))
		for i in range (0,5):
			puntosTotales = Texto(score_data[i][1], tamano= 30)
			aux=350
			aux+=i*20  
			pantalla.blit(puntosTotales.mostrar(), puntosTotales.pos(0,0,200,aux))
			puntosTotales2 = Texto(str(score_data[i][2]), tamano= 30)
			aux2=350
			aux2+=i*20  
			pantalla.blit(puntosTotales2.mostrar(), puntosTotales2.pos(0,0,340,aux2))
		Conexion.close()
		


    def insertarPuntos(self):
		# Establecemos la conexion
		Conexion = MySQLdb.connect(host='localhost', user='root',passwd='root', db='serpiente')
		# Creamos el cursor
		cursor = Conexion.cursor()
		self.insertar=True
		query= "SELECT * FROM Puntos WHERE id=(SELECT MAX(id) FROM Puntos)"
		cursor.execute(query)
		registros= cursor.fetchone()
		numero=registros[0]
		numero = numero+1
		#insertamos el la nueva puntuacion
		query='INSERT INTO Puntos (id,Nombre,Puntuacion) VALUES ("%d","%s","%d")'%(numero,self.nombre,self.puntos)
		cursor.execute(query)
		Conexion.commit()




