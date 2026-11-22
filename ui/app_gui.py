""" Capa de Interfaz Grafica (ui/) y Punto de Entrada Esta capa permite configurar parámetros,
validar entradas inválidas, iniciar/pausar/reiniciar la simulación y ver en vivo la fila FIFO, 
los técnicos y las métricas."""

import tkinter as tk
from tkinter import ttk, messagebox
from models.simulador import SimuladorCentroServicio
from analytics.metricas import CalculadorMetricas


class SimuladorGUI:
    """Interfaz gráfica principal para el Simulador de Centro de Servicio Técnico."""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Simulador de Centro de Servicio Técnico (cola FIFO)")
        self.root.geometry("920x640")
        self.root.minsize (850,600)

        self.simulador = None
        self.corriendo = False
        self.job_id = None
        self.velocidad_ms = 500  # medio segundo por cada minuto simulado

        self.construir_interfaz()

    def construir_interfaz(self):
        #  Panel superior: Configuracion de parametros 
        frame_config = ttk.LabelFrame(self.root, text="Configuración de Parámetros")
        frame_config.pack(fill="x", padx=10, pady=5)

        self.var_tecnicos = tk.StringVar(value="2")
        self.var_equipos = tk.StringVar(value="6")
        self.var_llegada = tk.StringVar(value="2")
        self.var_atencion = tk.StringVar(value="5")

        campos = [("tencicos (1-50): ", self.var_tecnicos), ("equipos (1-200): ", self.var_equipos), 
        ("intervalo llegada (min): ", self.var_llegada), ("tiempo atencion (min): ", self.var_atencion)]

        for col, (texto, variable) in enumerate(campos):
            ttk.Label(frame_config, text=texto).grid(row=0, column=col*2, padx=5, pady=5, sticky="e")
            ttk.Entry(frame_config, textvariable=variable, width=8).grid(row=0, column=col*2+1, padx=5, sticky="w")

        # Panel de controles
        frame_botones = ttk.Frame(self.root, padding=5)  
        frame_botones.pack(fill="x", padx=10)

        self.btn_iniciar = ttk.Button(frame_botones, text="▶Iniciar / Reanudar", command=self.iniciar_simulacion)
        self.btn_iniciar.pack(side="left", padx=5)

        self.btn_pausar = ttk.Button(frame_botones, text="⏸ Pausar", command=self.pausar_simulacion, state="disabled")
        self.btn_pausar.pack(side="left", padx=5)

        self.btn_reiniciar = ttk.Button(frame_botones, text="↻ Reiniciar", command=self.reiniciar_simulacion)
        self.btn_reiniciar.pack(side="left", padx=5)

        self.lbl_reloj = ttk.Label(frame_botones, text="Reloj: 0 min", font=("Arial", 12, "bold"))
        self.lbl_reloj.pack(side="right", padx=10)

        # panel central: cola de la fila y tecnicos
        frame_estado = ttk.Frame(self.root, padding=5)
        frame_estado.pack(fill="both", expand=True, padx=10)

        # Subpanel izquierdo cola FIFO 
        frame_cola = ttk.LabelFrame(frame_estado, text="fila de espera FIFO", padding=10)   
        frame_cola.pack(side="left", fill="both", expand=True, padx=(0, 5))

        self.lista_cola = tk.Listbox(frame_cola, font=("consolas", 10)) 
        self.lista_cola.pack(fill="both", expand=True)

        # Subpanel derecho: tecnicos
        frame_tecnicos = ttk.LabelFrame(frame_estado, text="estado de los Tecnicos", padding=10)
        frame_tecnicos.pack(side="right", fill="both", expand=True, padx=(5, 0))

        self.lista_tecnicos = tk.Listbox(frame_tecnicos, font=("consolas", 10))
        self.lista_tecnicos.pack(fill="both", expand=True)

        # Panel de metricas
        frame_metricas = ttk.LabelFrame(self.root, text="indicadores de tiempo real", padding=10)
        frame_metricas.pack(fill="x", padx=10, pady=5)

        self.lbl_atendidos = ttk.Label(frame_metricas, text="Equipos atendidos: 0 / 0", font=("Arial", 10, "bold"))
        self.lbl_atendidos.pack(side="left", padx=15)

        self.lbl_espera = ttk.Label(frame_metricas, text="Espera promedio: 0.00 min", font=("Arial", 10, "bold"))
        self.lbl_espera.pack(side="left", padx=15)

        self.lbl_utilizacion = ttk.Label(frame_metricas, text="Utilización promedio: 0.00%", font=("Arial", 10, "bold"))
        self.lbl_utilizacion.pack(side="left", padx=15)

        # Panel inferio: Registro de eventos 
        frame_log = ttk.LabelFrame(self.root, text="Registro de Eventos", padding=5)
        frame_log.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self.txt_log = tk.Text(frame_log, height=7, state="disabled", font=("consolas", 9))
        self.txt_log.pack(fill="both", expand=True)

    def _validar_parametros(self):
        """Valida que los datos ingresados sean enteros válidos dentro de rangos seguros."""
        try:
            num_tecnicos = int(self.var_tecnicos.get())
            num_equipos = int(self.var_equipos.get())
            intervalo = int(self.var_llegada.get())
            atencion = int(self.var_atencion.get())
        except ValueError:
            messagebox.showerror("Error de rango", "Todos los parámetros deben ser números enteros.")
            return None

        if not (1 <= num_tecnicos <= 50):
            messagebox.showerror("Error de rango", "Número de técnicos debe estar entre 1 y 50.")
            return None
        if not (1 <= num_equipos <= 200):
            messagebox.showerror("Error de rango", "la cantidad de equipos debe estar entre 1 y 200.")
            return None
        if intervalo <= 0:
            messagebox.showerror("Error de rango", "El intervalo de llegada no puede ser cero o negativo.")
            return None
        if atencion < 1:
            messagebox.showerror("Error de rango", "El tiempo de atención debe ser al menos 1 minuto.")
            return None

        return num_tecnicos, num_equipos, intervalo, atencion

    def iniciar_simulacion(self):
        if self.simulador is None or self.simulador.finalizada:
            params = self._validar_parametros()
            if params is None:
                return  # Parámetros inválidos, no iniciar simulación
            self.simulador = SimuladorCentroServicio(*params)
            self._limpiar_log()

        self.corriendo = True
        self.btn_iniciar.config(state="disabled")
        self.btn_pausar.config(state="normal")
        self._ejecutar_ciclo()

    def pausar_simulacion(self):
        self.corriendo = False
        if self.job_id is not None:
            self.root.after_cancel(self.job_id)
            self.job_id = None
        self.btn_iniciar.config(state="normal")
        self.btn_pausar.config(state="disabled")

    def reiniciar_simulacion(self):
        self.pausar_simulacion()
        self.simulador = None
        self.lbl_reloj.config(text="Reloj: 0 min")
        self.lista_cola.delete(0, tk.END)
        self.lista_tecnicos.delete(0, tk.END)
        self.lbl_atendidos.config(text="Equipos atendidos: 0 / 0")
        self.lbl_espera.config(text="Espera promedio: 0.0 min")
        self.lbl_utilizacion.config(text="Utilización promedio: 0.0%")
        self._limpiar_log()

    def _ejecutar_ciclo(self):
        if not self.corriendo or self.simulador is None:
            return

        continua = self.simulador.ejecutar_paso()
        self._actualizar_vista()

        if continua:
            self.job_id = self.root.after(self.velocidad_ms, self._ejecutar_ciclo) 
        else:
            self.pausar_simulacion()
            messagebox.showinfo("Simulación completada", "todos los equipos han sido atendidos.")

    def _actualizar_vista(self):
        metricas = CalculadorMetricas.calcular_resumen(self.simulador)

        self.lbl_reloj.config(text=f"Reloj: {metricas['reloj']} min")
        self.lbl_atendidos.config(text=f"Equipos atendidos: {metricas['equipos_atendidos']} / {metricas['total_equipos']}")
        self.lbl_espera.config(text=f"Espera promedio: {metricas['tiempo_promedio_espera']} min")
        self.lbl_utilizacion.config(text=f"Utilización promedio: {metricas['utilizacion_promedio']}%")

        # Actualizar la lista de la cola FIFO
        self.lista_cola.delete(0, tk.END)
        if not self.simulador.cola_espera:
            self.lista_cola.insert(tk.END, "(Fila vacia)")
        else:
            for pos, eq in enumerate(self.simulador.cola_espera, start=1):
                self.lista_cola.insert(tk.END, f"{pos}. {eq} (llegó min {eq.tiempo_llegada})")

        # Actualizar la lista de técnicos
        self.lista_tecnicos.delete(0, tk.END)
        for tec in self.simulador.tecnicos:
            uso = metricas['utilizacion_por_tecnico'][tec.id_tecnico]
            if tec.esta_libre():
                estado = "Libre"
            else:
                estado = f"Atendiendo {tec.equipo_actual} (fin min {tec.tiempo_fin_atencion})"   
            self.lista_tecnicos.insert(tk.END, f"Técnico {tec.id_tecnico}: [{uso}%]: {estado}")

        # agregar eventos al registro.
        self.txt_log.config(state="normal")
        for evento in self.simulador.eventos_ultimo_paso:
            self.txt_log.insert(tk.END, evento + "\n")
        self.txt_log.see(tk.END)
        self.txt_log.config(state="disabled")

    def _limpiar_log(self):
        self.txt_log.config(state="normal")
        self.txt_log.delete("1.0", tk.END)
        self.txt_log.config(state="disabled")

