
import unittest
from models.equipo import Equipo


class TestEquipo(unittest.TestCase):

    def test_iniciar_atencion(self):
        equipo = Equipo(1, 3, 5)

        equipo.iniciar_atencion(8)

        self.assertEqual(equipo.tiempo_inicio_atencion, 8)

    def test_calcular_tiempo_espera(self):
        equipo = Equipo(1, 3, 5)

        equipo.iniciar_atencion(8)

        self.assertEqual(equipo.calcular_tiempo_espera(), 5)

    def test_finalizar_atencion(self):
        equipo = Equipo(1, 3, 5)

        equipo.finalizar_atencion(13)

        self.assertEqual(equipo.tiempo_salida, 13)


if __name__ == "__main__":
    unittest.main()
