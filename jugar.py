"Script para ejecutar el juego."

from director import Director
from escenas import EscenaJuego
import sys

def main():
	"Ejecutar el juego."
	"Comprobacion de argumentos argv[1]=nombreJugador"
	if len(sys.argv) ==2:
		director = Director("Unbound Snake v0.2")
		director.ejecutar(EscenaJuego(str(sys.argv[1])))
	else:
		print "Argumentos invalidos, jugar.py Nombre"

if __name__ == "__main__":
    main()
