# Documentacion de Pruebas Automatizadas

Proyecto : Simulador de Atencion en Centro de Servicio Tecnico
Curso : Algoritmia y Programacion
Proyecto Asignado : Proyecto 3
Fecha de Validación : 25 de Noviembre de 2026

## 1. Objetivo

Comprobar que los componentes del simulador funcionan correctamente. Se probara con pruebas unitarias e integración. Tambien se testearan algunos casos limite. Para ello se verificarán que se cumplan las reglas algoritmicas del problema a resolver. Tambien se deben verificar que se cumple la disciplina FIFO. Por otro lado se deberan probar que se calculan bien las metricas. Por otro lado tambien se deben probar que se manejan bien los parámetros incorrectos.

## 2. Metodologia

Para realizar el testing se ha usado la libreria unittest que es una libreria estandar de Python.
En cada prueba se han seguido los pasos de preparacion, ejecucion y verificacion.

Preparacion: creacion de objetos y parámetros necesarios.
Ejecucion: llamada de los métodos o funcionalidades a testear.
Verificacion: comprobación de que el resultado es el esperado (aserciones).

## 3. Estructura de pruebas

Archivo | Numero de pruebas | Descripcion
-----|------------------|----------
test_simulador.py | 4 | Pruebas generales del simulador. Casos obligatorios. FIFO.
test_equipo.py | 3 | Registro de tiempos. Calculo de espera.
test_tecnico.py | 4 | Disponibilidad. Asignacion. Liberacion. Ocupacion.
test_metricas.py | 4 | Calculo de los indicadores del sistema.
test_casos_limites.py | 4 | Casos limites.
Total | 19 |

## 4. Detalle de pruebas

### 4.1. Pruebas del simulador
Prueba | Resultado esperado | Estado
-----|------------------|-------
Caso normal sin espera | Se atienden 4 equipos. El tiempo medio de espera es 0 minutos | Aprobada
Caso limite de acumulacion | El tiempo medio de espera es 4.5 minutos. La utilización es 100%. El reloj termina en 20 minutos | Aprobada
Parámetros inválidos | Se lanzan excepciones de tipo ValueError | Aprobada
Disciplina FIFO | Los equipos son atendidos por orden de llegada | Aprobada
### 4.2. Pruebas de la clase Equipo
Prueba | Resultado esperado | Estado
-----|------------------|-------
Inicio de atención | Se registra el minuto 8 | Aprobada
Calculo del tiempo de espera | El tiempo de espera es 5 minutos | Aprobada
Finalizacion de atención | Se registra el minuto 13 como tiempo de salida | Aprobada
### 4.3. Pruebas de la clase Tecnico
Prueba | Resultado esperado | Estado
-----|------------------|-------
Disponibilidad inicial | El tecnico empieza libre | Aprobada
Asignación de equipo | El tecnico pasa a estar ocupado. Se registran los tiempos adecuadamente | Aprobada
Liberación de equipo | El tecnico pasa a estar disponible. Incrementa el contador de equipos atendidos | Aprobada
Registro de trabajo | El tiempo ocupado se incrementa en un minuto | Aprobada
### 4.4. Pruebas de métricas
Prueba | Resultado esperado | Estado
-----|------------------|-------
Métricas iniciales | Los indicadores de actividad están a cero | Aprobada
Total de equipos | Se registran correctamente los 5 equipos configurados | Aprobada
Utilización parcial | Las utilizaciones individuales son 100% y 0%. La media es 50% | Aprobada
Cantidad de equipos en cola | Hay 3 equipos en espera | Aprobada
### 4.5. Casos límite adicionales
Prueba | Resultado esperado | Estado
-----|------------------|-------
Un equipo y un técnico | Se atiende 1 equipo en 1 minuto. Sin tiempos de espera | Aprobada
Llegadas simultaneas | Los tiempos de espera individuales son 0, 2 y 4 minutos | Aprobada
Mas técnicos que equipos | La utilización media es 40%. Sin tiempos de espera | Aprobada
Simulación finalizada | Una vez finalizada la simulación el reloj no sigue avanzando | Aprobada
## 5. Ejecución de pruebas
Desde el directorio raíz del proyecto se debe lanzar el siguiente comando en la terminal.
python -m unittest discover -s tests -t . -v
No es necesario instalar ninguna librería externa.

## 6. Resultados obtenidos
Indicador | Resultado
--------|--------
Pruebas originales | 4
Pruebas adicionales | 15
Total de pruebas ejecutadas | 19
Pruebas aprobadas | 19
Pruebas fallidas | 0
Porcentaje de aprobación | 100%
Tiempo de ejecución | 0.005 segundos
Los resultados obtenidos han sido los esperados en los escenarios analizados.

## 7. Uso de Inteligencia Artificial

Se ha utilizado la herramienta ChatGPT para ayudar en la revisión del código. También se ha usado para estructurar las pruebas unitarias adicionales. Además se ha usado para interpretar los errores de ejecución. También se ha usado para generar esta documentación.

Las pruebas propuestas se han integrado en el proyecto. Se han ejecutado localmente (con Python). Los resultados se han verificado en la terminal. Se han comprobado que los valores obtenidos son los esperados.

## 8. Conclusiones

El hecho de que hayan pasado las 19 pruebas es indicativo de que los componentes evaluados funcionan correctamente.

Con las pruebas adicionales se ha mejorado la cobertura de las clases Equipo y Tecnico. Se han comprobado los indicadores del sistema. También se ha verificado el comportamiento del motor de simulación en diferentes condiciones límite.

De esta forma se mejora la confiabilidad y mantenibilidad del proyecto. Esto no implica que no haya errores en otros escenarios. Tampoco sustituye a las pruebas manuales de la interfaz gráfica.