
# --- Clases ---

# Estas son diferentes clases para instanciar objetos,
# para luego utilizarlos en el juego y globalizar
# sus funciones y propiedades

# Imports necesarios
import tkinter as tk
import tkinter.ttk as ttk
import random as random

# Se define el modelo de jugador
class Player:
    def __init__(self, name="", img="", keySet=[]): # Parámetros de inicialización
        self.name = name if name else "" # Nombre del jugador
        self.img = img if img else "" # Imagen del jugador
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
        
    # Objetos
    def setItem(self, item):
        self.item = item
        
    
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
        self.item = None # Objeto de la estacion
        self.x = 0 # Posición x
        self.y = 0 # Posición y
        self.cocinarIntv = None # Tiempo para cocinar
        self.resultadoIntv = None # Tiempo para obtener el resultado
        self.quemarIntv = None # Tiempo para quemar
        self.cont_cocina = None

    # Método para procesar los ingredientes
    def procesar(self, ingrediente, root):
        
        if self.type == "Tira": # Basurero
            return []
        
        elif self.type == "Pica": # Tabla
            for i in range(0,len(self.ingredients)):
                # Buscamos si el ingrediente es procesable
                if ingrediente.name == self.ingredients[i].name:
                    self.item = ingrediente
                    return self.results[i]
            return -1
        
        
        elif self.type == "Cocina": # Cocina
            
            if self.item.name == "Nada": # Si no hay un item dentro
                for i in range(0,len(self.ingredients)):
                    # Buscamos si el ingrediente es procesable
                    if ingrediente.name == self.ingredients[i].name:
                        self.item = ingrediente
                        
                        def cocinar(self, i):
                            self.item = self.results[i]
                            root.updateSlots()
                        
                        if self.cocinarIntv != None:
                            root.after_cancel(self.cocinarIntv)
                        
                        if self.cocinarIntv == None:    
                            self.cocinarIntv = root.after(3000, lambda: cocinar(self, i))
                        return 1 # Devolvemos espera
                
                return -1 # No se encontró un resultado
            
            else:
                # Si aún se está procesando
                for ing in self.ingredients:
                    if ing.name == self.item.name:
                        return 0 # No se ha procesado aún
                
                # Si ya se procesó
                result = self.item
                self.item = Item("Nada", 0)
                self.cocinarIntv = None
                return result # Devolvemos el item


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
    def create_title(self, parent, text, fg="black", bg="white"): # Parámetros
        return tk.Label(
            parent, # Ubicación
            text=text, # Texto
            fg=fg, # Color
            bg=bg, # Fondo
            font=("Arial", 20, "bold"), # Fuente
            padx=0, # Distanciado en x
            pady=3, # Distanciado en y
            )
    
    
    # Método para crear textos grandes rápidamente
    def create_text1(self, parent, text, padx=0, pady=5, wraplength=800, fg="black", bg="white"): # Parámetros
        return tk.Label(
            parent, # Ubicación
            text=text, # Texto
            fg=fg, # Color
            bg=bg, # Fondo
            font=("Arial", 16), # Fuente
            padx=padx, # Distanciado en x
            pady=pady, # Distanciado en y
            wraplength=wraplength # Ancho máximo
            )


    # Método para crear textos medianos rápidamente
    def create_text2(self, parent, text, padx=0, pady=5, wraplength=800, justify="left", fg="black", bg="white"): # Parámetros
        return tk.Label(
            parent, # Ubicación
            text=text, # Texto
            fg=fg, # Color 
            bg=bg, # Fondo
            justify=justify, # Posición del texto
            font=("Arial", 12), # Fuente
            padx=padx, # Distanciado en x
            pady=pady, # Distanciado en y
            wraplength=wraplength # Ancho máximo
            )
    
    
    # Método para crear botones
    def create_button1(self, parent, text, command):
        return tk.Button(
            parent, # Ubicación
            text=text, # Texto
            bg="#dbd339", # Fondo
            fg="black",  # Color
            font=("Arial", 12), # Fuente
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
        
        
    # Método para actualizar los items
    def updateSlots(self):
        for i in range(0,len(self.estaciones)):
            self.estaciones_img[i][0] = tk.PhotoImage(file=self.estaciones[i].item.img).subsample(8,8)
            self.canvas_fg.itemconfig(self.estaciones_img[i][1], image=self.estaciones_img[i][0])
        
        for i in range(0,len(self.mostradores)):
            self.mostradores_img[i][0] = tk.PhotoImage(file=self.mostradores[i].item.img).subsample(8,8)
            self.canvas_fg.itemconfig(self.mostradores_img[i][1], image=self.mostradores_img[i][0])
        
        
    # Método para ocultar un elemento
    def hide(self, elem):
        elem.pack_forget()
    
    
    # Método para mostrar un elemento
    def show(self, elem):
        elem.pack(fill="both", expand=True)



# Creamos una clase que contenga todos los escenarios
class EscenarioList:
    def __init__(self):
        
        # Escenario 1
        self.escenario1 = Escenario(
            name = "La Soda", # Nombre del escenario
            desc = "Prepara platillos al más puro estilo de una Soda típica. Locura total.", # Descripción del escenario
            
            recetas = [ # Lista de recetas posibles
                       
                # Receta 1
                Receta(
            "Hamburguesa con papas", # Nombre de la receta
            [ # Lista de ingredientes
                Item("Pan", 1),
                Item("Torta de carne", 1),
                Item("Tajada de queso", 1),
                Item("Papas fritas", 1)
            ],
            "assets/img/hamburguesa.png" # Imagen de la receta
            ),
            
            # Receta 2
            Receta(
                "Hamburguesa doble", # Nombre de la receta
                [ # Lista de ingredientes
                    Item("Pan", 1),
                    Item("Torta de carne", 1),
                    Item("Torta de carne", 1),
                    Item("Tajada de queso", 1),
                ],
                "assets/img/hamburguesa.png" # Imagen de la receta
            ),
            
            # Receta 3
            Receta(
                "Hamburguesa Triple", # Nombre de la receta
                [ # Lista de ingredientes
                    Item("Pan", 1),
                    Item("Torta de carne", 1),
                    Item("Torta de carne", 1),
                    Item("Torta de carne", 1)
                ],
                "assets/img/hamburguesa.png" # Imagen de la receta
            ),
            
            # Receta 4
            Receta(
                "Hamburguesa con papas y queso", # Nombre de la receta
                [ # Lista de ingredientes
                    Item("Pan", 1),
                    Item("Torta de carne", 1),
                    Item("Tajada de queso", 1),
                    Item("Papas fritas", 1)
                ],
                "assets/img/hamburguesa.png" # Imagen de la receta
            ),
            
            # Receta 5
            Receta(
                "Papas fritas con queso", # Nombre de la receta
                [ # Lista de ingredientes
                    Item("Papas fritas", 1),
                    Item("Papas fritas", 1),
                    Item("Tajada de queso", 1),
                    Item("Tajada de queso", 1)
                ],
                "assets/img/papas.png" # Imagen de la receta
            )
            ],
            
            # Mapa
            # Simbología:
            # 0 = Suelo
            # 1 = Pared
            # 2 = Mostrador (Si se coloca abajo es para entregas)
            # 3 = Almacén 1
            # 4 = Almacén 2
            # 5 = Almacén 3
            # 6 = Almacén 4
            # 7 = Estación 7
            # 8 = Estación 8
            # 9 = Estación 9
            
            # Tip: Desde VSCode se puede colocar el cursor sobre un número para ver sus coincidencias e imaginar cómo se vería
    
            layout = [
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 9, 3, 3, 4, 4, 5, 5, 6, 6, 9, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 7, 7, 7, 0, 0, 0, 0, 8, 8, 8, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 1, 1, 1, 2, 2, 2, 2, 1, 1, 1, 1]
            ],
            
            # Tamaño
            # ---No modificar---
            tamaño = 50,
            
            # Posiciones iniciales
            posChef1 = [4, 9], # Posición inicial chef1
            posChef2 = [7, 9], # Posición inicial chef2
            
            # Tipos de cajas
            caja3 = Caja("Carnes", Item("Carne cruda", 1, "assets/img/carne_cruda.png")),
            caja4 = Caja("Papas", Item("Papa", 1, "assets/img/papa.png")),
            caja5 = Caja("Panes", Item("Pan", 1, "assets/img/pan.png")),
            caja6 = Caja("Quesos", Item("Queso", 1, "assets/img/queso.png")),
            
            # Tipos de estaciones
            estacion7 = Estacion(
                "Tabla",
                "Pica", # Acción que realiza
                [ # Items que recibe (el índice coincide)
                    Item("Lechuga", 1, "assets/img/lechuga.png"),
                    Item("Carne cruda", 1, "assets/img/carne_cruda.png"),
                    Item("Tomate", 1, "assets/img/tomate.png"),
                    Item("Queso", 1, "assets/img/queso.png"),
                    Item("Papa", 1, "assets/img/papa.png")
                ],
                [ # Items que devuelve (el índice coincide)
                    Item("Lechuga picada", 1, "assets/img/lechuga_picada.png"),
                    Item("Carne picada", 1, "assets/img/carne_picada.png"),
                    Item("Tomate picado", 1, "assets/img/tomate_picado.png"),
                    Item("Tajada de queso", 1, "assets/img/queso_picado.png"),
                    Item("Papa picada", 1, "assets/img/papa_picada.png")
                ],
                "assets/img/tabla.png"), # Imagen de la estación
            
            estacion8 = Estacion(
                "Cocina",
                "Cocina", # Acción que realiza
                [ # Items que recibe (el índice coincide)
                Item("Carne picada", 1, "assets/img/carne_picada.png"),
                Item("Papa picada", 1, "assets/img/papa_picada.png"),
                ],
                [ # Items que devuelve (el índice coincide)
                    Item("Torta de carne", 1, "assets/img/carne.png"),
                    Item("Papas fritas", 1, "assets/img/papas.png")
                ],
                "assets/img/cocina.png"), # Imagen de la estación
            
            # Basurero
            estacion9 = Estacion("Basurero", "Tira", [], [], "assets/img/basurero.png"),
            
            
            fondo="assets/img/escenario1.png" # Imagen de fondo
        )
        
        
        # Escenario 2
        self.escenario2 = Escenario(
            name = "El Puerto",
            desc = "Viaja hasta Limón. ¿Qué tal si dividimos el trabajo?.",
            
            recetas = [
                Receta(
                    "\"Uno con todo\"",
                    [
                        Item("Lechuga picada", 1),
                        Item("Tomate picado", 1),
                        Item("Tronaditas", 1),
                        Item("Fresco", 1)
                    ],
                    "assets/img/ensalada.png"
                    ),
                
                Receta(
            "Ensalada con tronaditas",
            [
                Item("Lechuga picada", 1),
                Item("Lechuga picada", 1),
                Item("Tomate picado", 1),
                Item("Tronaditas", 1)
            ],
            "assets/img/ensalada.png"
            ),
            
            Receta(
                "Ensalada verde",
                [
                    Item("Lechuga picada", 1),
                    Item("Lechuga picada", 1),
                    Item("Lechuga picada", 1),
                    Item("Lechuga picada", 1),
                ],
                "assets/img/ensalada.png"
            ),
            
            Receta(
                "Ensalada con tomate",
                [
                    Item("Lechuga picada", 1),
                    Item("Lechuga picada", 1),
                    Item("Tomate picado", 1),
                    Item("Tomate picado", 1)
                ],
                "assets/img/ensalada.png"
            ),
            
            Receta(
                "Ensalada con fresco",
                [
                    Item("Lechuga picada", 1),
                    Item("Lechuga picada", 1),
                    Item("Tomate picado", 1),
                    Item("Fresco", 1)
                ],
                "assets/img/ensalada.png"
            )
            ],
            
            # Mapa
            # Simbología:
            # 0 = Suelo
            # 1 = Pared
            # 2 = Mostrador (Si se coloca abajo es para entregas)
            # 3 = Almacén 1
            # 4 = Almacén 2
            # 5 = Almacén 3
            # 6 = Almacén 4
            # 7 = Estación 7
            # 8 = Estación 8
            # 9 = Estación 9
    
            layout = [
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 3, 3, 4, 4, 1, 1, 5, 5, 6, 6, 1],
                [1, 0, 0, 0, 0, 7, 1, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 7, 1, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 8, 1, 0, 0, 0, 0, 1],
                [1, 9, 0, 0, 0, 8, 1, 0, 0, 0, 0, 1],
                [1, 1, 2, 2, 1, 1, 1, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 1],
                [1, 1, 1, 1, 2, 2, 2, 2, 1, 1, 1, 1]
            ],
            
            # Tamaños y posiciones
            tamaño = 50,
            posChef1 = [3, 4],
            posChef2 = [8, 8],
            
            # Tipos de estaciones
            caja3 = Caja("Lechugas", Item("Lechuga", 1, "assets/img/lechuga.png")),
            caja4 = Caja("Tomates", Item("Tomate", 1, "assets/img/tomate.png")),
            caja5 = Caja("Tronaditas", Item("Tronaditas", 1, "assets/img/tronaditas.png")),
            caja6 = Caja("Fresco", Item("Fresco", 1, "assets/img/fresco.png")),
            
            estacion7 = Estacion(
                "Tabla",
                "Pica",
                [
                    Item("Lechuga", 1, "assets/img/lechuga.png"),
                    Item("Carne cruda", 1, "assets/img/carne_cruda.png"),
                    Item("Tomate", 1, "assets/img/tomate.png"),
                    Item("Queso", 1, "assets/img/queso.png"),
                    Item("Papa", 1, "assets/img/papa.png")
                ],
                [
                    Item("Lechuga picada", 1, "assets/img/lechuga_picada.png"),
                    Item("Carne picada", 1, "assets/img/carne_picada.png"),
                    Item("Tomate picado", 1, "assets/img/tomate_picado.png"),
                    Item("Tajada de queso", 1, "assets/img/queso_picado.png"),
                    Item("Papa picada", 1, "assets/img/papa_picada.png")
                ],
                "assets/img/tabla.png"),
            
            estacion8 = Estacion(
                "Cocina",
                "Cocina",
                [
                Item("Carne picada", 1, "assets/img/carne_picada.png"),
                Item("Papa picada", 1, "assets/img/papa_picada.png"),
                ],
                [
                    Item("Torta de carne", 1, "assets/img/carne.png"),
                    Item("Papas fritas", 1, "assets/img/papas.png")
                ],
                "assets/img/cocina.png"),
            
            estacion9 = Estacion("Basurero", "Tira", [], [], "assets/img/basurero.png"),
            
            fondo="assets/img/escenario2.png"
        )
        
        
        # Escenario 3
        self.escenario3 = Escenario(
            name = "El Mercado Central",
            desc = "El Mercado Central es muy ajetreado. ¿Serás capaz de aguantar la tensión?.",
            
            recetas = [
                Receta(
            "Hamburguesa con papas",
            [
                Item("Pan", 1),
                Item("Torta de carne", 1),
                Item("Tajada de queso", 1),
                Item("Papas fritas", 1)
            ],
            "assets/img/hamburguesa.png"
            ),
            
            Receta(
                "Hamburguesa doble",
                [
                    Item("Pan", 1),
                    Item("Torta de carne", 1),
                    Item("Torta de carne", 1),
                    Item("Tajada de queso", 1),
                ],
                "assets/img/hamburguesa.png"
            ),
            
            Receta(
                "Hamburguesa Triple",
                [
                    Item("Pan", 1),
                    Item("Torta de carne", 1),
                    Item("Torta de carne", 1),
                    Item("Torta de carne", 1)
                ],
                "assets/img/hamburguesa.png"
            ),
            
            Receta(
                "Hamburguesa con papas y queso",
                [
                    Item("Pan", 1),
                    Item("Torta de carne", 1),
                    Item("Tajada de queso", 1),
                    Item("Papas fritas", 1)
                ],
                "assets/img/hamburguesa.png"
            ),
            
            Receta(
                "Papas fritas con queso",
                [
                    Item("Papas fritas", 1),
                    Item("Papas fritas", 1),
                    Item("Tajada de queso", 1),
                    Item("Tajada de queso", 1)
                ],
                "assets/img/papas.png"
            )
            ],
            
            # Mapa
            # Simbología:
            # 0 = Suelo
            # 1 = Pared
            # 2 = Mostrador (Si se coloca abajo es para entregas)
            # 3 = Almacén 1
            # 4 = Almacén 2
            # 5 = Almacén 3
            # 6 = Almacén 4
            # 7 = Estación 7
            # 8 = Estación 8
            # 9 = Estación 9
    
            layout = [
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 0, 1, 7, 7, 7, 1, 0, 1, 0, 1, 8, 8, 8, 1, 0, 1],
                [1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1],
                [1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1],
                [1, 5, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 4, 1],
                [1, 5, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 4, 1],
                [1, 3, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 6, 1],
                [1, 3, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 6, 1],
                [1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1],
                [1, 0, 1, 0, 0, 0, 0, 9, 1, 9, 0, 0, 0, 0, 1, 0, 1],
                [1, 0, 1, 0, 0, 0, 0, 9, 1, 9, 0, 0, 0, 0, 1, 0, 1],
                [1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1],
            ],
            
            # Tamaños y posiciones
            tamaño = 50,
            posChef1 = [4, 4],
            posChef2 = [12, 4],
            
            # Tipos de estaciones
            caja3 = Caja("Carnes", Item("Carne cruda", 1, "assets/img/carne_cruda.png")),
            caja4 = Caja("Papas", Item("Papa", 1, "assets/img/papa.png")),
            caja5 = Caja("Panes", Item("Pan", 1, "assets/img/pan.png")),
            caja6 = Caja("Quesos", Item("Queso", 1, "assets/img/queso.png")),
            
            estacion7 = Estacion(
                "Tabla",
                "Pica",
                [
                    Item("Lechuga", 1, "assets/img/lechuga.png"),
                    Item("Carne cruda", 1, "assets/img/carne_cruda.png"),
                    Item("Tomate", 1, "assets/img/tomate.png"),
                    Item("Queso", 1, "assets/img/queso.png"),
                    Item("Papa", 1, "assets/img/papa.png")
                ],
                [
                    Item("Lechuga picada", 1, "assets/img/lechuga_picada.png"),
                    Item("Carne picada", 1, "assets/img/carne_picada.png"),
                    Item("Tomate picado", 1, "assets/img/tomate_picado.png"),
                    Item("Tajada de queso", 1, "assets/img/queso_picado.png"),
                    Item("Papa picada", 1, "assets/img/papa_picada.png")
                ],
                "assets/img/tabla.png"),
            
            estacion8 = Estacion(
                "Cocina",
                "Cocina",
                [
                Item("Carne picada", 1, "assets/img/carne_picada.png"),
                Item("Papa picada", 1, "assets/img/papa_picada.png"),
                ],
                [
                    Item("Torta de carne", 1, "assets/img/carne.png"),
                    Item("Papas fritas", 1, "assets/img/papas.png")
                ],
                "assets/img/cocina.png"),
            
            estacion9 = Estacion("Basurero", "Tira", [], [], "assets/img/basurero.png"),
            
            fondo="assets/img/escenario3.png"
        )
        
        
        # Lista de escenarios para fácil acceso
        self.list = [
            self.escenario1,
            self.escenario2,
            self.escenario3
            ]
        
    
    # Función getter por nombre
    def getEscenario(self, name):
        for escenario in self.list:
            if escenario.name == name:
                return escenario
        
        
    # Función getter de la lista
    def getEscenarios(self):
        return self.list