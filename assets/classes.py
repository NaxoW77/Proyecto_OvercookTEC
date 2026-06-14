
# --- Clases ---

# Estas son diferentes clases para instanciar objetos,
# para luego utilizarlos en el juego y globalizar
# sus funciones y propiedades

# Imports necesarios
import tkinter as tk
from tkinter import ttk
import random as random

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
        self.size = 0 # Tamaño del jugador
        self.keySet = keySet # Teclas
        self.item = None # Objeto seleccionado
        
    # Método para detectar teclas
    def keyEvent(self, key, canvas):
        key = key.lower() # Minúsculas
        
        if key in self.keySet: # Revisamos las teclas en este jugadpr
            
            keyIndex = self.keySet.index(key) # Tecla específica
            if keyIndex < len(self.keySet)-1: # Teclas de movimiento
                if keyIndex == 0:
                    key = "w"
                elif keyIndex == 1:
                    key = "s"
                elif keyIndex == 2:
                    key = "a"
                elif keyIndex == 3:
                    key = "d"
                return self.move(key, canvas) # Ejecutamos el movimiento
        
            else:
                if keyIndex == 4: # Tecla de interacción
                    key = "e"
                return self.act(key, canvas) # Ejecutamos la interacción
        
    # Método para interactuar
    def act(self, key, canvas):
        
        # Cálculo de coordenadas relativas al movimiento según la dirección
        if self.direction == "up":
            relative_x = self.posX
            relative_y = self.posY - self.size
            
        elif self.direction == "down":
            relative_x = self.posX
            relative_y = self.posY + self.size
        
        elif self.direction == "left":
            relative_x = self.posX - self.size
            relative_y = self.posY
        
        elif self.direction == "right":
            relative_x = self.posX + self.size
            relative_y = self.posY
        
        # Revisamos la casilla en la posición relativa
        return self.checkCasilla(canvas, relative_x+self.size/2, relative_y+self.size/2)
        
    # Método para moverse por el canvas
    def move(self, key, canvas):
        dx = 0
        dy = 0

        # Izquierda
        if key == "a":
            relative_x = self.posX - self.size
            relative_y = self.posY
            
            self.direction = "left"
            
            # Revisamos si hay colisión
            if self.checkCasilla(canvas, relative_x + self.size/2, relative_y + self.size/2) != 0:
                return [0, 0] # Si hay colisión, no se mueve
            
            dx = -self.size
            self.posX -= self.size

        # Derecha
        elif key == "d":
            relative_x = self.posX + self.size
            relative_y = self.posY
            
            self.direction = "right"
            
            # Revisamos si hay colisión
            if self.checkCasilla(canvas, relative_x + self.size/2, relative_y + self.size/2) != 0:
                return [0, 0] # Si hay colisión, no se mueve
            
            dx = self.size
            self.posX += self.size

        # Arriba
        elif key == "w":
            relative_x = self.posX
            relative_y = self.posY - self.size
            
            self.direction = "up"
            
            # Revisamos si hay colisión
            if self.checkCasilla(canvas, relative_x + self.size/2, relative_y + self.size/2) != 0:
                return [0, 0] # Si hay colisión, no se mueve
            
            dy = -self.size
            self.posY -= self.size

        # Abajo
        elif key == "s":
            relative_x = self.posX
            relative_y = self.posY + self.size
            
            self.direction = "down"
            
            # Revisamos si hay colisión
            if self.checkCasilla(canvas, relative_x + self.size/2, relative_y + self.size/2) != 0:
                return [0, 0] # Si hay colisión, no se mueve
            
            dy = self.size
            self.posY += self.size
        
        return [dx, dy]
    
    # Método para revisar la casilla y devolver su tipo
    def checkCasilla(self, canvas, x, y):
            item = canvas.find_closest(x, y) # Lo buscamos en el canvas
            if isinstance(item, (tuple, list)): # Si devuelve más de un item
                item = item[0] # Tomamos el primero

            # Revisamos el color
            fill = canvas.itemcget(item, "fill")
            
            # Devolvemos el tipo
            if fill == "blue": # Otro jugador
                return -1
            elif fill == "purple": # Otro jugador
                return -1
            elif fill == "black": # Suelo
                return 0
            elif fill == "red": # Pared
                return 1
            elif fill == "green": # Mostrador
                return 2
            elif fill == "#916223": # Caja 3
                return 3
            elif fill == "#916224": # Caja 4
                return 4
            elif fill == "#916225": # Caja 5
                return 5
            elif fill == "#916226": # Caja 6
                return 6
            elif fill == "#d8d8d7": # Estación 7
                return 7
            elif fill == "#d8d8d8": # Estación 8
                return 8
            elif fill == "#d8d8d9": # Estación 9
                return 9
            else: # Caso de error
                return -1
        
        
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
        
        self.item = item
        
    def getItems(self):
        return self.item
    
