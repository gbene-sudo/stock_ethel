class Barril:
    def __init__(self,capacidad,estado,tipo,id):
        self.capacidad = capacidad
        self.estado = estado
        self.tipo = tipo
        self.id = id

    def __str__(self):
        return f'{self.tipo} - {self.estado} - {self.capacidad}'
