class Equipo
    """Capa de Logica de Negocio. representa un equipo que llega al centro de servivicio tecnico"""
    def __init__(self, id_equipo: int, tiempo_llegada: int, duracion_atencion: int):
        self.id_equipo = id_equipo
        self.tiempo_llegada = tiempo_llegada
        self.duracion_atencion = duracion_atencion
        self.tiempo_inicio_atencion = None
        self.tiempo_salida = None

    def calcular_tiempo_espera(self) -> int:
        """calcula cuantos minutos espero en la fila el equipo antes de ser atendido"""
        if self.tiempo_inicio_atencion is None:
            return 0
        return self.tiempo_inicio_atencion - self.tiempo_llegada

    def __str__(self) -> str:
        return f"equipo #{self.id_equipo}"