
# --- Lista de recetas ---

# Estas son las recetas predefinidas que
# pueden aparecer durante el juego

# Importamos las definiciones de cada objeto
from assets.classes import Receta

from assets.classes import Item


# Creamos una clase que contenga todas las recetas

class RecetaList:
    def __init__(self):
        
        # Primer receta
        self.receta1 = Receta(
            "Hamburguesa",
            [
                Item("Pan", 1),
                Item("Carne", 1),
                Item("Lechuga", 1),
                Item("Queso", 1)
            ]
            
        )
        
        
        # Lista de recetas para fácil acceso
        self.list = [
            self.receta1
            ]
        
    
    # Función getter para obtener una receta según su nombre
    def getReceta(self, name):
        for receta in self.list:
            if receta.name == name:
                return receta
        
        
    # Función getter para obtener toda la lista de recetas
    def getNames(self):
        return [
            self.receta1.name
            ]