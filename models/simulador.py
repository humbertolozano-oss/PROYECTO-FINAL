from collections import deque
from models.equipo import Equipo
from models.tecnico import Tecnico


class SimuladorCentroServicio:
    """Motor de simulación discreta con cola FIFO para un centro de servicio técnico."""

    def __init__(self, num_tecnicos: int, num_equipos: int, intervalo_llegada: int, tiempo_atencion: int):
        if num_tecnicos <= 0:
            raise ValueError("El número de técnicos debe ser mayor a 0.")
        if num_equipos <= 0:
            raise ValueError("El número de equipos debe ser mayor a 0.")
        if intervalo_llegada < 0:
            raise ValueError("El intervalo de llegada no puede ser negativo.")
        if tiempo_atencion <= 0:
            raise ValueError("El tiempo de atención debe ser mayor a 0.")

        self.num_tecnicos = num_tecnicos
        self.num_equipos = num_equipos
        self.intervalo_llegada = intervalo_llegada
        self.tiempo_atencion = tiempo_atencion

        self.reloj = 0
        self.finalizada = False
        self.eventos_ultimo_paso = []

        # Crear técnicos disponibles
        self.tecnicos = [Tecnico(i + 1) for i in range(num_tecnicos)]

        # Generar lista de equipos pendientes con su minuto exacto de llegada
        self.equipos_pendientes = deque(
            Equipo(
                id_equipo=i + 1,
                tiempo_llegada=i * intervalo_llegada,
                duracion_atencion=tiempo_atencion
            )
            for i in range(num_equipos)
        )

        # Cola FIFO de espera
        self.cola_espera = deque()
        self.equipos_atendidos = []

    def ejecutar_paso(self) -> bool:
        """Ejecuta un paso discreto (1 minuto) en la simulación:
        1. Libera a los técnicos que terminaron su trabajo en el minuto actual.
        2. Recibe a los equipos que llegan en el minuto actual y los encola en la fila FIFO.
        3. Asigna equipos de la fila FIFO a técnicos libres.
        4. Verifica si la simulación ha concluido.
        5. Registra el trabajo activo de los técnicos y avanza el reloj.
        """
        if self.finalizada:
            return False

        self.eventos_ultimo_paso = []

        # Regla 1: Liberar técnicos cuya atención finalice en el minuto actual
        for tecnico in self.tecnicos:
            if not tecnico.esta_libre() and self.reloj >= tecnico.tiempo_fin_atencion:
                equipo_listo = tecnico.liberar_equipo(self.reloj)
                self.equipos_atendidos.append(equipo_listo)
                self.eventos_ultimo_paso.append(
                    f"[Min {self.reloj}] Técnico {tecnico.id_tecnico} terminó {equipo_listo}."
                )

        # Regla 2: Ingresar a la cola FIFO los equipos que llegan en este minuto
        while self.equipos_pendientes and self.equipos_pendientes[0].tiempo_llegada <= self.reloj:
            nuevo_equipo = self.equipos_pendientes.popleft()
            self.cola_espera.append(nuevo_equipo)
            self.eventos_ultimo_paso.append(
                f"[Min {self.reloj}] Llegó {nuevo_equipo} a la fila de espera."
            )

        # Regla 3: Asignar equipos en cola FIFO a técnicos que estén libres
        for tecnico in self.tecnicos:
            if tecnico.esta_libre() and self.cola_espera:
                siguiente_equipo = self.cola_espera.popleft()
                tecnico.asignar_equipo(siguiente_equipo, self.reloj)
                self.eventos_ultimo_paso.append(
                    f"[Min {self.reloj}] {siguiente_equipo} asignado a Técnico {tecnico.id_tecnico} "
                    f"(finaliza en min {tecnico.tiempo_fin_atencion})."
                )

        # Regla 4: Verificar si todos los equipos han sido atendidos
        todos_libres = all(t.esta_libre() for t in self.tecnicos)
        if not self.equipos_pendientes and not self.cola_espera and todos_libres:
            self.finalizada = True
            self.eventos_ultimo_paso.append(
                f"[Min {self.reloj}] Simulación finalizada con éxito. Todos los equipos fueron atendidos."
            )
            return False

        # Regla 5: Registrar tiempo trabajado en este minuto y avanzar el reloj
        for tecnico in self.tecnicos:
            tecnico.registrar_minuto_trabajo()

        self.reloj += 1
        return True
