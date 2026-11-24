class Equipo:
    """Representa un equipo que ingresa al centro de servicio técnico para diagnóstico y reparación."""

    def __init__(self, id_equipo: int, tiempo_llegada: int, duracion_atencion: int):
        self.id_equipo = id_equipo
        self.tiempo_llegada = tiempo_llegada
        self.duracion_atencion = duracion_atencion
        self.tiempo_inicio_atencion = None
        self.tiempo_salida = None

    def iniciar_atencion(self, reloj_actual: int) -> None:
        """Registra el minuto exacto en que el equipo entra a revisión con un técnico."""
        self.tiempo_inicio_atencion = reloj_actual

    def finalizar_atencion(self, reloj_actual: int) -> None:
        """Registra el minuto exacto en que concluye la reparación del equipo."""
        self.tiempo_salida = reloj_actual

    def calcular_tiempo_espera(self) -> int:
        """Calcula cuántos minutos esperó en la cola FIFO el equipo antes de ser atendido."""
        if self.tiempo_inicio_atencion is None:
            return 0
        return self.tiempo_inicio_atencion - self.tiempo_llegada

    def __str__(self) -> str:
        return f"Equipo #{self.id_equipo}"

    def __repr__(self) -> str:
        return f"Equipo(id={self.id_equipo}, llegada={self.tiempo_llegada}, duracion={self.duracion_atencion})"
