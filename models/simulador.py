from collections import deque
""" deque Es el nombre de la herramienta en si, abreviatura de Double-Ended Queue, cola de doble extremo"""
from models.equipo import Equipo
from models.tecnico import Tecnico


class SimuladorCentroServicio:
    """ motor de simulacion discreta( tiempo avanza en saltos fijos y contable min 1, min 2 ..... min n) con cola FIFO, First In, First Out"""

    def __init__(self, num_tecnicos: int, num_equipos: int, intervalo_llegada: int, tiempo_atencion: int):
        self.num_tecnicos = num_tecnicos
        self.num_equipos = num_equipos
        self.intervalo_llegada = intervalo_llegada
        self.tiempo_atencion = tiempo_atencion

        self.reloj = 0
        self.finalizada = False
        self.eventos_ultimo_paso = []

        # crear la lista de tecnicos
        self.tecnicos = [Tecnico(i + 1) for i in range(num_tecnicos)]

        # crear los equipos con su minuto exacto de llegada
        self.equipos_pendientes = deque(Equipo(id_equipo=i+1, tiempo_llegada=i * intervalo_llegada, 
        duracion_atencion=tiempo_atencion) for i in range(num_equipos))

        # cola FIFO: append() agrega al final, popleft() saca al primero
        """  append es agregar al final (agrega equipo nuevo al final de la cola),
         popleft saca el primero ( cuando un tecnico termina su trabajo y queda libre atiende el equipo que lleva mas tiempo en la cola"""
        self.cola_espera = deque()
        self.equipos_atendidos = []

    def ejecutar_paso(self) -> bool:
        """ ejecuta un minuto paso discreto de la simulacion:
        1. libera trcnicos que terminaron en el minuto actual
        2. rcibir equipos que llegan en el minuto actual
        3. asignar equipos de la cola a tecnicos libres
        4. verificar si la simulacion termino o avanzar el reloj 1 minuto """

        if self.finalizada:
            return False

        self.eventos_ultimo_paso = []

        # Regla 1: Revisar si algun tecnico termino su reparacion en este minuto
        for tecnico in self.tecnicos:
            if not tecnico.esta_libre() and self.reloj >= tecnico.tiempo_fin_atencion:
                equipo_listo = tecnico.liberar_equipo(self.reloj)
                self.equipos_atendidos. append(equipo_listo)
                self.eventos_ultimo_paso.append(f"[Min {self.reloj}] Tecnico {tecnico.id_tecnico} termino {equipo_listo}.")

        # Regla 2: Ingresar a la cola FIFO los equipos que llegan en este minuto.
        while self.equipos_pendientes and self.equipos_pendientes[0].tiempo_llegada <= self.reloj:
            nuevo_equipo = self.equipos_pendientes.popleft()
            self.cola_espera.append(nuevo_equipo)
            self.eventos_ultimo_paso.append(f" [Min {self.reloj}] llego {nuevo_equipo} a la fila. ")

        # Regal 3: Asignar equipos de la cola FIFO a los tecnicos libres
        for tecnico in self.tecnicos:
            if tecnico.esta_libre() and self.cola_espera:
                siguiente_equipo = self.cola_espera.popleft()
                tecnico.asignar_equipo(siguiente_equipo, self.reloj)
                self.eventos_ultimo_paso.append( f"[Min {self.reloj}] {siguiente_equipo} asignado a tecnico {tecnico.id_tecnico}"
                f"(termina en min {tecnico.tiempo_fin_atencion}).")

        # Regla 4: Verificar si todos los equipos fueron atendidos
        todos_libres = all(t.esta_libre() for t in self.tecnicos)
        if not self.equipos_pendientes and not self.cola_espera and todos_libres:
            self.finalizada = True
            self.eventos_ultimo_paso.append(f"[Min {self.reloj}] simulacion finalizada. todos los equipos atendidos")
            return False

        # Regla 5: Registrar tiempo trabajado en este minuto y avanzar el reloj
        for tecnico in self.tecnicos:
            tecnico.registrar_minuto_trabajo()

        self.reloj += 1
        return True
