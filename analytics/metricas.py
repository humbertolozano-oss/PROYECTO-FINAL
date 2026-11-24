class CalculadorMetricas:
    """Capa de Procesamiento de Datos. Calcula indicadores de desempeño a partir del estado del simulador."""

    @staticmethod
    def calcular_resumen(simulador) -> dict:
        """Calcula y retorna un diccionario con las métricas consolidadas del sistema."""
        # Equipos que ya iniciaron atención (terminados + en atención actual)
        equipos_en_atencion = [t.equipo_actual for t in simulador.tecnicos if not t.esta_libre()]
        equipos_con_espera = simulador.equipos_atendidos + equipos_en_atencion

        # 1. Tiempo promedio de espera
        if equipos_con_espera:
            total_espera = sum(e.calcular_tiempo_espera() for e in equipos_con_espera)
            tiempo_promedio_espera = total_espera / len(equipos_con_espera)
        else:
            tiempo_promedio_espera = 0.0

        # 2. Porcentaje de utilización por técnico
        utilizacion_por_tecnico = {}
        for tecnico in simulador.tecnicos:
            if simulador.reloj > 0:
                porcentaje = (tecnico.tiempo_ocupado / simulador.reloj) * 100
            else:
                porcentaje = 0.0
            utilizacion_por_tecnico[tecnico.id_tecnico] = round(porcentaje, 2)

        # 3. Utilización promedio del centro de servicio
        if utilizacion_por_tecnico:
            utilizacion_promedio = sum(utilizacion_por_tecnico.values()) / len(utilizacion_por_tecnico)
        else:
            utilizacion_promedio = 0.0

        return {
            "reloj": simulador.reloj,
            "equipos_atendidos": len(simulador.equipos_atendidos),
            "total_equipos": simulador.num_equipos,
            "en_cola": len(simulador.cola_espera),
            "tiempo_promedio_espera": round(tiempo_promedio_espera, 2),
            "utilizacion_por_tecnico": utilizacion_por_tecnico,
            "utilizacion_promedio": round(utilizacion_promedio, 2)
        }
