class Tecnico
    """representa un tecnico del centro de servicios"""
    def __init__(self, id_tecnico: int):
        self.id_tecnico = id_tecnico
        self.equipo_actual = None
        self.tiempo_fin_atencion = None
        self.tiempo_ocupado = 0
        self.equipos_atendidos = 0

    def esta_libre (self) -> bool:
        """ retorna true si el tecnico no esta atendiendo ningun equipo, bool solo puede ser verdadero ofalso, si o no """
        return self.equipo_actual is None

    def asignar_equipo(self, equipo, reloj_actual: int) -> None:
        """ asigna un equipo al tecnico y calcula en que minuto terminara """
        self.equipo_actual = equipo
        self.tiempo_inicio_atencio = reloj_actual
        self.tiempo_fin_atencion = reloj_actual + equipo.duracion_atencio

    def liberar_equipo(self, reloj_actual: int):
        """ filnaliza la atencion del equipo actual y deja al tecnico libre """
        equipo_terminado = self.equipo_actual
        equipo_terminado.tiempo_salida = reloj_actual
        self.equipos_atendidos += 1
        self.equipo_actual = None
        return equipo_terminado

    def registrar_minuto_trabajo(self) ->None:
        """ suma 1 minuto al tiempo total que el tecnico ha estado ocupado """
        if not self. esta_libre():
            self.tiempo_ocupado += 1