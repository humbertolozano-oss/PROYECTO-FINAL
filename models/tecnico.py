class Tecnico:
    """Representa a un técnico del centro de servicio técnico."""

    def __init__(self, id_tecnico: int):
        self.id_tecnico = id_tecnico
        self.equipo_actual = None
        self.tiempo_inicio_atencion = None
        self.tiempo_fin_atencion = None
        self.tiempo_ocupado = 0
        self.equipos_atendidos = 0

    def esta_libre(self) -> bool:
        """Retorna True si el técnico no está atendiendo ningún equipo actualmente."""
        return self.equipo_actual is None

    def asignar_equipo(self, equipo, reloj_actual: int) -> None:
        """Asigna un equipo al técnico, registra el inicio de atención y calcula el minuto proyectado de fin."""
        self.equipo_actual = equipo
        self.tiempo_inicio_atencion = reloj_actual
        self.tiempo_fin_atencion = reloj_actual + equipo.duracion_atencion
        equipo.iniciar_atencion(reloj_actual)

    def liberar_equipo(self, reloj_actual: int):
        """Finaliza la atención del equipo actual, actualiza métricas y deja al técnico libre."""
        equipo_terminado = self.equipo_actual
        equipo_terminado.finalizar_atencion(reloj_actual)
        self.equipos_atendidos += 1
        self.equipo_actual = None
        self.tiempo_inicio_atencion = None
        self.tiempo_fin_atencion = None
        return equipo_terminado

    def registrar_minuto_trabajo(self) -> None:
        """Suma 1 minuto al tiempo total que el técnico ha estado efectivamente ocupado."""
        if not self.esta_libre():
            self.tiempo_ocupado += 1

    def __str__(self) -> str:
        return f"Técnico #{self.id_tecnico}"
