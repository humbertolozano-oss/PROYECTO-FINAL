# Proyecto Final: Simulador de Atención en un Centro de Servicio Técnico

**Curso:** Algoritmia y Programación  
**Proyecto Asignado:** Proyecto 3  
**Docente Revisor en GitHub:** `DnelZpt`  

---

## 👥 Integrantes del Equipo

| Nombre del Integrante | Usuario GitHub | Responsabilidad Principal |
| :--- | :--- | :--- |
| Humberto Lozano | `@humbertolozano-oss` | Coordinación y Motor de Simulación (`models/`) |
| [Jefry  2] | `@[usuario_github_2]` | Interfaz Gráfica de Usuario Tkinter (`ui/`) |
| [Nombre Integrante 3] | `@[usuario_github_3]` | Procesamiento Analítico y Métricas (`analytics/`) |
| [Nombre Integrante 4] | `@[usuario_github_4]` | Pruebas Unitarias, Casos de Prueba y Documentación (`tests/`) |

---

## 📋 Descripción General del Proyecto

Este proyecto consiste en el desarrollo de una aplicación funcional en **Python** provista de una **interfaz gráfica (GUI)** basada en los principios de la **Programación Orientada a Objetos (POO)**. 

La herramienta implementa una **simulación discreta paso a paso** para modelar el comportamiento operativo de un centro de diagnóstico y reparación técnica. Los equipos ingresan al sistema, esperan en una fila organizada bajo la disciplina **FIFO (First In, First Out)** y son asignados a técnicos de soporte en cuanto estos quedan libres.

El sistema permite experimentar con diversas configuraciones para estudiar cómo varían los cuellos de botella, la acumulación en la fila, los tiempos medios de espera y la tasa de utilización de la capacidad instalada.

---

## 🏛️ Arquitectura de Software y Modelado Orientado a Objetos

El código se encuentra modularizado en capas desacopladas, garantizando separación de responsabilidades:

```
PROYECTO-FINAL/
│
├── models/                     # CAPA DE LÓGICA DE NEGOCIO Y DOMINIO
│   ├── __init__.py
│   ├── equipo.py               # Entidad Equipo (tiempos de llegada, atención y cálculo de espera)
│   ├── tecnico.py              # Entidad Técnico (disponibilidad, asignación y ocupación)
│   └── simulador.py            # Motor de simulación discreta paso a paso con cola FIFO
│
├── analytics/                  # CAPA DE PROCESAMIENTO ANALÍTICO
│   ├── __init__.py
│   └── metricas.py             # Cálculo estadístico de indicadores en tiempo real
│
├── ui/                         # CAPA DE INTERFAZ GRÁFICA DE USUARIO
│   ├── __init__.py
│   └── app_gui.py              # GUI interactiva con Tkinter (presets, controles y visualizador)
│
├── tests/                      # SUITE DE PRUEBAS AUTOMATIZADAS
│   ├── __init__.py
│   └── test_simulador.py       # Pruebas unitarias de los 3 casos obligatorios y FIFO
│
├── main.py                     # Punto de entrada de la aplicación
└── README.md                   # Documentación técnica obligatoria
```

### Responsabilidades de las Clases Principales:
- `Equipo`: Modela el ciclo de vida de un dispositivo (llegada, inicio de atención, salida y tiempo neto en cola).
- `Tecnico`: Administra el estado de ocupación, el equipo actualmente asignado y registra los minutos de trabajo efectivo.
- `SimuladorCentroServicio`: Orquesta el paso del tiempo en minutos discretos ejecutando un ciclo estricto de 5 reglas:
  1. Liberación de técnicos que terminaron servicio.
  2. Recepción y encolado de nuevos equipos en la fila FIFO (`collections.deque`).
  3. Asignación inmediata de equipos en espera a técnicos libres.
  4. Evaluación de condición de parada (todos atendidos y fila vacía).
  5. Registro de minutos laborados y avance del reloj discreto.
- `CalculadorMetricas`: Procesa el estado actual del simulador y calcula el tiempo promedio de espera, equipos atendidos y el porcentaje de utilización individual y global de los técnicos.
- `SimuladorGUI`: Permite parametrizar el modelo, cargar presets de prueba, controlar la velocidad de ejecución (lenta, normal, rápida, paso a paso o simulación instantánea) y observar la animación en vivo.

---

## ⚙️ Requisitos e Instalación

La aplicación fue desarrollada utilizando exclusivamente la **biblioteca estándar de Python**, por lo que **no requiere la instalación de paquetes externos ni entornos virtuales complejos**.

- **Python 3.10 o superior** (incluye `tkinter` y `unittest`).

