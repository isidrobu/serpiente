
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"Modulo para gestion de escenas en Pygame."

import pygame as p
from pygame.locals import K_ESCAPE
from comun import PANTALLA
import MySQLdb

def salir(cerrar, teclado):
    "Define el fin del programa por medio de la tecla [Escape]."
    if cerrar:
        return False
    elif teclado:
        teclado = teclado[0]
        if teclado.key == K_ESCAPE:
            return False
    return True


class Director():
	"Clase para gestionar el juego"
	def __init__(self, titulo= ""):
		"Inicializar Pygame."
		p.init()
		self.pantalla = p.display.set_mode(PANTALLA)
		p.display.set_caption(titulo)
		self.escena = None
		self.reloj = p.time.Clock()
		self.fps=10

	def ejecutar(self, escena_inicial):
		"Ejecuta la logica del juego"
		self.escena = escena_inicial
		jugando = True
		value=False
		while jugando:
			"Para aumentar la frecuencia cada vez que comemos"
			if self.escena.comer() == True:
				self.fps+=2
			if value==True:
				self.fps=10		
			self.reloj.tick(self.fps)
			"Adquisicion de eventos."
			cerrar  = p.event.get(p.QUIT)
			teclado = p.event.get(p.KEYDOWN)
			"Interaccion con la escena."
			self.escena.eventos(teclado)
			value=self.escena.actualizar()
			self.escena.dibujar(self.pantalla, value)
			"Salir del juego."
			jugando = salir(cerrar, teclado)
			p.display.flip()



