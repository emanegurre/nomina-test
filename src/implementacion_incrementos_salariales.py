import pandas as pd
import numpy as np
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                            QTableWidget, QTableWidgetItem, QLabel, QComboBox,
                            QGroupBox, QDateEdit, QDoubleSpinBox, QLineEdit,
                            QMessageBox, QFileDialog, QRadioButton, # QTextEdit, QCheckBox,
                            QButtonGroup, QSpinBox, QDialog, QFormLayout, QDialogButtonBox) # Añadido QDialog, QFormLayout, QDialogButtonBox
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QColor, QFont
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from datetime import datetime, timedelta

class IncrementosSalarialesWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.historial_incrementos = []
        self.proyecciones = []
        self.initUI()

    def initUI(self):
        layout_principal = QVBoxLayout(self)

        # Panel superior - Configuración de incremento
        panel_config = QGroupBox("Configuración de Incremento")
        layout_config = QVBoxLayout(panel_config)

        # Tipo de incremento
        layout_tipo = QHBoxLayout()
        layout_tipo.addWidget(QLabel("Tipo de incremento:"))

        self.grupo_tipo = QButtonGroup(self) # Asegurar que el QButtonGroup tiene un padre
        self.radio_porcentaje = QRadioButton("Porcentaje (%)")
        self.radio_porcentaje.setChecked(True)
        self.radio_cantidad = QRadioButton("Cantidad fija (€)")
        self.radio_mixto = QRadioButton("Mixto")

        self.grupo_tipo.addButton(self.radio_porcentaje)
        self.grupo_tipo.addButton(self.radio_cantidad)
        self.grupo_tipo.addButton(self.radio_mixto)

        layout_tipo.addWidget(self.radio_porcentaje)
        layout_tipo.addWidget(self.radio_cantidad)
        layout_tipo.addWidget(self.radio_mixto)
        layout_tipo.addStretch()

        layout_config.addLayout(layout_tipo)

        # Valores del incremento
        layout_valores = QHBoxLayout()

        # Porcentaje
        layout_valores.addWidget(QLabel("Incremento (%):"))
        self.spin_porcentaje = QDoubleSpinBox()
        self.spin_porcentaje.setRange(0, 100)
        self.spin_porcentaje.setDecimals(2)
        self.spin_porcentaje.setValue(3.0)
        self.spin_porcentaje.setSuffix("%")
        layout_valores.addWidget(self.spin_porcentaje)

        # Cantidad fija
        layout_valores.addWidget(QLabel("Cantidad fija (€):"))
        self.spin_cantidad = QDoubleSpinBox()
        self.spin_cantidad.setRange(0, 9999)
        self.spin_cantidad.setDecimals(2)
        self.spin_cantidad.setValue(100)
        self.spin_cantidad.setEnabled(False) # Deshabilitado inicialmente
        layout_valores.addWidget(self.spin_cantidad)

        # Fecha aplicación
        layout_valores.addWidget(QLabel("Fecha aplicación:"))
        self.date_aplicacion = QDateEdit()
        self.date_aplicacion.setCalendarPopup(True)
        self.date_aplicacion.setDate(QDate.currentDate())
        layout_valores.addWidget(self.date_aplicacion)

        layout_valores.addStretch()
        layout_config.addLayout(layout_valores)

        # Aplicar a
        layout_aplicar = QHBoxLayout()
        layout_aplicar.addWidget(QLabel("Aplicar a:"))

        self.combo_aplicar = QComboBox()
        self.combo_aplicar.addItems([
            "Salario base",
            "Salario total (base + pluses)",
            "Solo pluses",
            "Conceptos específicos" # Esta opción podría requerir más lógica
        ])
        layout_aplicar.addWidget(self.combo_aplicar)

        # Concepto
        layout_aplicar.addWidget(QLabel("Concepto:"))
        self.input_concepto = QLineEdit()
        self.input_concepto.setPlaceholderText("Ej: Incremento anual 2024")
        layout_aplicar.addWidget(self.input_concepto)

        layout_aplicar.addStretch()
        layout_config.addLayout(layout_aplicar)

        layout_principal.addWidget(panel_config)

        # Conectar eventos de cambio de tipo de incremento
        self.radio_porcentaje.toggled.connect(self.cambiar_tipo_incremento)
        self.radio_cantidad.toggled.connect(self.cambiar_tipo_incremento)
        self.radio_mixto.toggled.connect(self.cambiar_tipo_incremento)
        # Conectar cambios en valores para recalcular
        self.spin_porcentaje.valueChanged.connect(self.calcular_incremento)
        self.spin_cantidad.valueChanged.connect(self.calcular_incremento)
        self.combo_aplicar.currentTextChanged.connect(self.calcular_incremento)


        # Panel central - Vista previa y cálculo
        panel_calculo = QGroupBox("Cálculo y Vista Previa")
        layout_calculo = QVBoxLayout(panel_calculo)

        # Datos actuales
        layout_datos_actuales = QHBoxLayout()

        layout_datos_actuales.addWidget(QLabel("Salario base actual:"))
        self.spin_salario_actual = QDoubleSpinBox()
        self.spin_salario_actual.setRange(0, 99999)
        self.spin_salario_actual.setDecimals(2)
        self.spin_salario_actual.setValue(2000)
        self.spin_salario_actual.valueChanged.connect(self.calcular_incremento)
        layout_datos_actuales.addWidget(self.spin_salario_actual)

        layout_datos_actuales.addWidget(QLabel("Total pluses:"))
        self.spin_pluses_actual = QDoubleSpinBox()
        self.spin_pluses_actual.setRange(0, 9999)
        self.spin_pluses_actual.setDecimals(2)
        self.spin_pluses_actual.setValue(300)
        self.spin_pluses_actual.valueChanged.connect(self.calcular_incremento)
        layout_datos_actuales.addWidget(self.spin_pluses_actual)

        btn_calcular = QPushButton("🧮 Calcular")
        btn_calcular.clicked.connect(self.calcular_incremento)
        layout_datos_actuales.addWidget(btn_calcular)

        layout_datos_actuales.addStretch()
        layout_calculo.addLayout(layout_datos_actuales)

        # Resultados
        layout_resultados = QHBoxLayout()

        # Columna 1
        col1 = QVBoxLayout()
        self.lbl_salario_nuevo = QLabel("Nuevo salario base: € 0.00")
        self.lbl_salario_nuevo.setFont(QFont('Arial', 12, QFont.Bold))
        self.lbl_salario_nuevo.setStyleSheet("color: #4CAF50;")
        col1.addWidget(self.lbl_salario_nuevo)

        self.lbl_incremento_mensual = QLabel("Incremento mensual: € 0.00")
        col1.addWidget(self.lbl_incremento_mensual)

        layout_resultados.addLayout(col1)

        # Columna 2
        col2 = QVBoxLayout()
        self.lbl_total_nuevo = QLabel("Nuevo total: € 0.00")
        self.lbl_total_nuevo.setFont(QFont('Arial', 12, QFont.Bold))
        col2.addWidget(self.lbl_total_nuevo)

        self.lbl_incremento_anual = QLabel("Incremento anual: € 0.00")
        col2.addWidget(self.lbl_incremento_anual)

        layout_resultados.addLayout(col2)

        # Columna 3
        col3 = QVBoxLayout()
        self.lbl_porcentaje_real = QLabel("Incremento real: 0.00%")
        col3.addWidget(self.lbl_porcentaje_real)

        self.lbl_coste_empresa = QLabel("Coste empresa (+30%): € 0.00")
        col3.addWidget(self.lbl_coste_empresa)

        layout_resultados.addLayout(col3)
        layout_calculo.addLayout(layout_resultados)

        # Tabla comparativa
        self.tabla_comparativa = QTableWidget()
        self.tabla_comparativa.setColumnCount(5)
        self.tabla_comparativa.setHorizontalHeaderLabels([
            'Concepto', 'Actual', 'Incremento', 'Nuevo', 'Diferencia %'
        ])
        self.tabla_comparativa.setMaximumHeight(150)
        layout_calculo.addWidget(self.tabla_comparativa)

        layout_principal.addWidget(panel_calculo)

        # Panel de historial y proyecciones
        panel_historial = QGroupBox("Historial y Proyecciones")
        layout_historial = QVBoxLayout(panel_historial)

        # Botones
        layout_botones_hist = QHBoxLayout()

        btn_agregar_historial = QPushButton("➕ Registrar Incremento")
        btn_agregar_historial.clicked.connect(self.agregar_incremento_historial)
        layout_botones_hist.addWidget(btn_agregar_historial)

        btn_proyectar = QPushButton("📈 Proyectar a Futuro")
        btn_proyectar.clicked.connect(self.proyectar_incrementos)
        layout_botones_hist.addWidget(btn_proyectar)

        btn_comparar_ipc = QPushButton("💹 Comparar con IPC")
        btn_comparar_ipc.clicked.connect(self.comparar_con_ipc)
        layout_botones_hist.addWidget(btn_comparar_ipc)

        layout_botones_hist.addStretch()
        layout_historial.addLayout(layout_botones_hist)

        # Tabla de historial
        self.tabla_historial = QTableWidget()
        self.tabla_historial.setColumnCount(6)
        self.tabla_historial.setHorizontalHeaderLabels([
            'Fecha', 'Concepto', 'Tipo', 'Valor', 'Salario Resultante', 'Acumulado'
        ])
        layout_historial.addWidget(self.tabla_historial)

        layout_principal.addWidget(panel_historial)

        # Panel de gráficos
        panel_graficos = QGroupBox("Análisis Gráfico")
        layout_graficos = QVBoxLayout(panel_graficos)

        # Canvas para gráficos
        self.figure = Figure(figsize=(10, 4))
        self.canvas = FigureCanvas(self.figure)
        layout_graficos.addWidget(self.canvas)

        # Controles de gráfico
        layout_controles_grafico = QHBoxLayout()

        layout_controles_grafico.addWidget(QLabel("Tipo de gráfico:"))
        self.combo_tipo_grafico = QComboBox()
        self.combo_tipo_grafico.addItems([
            "Evolución salarial",
            "Incrementos por año",
            "Comparación con inflación",
            "Proyección a 5 años"
        ])
        self.combo_tipo_grafico.currentTextChanged.connect(self.actualizar_grafico)
        layout_controles_grafico.addWidget(self.combo_tipo_grafico)

        layout_controles_grafico.addStretch()
        layout_graficos.addLayout(layout_controles_grafico)

        layout_principal.addWidget(panel_graficos)

        # Botones de acción
        layout_acciones = QHBoxLayout()

        btn_simular_escenarios = QPushButton("🎯 Simular Escenarios")
        btn_simular_escenarios.clicked.connect(self.simular_escenarios)
        layout_acciones.addWidget(btn_simular_escenarios)

        btn_exportar = QPushButton("📊 Exportar Análisis")
        btn_exportar.clicked.connect(self.exportar_analisis)
        layout_acciones.addWidget(btn_exportar)

        layout_acciones.addStretch()

        btn_limpiar = QPushButton("🗑️ Limpiar")
        btn_limpiar.clicked.connect(self.limpiar_datos)
        layout_acciones.addWidget(btn_limpiar)

        layout_principal.addLayout(layout_acciones)

        # Cargar datos de ejemplo e inicializar cálculos
        self.cargar_datos_ejemplo()
        self.cambiar_tipo_incremento() # Para asegurar que los spinboxes estén bien configurados
        self.calcular_incremento()
        self.actualizar_grafico()

    def cambiar_tipo_incremento(self):
        """Habilita/deshabilita campos según el tipo de incremento"""
        if self.radio_porcentaje.isChecked():
            self.spin_porcentaje.setEnabled(True)
            self.spin_cantidad.setEnabled(False)
        elif self.radio_cantidad.isChecked():
            self.spin_porcentaje.setEnabled(False)
            self.spin_cantidad.setEnabled(True)
        else:  # Mixto
            self.spin_porcentaje.setEnabled(True)
            self.spin_cantidad.setEnabled(True)
        self.calcular_incremento() # Recalcular al cambiar el tipo

    def calcular_incremento(self):
        """Calcula el incremento salarial"""
        salario_actual = self.spin_salario_actual.value()
        pluses_actual = self.spin_pluses_actual.value()
        total_actual = salario_actual + pluses_actual

        incremento = 0
        aplicar_a = self.combo_aplicar.currentText()

        if self.radio_porcentaje.isChecked():
            porcentaje = self.spin_porcentaje.value() / 100.0 # Asegurar flotante
            if aplicar_a == "Salario base":
                incremento = salario_actual * porcentaje
            elif aplicar_a == "Salario total (base + pluses)":
                incremento = total_actual * porcentaje
            elif aplicar_a == "Solo pluses":
                incremento = pluses_actual * porcentaje
            # Considerar "Conceptos específicos" si se implementa lógica adicional

        elif self.radio_cantidad.isChecked():
            incremento = self.spin_cantidad.value()

        else:  # Mixto
            porcentaje = self.spin_porcentaje.value() / 100.0 # Asegurar flotante
            cantidad_fija = self.spin_cantidad.value()
            if aplicar_a == "Salario base":
                incremento = (salario_actual * porcentaje) + cantidad_fija
            elif aplicar_a == "Salario total (base + pluses)":
                incremento = (total_actual * porcentaje) + cantidad_fija
            elif aplicar_a == "Solo pluses":
                incremento = (pluses_actual * porcentaje) + cantidad_fija
            # Considerar "Conceptos específicos"

        nuevo_salario_base = salario_actual
        nuevos_pluses = pluses_actual

        if aplicar_a == "Solo pluses":
            nuevos_pluses += incremento
        elif aplicar_a == "Salario base":
            nuevo_salario_base += incremento
        elif aplicar_a == "Salario total (base + pluses)":
            # Distribuir el incremento proporcionalmente o según alguna regla
            # Por simplicidad, lo añadimos al salario base si no es solo pluses
            if total_actual > 0: # Evitar división por cero
                prop_salario = salario_actual / total_actual
                prop_pluses = pluses_actual / total_actual
                nuevo_salario_base += incremento * prop_salario
                nuevos_pluses += incremento * prop_pluses
            else: # Si el total actual es 0, añadir al salario base
                 nuevo_salario_base += incremento


        nuevo_total = nuevo_salario_base + nuevos_pluses
        incremento_mensual = nuevo_total - total_actual
        incremento_anual = incremento_mensual * 12

        porcentaje_real = (incremento_mensual / total_actual * 100) if total_actual > 0 else 0
        coste_empresa = nuevo_total * 1.30 # Estimación

        self.lbl_salario_nuevo.setText(f"Nuevo salario base: € {nuevo_salario_base:.2f}")
        self.lbl_incremento_mensual.setText(f"Incremento mensual: € {incremento_mensual:.2f}")
        self.lbl_total_nuevo.setText(f"Nuevo total: € {nuevo_total:.2f}")
        self.lbl_incremento_anual.setText(f"Incremento anual: € {incremento_anual:.2f}")
        self.lbl_porcentaje_real.setText(f"Incremento real: {porcentaje_real:.2f}%")
        self.lbl_coste_empresa.setText(f"Coste empresa (+30%): € {coste_empresa:.2f}")

        self.actualizar_tabla_comparativa(
            salario_actual, pluses_actual, total_actual,
            nuevo_salario_base, nuevos_pluses, nuevo_total
        )

    def actualizar_tabla_comparativa(self, sal_act, plus_act, tot_act, sal_nuevo, plus_nuevo, tot_nuevo):
        """Actualiza la tabla comparativa de salarios"""
        self.tabla_comparativa.setRowCount(0)
        datos = [
            ("Salario Base", sal_act, sal_nuevo - sal_act, sal_nuevo),
            ("Pluses", plus_act, plus_nuevo - plus_act, plus_nuevo),
            ("TOTAL", tot_act, tot_nuevo - tot_act, tot_nuevo)
        ]

        for concepto, actual, incremento_val, nuevo in datos: # Renombrado 'incremento' a 'incremento_val'
            row = self.tabla_comparativa.rowCount()
            self.tabla_comparativa.insertRow(row)

            self.tabla_comparativa.setItem(row, 0, QTableWidgetItem(concepto))
            self.tabla_comparativa.setItem(row, 1, QTableWidgetItem(f"€ {actual:.2f}"))
            self.tabla_comparativa.setItem(row, 2, QTableWidgetItem(f"€ {incremento_val:.2f}"))
            self.tabla_comparativa.setItem(row, 3, QTableWidgetItem(f"€ {nuevo:.2f}"))

            porcentaje = (incremento_val / actual * 100) if actual > 0 else 0
            self.tabla_comparativa.setItem(row, 4, QTableWidgetItem(f"{porcentaje:.2f}%"))

            if concepto == "TOTAL":
                for col in range(5):
                    item = self.tabla_comparativa.item(row, col)
                    if item: # Comprobar que el item existe
                        item.setFont(QFont('Arial', 10, QFont.Bold))
                        item.setBackground(QColor(220, 220, 220))

    def agregar_incremento_historial(self):
        """Agrega el incremento actual al historial de incrementos"""
        fecha = self.date_aplicacion.date()
        concepto = self.input_concepto.text() or "Incremento sin descripción"

        tipo = ""
        valor_str = "" # Renombrado 'valor' a 'valor_str' para evitar conflicto
        if self.radio_porcentaje.isChecked():
            tipo = "Porcentaje"
            valor_str = f"{self.spin_porcentaje.value():.2f}%"
        elif self.radio_cantidad.isChecked():
            tipo = "Cantidad fija"
            valor_str = f"€ {self.spin_cantidad.value():.2f}"
        else: # Mixto
            tipo = "Mixto"
            valor_str = f"{self.spin_porcentaje.value():.2f}% + € {self.spin_cantidad.value():.2f}"

        try:
            salario_resultante_text = self.lbl_total_nuevo.text().split('€ ')[1]
            salario_resultante = float(salario_resultante_text)
        except (IndexError, ValueError):
            QMessageBox.warning(self, "Error", "No se pudo obtener el salario resultante.")
            return

        acumulado = 0
        salario_base_actual_para_calculo = self.spin_salario_actual.value()
        pluses_actual_para_calculo = self.spin_pluses_actual.value()
        salario_inicial_calculo = salario_base_actual_para_calculo + pluses_actual_para_calculo


        if self.historial_incrementos:
            # El salario inicial para el cálculo del acumulado es el salario_inicial del primer incremento registrado.
            # O si no hay 'salario_inicial' en el primer incremento, usar un default o el salario actual antes de cualquier incremento.
            primer_incremento = self.historial_incrementos[0]
            salario_base_historico = primer_incremento.get('salario_inicial_base', salario_base_actual_para_calculo) # Usar valor actual si no existe
            # pluses_historico = primer_incremento.get('salario_inicial_pluses', pluses_actual_para_calculo)
            # salario_inicial_historico = salario_base_historico + pluses_historico
            salario_inicial_historico = primer_incremento.get('salario_inicial_total_antes_primer_incremento', salario_inicial_calculo)


            if salario_inicial_historico > 0:
                 acumulado = ((salario_resultante - salario_inicial_historico) / salario_inicial_historico * 100)
            else:
                acumulado = 0 # O manejar como error/advertencia
        else:
            # Es el primer incremento que se registra
            if salario_inicial_calculo > 0:
                acumulado = ((salario_resultante - salario_inicial_calculo) / salario_inicial_calculo * 100)
            else:
                acumulado = 0


        incremento_data = {
            'fecha': fecha.toString("yyyy-MM-dd"),
            'concepto': concepto,
            'tipo': tipo,
            'valor': valor_str, # Usar valor_str
            'salario_resultante': salario_resultante,
            'acumulado': acumulado,
            'salario_inicial_base': salario_base_actual_para_calculo, # Guardar estado antes de este incremento
            'salario_inicial_pluses': pluses_actual_para_calculo, # Guardar estado antes de este incremento
            'salario_inicial_total_antes_primer_incremento': salario_inicial_calculo if not self.historial_incrementos else self.historial_incrementos[0].get('salario_inicial_total_antes_primer_incremento', salario_inicial_calculo)

        }
        self.historial_incrementos.append(incremento_data)

        row = self.tabla_historial.rowCount()
        self.tabla_historial.insertRow(row)
        self.tabla_historial.setItem(row, 0, QTableWidgetItem(fecha.toString("dd/MM/yyyy")))
        self.tabla_historial.setItem(row, 1, QTableWidgetItem(concepto))
        self.tabla_historial.setItem(row, 2, QTableWidgetItem(tipo))
        self.tabla_historial.setItem(row, 3, QTableWidgetItem(valor_str)) # Usar valor_str
        self.tabla_historial.setItem(row, 4, QTableWidgetItem(f"€ {salario_resultante:.2f}"))
        self.tabla_historial.setItem(row, 5, QTableWidgetItem(f"{acumulado:.2f}%"))

        # Actualizar el salario actual para el siguiente incremento potencial
        # Esto es importante: el "salario actual" para el próximo cálculo debe ser el "salario resultante" de este.
        # Sin embargo, el spin_salario_actual debería reflejar el salario base, no el total.
        # Necesitamos decidir cómo se actualizan self.spin_salario_actual y self.spin_pluses_actual.
        # Una opción es que el usuario los ajuste manualmente o que se actualicen según el 'aplicar_a'.
        # Por ahora, actualizaremos el salario base con el nuevo salario base calculado y los pluses a 0,
        # asumiendo que los pluses se re-evaluarán o se mantendrán. Esto es una simplificación.

        # Extraer el nuevo salario base y nuevos pluses del cálculo más reciente
        try:
            nuevo_salario_base_text = self.lbl_salario_nuevo.text().split('€ ')[1]
            nuevo_salario_base_val = float(nuevo_salario_base_text)

            # Para los pluses, si el incremento fue "Solo pluses", el salario base no cambió.
            # Si el incremento fue al "Salario base" o "Salario total", los pluses podrían o no haber cambiado.
            # Vamos a asumir que los pluses se resetean o se mantienen según la lógica del usuario para el siguiente cálculo.
            # Una forma simple es actualizar el salario base al nuevo_salario_base y los pluses a los nuevos_pluses del cálculo.
            # Esto requiere que calcular_incremento devuelva o almacene estos valores.
            # Por ahora, una simplificación:
            self.spin_salario_actual.setValue(nuevo_salario_base_val)

            # Si el incremento fue sobre el total o solo pluses, los pluses también cambiaron.
            # Necesitamos el valor de 'nuevos_pluses' de la función calcular_incremento.
            # Como no lo tenemos directamente aquí, una aproximación sería:
            total_nuevo_val = salario_resultante
            nuevos_pluses_val = total_nuevo_val - nuevo_salario_base_val
            self.spin_pluses_actual.setValue(nuevos_pluses_val if nuevos_pluses_val >= 0 else 0)

        except (IndexError, ValueError):
            QMessageBox.warning(self, "Advertencia", "No se pudieron actualizar los campos de salario base y pluses automáticamente.")


        self.actualizar_grafico()
        QMessageBox.information(
            self, "Incremento registrado",
            f"Se ha registrado el incremento '{concepto}' en el historial."
        )

    def cargar_datos_ejemplo(self):
        """Carga datos de ejemplo en el historial de incrementos"""
        # Salario inicial antes de cualquier incremento para los ejemplos
        salario_inicial_base_ejemplo = 1900.0
        pluses_iniciales_ejemplo = 100.0
        salario_inicial_total_ejemplo = salario_inicial_base_ejemplo + pluses_iniciales_ejemplo


        ejemplos = [
            {
                'fecha': '2022-01-01', 'concepto': 'Incremento anual 2022', 'tipo': 'Porcentaje',
                'valor': '2.5%', 'salario_resultante': 2050.0, # Asumiendo que 2000 era el base + pluses
                'acumulado': ((2050.0 - salario_inicial_total_ejemplo) / salario_inicial_total_ejemplo * 100) if salario_inicial_total_ejemplo > 0 else 0,
                'salario_inicial_base': salario_inicial_base_ejemplo, 'salario_inicial_pluses': pluses_iniciales_ejemplo,
                'salario_inicial_total_antes_primer_incremento': salario_inicial_total_ejemplo
            },
            {
                'fecha': '2023-01-01', 'concepto': 'Incremento anual 2023', 'tipo': 'Porcentaje',
                'valor': '3.0%', 'salario_resultante': 2111.5, # Sobre 2050
                'acumulado': ((2111.5 - salario_inicial_total_ejemplo) / salario_inicial_total_ejemplo * 100) if salario_inicial_total_ejemplo > 0 else 0,
                'salario_inicial_base': 2050.0*0.95, # Estimación inversa
                'salario_inicial_pluses': 2050.0*0.05, # Estimación inversa
                'salario_inicial_total_antes_primer_incremento': salario_inicial_total_ejemplo
            },
            {
                'fecha': '2023-07-01', 'concepto': 'Promoción', 'tipo': 'Cantidad fija',
                'valor': '€ 200.00', 'salario_resultante': 2311.5, # Sobre 2111.5
                'acumulado': ((2311.5 - salario_inicial_total_ejemplo) / salario_inicial_total_ejemplo * 100) if salario_inicial_total_ejemplo > 0 else 0,
                'salario_inicial_base': 2111.5*0.95, # Estimación inversa
                'salario_inicial_pluses': 2111.5*0.05, # Estimación inversa
                'salario_inicial_total_antes_primer_incremento': salario_inicial_total_ejemplo
            }
        ]
        self.historial_incrementos = ejemplos
        self.tabla_historial.setRowCount(0)
        for inc in ejemplos:
            row = self.tabla_historial.rowCount()
            self.tabla_historial.insertRow(row)
            fecha_qdate = QDate.fromString(inc['fecha'], "yyyy-MM-dd")
            self.tabla_historial.setItem(row, 0, QTableWidgetItem(fecha_qdate.toString("dd/MM/yyyy")))
            self.tabla_historial.setItem(row, 1, QTableWidgetItem(inc['concepto']))
            self.tabla_historial.setItem(row, 2, QTableWidgetItem(inc['tipo']))
            self.tabla_historial.setItem(row, 3, QTableWidgetItem(inc['valor']))
            self.tabla_historial.setItem(row, 4, QTableWidgetItem(f"€ {inc['salario_resultante']:.2f}"))
            self.tabla_historial.setItem(row, 5, QTableWidgetItem(f"{inc['acumulado']:.2f}%"))

    def proyectar_incrementos(self):
        """Proyecta incrementos salariales futuros"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Proyectar Incrementos")
        dialog.setModal(True)
        layout_form = QFormLayout(dialog) # Renombrado 'layout' a 'layout_form'

        spin_anos = QSpinBox()
        spin_anos.setRange(1, 10)
        spin_anos.setValue(5)
        layout_form.addRow("Años a proyectar:", spin_anos)

        spin_incremento = QDoubleSpinBox()
        spin_incremento.setRange(0, 20)
        spin_incremento.setDecimals(2)
        spin_incremento.setValue(2.5)
        spin_incremento.setSuffix("%")
        layout_form.addRow("Incremento anual esperado:", spin_incremento)

        spin_inflacion = QDoubleSpinBox()
        spin_inflacion.setRange(0, 20)
        spin_inflacion.setDecimals(2)
        spin_inflacion.setValue(2.0)
        spin_inflacion.setSuffix("%")
        layout_form.addRow("Inflación anual esperada:", spin_inflacion)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, dialog)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout_form.addRow(buttons)

        if dialog.exec_() == QDialog.Accepted:
            anos = spin_anos.value()
            incremento_anual_pct = spin_incremento.value() / 100.0 # Renombrado 'incremento_anual'
            inflacion_anual_pct = spin_inflacion.value() / 100.0 # Renombrado 'inflacion_anual'

            if self.historial_incrementos:
                salario_actual_proy = self.historial_incrementos[-1]['salario_resultante'] # Renombrado 'salario_actual'
            else:
                salario_actual_proy = self.spin_salario_actual.value() + self.spin_pluses_actual.value()

            self.proyecciones = []
            salario_proyectado = salario_actual_proy
            # salario_real = salario_actual_proy # No se usa 'salario_real' aquí

            for i in range(1, anos + 1):
                salario_proyectado *= (1 + incremento_anual_pct)
                salario_real_calc = salario_proyectado / ((1 + inflacion_anual_pct) ** i) # Renombrado 'salario_real'

                self.proyecciones.append({
                    'año': datetime.now().year + i,
                    'salario_nominal': salario_proyectado,
                    'salario_real': salario_real_calc, # Usar 'salario_real_calc'
                    'poder_adquisitivo': ((salario_real_calc / salario_actual_proy - 1) * 100) if salario_actual_proy > 0 else 0
                })

            self.combo_tipo_grafico.setCurrentText("Proyección a 5 años") # Esto llamará a actualizar_grafico
            # self.actualizar_grafico() # No es necesario si el cambio de texto lo hace

            if self.proyecciones: # Comprobar si hay proyecciones
                ultimo = self.proyecciones[-1]
                mensaje = (f"Proyección a {anos} años:\n\n"
                           f"Salario actual base para proyección: € {salario_actual_proy:.2f}\n"
                           f"Salario proyectado (nominal): € {ultimo['salario_nominal']:.2f}\n"
                           f"Salario real (ajustado por inflación): € {ultimo['salario_real']:.2f}\n"
                           f"Cambio en poder adquisitivo: {ultimo['poder_adquisitivo']:.2f}%")
                QMessageBox.information(self, "Proyección Completada", mensaje)
            else:
                QMessageBox.information(self, "Proyección", "No se generaron proyecciones.")


    def comparar_con_ipc(self):
        """Compara los incrementos registrados con datos históricos del IPC"""
        ipc_historico = {'2022': 3.5, '2023': 3.8, '2024': 2.1} # Ejemplo
        mensaje = "=== COMPARACIÓN CON IPC ===\n\n"
        if not self.historial_incrementos:
            mensaje += "No hay historial de incrementos para comparar."
            QMessageBox.information(self, "Comparación con IPC", mensaje)
            return

        for inc in self.historial_incrementos:
            fecha = QDate.fromString(inc['fecha'], "yyyy-MM-dd")
            año_str = str(fecha.year()) # Renombrado 'año' a 'año_str'

            if año_str in ipc_historico:
                ipc_val = ipc_historico[año_str] # Renombrado 'ipc' a 'ipc_val'

                incremento_pct = 0
                if inc['tipo'] == 'Porcentaje':
                    try:
                        incremento_pct = float(inc['valor'].replace('%', ''))
                    except ValueError:
                        incremento_pct = 0 # O manejar el error
                else:
                    salario_inicial_inc = inc.get('salario_inicial_base', 0) + inc.get('salario_inicial_pluses', 0)
                    if salario_inicial_inc > 0:
                         incremento_pct = ((inc['salario_resultante'] - salario_inicial_inc) / salario_inicial_inc * 100)

                diferencia = incremento_pct - ipc_val

                mensaje += f"{inc['concepto']} ({año_str}):\n"
                mensaje += f"  Incremento: {incremento_pct:.2f}%\n"
                mensaje += f"  IPC: {ipc_val:.2f}%\n"
                mensaje += f"  Diferencia: {diferencia:+.2f}%\n"
                mensaje += "  ✅ Ganancia de poder adquisitivo\n" if diferencia > 0 else "  ❌ Pérdida de poder adquisitivo\n"
                mensaje += "\n"
            else:
                mensaje += f"{inc['concepto']} ({año_str}): No hay datos de IPC para este año.\n\n"

        QMessageBox.information(self, "Comparación con IPC", mensaje)

    def actualizar_grafico(self):
        """Actualiza el gráfico mostrado según la selección del ComboBox"""
        self.figure.clear()
        tipo_grafico = self.combo_tipo_grafico.currentText()

        if tipo_grafico == "Evolución salarial":
            self.grafico_evolucion_salarial()
        elif tipo_grafico == "Incrementos por año":
            self.grafico_incrementos_por_año()
        elif tipo_grafico == "Comparación con inflación":
            self.grafico_comparacion_inflacion()
        elif tipo_grafico == "Proyección a 5 años":
            self.grafico_proyeccion()

        self.canvas.draw()

    def grafico_evolucion_salarial(self):
        """Genera y muestra un gráfico de la evolución salarial"""
        ax = self.figure.add_subplot(111)
        if not self.historial_incrementos:
            ax.text(0.5, 0.5, 'Sin datos de historial', horizontalalignment='center', verticalalignment='center')
            self.canvas.draw() # Asegurar que se actualiza el canvas vacío
            return

        fechas_plot = [] # Renombrado 'fechas' a 'fechas_plot'
        salarios_plot = [] # Renombrado 'salarios' a 'salarios_plot'

        # Punto inicial (antes del primer incremento)
        primer_inc_data = self.historial_incrementos[0]
        salario_inicial_total = primer_inc_data.get('salario_inicial_base', 0) + primer_inc_data.get('salario_inicial_pluses', 0)
        # Para la fecha inicial, restamos un mes a la fecha del primer incremento para visualización
        fecha_qdate_primer_inc = QDate.fromString(primer_inc_data['fecha'], "yyyy-MM-dd")
        fecha_inicial_plot = fecha_qdate_primer_inc.addMonths(-1).toString("MM/yyyy")

        fechas_plot.append(fecha_inicial_plot)
        salarios_plot.append(salario_inicial_total)


        for inc in self.historial_incrementos:
            fecha_qdate = QDate.fromString(inc['fecha'], "yyyy-MM-dd")
            fechas_plot.append(fecha_qdate.toString("MM/yyyy"))
            salarios_plot.append(inc['salario_resultante'])

        ax.plot(fechas_plot, salarios_plot, 'b-o', linewidth=2, markersize=8)
        for i, salario_val in enumerate(salarios_plot): # Renombrado 'salario' a 'salario_val'
            ax.annotate(f'€{salario_val:.0f}', (i, salario_val), textcoords="offset points", xytext=(0,10), ha='center', fontsize=9)

        ax.set_xlabel('Fecha')
        ax.set_ylabel('Salario Total (€)')
        ax.set_title('Evolución Salarial')
        ax.grid(True, alpha=0.3)
        ax.tick_params(axis='x', rotation=45)
        self.figure.tight_layout() # Ajustar layout para evitar solapamientos

    def grafico_incrementos_por_año(self):
        """Genera y muestra un gráfico de los incrementos totales por año"""
        ax = self.figure.add_subplot(111)
        if not self.historial_incrementos:
            ax.text(0.5, 0.5, 'Sin datos de historial', horizontalalignment='center', verticalalignment='center')
            self.canvas.draw()
            return

        incrementos_por_año_dict = {} # Renombrado 'incrementos_por_año'
        salario_anterior_año = {}

        for inc in self.historial_incrementos:
            fecha_qdate = QDate.fromString(inc['fecha'], "yyyy-MM-dd")
            año_val = fecha_qdate.year() # Renombrado 'año' a 'año_val'

            if año_val not in incrementos_por_año_dict:
                incrementos_por_año_dict[año_val] = 0
                # Determinar el salario base para el primer incremento del año
                # Si es el primer incremento en el historial, usar su salario_inicial_total
                # Si no, usar el salario_resultante del último incremento del año anterior.
                if inc == self.historial_incrementos[0]:
                     salario_anterior_año[año_val] = inc.get('salario_inicial_base', 0) + inc.get('salario_inicial_pluses', 0)
                else:
                    # Buscar el último salario resultante del año anterior o el inicial si es el primer año con datos
                    idx = self.historial_incrementos.index(inc)
                    salario_previo_directo = self.historial_incrementos[idx-1]['salario_resultante']
                    salario_anterior_año[año_val] = salario_previo_directo


            incremento_actual_euros = inc['salario_resultante'] - salario_anterior_año[año_val]
            incrementos_por_año_dict[año_val] += incremento_actual_euros
            salario_anterior_año[año_val] = inc['salario_resultante'] # Actualizar para el siguiente incremento en el mismo año


        años_labels = sorted(incrementos_por_año_dict.keys()) # Renombrado 'años' a 'años_labels'
        totales_plot = [incrementos_por_año_dict[a] for a in años_labels] # Renombrado 'totales' a 'totales_plot'

        bars = ax.bar([str(a) for a in años_labels], totales_plot, color='#4CAF50') # Convertir años a string para el eje X
        for bar_item, total_val in zip(bars, totales_plot): # Renombrado 'bar' a 'bar_item', 'total' a 'total_val'
            height = bar_item.get_height()
            ax.text(bar_item.get_x() + bar_item.get_width()/2., height, f'€{total_val:.0f}', ha='center', va='bottom')

        ax.set_xlabel('Año')
        ax.set_ylabel('Incremento Total (€)')
        ax.set_title('Incrementos por Año')
        ax.grid(True, alpha=0.3, axis='y')
        self.figure.tight_layout()

    def grafico_comparacion_inflacion(self):
        """Genera y muestra un gráfico comparando incrementos con la inflación (IPC)"""
        ax = self.figure.add_subplot(111)
        ipc_historico_ejemplo = {'2022': 3.5, '2023': 3.8, '2024': 2.1} # Renombrado 'ipc_historico'
        años_graf = [] # Renombrado 'años'
        incrementos_graf = [] # Renombrado 'incrementos'
        inflacion_graf = [] # Renombrado 'inflacion'

        # Agrupar incrementos por año para obtener el % total anual
        incrementos_anuales_pct = {}
        salario_inicio_año = {}

        for inc in self.historial_incrementos:
            fecha_qdate = QDate.fromString(inc['fecha'], "yyyy-MM-dd")
            año_val = fecha_qdate.year() # Renombrado 'año'

            if año_val not in salario_inicio_año:
                 # Salario al inicio de este año (o el inicial si es el primer año)
                if inc == self.historial_incrementos[0]:
                    salario_inicio_año[año_val] = inc.get('salario_inicial_base',0) + inc.get('salario_inicial_pluses',0)
                else:
                    # Buscar el último salario del año anterior
                    idx = self.historial_incrementos.index(inc)
                    salario_inicio_año[año_val] = self.historial_incrementos[idx-1]['salario_resultante']


            if año_val not in incrementos_anuales_pct:
                incrementos_anuales_pct[año_val] = 0


        # Calcular el porcentaje de incremento total para cada año
        salario_fin_año_anterior = 0
        if self.historial_incrementos:
            salario_fin_año_anterior = self.historial_incrementos[0].get('salario_inicial_base',0) + self.historial_incrementos[0].get('salario_inicial_pluses',0)

        for año_val in sorted(salario_inicio_año.keys()):
            salario_al_inicio_de_este_año = salario_fin_año_anterior
            salario_al_final_de_este_año = salario_al_inicio_de_este_año # Inicializar

            for inc in self.historial_incrementos:
                 if QDate.fromString(inc['fecha'], "yyyy-MM-dd").year() == año_val:
                     salario_al_final_de_este_año = inc['salario_resultante'] # El último incremento del año da el salario final

            if salario_al_inicio_de_este_año > 0:
                incremento_total_pct_año = ((salario_al_final_de_este_año - salario_al_inicio_de_este_año) / salario_al_inicio_de_este_año) * 100
                incrementos_anuales_pct[año_val] = incremento_total_pct_año
            else:
                incrementos_anuales_pct[año_val] = 0
            salario_fin_año_anterior = salario_al_final_de_este_año


        for año_str_key in sorted(ipc_historico_ejemplo.keys()): # Renombrado 'año'
            if int(año_str_key) in incrementos_anuales_pct: # Comprobar si hay datos de incremento para ese año
                años_graf.append(año_str_key)
                incrementos_graf.append(incrementos_anuales_pct[int(año_str_key)])
                inflacion_graf.append(ipc_historico_ejemplo[año_str_key])

        if not años_graf:
            ax.text(0.5, 0.5, 'No hay datos suficientes para comparar con IPC', horizontalalignment='center', verticalalignment='center')
            self.canvas.draw()
            return

        x_indices = np.arange(len(años_graf)) # Renombrado 'x'
        width_bar = 0.35 # Renombrado 'width'

        bars1 = ax.bar(x_indices - width_bar/2, incrementos_graf, width_bar, label='Incremento salarial', color='#4CAF50')
        bars2 = ax.bar(x_indices + width_bar/2, inflacion_graf, width_bar, label='IPC', color='#f44336')

        ax.set_xlabel('Año')
        ax.set_ylabel('Porcentaje (%)')
        ax.set_title('Incremento Salarial vs IPC')
        ax.set_xticks(x_indices)
        ax.set_xticklabels(años_graf)
        ax.legend()
        ax.grid(True, alpha=0.3, axis='y')

        for bars_group in [bars1, bars2]: # Renombrado 'bars'
            for bar_item_infl in bars_group: # Renombrado 'bar'
                height = bar_item_infl.get_height()
                ax.text(bar_item_infl.get_x() + bar_item_infl.get_width()/2., height, f'{height:.1f}%', ha='center', va='bottom', fontsize=9)
        self.figure.tight_layout()

    def grafico_proyeccion(self):
        """Genera y muestra un gráfico de la proyección salarial"""
        ax = self.figure.add_subplot(111)
        if not self.proyecciones:
            ax.text(0.5, 0.5, 'Sin proyecciones disponibles\nUse "Proyectar a Futuro" primero', horizontalalignment='center', verticalalignment='center')
            self.canvas.draw()
            return

        años_proy = [p['año'] for p in self.proyecciones] # Renombrado 'años'
        salarios_nominales_proy = [p['salario_nominal'] for p in self.proyecciones] # Renombrado 'salarios_nominales'
        salarios_reales_proy = [p['salario_real'] for p in self.proyecciones] # Renombrado 'salarios_reales'

        año_actual_val = datetime.now().year # Renombrado 'año_actual'
        salario_actual_val = 0 # Renombrado 'salario_actual'
        if self.historial_incrementos:
            salario_actual_val = self.historial_incrementos[-1]['salario_resultante']
        else:
            salario_actual_val = self.spin_salario_actual.value() + self.spin_pluses_actual.value()

        # Insertar datos actuales al inicio de las listas de proyección para el gráfico
        años_plot_proy = [año_actual_val] + años_proy # Renombrado 'años'
        salarios_nominales_plot = [salario_actual_val] + salarios_nominales_proy # Renombrado 'salarios_nominales'
        salarios_reales_plot = [salario_actual_val] + salarios_reales_proy # Renombrado 'salarios_reales'


        ax.plot([str(a) for a in años_plot_proy], salarios_nominales_plot, 'b-o', label='Salario nominal', linewidth=2)
        ax.plot([str(a) for a in años_plot_proy], salarios_reales_plot, 'r--o', label='Salario real (ajustado)', linewidth=2)

        ax.set_xlabel('Año')
        ax.set_ylabel('Salario (€)')
        ax.set_title('Proyección Salarial a Futuro')
        ax.legend()
        ax.grid(True, alpha=0.3)
        ax.fill_between([str(a) for a in años_plot_proy], salarios_reales_plot, salarios_nominales_plot, alpha=0.2, color='gray', label='Pérdida por inflación')
        self.figure.tight_layout()

    def simular_escenarios(self):
        """Simula y muestra diferentes escenarios de incrementos salariales"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Simulación de Escenarios")
        dialog.setModal(True)
        dialog.resize(800, 400)
        layout_dialog = QVBoxLayout(dialog) # Renombrado 'layout'

        tabla_escenarios = QTableWidget() # Renombrado 'tabla'
        tabla_escenarios.setColumnCount(6)
        tabla_escenarios.setHorizontalHeaderLabels(['Escenario', 'Incremento Anual', 'Salario en 5 años', 'Total 5 años', 'Poder Adquisitivo', 'Recomendación'])

        salario_actual_sim = 0 # Renombrado 'salario_actual'
        if self.historial_incrementos:
            salario_actual_sim = self.historial_incrementos[-1]['salario_resultante']
        else:
            salario_actual_sim = self.spin_salario_actual.value() + self.spin_pluses_actual.value()

        escenarios_data = [('Conservador', 1.5), ('Moderado', 2.5), ('Optimista', 4.0), ('Muy optimista', 6.0)] # Renombrado 'escenarios'
        inflacion_estimada_sim = 2.0 / 100.0 # Renombrado 'inflacion_estimada'

        tabla_escenarios.setRowCount(len(escenarios_data))
        for i, (nombre_esc, incremento_esc) in enumerate(escenarios_data): # Renombrado 'nombre', 'incremento'
            incremento_pct_esc = incremento_esc / 100.0 # Renombrado 'incremento'
            salario_5_anos_esc = salario_actual_sim * ((1 + incremento_pct_esc) ** 5) # Renombrado 'salario_5_anos'
            total_5_anos_esc = sum(salario_actual_sim * ((1 + incremento_pct_esc) ** j) * 12 for j in range(1, 6)) # Renombrado 'total_5_anos'
            salario_real_5_anos_esc = salario_5_anos_esc / ((1 + inflacion_estimada_sim) ** 5) # Renombrado 'salario_real_5_anos'
            cambio_poder_adq_esc = ((salario_real_5_anos_esc / salario_actual_sim - 1) * 100) if salario_actual_sim > 0 else 0 # Renombrado 'cambio_poder_adq'

            recomendacion_str = "" # Renombrado 'recomendacion'
            if cambio_poder_adq_esc > 5: recomendacion_str = "✅ Excelente"
            elif cambio_poder_adq_esc > 0: recomendacion_str = "👍 Bueno"
            elif cambio_poder_adq_esc > -5: recomendacion_str = "⚠️ Regular"
            else: recomendacion_str = "❌ Insuficiente"

            tabla_escenarios.setItem(i, 0, QTableWidgetItem(nombre_esc))
            tabla_escenarios.setItem(i, 1, QTableWidgetItem(f"{incremento_esc}%"))
            tabla_escenarios.setItem(i, 2, QTableWidgetItem(f"€ {salario_5_anos_esc:.2f}"))
            tabla_escenarios.setItem(i, 3, QTableWidgetItem(f"€ {total_5_anos_esc:.2f}"))
            tabla_escenarios.setItem(i, 4, QTableWidgetItem(f"{cambio_poder_adq_esc:.2f}%"))
            tabla_escenarios.setItem(i, 5, QTableWidgetItem(recomendacion_str))

        layout_dialog.addWidget(tabla_escenarios)
        btn_cerrar_dialog = QPushButton("Cerrar") # Renombrado 'btn_cerrar'
        btn_cerrar_dialog.clicked.connect(dialog.accept)
        layout_dialog.addWidget(btn_cerrar_dialog)
        dialog.exec_()

    def exportar_analisis(self):
        """Exporta el análisis de incrementos a un archivo Excel"""
        archivo_exp, _ = QFileDialog.getSaveFileName(self, 'Exportar análisis', 'analisis_incrementos_salariales.xlsx', 'Excel (*.xlsx)') # Renombrado 'archivo'
        if archivo_exp:
            try:
                historial_data_exp = [] # Renombrado 'historial_data'
                for inc in self.historial_incrementos:
                    fecha_qdate_exp = QDate.fromString(inc['fecha'], "yyyy-MM-dd") # Renombrado 'fecha'
                    historial_data_exp.append({
                        'Fecha': fecha_qdate_exp.toString('dd/MM/yyyy'), 'Concepto': inc['concepto'], 'Tipo': inc['tipo'],
                        'Valor': inc['valor'], 'Salario Resultante': f"€ {inc['salario_resultante']:.2f}",
                        'Incremento Acumulado': f"{inc['acumulado']:.2f}%"
                    })
                df_historial_exp = pd.DataFrame(historial_data_exp) # Renombrado 'df_historial'

                df_proyeccion_exp = pd.DataFrame() # Renombrado 'df_proyeccion'
                if self.proyecciones:
                    proyeccion_data_exp = [] # Renombrado 'proyeccion_data'
                    for proy in self.proyecciones:
                        proyeccion_data_exp.append({
                            'Año': proy['año'], 'Salario Nominal': f"€ {proy['salario_nominal']:.2f}",
                            'Salario Real': f"€ {proy['salario_real']:.2f}", 'Poder Adquisitivo': f"{proy['poder_adquisitivo']:.2f}%"
                        })
                    df_proyeccion_exp = pd.DataFrame(proyeccion_data_exp)

                ultimo_concepto_hist = self.historial_incrementos[-1]['concepto'] if self.historial_incrementos else 'N/A'
                ultimo_acumulado_hist = f"{self.historial_incrementos[-1]['acumulado']:.2f}%" if self.historial_incrementos else '0%'

                resumen_data_exp = { # Renombrado 'resumen_data'
                    'Concepto': ['Salario Base Actual', 'Pluses Actuales', 'Total Actual', 'Último Incremento', 'Incremento Acumulado Total'],
                    'Valor': [
                        f"€ {self.spin_salario_actual.value():.2f}", f"€ {self.spin_pluses_actual.value():.2f}",
                        f"€ {self.spin_salario_actual.value() + self.spin_pluses_actual.value():.2f}",
                        ultimo_concepto_hist, ultimo_acumulado_hist
                    ]
                }
                df_resumen_exp = pd.DataFrame(resumen_data_exp) # Renombrado 'df_resumen'

                with pd.ExcelWriter(archivo_exp, engine='openpyxl') as writer_excel: # Renombrado 'writer'
                    df_resumen_exp.to_excel(writer_excel, sheet_name='Resumen', index=False)
                    df_historial_exp.to_excel(writer_excel, sheet_name='Historial', index=False)
                    if not df_proyeccion_exp.empty:
                        df_proyeccion_exp.to_excel(writer_excel, sheet_name='Proyecciones', index=False)
                QMessageBox.information(self, 'Exportación exitosa', f'El análisis se ha exportado a:\n{archivo_exp}')
            except Exception as e:
                QMessageBox.critical(self, 'Error al exportar', f'Error al exportar el análisis:\n{str(e)}')

    def limpiar_datos(self):
        """Limpia todos los datos del formulario y el historial"""
        respuesta = QMessageBox.question(self, 'Confirmar limpieza', '¿Limpiar todos los datos?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if respuesta == QMessageBox.Yes:
            self.historial_incrementos = []
            self.proyecciones = []
            self.tabla_historial.setRowCount(0)
            self.spin_salario_actual.setValue(2000)
            self.spin_pluses_actual.setValue(300)
            self.spin_porcentaje.setValue(3.0)
            self.spin_cantidad.setValue(100)
            self.input_concepto.clear()
            self.date_aplicacion.setDate(QDate.currentDate())
            self.calcular_incremento()
            self.figure.clear() # Limpiar figura explícitamente
            self.canvas.draw() # Redibujar canvas vacío
            QMessageBox.information(self, 'Datos limpiados', 'Todos los datos han sido eliminados.')