### Pasos de Ejecución

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/humbertolozano-oss/PROYECTO-FINAL.git
   cd PROYECTO-FINAL
   ```

2. **Ejecutar la aplicación gráfica:**
   ```bash
   python main.py
   ```

3. **Ejecutar las pruebas unitarias automatizadas:**
   ```bash
   python -m unittest discover -s tests
   ```

---

## 🧪 Demostración de los Tres Casos de Prueba Obligatorios

La aplicación cuenta con botones de acceso rápido (**Presets**) en la parte superior de la GUI para cargar y ejecutar directamente cada uno de estos escenarios durante la sustentación:

| Parámetro | Caso 1: Normal (Sin Espera) | Caso 2: Límite (Acumulación / Cuello de Botella) | Caso 3: Entrada Inválida / Excepciones |
| :--- | :---: | :---: | :---: |
| **Técnicos** | `2` | `1` | `0` (o `-2`) |
| **Equipos** | `4` | `4` | `-3` |
| **Intervalo de llegada** | `5 min` | `2 min` | `-1 min` |
| **Tiempo de atención** | `4 min` | `5 min` | `0 min` |

### Detalle Analítico y Comparación:

### 🔹 Caso 1: Escenario Normal / Holgado (Sin Espera)
* **Comportamiento:** Como el intervalo de llegada (5 min) es superior al tiempo de diagnóstico (4 min), cada equipo es recibido inmediatamente por un técnico disponible.
* **Resultado Esperado:** 
  * Tiempo promedio de espera: **0.00 min**.
  * Fila máxima: **0 equipos**.
  * Equipos atendidos: **4 de 4**.
* **Resultado Observado:** Idéntico al valor teórico (0.00 min).

### 🔹 Caso 2: Escenario Límite / Saturación (Cuello de Botella)
* **Comportamiento:** 
  * Eq 1: llega en min 0 $\rightarrow$ atiende en min 0, termina en min 5 $\rightarrow$ **Espera = 0 min**.
  * Eq 2: llega en min 2 $\rightarrow$ espera en cola hasta min 5 $\rightarrow$ **Espera = 3 min**.
  * Eq 3: llega en min 4 $\rightarrow$ espera en cola hasta min 10 $\rightarrow$ **Espera = 6 min**.
  * Eq 4: llega en min 6 $\rightarrow$ espera en cola hasta min 15 $\rightarrow$ **Espera = 9 min**.
* **Cálculo Analítico:** $\text{Espera promedio} = \frac{0 + 3 + 6 + 9}{4} = \frac{18}{4} = \mathbf{4.50\text{ min}}$.
* **Resultado Esperado:** 4.50 min de espera promedio, 100% utilización del técnico, reloj final en 20 min.
* **Resultado Observado:** Coincidencia exacta con 4.50 min y 100.0% de utilización.

### 🔹 Caso 3: Escenario con Parámetros Inválidos
* **Comportamiento:** Al introducir valores fuera de rango o caracteres alfanuméricos, la capa de interfaz y la capa de dominio capturan la excepción antes de alterar la memoria.
* **Resultado Esperado:** Ventana modal de alerta (`Error de Rango` / `Error de Formato`), impidiendo el colapso (*crash*) del programa.
* **Resultado Observado:** Captura limpia del error y preservación del estado del sistema.

---

## 🤖 Declaración de Uso de Herramientas de Inteligencia Artificial

En cumplimiento con el numeral 10 de los requerimientos transversales del curso:

1. **Herramientas utilizadas:** Google Antigravity (Agentic AI).
2. **Actividades asistidas:**
   - Propuesta inicial de la estructura modular por capas y diseño del diagrama de clases.
   - Generación de la plantilla base para los controles de Tkinter.
   - Asistencia en la estructuración de la suite de pruebas unitarias.
3. **Apropiación técnica, verificación humana y corrección de errores:**
   - Durante la auditoría técnica y revisión manual del código generado, el equipo detectó un **error crítico en `Tecnico.asignar_equipo`**: el código asignaba una variable incorrecta (`self.tiempo_inicio_atencio = reloj_actual`) en lugar de actualizar el atributo del objeto `equipo.tiempo_inicio_atencion`. Esto provocaba que `calcular_tiempo_espera()` devolviera siempre `0` en todas las simulaciones.
   - El equipo corrigió el error en los modelos, desacopló el método `iniciar_atencion()` en la clase `Equipo` y verificó analíticamente los resultados esperados mediante pruebas unitarias (`test_simulador.py`).
   - Se concluye que las respuestas de la IA fueron sometidas a revisión crítica, validación matemática y depuración antes de su integración definitiva.
