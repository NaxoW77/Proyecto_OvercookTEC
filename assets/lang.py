
# --- Archivo de idiomas ---

# Aquí se guardan todos los textos del juego para
# poder utilizarlos en cualquier parte del proyecto

# NOTA: Este archivo se debe dejar de último

# Se define la clase principal
# Por cada clase hay una subclase para cada pantalla
class Lang:
    
    # Textos principales
    def __init__(self):
        self.title = "OvercookTEC" # Título principal del proyecto
        
        # Llamada a subclases
        self.titleScreen = Lang.TitleScreen(self)
        
        # Footer principal del proyecto
        self.copyright = "Copyright © 2026 Ignacio Apuy, Jordanny Hernandez."
        
        # Mensaje en blanco
        self.default = "---"
    
    
    # Subclase para la pantalla de título
    class TitleScreen:
        def __init__(self, super):
            
            # Títulos
            self.title = "Bienvenido"
            self.description = self.concat(
                f"{super.title} es un proyecto.",
                "\nEl objetivo de este proyecto es.",
            )
            
            # Test
            self.test = "Test:"
            
            # Sección de tests
            # Concat() se utiliza para unir los textos por línea
            self.tests = self.concat(
                "Hola",
                "\ny",
                "\nAdios.",
            )
            
            # Mensaje en blanco
            self.default = "---"
            
            
        
        # Función para concatenar texto por líneas
        def concat(self, *args):
            return "\n".join(args)