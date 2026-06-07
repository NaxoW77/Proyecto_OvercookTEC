
# --- Lista de escenarios ---

# Estas son las recetas predefinidas que
# se pueden utilizar en el juego

# Importamos las definiciones de cada objeto
from assets.classes import Escenario
from assets.classes import Caja
from assets.classes import Estacion
from assets.classes import Item
from assets.data import recetas
resetas = recetas.RecetaList()


# Creamos una clase que contenga todas las recetas

class EscenarioList:
    def __init__(self):
        
        # Primer escenario
        self.escenario1 = Escenario(
            name = "E1",
            recetas = [
                resetas.getReceta("Test1"),
                resetas.getReceta("Test2"),
                resetas.getReceta("Test3"),],
            
            # Mapa
            # Simbología:
            # 0 = vacío
            # 1 = pared
            # 2 = mostrador
            # 3 = Almacén 1
            # 4 = Almacén 2
            # 5 = Almacén 3
            # 6 = Estación 1
            # 7 = Estación 2
            layout = [
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 3, 3, 4, 4, 5, 5, 4, 4, 3, 3, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 6, 6, 6, 0, 0, 0, 0, 7, 7, 7, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 1, 1, 1, 2, 2, 2, 2, 1, 1, 1, 1]
            ],
            
            # Tamaños y posiciones
            tamaño = 50,
            posChef1 = [4, 9],
            posChef2 = [7, 9],
            
            # Tipos de estaciones
            estacion3 = Caja("Tomates", Item("Tomate", 1, "assets/img/tomate.png")),
        )
        
        
        # Lista de escenarios para fácil acceso
        self.list = [
            self.escenario1
            ]
        
    
    # Función getter por nombre
    def getEscenario(self, name):
        for escenario in self.list:
            if escenario.name == name:
                return escenario
        
        
    # Función getter de la lista
    def getEscenarios(self):
        return [
            self.escenario1.name
            ]