
import unittest
from models.simulador import SimuladorCentroServicio
from analytics.metricas import CalculadorMetricas


class TestMetricas(unittest.TestCase):

    def test_metricas_iniciales(self):
        sim = SimuladorCentroServicio(2, 4, 5, 4)

        resumen = CalculadorMetricas.calcular_resumen(sim)

        self.assertEqual(resumen["reloj"], 0)
        self.assertEqual(resumen["equipos_atendidos"], 0)
        self.assertEqual(resumen["tiempo_promedio_espera"], 0.0)
        self.assertEqual(resumen["utilizacion_promedio"], 0.0)

    def test_total_equipos(self):
        sim = SimuladorCentroServicio(2, 5, 3, 2)

        resumen = CalculadorMetricas.calcular_resumen(sim)

        self.assertEqual(resumen["total_equipos"], 5)

    def test_utilizacion_parcial(self):
        sim = SimuladorCentroServicio(2, 1, 1, 4)

        while sim.ejecutar_paso():
            pass

        resumen = CalculadorMetricas.calcular_resumen(sim)

        self.assertEqual(resumen["utilizacion_por_tecnico"][1], 100.0)
        self.assertEqual(resumen["utilizacion_por_tecnico"][2], 0.0)
        self.assertEqual(resumen["utilizacion_promedio"], 50.0)

    def test_cantidad_equipos_en_cola(self):
        sim = SimuladorCentroServicio(1, 4, 0, 5)

        sim.ejecutar_paso()

        resumen = CalculadorMetricas.calcular_resumen(sim)

        self.assertEqual(resumen["en_cola"], 3)


if __name__ == "__main__":
    unittest.main()
