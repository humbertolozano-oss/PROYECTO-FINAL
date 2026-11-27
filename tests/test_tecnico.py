
import unittest
from models.equipo import Equipo
from models.tecnico import Tecnico


class TestTecnico(unittest.TestCase):

    def test_tecnico_inicia_libre(self):
        tecnico = Tecnico(1)

        self.assertTrue(tecnico.esta_libre())

    def test_asignar_equipo(self):
        tecnico = Tecnico(1)
        equipo = Equipo(1, 0, 5)

        tecnico.asignar_equipo(equipo, 0)

        self.assertFalse(tecnico.esta_libre())
        self.assertEqual(tecnico.tiempo_fin_atencion, 5)
        self.assertEqual(equipo.tiempo_inicio_atencion, 0)

    def test_liberar_equipo(self):
        tecnico = Tecnico(1)
        equipo = Equipo(1, 0, 5)

        tecnico.asignar_equipo(equipo, 0)
        resultado = tecnico.liberar_equipo(5)

        self.assertTrue(tecnico.esta_libre())
        self.assertEqual(resultado, equipo)
        self.assertEqual(equipo.tiempo_salida, 5)
        self.assertEqual(tecnico.equipos_atendidos, 1)

    def test_registrar_minuto_trabajo(self):
        tecnico = Tecnico(1)
        equipo = Equipo(1, 0, 5)

        tecnico.asignar_equipo(equipo, 0)
        tecnico.registrar_minuto_trabajo()

        self.assertEqual(tecnico.tiempo_ocupado, 1)


if __name__ == "__main__":
    unittest.main()
