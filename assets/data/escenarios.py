
# --- Lista de escenarios ---

# Estas son las recetas predefinidas que
# se pueden utilizar en el juego

# Importamos las definiciones de cada objeto
from assets.classes import Escenario
from assets.classes import Caja
from assets.classes import Estacion
from assets.classes import Item
from assets.classes import Receta


# Creamos una clase que contenga todas las recetas

class EscenarioList:
    def __init__(self):
        
        # Primer escenario
        self.escenario1 = Escenario(
            name = "E1",
            
            recetas = [
                Receta(
            "Hamburguesa con papas",
            [
                Item("Pan", 1),
                Item("Torta de carne", 1),
                Item("Queso picado", 1),
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
                    Item("Queso picado", 1),
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
                    Item("Queso picado", 1),
                    Item("Papas fritas", 1)
                ],
                "assets/img/hamburguesa.png"
            ),
            
            Receta(
                "Papas fritas con queso",
                [
                    Item("Papas fritas", 1),
                    Item("Papas fritas", 1),
                    Item("Queso picado", 1),
                    Item("Queso picado", 1)
                ],
                "assets/img/papas.png"
            )
            ],
            
            # Mapa
            # Simbología:
            # 0 = Suelo
            # 1 = Pared
            # 2 = Mostrador
            # 3 = Almacén 1
            # 4 = Almacén 2
            # 5 = Almacén 3
            # 6 = Almacén 4
            # 7 = Estación 1
            # 8 = Estación 1
            # 9 = Estación 2
    
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
            
            # Tamaños y posiciones
            tamaño = 50,
            posChef1 = [4, 9],
            posChef2 = [7, 9],
            
            # Tipos de estaciones
            caja3 = Caja("Carnes", Item("Carne cruda", 1, "assets/img/carne_cruda.png")),
            caja4 = Caja("Papas", Item("Papa", 1, "assets/img/papa_cruda.png")),
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
                    Item("Queso picado", 1, "assets/img/queso_picado.png"),
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
            
            fondo="assets/img/escenario1.png"
        )
        
        self.escenario2 = Escenario()
        
        self.escenario3 = Escenario()
        
        
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
        return [
            self.escenario1.name
            ]