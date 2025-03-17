class Barril:
    def __init__(self,id,capacidad,estado,tipo):
        self.id = id  # ID autoincrementada
        self.tipo = tipo  # Roja, Negra, Rubia, IPA, APA
        self.capacidad = capacidad #10L, 20L, 50L
        self.estado = estado # Disponible, En uso, Limpieza


    def __str__(self):
        return f'ID: {self.id} | Tipo: {self.tipo} | Estado: {self.estado} | Capacidad: {self.capacidad}'

