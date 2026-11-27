"""Capa de Interfaz Gráfica (ui/).
Permite configurar parámetros, cargar casos de prueba oficiales,
controlar la velocidad de simulación, avanzar paso a paso o en tiempo real,
y visualizar la cola FIFO, el estado de los técnicos y las métricas del sistema.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from models.simulador import SimuladorCentroServicio
from analytics.metricas import CalculadorMetricas


class SimuladorGUI:
    """Interfaz gráfica principal para el Simulador de Centro de Servicio Técnico."""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Simulador de Centro de Servicio Técnico - Cola FIFO")
        self.root.geometry("980x700")
        self.root.minsize(900, 650)

        self.simulador = None
        self.corriendo = False
        self.job_id = None
        self.velocidad_ms = 250  # Velocidad por defecto

        self.construir_interfaz()

    def construir_interfaz(self):
       

        # 2. Panel superior: Configuración de Parámetros
        self.frame_config = ttk.LabelFrame(self.root, text="Configuración de Parámetros")
        self.frame_config.pack(fill="x", padx=10, pady=5)

        self.var_tecnicos = tk.StringVar(value="2")
        self.var_equipos = tk.StringVar(value="6")
        self.var_llegada = tk.StringVar(value="3")
        self.var_atencion = tk.StringVar(value="5")

        campos = [
            ("Técnicos (1-30):", self.var_tecnicos),
            ("Equipos (1-100):", self.var_equipos),
            ("Intervalo llegada (min):", self.var_llegada),
            ("Tiempo atención (min):", self.var_atencion)
        ]

        self.entries_config = []
        for col, (texto, variable) in enumerate(campos):
            ttk.Label(self.frame_config, text=texto).grid(row=0, column=col * 2, padx=5, pady=5, sticky="e")
            entry = ttk.Entry(self.frame_config, textvariable=variable, width=8)
            entry.grid(row=0, column=col * 2 + 1, padx=5, sticky="w")
            self.entries_config.append(entry)

        # 3. Panel de Controles y Velocidad
        frame_controles = ttk.LabelFrame(self.root, text="Controles de Ejecución y Velocidad")
        frame_controles.pack(fill="x", padx=10, pady=5)

        self.btn_iniciar = ttk.Button(frame_controles, text="▶ Iniciar / Reanudar", command=self.iniciar_simulacion)
        self.btn_iniciar.pack(side="left", padx=5, pady=5)

        self.btn_pausar = ttk.Button(frame_controles, text="⏸ Pausar", command=self.pausar_simulacion, state="disabled")
        self.btn_pausar.pack(side="left", padx=5, pady=5)

        self.btn_paso = ttk.Button(frame_controles, text="⏭ Paso a Paso (+1 min)", command=self.ejecutar_un_paso)
        self.btn_paso.pack(side="left", padx=5, pady=5)

        self.btn_completar = ttk.Button(frame_controles, text="⚡ Ejecutar Completo", command=self.ejecutar_todo)
        self.btn_completar.pack(side="left", padx=5, pady=5)

        self.btn_reiniciar = ttk.Button(frame_controles, text="↻ Reiniciar", command=self.reiniciar_simulacion)
        self.btn_reiniciar.pack(side="left", padx=5, pady=5)

        # Control de velocidad
        ttk.Label(frame_controles, text="Velocidad:").pack(side="left", padx=(15, 5))
        self.combo_velocidad = ttk.Combobox(
            frame_controles,
            values=["Lenta (600 ms)", "Normal (250 ms)", "Rápida (60 ms)"],
            state="readonly",
            width=16
        )
        self.combo_velocidad.current(1)
        self.combo_velocidad.bind("<<ComboboxSelected>>", self._cambiar_velocidad)
        self.combo_velocidad.pack(side="left", padx=5)

        self.lbl_reloj = ttk.Label(frame_controles, text="Reloj: 0 min", font=("Arial", 11, "bold"))
        self.lbl_reloj.pack(side="right", padx=15)

        # 4. Panel central: Fila FIFO y Estado de Técnicos
        frame_estado = ttk.Frame(self.root, padding=5)
        frame_estado.pack(fill="both", expand=True, padx=10)

        # Subpanel izquierdo: Cola FIFO
        frame_cola = ttk.LabelFrame(frame_estado, text="Fila de Espera (Cola FIFO)", padding=8)
        frame_cola.pack(side="left", fill="both", expand=True, padx=(0, 5))

        self.lista_cola = tk.Listbox(frame_cola, font=("Consolas", 10))
        self.lista_cola.pack(fill="both", expand=True)

        # Subpanel derecho: Técnicos
        frame_tecnicos = ttk.LabelFrame(frame_estado, text="Estado de los Técnicos", padding=8)
        frame_tecnicos.pack(side="right", fill="both", expand=True, padx=(5, 0))

        self.lista_tecnicos = tk.Listbox(frame_tecnicos, font=("Consolas", 10))
        self.lista_tecnicos.pack(fill="both", expand=True)

        # 5. Panel de Métricas en Tiempo Real
        frame_metricas = ttk.LabelFrame(self.root, text="Indicadores de Desempeño en Tiempo Real", padding=8)
        frame_metricas.pack(fill="x", padx=10, pady=5)

        self.lbl_atendidos = ttk.Label(frame_metricas, text="Equipos atendidos: 0 / 0", font=("Arial", 10, "bold"))
        self.lbl_atendidos.pack(side="left", padx=15)

        self.lbl_espera = ttk.Label(frame_metricas, text="Espera promedio: 0.00 min", font=("Arial", 10, "bold"))
        self.lbl_espera.pack(side="left", padx=15)

        self.lbl_utilizacion = ttk.Label(frame_metricas, text="Utilización promedio: 0.00%", font=("Arial", 10, "bold"))
        self.lbl_utilizacion.pack(side="left", padx=15)

        # 6. Panel inferior: Registro de Eventos
        frame_log = ttk.LabelFrame(self.root, text="Registro Detallado de Eventos (Auditoría)", padding=5)
        frame_log.pack(fill="both", expand=True, padx=10, pady=(0, 8))

        self.txt_log = tk.Text(frame_log, height=6, state="disabled", font=("Consolas", 9))
        self.txt_log.pack(fill="both", expand=True)

    def _cambiar_velocidad(self, _event=None):
        seleccion = self.combo_velocidad.get()
        if "Lenta" in seleccion:
            self.velocidad_ms = 600
        elif "Normal" in seleccion:
            self.velocidad_ms = 250
        elif "Rápida" in seleccion:
            self.velocidad_ms = 60

    def cargar_caso_normal(self):
        """Caso 1: Sin espera (Intervalo de llegada > Tiempo de atención / capacidad amplia)."""
        self.reiniciar_simulacion()
        self.var_tecnicos.set("2")
        self.var_equipos.set("4")
        self.var_llegada.set("5")
        self.var_atencion.set("4")
        self._agregar_al_log("[PRESET] Cargado Caso 1: Normal / Sin Espera (2 técnicos, 4 equipos, llegada c/5 min, atención 4 min). Espera esperada = 0.00 min.\n")

    def cargar_caso_limite(self):
        """Caso 2: Límite / Acumulación de equipos (Cuello de botella progresivo)."""
        self.reiniciar_simulacion()
        self.var_tecnicos.set("1")
        self.var_equipos.set("4")
        self.var_llegada.set("2")
        self.var_atencion.set("5")
        self._agregar_al_log("[PRESET] Cargado Caso 2: Acumulación de Cola (1 técnico, 4 equipos, llegada c/2 min, atención 5 min). Espera promedio esperada = 4.50 min.\n")

    def cargar_caso_invalido(self):
        """Caso 3: Entradas inválidas para verificar manejo de excepciones."""
        self.reiniciar_simulacion()
        self.var_tecnicos.set("0")
        self.var_equipos.set("-3")
        self.var_llegada.set("-1")
        self.var_atencion.set("0")
        self._agregar_al_log("[PRESET] Cargado Caso 3: Valores fuera de rango. Al hacer clic en Iniciar se validará y mostrará advertencia.\n")

    def _bloquear_configuracion(self, bloquear: bool):
        estado = "disabled" if bloquear else "normal"
        for entry in self.entries_config:
            entry.config(state=estado)

    def _validar_parametros(self):
        """Valida que los datos ingresados sean enteros válidos dentro de los rangos del sistema."""
        try:
            num_tecnicos = int(self.var_tecnicos.get())
            num_equipos = int(self.var_equipos.get())
            intervalo = int(self.var_llegada.get())
            atencion = int(self.var_atencion.get())
        except ValueError:
            messagebox.showerror("Error de Formato", "Todos los parámetros deben ser números enteros válidos.")
            return None

        if not (1 <= num_tecnicos <= 30):
            messagebox.showerror("Error de Rango", "El número de técnicos debe estar entre 1 y 30.")
            return None
        if not (1 <= num_equipos <= 100):
            messagebox.showerror("Error de Rango", "La cantidad de equipos debe estar entre 1 y 100.")
            return None
        if intervalo < 0:
            messagebox.showerror("Error de Rango", "El intervalo de llegada no puede ser negativo.")
            return None
        if atencion < 1:
            messagebox.showerror("Error de Rango", "El tiempo de atención debe ser de al menos 1 minuto.")
            return None

        return num_tecnicos, num_equipos, intervalo, atencion

    def _asegurar_simulador(self) -> bool:
        """Inicializa el simulador si no existe o si ya finalizó."""
        if self.simulador is None or self.simulador.finalizada:
            params = self._validar_parametros()
            if params is None:
                return False
            try:
                self.simulador = SimuladorCentroServicio(*params)
            except ValueError as e:
                messagebox.showerror("Error de Dominio", str(e))
                return False
            self._limpiar_log()
            self._agregar_al_log(
                f"--- INICIO DE SIMULACIÓN ---\n"
                f"Técnicos: {params[0]} | Equipos: {params[1]} | Intervalo: {params[2]} min | Atención: {params[3]} min\n"
            )
        return True

    def iniciar_simulacion(self):
        if not self._asegurar_simulador():
            return

        self.corriendo = True
        self._bloquear_configuracion(True)
        self.btn_iniciar.config(state="disabled")
        self.btn_pausar.config(state="normal")
        self.btn_paso.config(state="disabled")
        self.btn_completar.config(state="disabled")
        self._ejecutar_ciclo()

    def pausar_simulacion(self):
        self.corriendo = False
        if self.job_id is not None:
            self.root.after_cancel(self.job_id)
            self.job_id = None
        self.btn_iniciar.config(state="normal")
        self.btn_pausar.config(state="disabled")
        self.btn_paso.config(state="normal")
        self.btn_completar.config(state="normal")

    def ejecutar_un_paso(self):
        """Avanza exactamente 1 minuto en la simulación."""
        if not self._asegurar_simulador():
            return

        self._bloquear_configuracion(True)
        continua = self.simulador.ejecutar_paso()
        self._actualizar_vista()

        if not continua:
            self._finalizar_ejecucion()

    def ejecutar_todo(self):
        """Ejecuta toda la simulación hasta el final de forma instantánea."""
        if not self._asegurar_simulador():
            return

        self.pausar_simulacion()
        self._bloquear_configuracion(True)
        while self.simulador.ejecutar_paso():
            pass

        self._actualizar_vista()
        self._finalizar_ejecucion()

    def reiniciar_simulacion(self):
        self.pausar_simulacion()
        self.simulador = None
        self._bloquear_configuracion(False)
        self.lbl_reloj.config(text="Reloj: 0 min")
        self.lista_cola.delete(0, tk.END)
        self.lista_tecnicos.delete(0, tk.END)
        self.lbl_atendidos.config(text="Equipos atendidos: 0 / 0")
        self.lbl_espera.config(text="Espera promedio: 0.00 min")
        self.lbl_utilizacion.config(text="Utilización promedio: 0.00%")
        self._limpiar_log()

    def _ejecutar_ciclo(self):
        if not self.corriendo or self.simulador is None:
            return

        continua = self.simulador.ejecutar_paso()
        self._actualizar_vista()

        if continua:
            self.job_id = self.root.after(self.velocidad_ms, self._ejecutar_ciclo)
        else:
            self._finalizar_ejecucion()

    def _finalizar_ejecucion(self):
        self.pausar_simulacion()
        self.btn_iniciar.config(state="normal")
        self.btn_paso.config(state="disabled")
        self.btn_completar.config(state="disabled")
        self._bloquear_configuracion(False)
        messagebox.showinfo("Simulación Completada", "Todos los equipos han sido diagnosticados y reparados con éxito.")

    def _actualizar_vista(self):
        metricas = CalculadorMetricas.calcular_resumen(self.simulador)

        self.lbl_reloj.config(text=f"Reloj: {metricas['reloj']} min")
        self.lbl_atendidos.config(text=f"Equipos atendidos: {metricas['equipos_atendidos']} / {metricas['total_equipos']}")
        self.lbl_espera.config(text=f"Espera promedio: {metricas['tiempo_promedio_espera']:.2f} min")
        self.lbl_utilizacion.config(text=f"Utilización promedio: {metricas['utilizacion_promedio']:.2f}%")

        # Actualizar lista de cola FIFO
        self.lista_cola.delete(0, tk.END)
        if not self.simulador.cola_espera:
            self.lista_cola.insert(tk.END, "  (Fila vacía - sin espera)")
        else:
            for pos, eq in enumerate(self.simulador.cola_espera, start=1):
                self.lista_cola.insert(tk.END, f"  [{pos}] {eq} (Llegó en min {eq.tiempo_llegada})")

        # Actualizar lista de técnicos
        self.lista_tecnicos.delete(0, tk.END)
        for tec in self.simulador.tecnicos:
            uso = metricas['utilizacion_por_tecnico'][tec.id_tecnico]
            if tec.esta_libre():
                estado = "🟢 LIBRE"
            else:
                estado = f"🟠 ATENDIENDO {tec.equipo_actual} (Fin: min {tec.tiempo_fin_atencion})"
            self.lista_tecnicos.insert(tk.END, f"  Técnico {tec.id_tecnico:02d} [{uso:5.1f}% ocupado] -> {estado}")

        # Agregar eventos al registro
        if self.simulador.eventos_ultimo_paso:
            for evento in self.simulador.eventos_ultimo_paso:
                self._agregar_al_log(evento + "\n")

    def _agregar_al_log(self, texto: str):
        self.txt_log.config(state="normal")
        self.txt_log.insert(tk.END, texto)
        self.txt_log.see(tk.END)
        self.txt_log.config(state="disabled")

    def _limpiar_log(self):
        self.txt_log.config(state="normal")
        self.txt_log.delete("1.0", tk.END)
        self.txt_log.config(state="disabled")
