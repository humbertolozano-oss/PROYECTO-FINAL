"""Pruebas unitarias para el Simulador de Centro de Servicio Técnico (Proyecto 3).
Verifica el cumplimiento de las reglas algorítmicas, la cola FIFO, el cálculo de métricas
y el manejo de entradas límite o inválidas.
"""

import unittest
import sys
import os

# Asegurar que el directorio raíz del proyecto esté en sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from models.simulador import SimuladorCentroServicio
from models.equipo import Equipo
from models.tecnico import Tecnico
from analytics.metricas import CalculadorMetricas


class TestSimuladorCentroServicio(unittest.TestCase):

    def test_caso_1_normal_sin_espera(self):
        """Caso 1: Normal / Holgado.
        2 técnicos, 4 equipos, llegada cada 5 min, atención 4 min.
        Como el intervalo entre llegadas (5 min) supera la atención (4 min),
        ningún equipo debe esperar en fila.
        """
        sim = SimuladorCentroServicio(
            num_tecnicos=2,
            num_equipos=4,
            intervalo_llegada=5,
            tiempo_atencion=4
        )
        while sim.ejecutar_paso():
            pass

        resumen = CalculadorMetricas.calcular_resumen(sim)

        self.assertEqual(resumen["equipos_atendidos"], 4)
        self.assertEqual(resumen["tiempo_promedio_espera"], 0.0)
        for eq in sim.equipos_atendidos:
            self.assertEqual(eq.calcular_tiempo_espera(), 0)

    def test_caso_2_limite_acumulacion_cola(self):
        """Caso 2: Límite / Saturación de cola (Cuello de botella).
        1 técnico, 4 equipos, llegada cada 2 min, atención 5 min.
        Cálculo teórico manual:
          - Eq 1: llega min 0, inicia min 0  -> espera 0 min.
          - Eq 2: llega min 2, inicia min 5  -> espera 3 min.
          - Eq 3: llega min 4, inicia min 10 -> espera 6 min.
          - Eq 4: llega min 6, inicia min 15 -> espera 9 min.
          Total espera = 0 + 3 + 6 + 9 = 18 min.
          Promedio espera = 18 / 4 = 4.50 min.
          Técnico ocupado de min 0 a 20 -> Utilización = 100.0%.
        """
        sim = SimuladorCentroServicio(
            num_tecnicos=1,
            num_equipos=4,
            intervalo_llegada=2,
            tiempo_atencion=5
        )
        while sim.ejecutar_paso():
            pass

        resumen = CalculadorMetricas.calcular_resumen(sim)

        self.assertEqual(resumen["equipos_atendidos"], 4)
        self.assertEqual(resumen["tiempo_promedio_espera"], 4.5)
        self.assertEqual(resumen["utilizacion_promedio"], 100.0)
        self.assertEqual(resumen["reloj"], 20)

        # Verificar tiempos individuales
        esperas_esperadas = [0, 3, 6, 9]
        for idx, eq in enumerate(sim.equipos_atendidos):
            self.assertEqual(eq.calcular_tiempo_espera(), esperas_esperadas[idx])

    def test_caso_3_parametros_invalidos(self):
        """Caso 3: Entradas inválidas y condiciones límite.
        El constructor del modelo debe rechazar valores que violen las restricciones de dominio.
        """
        # Técnicos no positivos
        with self.assertRaises(ValueError):
            SimuladorCentroServicio(num_tecnicos=0, num_equipos=5, intervalo_llegada=2, tiempo_atencion=5)
        with self.assertRaises(ValueError):
            SimuladorCentroServicio(num_tecnicos=-2, num_equipos=5, intervalo_llegada=2, tiempo_atencion=5)

        # Equipos no positivos
        with self.assertRaises(ValueError):
            SimuladorCentroServicio(num_tecnicos=2, num_equipos=0, intervalo_llegada=2, tiempo_atencion=5)
        with self.assertRaises(ValueError):
            SimuladorCentroServicio(num_tecnicos=2, num_equipos=-10, intervalo_llegada=2, tiempo_atencion=5)

        # Intervalo negativo
        with self.assertRaises(ValueError):
            SimuladorCentroServicio(num_tecnicos=2, num_equipos=5, intervalo_llegada=-1, tiempo_atencion=5)

        # Tiempo de atención no positivo
        with self.assertRaises(ValueError):
            SimuladorCentroServicio(num_tecnicos=2, num_equipos=5, intervalo_llegada=2, tiempo_atencion=0)

    def test_disciplina_fifo(self):
        """Verifica que el orden de atención cumpla estrictamente con First-In, First-Out."""
        sim = SimuladorCentroServicio(
            num_tecnicos=1,
            num_equipos=5,
            intervalo_llegada=1,
            tiempo_atencion=3
        )
        while sim.ejecutar_paso():
            pass

        ids_atendidos = [eq.id_equipo for eq in sim.equipos_atendidos]
        self.assertEqual(ids_atendidos, [1, 2, 3, 4, 5])


if __name__ == "__main__":
    unittest.main()
