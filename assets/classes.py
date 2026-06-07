
# --- Clases ---

# Estas son diferentes clases para instanciar objetos,
# para luego utilizarlos en el juego y globalizar
# sus funciones y propiedades

# Imports necesarios
import tkinter as tk
from tkinter import ttk
import random as random

# Se optó por utilizar deepcopy para instanciar objetos
# Referencia: https://docs.python.org/3/library/copy.html
from copy import deepcopy

# Importar textos
from assets.lang import Lang
lang = Lang()

# Importar estilos
from assets.styles import Style
style = Style()


# Se define el modelo de jugador
class Player:
    def __init__(self, name="", character="", keySet=[]): # Parámetros de inicialización
        self.name = name if name else "" # Nombre del jugador
        self.character = character if character else "" # Imagen del jugador
        self.posX = 0 # Posición en x
        self.posY = 0 # Posición en y
        self.direction = "up" # Dirección
        self.size = 0
        self.keySet = keySet
        
        self.item = None
        
    # Método para detectar teclas
    def keyEvent(self, key, canvas):
        key = key.lower()
        
        if key in self.keySet:
            
            keyIndex = self.keySet.index(key)
            if keyIndex < len(self.keySet)-1:
                if keyIndex == 0:
                    key = "w"
                elif keyIndex == 1:
                    key = "s"
                elif keyIndex == 2:
                    key = "a"
                elif keyIndex == 3:
                    key = "d"
                return self.move(key, canvas)
        
            else:
                if keyIndex == 4:
                    key = "e"
                return self.act(key, canvas)
        
    # Método para interactuar
    def act(self, key, canvas):
        if self.direction == "up":
            return self.checkCasilla(canvas, self.posX + self.size/2, self.posY - self.size/2)
        elif self.direction == "down":
            return self.checkCasilla(canvas, self.posX + self.size/2, self.posY + self.size/2)
        elif self.direction == "left":
            return self.checkCasilla(canvas, self.posX - self.size/2, self.posY + self.size/2)
        elif self.direction == "right":
            return self.checkCasilla(canvas, self.posX + self.size/2, self.posY + self.size/2)
        
    # Método para moverse
    def move(self, key, canvas):
        dx = 0
        dy = 0

        if key == "a":
            relative_x = self.posX - self.size
            relative_y = self.posY
            
            self.direction = "left"
            
            if self.checkCasilla(canvas, relative_x + self.size/2, relative_y + self.size/2) != 0:
                return [0, 0]
            
            dx = -self.size
            self.posX -= self.size

        elif key == "d":
            relative_x = self.posX + self.size
            relative_y = self.posY
            
            self.direction = "right"
            
            if self.checkCasilla(canvas, relative_x + self.size/2, relative_y + self.size/2) != 0:
                return [0, 0]
            
            dx = self.size
            self.posX += self.size

        elif key == "w":
            relative_x = self.posX
            relative_y = self.posY - self.size
            
            self.direction = "up"
            
            if self.checkCasilla(canvas, relative_x + self.size/2, relative_y + self.size/2) != 0:
                return [0, 0]
            
            dy = -self.size
            self.posY -= self.size

        elif key == "s":
            relative_x = self.posX
            relative_y = self.posY + self.size
            
            self.direction = "down"
            
            if self.checkCasilla(canvas, relative_x + self.size/2, relative_y + self.size/2) != 0:
                return [0, 0]
            
            dy = self.size
            self.posY += self.size
        
        return [dx, dy]
    
    def checkCasilla(self, canvas, x, y):
            print(x, y)
            
            item = canvas.find_closest(x, y)
            if isinstance(item, (tuple, list)):
                item = item[0]
                
            fill = canvas.itemcget(item, "fill")
            print(fill)
            
            if fill == "blue":
                return -1
            elif fill == "purple":
                return -1
            elif fill == "red":
                return 1
            elif fill == "green":
                return 2
            elif fill == "cyan":
                return 3
            elif fill == "yellow":
                return 4
            else:
                return 0
        
        
    # --- Setters y getters
    
    # Nombre
    def setName(self, name):
        self.name = name
    
    def getName(self):
        return self.name
    
    # Avatar
    def setAvatar(self, avatar):
        self.avatar = avatar
    
    def getAvatar(self):
        return self.avatar
    
    # Puntaje
    def setScore(self, score):
        self.score = score
        
    def getScore(self):
        return self.score
    
    # Objetos
    def setItem(self, item):
        print("ITEM:", item)
        self.item = item
        
    def getItems(self):
        return self.item
    
