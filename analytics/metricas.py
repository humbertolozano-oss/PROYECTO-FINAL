class CalculadorMetricas:
    """Capa de Procesamiento de Datos. Calcula los indicadores de desempeno a partir del estado del simulador.
    es obligatorio escribir @staticmethod sino el programa se detendra con un error"""

    @staticmethod
    def calcular_resumen(simulador) -> dict:
        """Retorna un diccionario con las metricas actuales de la simulacion."""
        # Equipos que ya empezaron a ser atendidos (terminados + en atencion actual)
        equipos_en_atencion = [t.equipo_actual for t in simulador.tecnicos if not t.esta_libre()]
        equipos_con_espera = simulador.equipos_atendidos + equipos_en_atencion

        # 1. Tiempo promedio de espera (evitando division por cero) len(cuenta cuantos elementos hay dentro de una lista)
        if equipos_con_espera:
            total_espera = sum(e.calcular_tiempo_espera() for e in equipos_con_espera)
            tiempo_promedio_espera = total_espera / len(equipos_con_espera)
        else:
            tiempo_promedio_espera = 0.0

        # 2. Utilizacion de cada tecnico (%)
        utilizacio_por_tecnico = {}
        for tecnico in simulador.tecnicos:
            if simulador.reloj > 0:
                porcentaje = (tecnico.tiempo_ocupado / simulador.reloj) * 100
            else:
                porcentaje = 0.0
            