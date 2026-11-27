
import unittest
from models.simulador import SimuladorCentroServicio
from analytics.metricas import CalculadorMetricas


class TestCasosLimite(unittest.TestCase):

    def test_un_equipo_un_tecnico(self):
        sim = SimuladorCentroServicio(1, 1, 1, 1)

        while sim.ejecutar_paso():
            pass

        resumen = CalculadorMetricas.calcular_resumen(sim)

        self.assertEqual(resumen["equipos_atendidos"], 1)
        self.assertEqual(resumen["reloj"], 1)
        self.assertEqual(resumen["tiempo_promedio_espera"], 0.0)

    def test_llegadas_simultaneas(self):
        sim = SimuladorCentroServicio(1, 3, 0, 2)

        while sim.ejecutar_paso():
            pass

        esperas = [
            equipo.calcular_tiempo_espera()
            for equipo in sim.equipos_atendidos
        ]

        self.assertEqual(esperas, [0, 2, 4])

    def test_mas_tecnicos_que_equipos(self):
        sim = SimuladorCentroServicio(5, 2, 0, 3)

        while sim.ejecutar_paso():
            pass

        resumen = CalculadorMetricas.calcular_resumen(sim)

        self.assertEqual(resumen["equipos_atendidos"], 2)
        self.assertEqual(resumen["tiempo_promedio_espera"], 0.0)
        self.assertEqual(resumen["utilizacion_promedio"], 40.0)

    def test_simulacion_finalizada(self):
        sim = SimuladorCentroServicio(1, 2, 1, 2)

        while sim.ejecutar_paso():
            pass

        reloj_final = sim.reloj

        self.assertTrue(sim.finalizada)
        self.assertFalse(sim.ejecutar_paso())
        self.assertEqual(sim.reloj, reloj_final)
        self.assertEqual(len(sim.equipos_atendidos), 2)


if __name__ == "__main__":
    unittest.main()