# Se define el modelo de escenario
class Escenario:
    def __init__(self, name="", recetas=[], layout=[], tamaño=0, posChef1=[0,0], posChef2=[0,0], estacion3=None, img=""): # Parámetros de inicialización
        self.name = name # Nombre del escenario
        self.recetas = recetas # Recetas disponibles
        self.layout = layout # Mapa
        self.tamaño = tamaño # Tamaño visual
        self.posChef1 = posChef1 # Posición inicial del chef 1
        self.posChef2 = posChef2 # Posición inicial del chef 2
        self.estacion3 = estacion3 # Estación 3
        self.img = img # Imagen del escenario
    
    
# Clase de Caja de donde se obtienen ingredientes
class Caja:
    def __init__(self, name="", item=None, img=""): # Parámetros de inicialización
        self.name = name # Nombre de la caja
        self.item = item # Objeto de la caja
        self.img = img # Imagen de la caja
        
    def obtener(self):
        return self.item
        
# Clase de Estacion donde se procesan ingredientes
class Estacion:
    def __init__(self, name="", type="", ingredients={}, result={}, img=""): # Parámetros de inicialización
        self.name = name # Nombre de la estacion
        self.type = type # Tipo de la estacion
        self.ingredients = ingredients # Ingredientes de la estacion
        self.result = result # Resultado de la estacion
        self.img = img # Imagen de la estacion

    def procesar(self, ingredients):
        if self.ingredients == ingredients:
            return self.result
        else:
            return None

# Se define el modelo de receta
class Receta:
    def __init__(self, name="", type="", ingredients={}, img=""): # Parámetros de inicialización
        self.name = name # Nombre de la receta
        self.type = type # Tipo de la receta
        self.ingredients = ingredients # Ingredientes de la receta
        self.img = img # Imagen de la receta
        
    def test(self):
        print(self.name, self.type, self.ingredients, self.img)
        

class Item:
    def __init__(self, name="", count=0, img=""): # Parámetros de inicialización
        self.name = name # Nombre del item
        self.count = count # Cantidad del item
        self.img = img

# Se define el modelo de pantalla
# Este es el modelo que guardará secciones para poder mostrarlas luego
class StyledFrame(tk.Frame):
    def __init__(self, parent, controller, bg_color, root):
        super().__init__(parent, bg=bg_color)
        self.controller = controller # Controlador para llamar variables globales
        
    # Método para crear títulos rápidamente
    def create_title(self, parent, text, fg=style.colors["black"], bg=style.colors["default"]): # Parámetros
        return tk.Label(
            parent, # Ubicación
            text=text, # Texto
            fg=fg, # Color
            bg=bg, # Fondo
            font=style.A20, # Fuente
            padx=0, # Distanciado en x
            pady=3, # Distanciado en y
            )
    
    
    # Método para crear textos grandes rápidamente
    def create_text1(self, parent, text, padx=0, pady=5, wraplength=800, fg=style.colors["black"], bg=style.colors["default"]): # Parámetros
        return tk.Label(
            parent, # Ubicación
            text=text, # Texto
            fg=fg, # Color
            bg=bg, # Fondo
            font=style.a16, # Fuente
            padx=padx, # Distanciado en x
            pady=pady, # Distanciado en y
            wraplength=wraplength # Ancho máximo
            )


    # Método para crear textos medianos rápidamente
    def create_text2(self, parent, text, padx=0, pady=5, wraplength=800, justify="left", fg=style.colors["black"], bg=style.colors["default"]): # Parámetros
        return tk.Label(
            parent, # Ubicación
            text=text, # Texto
            fg=fg, # Color 
            bg=bg, # Fondo
            justify=justify, # Posición del texto
            font=style.a14, # Fuente
            padx=padx, # Distanciado en x
            pady=pady, # Distanciado en y
            wraplength=wraplength # Ancho máximo
            )
    
    # Método para crear botones
    def create_button1(self, parent, text, command):
        return tk.Button(
            parent, # Ubicación
            text=text, # Texto
            bg=style.colors["main"], # Fondo
            fg=style.colors["default"],  # Color
            font=style.a12, # Fuente
            padx=20, # Distanciado en x
            pady=10, # Distanciado en y
            relief="flat", # Diseño
            cursor="hand2", # Cursor
            command=command # Función
            )
        
        
    # Método para ocultar un elemento
    def hide(self, elem):
        elem.pack_forget()
    
    
    # Método para mostrar un elemento
    def show(self, elem):
        elem.pack(fill="both", expand=True)