# Se define el modelo de escenario
class Escenario:
    def __init__( # Parámetros de inicialización
        self,
        name="",
        desc = "",
        recetas=[],
        layout=[],
        tamaño=0,
        posChef1=[0,0],
        posChef2=[0,0],
        caja3=None,
        caja4=None,
        caja5=None,
        caja6=None,
        estacion7=None,
        estacion8=None,
        estacion9=None,
        fondo=""):
        
        self.name = name # Nombre del escenario
        self.desc = desc # Descripción
        self.recetas = recetas # Recetas disponibles
        self.layout = layout # Mapa
        self.tamaño = tamaño # Tamaño visual
        self.posChef1 = posChef1 # Posición inicial del chef 1
        self.posChef2 = posChef2 # Posición inicial del chef 2
        self.caja3 = caja3 # Estación 3
        self.caja4 = caja4 # Estación 4
        self.caja5 = caja5 # Estación 5
        self.caja6 = caja6 # Estación 6
        self.estacion7 = estacion7 # Estación 7
        self.estacion8 = estacion8 # Estación 8
        self.estacion9 = estacion9 # Estación 9
        self.cajas = [caja3, caja4, caja5, caja6] # Cajas
        self.estaciones = [estacion7, estacion8, estacion9] # Estaciones
        self.fondo = fondo # Imagen del escenario
    
    
# Clase de Caja de donde se obtienen ingredientes
class Caja:
    def __init__(self, name="", item=None): # Parámetros de inicialización
        self.name = name # Nombre de la caja
        self.item = item # Objeto de la caja
        
    # Método para obtener el item
    def obtener(self):
        return self.item


# Clase de Estacion donde se procesan ingredientes
class Estacion:
    def __init__(self, name="", type="", ingredients=[], results=[], img=""): # Parámetros de inicialización
        self.name = name # Nombre de la estacion
        self.type = type # Tipo de la estacion
        self.ingredients = ingredients # Ingredientes de la estacion
        self.results = results # Resultado de la estacion
        self.img = img # Imagen de la estacion

    # Método para procesar los ingredientes
    def procesar(self, ingrediente):
        if self.type == "Tira": # Basurero
            return []
        
        elif self.type == "Pica" or self.type == "Cocina": # Tabla o sartén
            
            for i in range(0,len(self.ingredients)):
                # Buscamos si el ingrediente es procesable
                if ingrediente.name == self.ingredients[i].name:
                    return self.results[i] # Devolvemos el resultado
            return -1


# Clase de Mostrador
class Mostrador:
    def __init__(self, name="", item=None): # Parámetros de inicialización
        self.name = name # Nombre del mostrador
        self.item = item # Objeto del mostrador
        self.x = 0 # Posición x
        self.y = 0 # Posición y
        
    # Método para colocar el item
    def colocar(self, item):
        self.item = item
        
    # Método para recoger el item
    def recoger(self, item):
        self.item = item
        return self.item



# Modelo de Receta
class Receta:
    def __init__(self, name="", ingredientes={}, img=""): # Parámetros de inicialización
        self.name = name # Nombre de la receta
        self.ingredientes = ingredientes # Ingredientes de la receta
        self.img = img # Imagen de la receta
        

# Modelo de Item
class Item:
    def __init__(self, name="", count=0, img=""): # Parámetros de inicialización
        self.name = name # Nombre del item
        self.count = count # Cantidad del item
        self.img = img # Imagen del item


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
    
    
    # Método para actualizar el item de un jugador
    def showPlayerItem(self, chef, chef_item,  canvas):
        item_img = tk.PhotoImage(file=chef.item.img).subsample(8,8)
        if chef.name == "Chef1":
            canvas.img1 = item_img
        else:
            canvas.img2 = item_img
        canvas.itemconfig(chef_item, image=item_img)
        
        
    # Método para actualizar los items de los mostradores
    def updateMostradores(self, mostradores, mostradores_img, canvas):
        for i in range(0,len(mostradores)):
            mostradores_img[i][0] = tk.PhotoImage(file=mostradores[i].item.img).subsample(8,8)
            canvas.itemconfig(mostradores_img[i][1], image=mostradores_img[i][0])
        
        
    # Método para ocultar un elemento
    def hide(self, elem):
        elem.pack_forget()
    
    
    # Método para mostrar un elemento
    def show(self, elem):
        elem.pack(fill="both", expand=True)