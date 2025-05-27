import pandas as pd
import numpy as np
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                            QTableWidget, QTableWidgetItem, QLabel, QComboBox,
                            QGroupBox, QDateEdit, QSpinBox, QDoubleSpinBox,
                            QMessageBox, QFileDialog, QTextEdit, QCheckBox,
                            QTabWidget, QRadioButton, QButtonGroup)
from PyQt5.QtCore import Qt, QDate, pyqtSignal
from PyQt5.QtGui import QColor, QFont
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from datetime import datetime, timedelta
import calendar

class PrediccionNominaWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.datos_historicos = []
        self.calendario_laboral = {}
        self.initUI()
        
    def initUI(self):
        layout_principal = QVBoxLayout(self)
        
        # Crear tabs
        self.tabs = QTabWidget()
        
        # Tab 1: Configuración
        self.tab_configuracion = QWidget()
        self.setup_tab_configuracion()
        self.tabs.addTab(self.tab_configuracion, "⚙️ Configuración")
        
        # Tab 2: Predicción
        self.tab_prediccion = QWidget()
        self.setup_tab_prediccion()
        self.tabs.addTab(self.tab_prediccion, "🔮 Predicción")
        
        # Tab 3: Análisis
        self.tab_analisis = QWidget()
        self.setup_tab_analisis()
        self.tabs.addTab(self.tab_analisis, "📊 Análisis")
        
        layout_principal.addWidget(self.tabs)
        
    def setup_tab_configuracion(self):
        """Configura la pestaña de configuración"""
        layout = QVBoxLayout(self.tab_configuracion)
        
        # Panel de datos base
        panel_datos = QGroupBox("Datos Base para Predicción")
        layout_datos = QVBoxLayout(panel_datos)
        
        # Fila 1: Periodo y tipo
        layout_periodo = QHBoxLayout()
        
        layout_periodo.addWidget(QLabel("Periodo a predecir:"))
        self.combo_mes = QComboBox()
        meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
                'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
        self.combo_mes.addItems(meses)
        self.combo_mes.setCurrentIndex(datetime.now().month - 1)
        layout_periodo.addWidget(self.combo_mes)
        
        self.spin_year = QSpinBox()
        self.spin_year.setRange(2020, 2030)
        self.spin_year.setValue(datetime.now().year)
        layout_periodo.addWidget(self.spin_year)
        
        layout_periodo.addStretch()
        
        layout_periodo.addWidget(QLabel("Tipo de predicción:"))
        self.combo_tipo_prediccion = QComboBox()
        self.combo_tipo_prediccion.addItems([
            "Basada en histórico",
            "Basada en calendario laboral",
            "Modelo combinado",
            "Simulación manual"
        ])
        layout_periodo.addWidget(self.combo_tipo_prediccion)
        
        layout_datos.addLayout(layout_periodo)
        
        # Fila 2: Datos salariales
        layout_salarios = QHBoxLayout()
        
        layout_salarios.addWidget(QLabel("Salario base mensual:"))
        self.input_salario_base = QDoubleSpinBox()
        self.input_salario_base.setRange(0, 99999)
        self.input_salario_base.setDecimals(2)
        self.input_salario_base.setValue(2000)
        layout_salarios.addWidget(self.input_salario_base)
        
        layout_salarios.addWidget(QLabel("Precio hora ordinaria:"))
        self.input_precio_hora = QDoubleSpinBox()
        self.input_precio_hora.setRange(0, 999)
        self.input_precio_hora.setDecimals(2)
        self.input_precio_hora.setValue(12.50)
        layout_salarios.addWidget(self.input_precio_hora)
        
        layout_salarios.addWidget(QLabel("Precio hora extra:"))
        self.input_precio_hora_extra = QDoubleSpinBox()
        self.input_precio_hora_extra.setRange(0, 999)
        self.input_precio_hora_extra.setDecimals(2)
        self.input_precio_hora_extra.setValue(18.75)
        layout_salarios.addWidget(self.input_precio_hora_extra)
        
        layout_datos.addLayout(layout_salarios)
        
        layout.addWidget(panel_datos)
        
        # Panel de pluses y deducciones
        panel_pluses = QGroupBox("Pluses y Deducciones")
        layout_pluses = QVBoxLayout(panel_pluses)
        
        # Botones para gestionar pluses
        layout_botones_pluses = QHBoxLayout()
        btn_agregar_plus = QPushButton("➕ Agregar Plus")
        btn_agregar_plus.clicked.connect(self.agregar_plus_deduccion)
        layout_botones_pluses.addWidget(btn_agregar_plus)
        
        btn_cargar_historico = QPushButton("📁 Cargar desde Histórico")
        btn_cargar_historico.clicked.connect(self.cargar_pluses_historico)
        layout_botones_pluses.addWidget(btn_cargar_historico)
        
        layout_botones_pluses.addStretch()
        layout_pluses.addLayout(layout_botones_pluses)
        
        # Tabla de pluses y deducciones
        self.tabla_pluses = QTableWidget()
        self.tabla_pluses.setColumnCount(6)
        self.tabla_pluses.setHorizontalHeaderLabels([
            'Concepto', 'Tipo', 'Importe', 'Aplicar', 'Recurrente', 'Eliminar'
        ])
        self.tabla_pluses.setMaximumHeight(200)
        layout_pluses.addWidget(self.tabla_pluses)
        
        # Agregar algunos conceptos por defecto
        self.agregar_conceptos_default()
        
        layout.addWidget(panel_pluses)
        
        # Panel de factores de ajuste
        panel_ajustes = QGroupBox("Factores de Ajuste")
        layout_ajustes = QHBoxLayout(panel_ajustes)
        
        layout_ajustes.addWidget(QLabel("Factor estacionalidad:"))
        self.spin_estacionalidad = QDoubleSpinBox()
        self.spin_estacionalidad.setRange(-50, 50)
        self.spin_estacionalidad.setDecimals(1)
        self.spin_estacionalidad.setValue(0)
        self.spin_estacionalidad.setSuffix("%")
        layout_ajustes.addWidget(self.spin_estacionalidad)
        
        layout_ajustes.addWidget(QLabel("Factor inflación:"))
        self.spin_inflacion = QDoubleSpinBox()
        self.spin_inflacion.setRange(0, 20)
        self.spin_inflacion.setDecimals(1)
        self.spin_inflacion.setValue(2.5)
        self.spin_inflacion.setSuffix("%")
        layout_ajustes.addWidget(self.spin_inflacion)
        
        layout_ajustes.addWidget(QLabel("Confianza predicción:"))
        self.spin_confianza = QSpinBox()
        self.spin_confianza.setRange(50, 99)
        self.spin_confianza.setValue(95)
        self.spin_confianza.setSuffix("%")
        layout_ajustes.addWidget(self.spin_confianza)
        
        layout_ajustes.addStretch()
        
        layout.addWidget(panel_ajustes)
        
        # Botón calcular predicción
        btn_calcular = QPushButton("🔮 Calcular Predicción")
        btn_calcular.clicked.connect(self.calcular_prediccion)
        btn_calcular.setStyleSheet("QPushButton { background-color: #FF9800; font-size: 14px; font-weight: bold; padding: 10px; }")
        layout.addWidget(btn_calcular)
        
    def setup_tab_prediccion(self):
        """Configura la pestaña de resultados de predicción"""
        layout = QVBoxLayout(self.tab_prediccion)
        
        # Panel de resultados principales
        panel_resultados = QGroupBox("Resultados de la Predicción")
        layout_resultados = QVBoxLayout(panel_resultados)
        
        # Grid de resultados
        layout_grid = QHBoxLayout()
        
        # Columna 1
        col1 = QVBoxLayout()
        self.lbl_salario_predicho = QLabel("Salario Bruto Predicho: € 0.00")
        self.lbl_salario_predicho.setFont(QFont('Arial', 14, QFont.Bold))
        self.lbl_salario_predicho.setStyleSheet("color: #4CAF50;")
        col1.addWidget(self.lbl_salario_predicho)
        
        self.lbl_salario_neto_predicho = QLabel("Salario Neto Estimado: € 0.00")
        self.lbl_salario_neto_predicho.setFont(QFont('Arial', 12))
        col1.addWidget(self.lbl_salario_neto_predicho)
        
        layout_grid.addLayout(col1)
        
        # Columna 2
        col2 = QVBoxLayout()
        self.lbl_horas_predichas = QLabel("Horas Trabajadas: 0")
        self.lbl_horas_predichas.setFont(QFont('Arial', 12))
        col2.addWidget(self.lbl_horas_predichas)
        
        self.lbl_dias_laborables = QLabel("Días Laborables: 0")
        self.lbl_dias_laborables.setFont(QFont('Arial', 12))
        col2.addWidget(self.lbl_dias_laborables)
        
        layout_grid.addLayout(col2)
        
        # Columna 3
        col3 = QVBoxLayout()
        self.lbl_variacion_esperada = QLabel("Variación Esperada: 0.00%")
        self.lbl_variacion_esperada.setFont(QFont('Arial', 12))
        col3.addWidget(self.lbl_variacion_esperada)
        
        self.lbl_intervalo_confianza = QLabel("Intervalo: € 0.00 - € 0.00")
        self.lbl_intervalo_confianza.setFont(QFont('Arial', 12))
        col3.addWidget(self.lbl_intervalo_confianza)
        
        layout_grid.addLayout(col3)
        
        layout_resultados.addLayout(layout_grid)
        layout.addWidget(panel_resultados)
        
        # Tabla de desglose
        panel_desglose = QGroupBox("Desglose de la Predicción")
        layout_desglose = QVBoxLayout(panel_desglose)
        
        self.tabla_desglose = QTableWidget()
        self.tabla_desglose.setColumnCount(4)
        self.tabla_desglose.setHorizontalHeaderLabels([
            'Concepto', 'Importe', '% del Total', 'Observaciones'
        ])
        layout_desglose.addWidget(self.tabla_desglose)
        
        layout.addWidget(panel_desglose)
        
        # Panel de comparación
        panel_comparacion = QGroupBox("Comparación con Histórico")
        layout_comparacion = QVBoxLayout(panel_comparacion)
        
        self.texto_comparacion = QTextEdit()
        self.texto_comparacion.setMaximumHeight(100)
        self.texto_comparacion.setReadOnly(True)
        layout_comparacion.addWidget(self.texto_comparacion)
        
        layout.addWidget(panel_comparacion)
        
        # Botones de acción
        layout_acciones = QHBoxLayout()
        
        btn_exportar = QPushButton("📊 Exportar Predicción")
        btn_exportar.clicked.connect(self.exportar_prediccion)
        layout_acciones.addWidget(btn_exportar)
        
        btn_guardar_escenario = QPushButton("💾 Guardar Escenario")
        btn_guardar_escenario.clicked.connect(self.guardar_escenario)
        layout_acciones.addWidget(btn_guardar_escenario)
        
        btn_comparar_escenarios = QPushButton("🔄 Comparar Escenarios")
        btn_comparar_escenarios.clicked.connect(self.comparar_escenarios)
        layout_acciones.addWidget(btn_comparar_escenarios)
        
        layout_acciones.addStretch()
        
        layout.addLayout(layout_acciones)
        
    def setup_tab_analisis(self):
        """Configura la pestaña de análisis"""
        layout = QVBoxLayout(self.tab_analisis)
        
        # Canvas para gráficos
        self.figure = Figure(figsize=(12, 8))
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        
        # Controles de visualización
        panel_controles = QGroupBox("Controles de Visualización")
        layout_controles = QHBoxLayout(panel_controles)
        
        layout_controles.addWidget(QLabel("Tipo de gráfico:"))
        self.combo_tipo_grafico = QComboBox()
        self.combo_tipo_grafico.addItems([
            "Evolución temporal",
            "Comparación mensual",
            "Distribución de conceptos",
            "Análisis de tendencias",
            "Proyección anual"
        ])
        self.combo_tipo_grafico.currentTextChanged.connect(self.actualizar_grafico)
        layout_controles.addWidget(self.combo_tipo_grafico)
        
        self.check_mostrar_prediccion = QCheckBox("Mostrar predicción")
        self.check_mostrar_prediccion.setChecked(True)
        self.check_mostrar_prediccion.stateChanged.connect(self.actualizar_grafico)
        layout_controles.addWidget(self.check_mostrar_prediccion)
        
        self.check_mostrar_intervalos = QCheckBox("Mostrar intervalos de confianza")
        self.check_mostrar_intervalos.setChecked(True)
        self.check_mostrar_intervalos.stateChanged.connect(self.actualizar_grafico)
        layout_controles.addWidget(self.check_mostrar_intervalos)
        
        layout_controles.addStretch()
        
        layout.addWidget(panel_controles)
        
    def agregar_conceptos_default(self):
        """Agrega conceptos por defecto a la tabla"""
        conceptos = [
            ("Plus Transporte", "Plus", 100.0, True, True),
            ("Plus Productividad", "Plus", 150.0, True, True),
            ("Seguridad Social", "Deducción", -200.0, True, True),
            ("IRPF", "Deducción", -300.0, True, True),
            ("Paga Extra Prorrateada", "Plus", 166.67, True, True)
        ]
        
        for concepto, tipo, importe, aplicar, recurrente in conceptos:
            self.agregar_concepto_tabla(concepto, tipo, importe, aplicar, recurrente)
            
    def agregar_concepto_tabla(self, concepto, tipo, importe, aplicar, recurrente):
        """Agrega un concepto a la tabla"""
        row = self.tabla_pluses.rowCount()
        self.tabla_pluses.insertRow(row)
        
        # Concepto
        self.tabla_pluses.setItem(row, 0, QTableWidgetItem(concepto))
        
        # Tipo
        combo_tipo = QComboBox()
        combo_tipo.addItems(["Plus", "Deducción", "Variable"])
        combo_tipo.setCurrentText(tipo)
        self.tabla_pluses.setCellWidget(row, 1, combo_tipo)
        
        # Importe
        self.tabla_pluses.setItem(row, 2, QTableWidgetItem(f"{importe:.2f}"))
        
        # Aplicar
        check_aplicar = QCheckBox()
        check_aplicar.setChecked(aplicar)
        widget_aplicar = QWidget()
        layout_aplicar = QHBoxLayout(widget_aplicar)
        layout_aplicar.addWidget(check_aplicar)
        layout_aplicar.setAlignment(Qt.AlignCenter)
        layout_aplicar.setContentsMargins(0, 0, 0, 0)
        self.tabla_pluses.setCellWidget(row, 3, widget_aplicar)
        
        # Recurrente
        check_recurrente = QCheckBox()
        check_recurrente.setChecked(recurrente)
        widget_recurrente = QWidget()
        layout_recurrente = QHBoxLayout(widget_recurrente)
        layout_recurrente.addWidget(check_recurrente)
        layout_recurrente.setAlignment(Qt.AlignCenter)
        layout_recurrente.setContentsMargins(0, 0, 0, 0)
        self.tabla_pluses.setCellWidget(row, 4, widget_recurrente)
        
        # Eliminar
        btn_eliminar = QPushButton("❌")
        btn_eliminar.clicked.connect(lambda: self.eliminar_concepto(row))
        self.tabla_pluses.setCellWidget(row, 5, btn_eliminar)
        
    def agregar_plus_deduccion(self):
        """Muestra diálogo para agregar un nuevo plus o deducción"""
        from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QFormLayout
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Agregar Plus/Deducción")
        dialog.setModal(True)
        
        layout = QFormLayout(dialog)
        
        # Campos del formulario
        input_concepto = QLineEdit()
        layout.addRow("Concepto:", input_concepto)
        
        combo_tipo = QComboBox()
        combo_tipo.addItems(["Plus", "Deducción", "Variable"])
        layout.addRow("Tipo:", combo_tipo)
        
        input_importe = QDoubleSpinBox()
        input_importe.setRange(-9999, 9999)
        input_importe.setDecimals(2)
        layout.addRow("Importe (€):", input_importe)
        
        check_aplicar = QCheckBox("Aplicar en predicción")
        check_aplicar.setChecked(True)
        layout.addRow(check_aplicar)
        
        check_recurrente = QCheckBox("Es recurrente")
        check_recurrente.setChecked(True)
        layout.addRow(check_recurrente)
        
        # Botones
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, dialog
        )
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addRow(buttons)
        
        if dialog.exec_() == QDialog.Accepted:
            concepto = input_concepto.text()
            if concepto:
                self.agregar_concepto_tabla(
                    concepto,
                    combo_tipo.currentText(),
                    input_importe.value(),
                    check_aplicar.isChecked(),
                    check_recurrente.isChecked()
                )
            else:
                QMessageBox.warning(self, "Error", "Debe especificar un concepto")
                
    def eliminar_concepto(self, row):
        """Elimina un concepto de la tabla"""
        for i in range(self.tabla_pluses.rowCount()):
            btn = self.tabla_pluses.cellWidget(i, 5)
            if btn and btn.clicked == self.sender().clicked:
                self.tabla_pluses.removeRow(i)
                break
                
    def cargar_pluses_historico(self):
        """Carga pluses desde el histórico"""
        QMessageBox.information(
            self,
            "Función en desarrollo",
            "La carga de pluses desde histórico se implementará próximamente."
        )
        
    def calcular_prediccion(self):
        """Calcula la predicción de nómina"""
        mes = self.combo_mes.currentIndex() + 1
        año = self.spin_year.value()
        tipo_prediccion = self.combo_tipo_prediccion.currentText()
        
        # Obtener días laborables del mes
        dias_mes = calendar.monthrange(año, mes)[1]
        dias_laborables = self.calcular_dias_laborables(año, mes)
        
        # Calcular horas trabajadas estimadas
        horas_dia = 8  # Por defecto
        horas_mes = dias_laborables * horas_dia
        
        # Calcular salario base
        salario_base = self.input_salario_base.value()
        
        # Si es por horas, calcular según horas
        if tipo_prediccion == "Basada en calendario laboral":
            precio_hora = self.input_precio_hora.value()
            salario_base = horas_mes * precio_hora
            
        # Aplicar factores de ajuste
        factor_estacionalidad = 1 + (self.spin_estacionalidad.value() / 100)
        factor_inflacion = 1 + (self.spin_inflacion.value() / 100 / 12)  # Mensual
        
        salario_ajustado = salario_base * factor_estacionalidad * factor_inflacion
        
        # Calcular pluses y deducciones
        total_pluses = 0
        total_deducciones = 0
        conceptos_aplicados = []
        
        for row in range(self.tabla_pluses.rowCount()):
            # Verificar si está marcado para aplicar
            check_widget = self.tabla_pluses.cellWidget(row, 3)
            if check_widget:
                checkbox = check_widget.findChild(QCheckBox)
                if checkbox and checkbox.isChecked():
                    concepto = self.tabla_pluses.item(row, 0).text()
                    importe = float(self.tabla_pluses.item(row, 2).text())
                    tipo_combo = self.tabla_pluses.cellWidget(row, 1)
                    tipo = tipo_combo.currentText() if tipo_combo else "Plus"
                    
                    if tipo == "Deducción":
                        total_deducciones += abs(importe)
                    else:
                        total_pluses += importe
                        
                    conceptos_aplicados.append({
                        'concepto': concepto,
                        'importe': importe,
                        'tipo': tipo
                    })
                    
        # Calcular totales
        salario_bruto_predicho = salario_ajustado + total_pluses
        salario_neto_predicho = salario_bruto_predicho - total_deducciones
        
        # Calcular intervalo de confianza
        confianza = self.spin_confianza.value() / 100
        margen_error = salario_bruto_predicho * 0.05  # 5% de margen
        intervalo_min = salario_bruto_predicho - margen_error
        intervalo_max = salario_bruto_predicho + margen_error
        
        # Actualizar resultados
        self.lbl_salario_predicho.setText(f"Salario Bruto Predicho: € {salario_bruto_predicho:.2f}")
        self.lbl_salario_neto_predicho.setText(f"Salario Neto Estimado: € {salario_neto_predicho:.2f}")
        self.lbl_horas_predichas.setText(f"Horas Trabajadas: {horas_mes}")
        self.lbl_dias_laborables.setText(f"Días Laborables: {dias_laborables}")
        
        # Calcular variación si hay histórico
        variacion = 0
        if self.datos_historicos:
            promedio_historico = np.mean([d.get('salario_bruto', 0) for d in self.datos_historicos])
            if promedio_historico > 0:
                variacion = ((salario_bruto_predicho - promedio_historico) / promedio_historico) * 100
                
        self.lbl_variacion_esperada.setText(f"Variación Esperada: {variacion:+.2f}%")
        self.lbl_intervalo_confianza.setText(f"Intervalo: € {intervalo_min:.2f} - € {intervalo_max:.2f}")
        
        # Actualizar tabla de desglose
        self.actualizar_tabla_desglose(salario_base, conceptos_aplicados, salario_bruto_predicho)
        
        # Actualizar comparación
        self.actualizar_comparacion(salario_bruto_predicho, salario_neto_predicho)
        
        # Actualizar gráfico
        self.actualizar_grafico()
        
        # Cambiar a la pestaña de resultados
        self.tabs.setCurrentIndex(1)
        
    def calcular_dias_laborables(self, año, mes):
        """Calcula los días laborables del mes"""
        dias_mes = calendar.monthrange(año, mes)[1]
        dias_laborables = 0
        
        for dia in range(1, dias_mes + 1):
            fecha = datetime(año, mes, dia)
            # Excluir sábados (5) y domingos (6)
            if fecha.weekday() < 5:
                dias_laborables += 1
                
        # Aquí se podrían restar festivos del calendario laboral
        return dias_laborables
        
    def actualizar_tabla_desglose(self, salario_base, conceptos, total):
        """Actualiza la tabla de desglose"""
        self.tabla_desglose.setRowCount(0)
        
        # Salario base
        row = self.tabla_desglose.rowCount()
        self.tabla_desglose.insertRow(row)
        self.tabla_desglose.setItem(row, 0, QTableWidgetItem("Salario Base"))
        self.tabla_desglose.setItem(row, 1, QTableWidgetItem(f"€ {salario_base:.2f}"))
        porcentaje = (salario_base / total * 100) if total > 0 else 0
        self.tabla_desglose.setItem(row, 2, QTableWidgetItem(f"{porcentaje:.1f}%"))
        self.tabla_desglose.setItem(row, 3, QTableWidgetItem("Calculado"))
        
        # Conceptos
        for concepto in conceptos:
            row = self.tabla_desglose.rowCount()
            self.tabla_desglose.insertRow(row)
            self.tabla_desglose.setItem(row, 0, QTableWidgetItem(concepto['concepto']))
            self.tabla_desglose.setItem(row, 1, QTableWidgetItem(f"€ {concepto['importe']:.2f}"))
            porcentaje = (abs(concepto['importe']) / total * 100) if total > 0 else 0
            self.tabla_desglose.setItem(row, 2, QTableWidgetItem(f"{porcentaje:.1f}%"))
            self.tabla_desglose.setItem(row, 3, QTableWidgetItem(concepto['tipo']))
            
            # Colorear según tipo
            if concepto['tipo'] == "Deducción":
                color = QColor(255, 193, 193)
            else:
                color = QColor(200, 230, 201)
                
            for col in range(4):
                self.tabla_desglose.item(row, col).setBackground(color)
                
        # Total
        row = self.tabla_desglose.rowCount()
        self.tabla_desglose.insertRow(row)
        self.tabla_desglose.setItem(row, 0, QTableWidgetItem("TOTAL PREDICHO"))
        self.tabla_desglose.setItem(row, 1, QTableWidgetItem(f"€ {total:.2f}"))
        self.tabla_desglose.setItem(row, 2, QTableWidgetItem("100.0%"))
        self.tabla_desglose.setItem(row, 3, QTableWidgetItem("-"))
        
        # Formatear fila de total
        for col in range(4):
            item = self.tabla_desglose.item(row, col)
            item.setFont(QFont('Arial', 10, QFont.Bold))
            
    def actualizar_comparacion(self, salario_bruto, salario_neto):
        """Actualiza el texto de comparación"""
        mes = self.combo_mes.currentText()
        año = self.spin_year.value()
        
        texto = f"=== PREDICCIÓN PARA {mes.upper()} {año} ===\n\n"
        texto += f"Salario bruto predicho: € {salario_bruto:.2f}\n"
        texto += f"Salario neto estimado: € {salario_neto:.2f}\n"
        texto += f"Retención estimada: € {salario_bruto - salario_neto:.2f}\n\n"
        
        if self.datos_historicos:
            promedio = np.mean([d.get('salario_bruto', 0) for d in self.datos_historicos])
            texto += f"Promedio histórico: € {promedio:.2f}\n"
            diferencia = salario_bruto - promedio
            texto += f"Diferencia: € {diferencia:+.2f}\n"
        else:
            texto += "No hay datos históricos para comparar.\n"
            
        tipo_prediccion = self.combo_tipo_prediccion.currentText()
        texto += f"\nMétodo utilizado: {tipo_prediccion}"
        
        self.texto_comparacion.setText(texto)
        
    def actualizar_grafico(self):
        """Actualiza el gráfico de análisis"""
        self.figure.clear()
        
        tipo_grafico = self.combo_tipo_grafico.currentText()
        
        if tipo_grafico == "Evolución temporal":
            self.grafico_evolucion_temporal()
        elif tipo_grafico == "Comparación mensual":
            self.grafico_comparacion_mensual()
        elif tipo_grafico == "Distribución de conceptos":
            self.grafico_distribucion_conceptos()
        elif tipo_grafico == "Análisis de tendencias":
            self.grafico_analisis_tendencias()
        elif tipo_grafico == "Proyección anual":
            self.grafico_proyeccion_anual()
            
        self.canvas.draw()
        
    def grafico_evolucion_temporal(self):
        """Genera gráfico de evolución temporal"""
        ax = self.figure.add_subplot(111)
        
        # Datos de ejemplo (en producción vendrían del histórico)
        meses = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun']
        valores = [2200, 2250, 2180, 2300, 2280, 2350]
        
        # Agregar predicción si está activa
        if self.check_mostrar_prediccion.isChecked():
            mes_actual = self.combo_mes.currentIndex()
            if mes_actual < len(meses):
                meses.append(self.combo_mes.currentText()[:3])
                # Obtener valor predicho de la etiqueta
                texto_predicho = self.lbl_salario_predicho.text()
                valor_predicho = float(texto_predicho.split('€ ')[1])
                valores.append(valor_predicho)
                
        ax.plot(meses[:-1], valores[:-1], 'b-o', label='Histórico', linewidth=2)
        
        if len(meses) > 6:
            ax.plot(meses[-2:], valores[-2:], 'r--o', label='Predicción', linewidth=2)
            
        ax.set_xlabel('Mes')
        ax.set_ylabel('Salario Bruto (€)')
        ax.set_title('Evolución Temporal del Salario')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
    def grafico_distribucion_conceptos(self):
        """Genera gráfico de distribución de conceptos"""
        ax = self.figure.add_subplot(111)
        
        # Recopilar datos de la tabla de desglose
        conceptos = []
        valores = []
        
        for row in range(self.tabla_desglose.rowCount() - 1):  # Excluir total
            concepto = self.tabla_desglose.item(row, 0).text()
            valor_text = self.tabla_desglose.item(row, 1).text()
            valor = float(valor_text.replace('€', '').strip())
            
            if valor > 0:  # Solo incluir valores positivos
                conceptos.append(concepto)
                valores.append(valor)
                
        if conceptos:
            colors = plt.cm.Set3(range(len(conceptos)))
            ax.pie(valores, labels=conceptos, colors=colors, autopct='%1.1f%%', startangle=90)
            ax.set_title('Distribución de Conceptos Salariales')
            
    def exportar_prediccion(self):
        """Exporta la predicción a Excel"""
        archivo, _ = QFileDialog.getSaveFileName(
            self,
            'Exportar predicción',
            f'prediccion_nomina_{self.combo_mes.currentText()}_{self.spin_year.value()}.xlsx',
            'Excel (*.xlsx)'
        )
        
        if archivo:
            try:
                # Crear DataFrames
                # Resumen
                resumen_data = {
                    'Concepto': ['Mes', 'Año', 'Salario Bruto Predicho', 'Salario Neto Estimado',
                                'Horas Trabajadas', 'Días Laborables', 'Método'],
                    'Valor': [
                        self.combo_mes.currentText(),
                        str(self.spin_year.value()),
                        self.lbl_salario_predicho.text().split(': ')[1],
                        self.lbl_salario_neto_predicho.text().split(': ')[1],
                        self.lbl_horas_predichas.text().split(': ')[1],
                        self.lbl_dias_laborables.text().split(': ')[1],
                        self.combo_tipo_prediccion.currentText()
                    ]
                }
                df_resumen = pd.DataFrame(resumen_data)
                
                # Desglose
                desglose_data = []
                for row in range(self.tabla_desglose.rowCount()):
                    fila = []
                    for col in range(self.tabla_desglose.columnCount()):
                        item = self.tabla_desglose.item(row, col)
                        fila.append(item.text() if item else '')
                    desglose_data.append(fila)
                    
                df_desglose = pd.DataFrame(
                    desglose_data,
                    columns=['Concepto', 'Importe', '% del Total', 'Observaciones']
                )
                
                # Guardar en Excel
                with pd.ExcelWriter(archivo, engine='openpyxl') as writer:
                    df_resumen.to_excel(writer, sheet_name='Resumen', index=False)
                    df_desglose.to_excel(writer, sheet_name='Desglose', index=False)
                    
                QMessageBox.information(
                    self,
                    'Exportación exitosa',
                    f'La predicción se ha exportado correctamente a:\n{archivo}'
                )
                
            except Exception as e:
                QMessageBox.critical(
                    self,
                    'Error al exportar',
                    f'Error al exportar la predicción:\n{str(e)}'
                )
                
    def guardar_escenario(self):
        """Guarda el escenario actual"""
        QMessageBox.information(
            self,
            "Función en desarrollo",
            "La función de guardar escenarios se implementará próximamente."
        )
        
    def comparar_escenarios(self):
        """Compara diferentes escenarios"""
        QMessageBox.information(
            self,
            "Función en desarrollo",
            "La comparación de escenarios se implementará próximamente."
        )
        
    def grafico_comparacion_mensual(self):
        """Genera gráfico de comparación mensual"""
        ax = self.figure.add_subplot(111)
        
        # Datos de ejemplo
        meses = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun']
        salario_base = [1800] * len(meses)
        pluses = [400, 420, 380, 450, 430, 480]
        
        x = range(len(meses))
        width = 0.35
        
        ax.bar(x, salario_base, width, label='Salario Base', color='#4CAF50')
        ax.bar(x, pluses, width, bottom=salario_base, label='Pluses', color='#2196F3')
        
        ax.set_xlabel('Mes')
        ax.set_ylabel('Importe (€)')
        ax.set_title('Comparación Mensual de Conceptos')
        ax.set_xticks(x)
        ax.set_xticklabels(meses)
        ax.legend()
        ax.grid(True, alpha=0.3, axis='y')
        
    def grafico_analisis_tendencias(self):
        """Genera gráfico de análisis de tendencias"""
        ax = self.figure.add_subplot(111)
        
        # Datos de ejemplo con tendencia
        meses = list(range(1, 13))
        valores = [2000 + i*20 + np.random.randint(-50, 50) for i in meses]
        
        # Calcular línea de tendencia
        z = np.polyfit(meses, valores, 1)
        p = np.poly1d(z)
        
        ax.scatter(meses, valores, color='blue', label='Datos reales')
        ax.plot(meses, p(meses), "r--", label=f'Tendencia: y={z[0]:.1f}x+{z[1]:.0f}')
        
        ax.set_xlabel('Mes')
        ax.set_ylabel('Salario (€)')
        ax.set_title('Análisis de Tendencias')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
    def grafico_proyeccion_anual(self):
        """Genera gráfico de proyección anual"""
        ax = self.figure.add_subplot(111)
        
        # Meses del año
        meses = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 
                'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
        
        # Valores históricos (6 meses)
        valores_historicos = [2200, 2250, 2180, 2300, 2280, 2350]
        
        # Proyección para el resto del año
        valores_proyectados = []
        ultimo_valor = valores_historicos[-1]
        for i in range(6):
            # Aplicar factores de estacionalidad y tendencia
            factor = 1 + (self.spin_estacionalidad.value() / 100 / 12)
            ultimo_valor = ultimo_valor * factor
            valores_proyectados.append(ultimo_valor)
            
        # Combinar valores
        todos_valores = valores_historicos + valores_proyectados
        
        # Graficar
        ax.plot(meses[:6], valores_historicos, 'b-o', label='Histórico', linewidth=2)
        ax.plot(meses[5:], [valores_historicos[-1]] + valores_proyectados, 
                'r--o', label='Proyección', linewidth=2)
        
        # Agregar banda de confianza si está activada
        if self.check_mostrar_intervalos.isChecked():
            confianza = 0.05  # 5% de margen
            upper = [v * (1 + confianza) for v in valores_proyectados]
            lower = [v * (1 - confianza) for v in valores_proyectados]
            
            ax.fill_between(meses[6:], lower, upper, alpha=0.2, color='red', 
                          label='Intervalo de confianza')
            
        ax.set_xlabel('Mes')
        ax.set_ylabel('Salario Bruto (€)')
        ax.set_title('Proyección Anual de Salarios')
        ax.legend()
        ax.grid(True, alpha=0.3)
        ax.tick_params(axis='x', rotation=45)