import pandas as pd
import numpy as np
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                            QTableWidget, QTableWidgetItem, QLabel, QComboBox,
                            QGroupBox, QDateEdit, QDoubleSpinBox, QCheckBox,
                            QMessageBox, QFileDialog, QTextEdit, QRadioButton,
                            QButtonGroup, QSpinBox)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QColor, QFont
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from datetime import datetime
import calendar

class PagasExtrasWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.pagas_extras_config = []
        self.historial_pagas = []
        self.initUI()
        
    def initUI(self):
        layout_principal = QVBoxLayout(self)
        
        # Panel de configuración
        panel_config = QGroupBox("Configuración de Pagas Extras")
        layout_config = QVBoxLayout(panel_config)
        
        # Tipo de distribución
        layout_tipo = QHBoxLayout()
        layout_tipo.addWidget(QLabel("Distribución de pagas:"))
        
        self.grupo_distribucion = QButtonGroup()
        self.radio_prorrateadas = QRadioButton("Prorrateadas (12 pagas)")
        self.radio_separadas = QRadioButton("Separadas (14 pagas)")
        self.radio_personalizado = QRadioButton("Personalizado")
        
        self.grupo_distribucion.addButton(self.radio_prorrateadas)
        self.grupo_distribucion.addButton(self.radio_separadas)
        self.grupo_distribucion.addButton(self.radio_personalizado)
        
        self.radio_separadas.setChecked(True)
        
        layout_tipo.addWidget(self.radio_prorrateadas)
        layout_tipo.addWidget(self.radio_separadas)
        layout_tipo.addWidget(self.radio_personalizado)
        layout_tipo.addStretch()
        
        layout_config.addLayout(layout_tipo)
        
        # Conectar eventos
        self.grupo_distribucion.buttonClicked.connect(self.cambiar_tipo_distribucion)
        
        # Datos salariales
        layout_salario = QHBoxLayout()
        
        layout_salario.addWidget(QLabel("Salario base mensual:"))
        self.spin_salario_base = QDoubleSpinBox()
        self.spin_salario_base.setRange(0, 99999)
        self.spin_salario_base.setDecimals(2)
        self.spin_salario_base.setValue(2000)
        self.spin_salario_base.valueChanged.connect(self.calcular_pagas)
        layout_salario.addWidget(self.spin_salario_base)
        
        layout_salario.addWidget(QLabel("Pluses mensuales:"))
        self.spin_pluses = QDoubleSpinBox()
        self.spin_pluses.setRange(0, 9999)
        self.spin_pluses.setDecimals(2)
        self.spin_pluses.setValue(300)
        self.spin_pluses.valueChanged.connect(self.calcular_pagas)
        layout_salario.addWidget(self.spin_pluses)
        
        self.check_pluses_en_extras = QCheckBox("Incluir pluses en pagas extras")
        self.check_pluses_en_extras.setChecked(True)
        self.check_pluses_en_extras.stateChanged.connect(self.calcular_pagas)
        layout_salario.addWidget(self.check_pluses_en_extras)
        
        layout_salario.addStretch()
        layout_config.addLayout(layout_salario)
        
        layout_principal.addWidget(panel_config)
        
        # Panel de pagas extras
        panel_pagas = QGroupBox("Configuración de Pagas Extras")
        layout_pagas = QVBoxLayout(panel_pagas)
        
        # Botones de gestión
        layout_botones = QHBoxLayout()
        
        self.btn_agregar_paga = QPushButton("➕ Agregar Paga Extra")
        self.btn_agregar_paga.clicked.connect(self.agregar_paga_extra)
        layout_botones.addWidget(self.btn_agregar_paga)
        
        self.btn_eliminar_paga = QPushButton("❌ Eliminar Seleccionada")
        self.btn_eliminar_paga.clicked.connect(self.eliminar_paga_extra)
        layout_botones.addWidget(self.btn_eliminar_paga)
        
        btn_cargar_convenio = QPushButton("📋 Cargar desde Convenio")
        btn_cargar_convenio.clicked.connect(self.cargar_desde_convenio)
        layout_botones.addWidget(btn_cargar_convenio)
        
        layout_botones.addStretch()
        layout_pagas.addLayout(layout_botones)
        
        # Tabla de pagas extras
        self.tabla_pagas = QTableWidget()
        self.tabla_pagas.setColumnCount(6)
        self.tabla_pagas.setHorizontalHeaderLabels([
            'Concepto', 'Mes', 'Importe Base', 'Pluses', 'Total', 'Estado'
        ])
        layout_pagas.addWidget(self.tabla_pagas)
        
        layout_principal.addWidget(panel_pagas)
        
        # Panel de resumen y cálculos
        panel_resumen = QGroupBox("Resumen Anual")
        layout_resumen = QVBoxLayout(panel_resumen)
        
        # Grid de resumen
        layout_grid_resumen = QHBoxLayout()
        
        # Columna 1
        col1 = QVBoxLayout()
        self.lbl_total_anual = QLabel("Total anual bruto: € 0.00")
        self.lbl_total_anual.setFont(QFont('Arial', 12, QFont.Bold))
        self.lbl_total_anual.setStyleSheet("color: #2196F3;")
        col1.addWidget(self.lbl_total_anual)
        
        self.lbl_mensual_efectivo = QLabel("Mensual efectivo: € 0.00")
        col1.addWidget(self.lbl_mensual_efectivo)
        
        layout_grid_resumen.addLayout(col1)
        
        # Columna 2
        col2 = QVBoxLayout()
        self.lbl_total_pagas_extras = QLabel("Total pagas extras: € 0.00")
        self.lbl_total_pagas_extras.setFont(QFont('Arial', 12, QFont.Bold))
        col2.addWidget(self.lbl_total_pagas_extras)
        
        self.lbl_numero_pagas = QLabel("Número de pagas: 14")
        col2.addWidget(self.lbl_numero_pagas)
        
        layout_grid_resumen.addLayout(col2)
        
        # Columna 3
        col3 = QVBoxLayout()
        self.lbl_diferencia_prorrateo = QLabel("Diferencia prorrateo: € 0.00")
        col3.addWidget(self.lbl_diferencia_prorrateo)
        
        self.lbl_porcentaje_extras = QLabel("% Pagas extras: 0.00%")
        col3.addWidget(self.lbl_porcentaje_extras)
        
        layout_grid_resumen.addLayout(col3)
        
        layout_resumen.addLayout(layout_grid_resumen)
        
        # Calendario de pagos
        self.tabla_calendario = QTableWidget()
        self.tabla_calendario.setColumnCount(4)
        self.tabla_calendario.setHorizontalHeaderLabels([
            'Mes', 'Salario Base', 'Paga Extra', 'Total Mes'
        ])
        self.tabla_calendario.setMaximumHeight(200)
        layout_resumen.addWidget(self.tabla_calendario)
        
        layout_principal.addWidget(panel_resumen)
        
        # Panel de gráficos
        panel_graficos = QGroupBox("Visualización")
        layout_graficos = QVBoxLayout(panel_graficos)
        
        # Canvas para gráficos
        self.figure = Figure(figsize=(10, 4))
        self.canvas = FigureCanvas(self.figure)
        layout_graficos.addWidget(self.canvas)
        
        # Selector de gráfico
        layout_selector = QHBoxLayout()
        layout_selector.addWidget(QLabel("Tipo de gráfico:"))
        
        self.combo_grafico = QComboBox()
        self.combo_grafico.addItems([
            "Distribución mensual",
            "Comparación 12 vs 14 pagas",
            "Flujo de caja anual",
            "Impacto fiscal"
        ])
        self.combo_grafico.currentTextChanged.connect(self.actualizar_grafico)
        layout_selector.addWidget(self.combo_grafico)
        
        layout_selector.addStretch()
        layout_graficos.addLayout(layout_selector)
        
        layout_principal.addWidget(panel_graficos)
        
        # Botones de acción
        layout_acciones = QHBoxLayout()
        
        btn_simular = QPushButton("🎯 Simular Escenarios")
        btn_simular.clicked.connect(self.simular_escenarios)
        layout_acciones.addWidget(btn_simular)
        
        btn_exportar = QPushButton("📊 Exportar Análisis")
        btn_exportar.clicked.connect(self.exportar_analisis)
        layout_acciones.addWidget(btn_exportar)
        
        btn_generar_calendario = QPushButton("📅 Generar Calendario de Pagos")
        btn_generar_calendario.clicked.connect(self.generar_calendario_pagos)
        layout_acciones.addWidget(btn_generar_calendario)
        
        layout_acciones.addStretch()
        
        layout_principal.addLayout(layout_acciones)
        
        # Inicializar con pagas por defecto
        self.inicializar_pagas_defecto()
        self.calcular_pagas()
        self.actualizar_grafico()
        
    def cambiar_tipo_distribucion(self):
        """Cambia el tipo de distribución de pagas"""
        if self.radio_prorrateadas.isChecked():
            self.btn_agregar_paga.setEnabled(False)
            self.btn_eliminar_paga.setEnabled(False)
            self.tabla_pagas.setEnabled(False)
            # Limpiar pagas extras
            self.pagas_extras_config = []
            self.actualizar_tabla_pagas()
        elif self.radio_separadas.isChecked():
            self.btn_agregar_paga.setEnabled(True)
            self.btn_eliminar_paga.setEnabled(True)
            self.tabla_pagas.setEnabled(True)
            # Cargar pagas estándar si no hay
            if not self.pagas_extras_config:
                self.inicializar_pagas_defecto()
        else:  # Personalizado
            self.btn_agregar_paga.setEnabled(True)
            self.btn_eliminar_paga.setEnabled(True)
            self.tabla_pagas.setEnabled(True)
            
        self.calcular_pagas()
        
    def inicializar_pagas_defecto(self):
        """Inicializa las pagas extras por defecto (verano y navidad)"""
        self.pagas_extras_config = [
            {
                'concepto': 'Paga Extra de Verano',
                'mes': 6,  # Junio
                'porcentaje_base': 100,
                'incluir_pluses': True
            },
            {
                'concepto': 'Paga Extra de Navidad',
                'mes': 12,  # Diciembre
                'porcentaje_base': 100,
                'incluir_pluses': True
            }
        ]
        self.actualizar_tabla_pagas()
        
    def agregar_paga_extra(self):
        """Agrega una nueva paga extra"""
        from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QFormLayout, QLineEdit
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Agregar Paga Extra")
        dialog.setModal(True)
        
        layout = QFormLayout(dialog)
        
        # Concepto
        input_concepto = QLineEdit()
        layout.addRow("Concepto:", input_concepto)
        
        # Mes
        combo_mes = QComboBox()
        meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
                'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
        combo_mes.addItems(meses)
        layout.addRow("Mes de pago:", combo_mes)
        
        # Porcentaje del salario base
        spin_porcentaje = QSpinBox()
        spin_porcentaje.setRange(0, 200)
        spin_porcentaje.setValue(100)
        spin_porcentaje.setSuffix("%")
        layout.addRow("Porcentaje del salario base:", spin_porcentaje)
        
        # Incluir pluses
        check_pluses = QCheckBox("Incluir pluses")
        check_pluses.setChecked(True)
        layout.addRow(check_pluses)
        
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
                paga = {
                    'concepto': concepto,
                    'mes': combo_mes.currentIndex() + 1,
                    'porcentaje_base': spin_porcentaje.value(),
                    'incluir_pluses': check_pluses.isChecked()
                }
                self.pagas_extras_config.append(paga)
                self.actualizar_tabla_pagas()
                self.calcular_pagas()
            else:
                QMessageBox.warning(self, "Error", "Debe especificar un concepto")
                
    def eliminar_paga_extra(self):
        """Elimina la paga extra seleccionada"""
        row = self.tabla_pagas.currentRow()
        if row >= 0 and row < len(self.pagas_extras_config):
            del self.pagas_extras_config[row]
            self.actualizar_tabla_pagas()
            self.calcular_pagas()
            
    def actualizar_tabla_pagas(self):
        """Actualiza la tabla de pagas extras"""
        self.tabla_pagas.setRowCount(0)
        
        salario_base = self.spin_salario_base.value()
        pluses = self.spin_pluses.value()
        
        for paga in self.pagas_extras_config:
            row = self.tabla_pagas.rowCount()
            self.tabla_pagas.insertRow(row)
            
            # Concepto
            self.tabla_pagas.setItem(row, 0, QTableWidgetItem(paga['concepto']))
            
            # Mes
            meses = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun',
                    'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
            self.tabla_pagas.setItem(row, 1, QTableWidgetItem(meses[paga['mes']-1]))
            
            # Calcular importes
            importe_base = salario_base * paga['porcentaje_base'] / 100
            importe_pluses = pluses if paga['incluir_pluses'] else 0
            total = importe_base + importe_pluses
            
            self.tabla_pagas.setItem(row, 2, QTableWidgetItem(f"€ {importe_base:.2f}"))
            self.tabla_pagas.setItem(row, 3, QTableWidgetItem(f"€ {importe_pluses:.2f}"))
            self.tabla_pagas.setItem(row, 4, QTableWidgetItem(f"€ {total:.2f}"))
            self.tabla_pagas.setItem(row, 5, QTableWidgetItem("✓ Configurada"))
            
            # Colorear fila
            for col in range(6):
                self.tabla_pagas.item(row, col).setBackground(QColor(200, 230, 201))
                
    def calcular_pagas(self):
        """Calcula todos los valores relacionados con las pagas"""
        salario_base = self.spin_salario_base.value()
        pluses = self.spin_pluses.value()
        salario_mensual = salario_base + pluses
        
        if self.radio_prorrateadas.isChecked():
            # 12 pagas iguales
            total_anual = salario_mensual * 14  # 14 mensualidades prorrateadas en 12
            mensual_efectivo = total_anual / 12
            total_pagas_extras = salario_mensual * 2  # 2 pagas prorrateadas
            numero_pagas = 12
            
        elif self.radio_separadas.isChecked() or self.radio_personalizado.isChecked():
            # Calcular pagas extras
            total_pagas_extras = 0
            for paga in self.pagas_extras_config:
                importe_base = salario_base * paga['porcentaje_base'] / 100
                importe_pluses = pluses if paga['incluir_pluses'] else 0
                total_pagas_extras += importe_base + importe_pluses
                
            total_anual = (salario_mensual * 12) + total_pagas_extras
            mensual_efectivo = total_anual / 12
            numero_pagas = 12 + len(self.pagas_extras_config)
            
        # Calcular diferencia con prorrateo
        total_prorrateo = salario_mensual * 14
        diferencia_prorrateo = total_anual - total_prorrateo
        
        # Calcular porcentaje que representan las pagas extras
        porcentaje_extras = (total_pagas_extras / total_anual * 100) if total_anual > 0 else 0
        
        # Actualizar labels
        self.lbl_total_anual.setText(f"Total anual bruto: € {total_anual:.2f}")
        self.lbl_mensual_efectivo.setText(f"Mensual efectivo: € {mensual_efectivo:.2f}")
        self.lbl_total_pagas_extras.setText(f"Total pagas extras: € {total_pagas_extras:.2f}")
        self.lbl_numero_pagas.setText(f"Número de pagas: {numero_pagas}")
        self.lbl_diferencia_prorrateo.setText(f"Diferencia prorrateo: € {diferencia_prorrateo:+.2f}")
        self.lbl_porcentaje_extras.setText(f"% Pagas extras: {porcentaje_extras:.2f}%")
        
        # Actualizar calendario
        self.actualizar_calendario_pagos()
        
        # Actualizar gráfico
        self.actualizar_grafico()
        
    def actualizar_calendario_pagos(self):
        """Actualiza el calendario de pagos mensual"""
        self.tabla_calendario.setRowCount(12)
        
        salario_base = self.spin_salario_base.value()
        pluses = self.spin_pluses.value()
        salario_mensual = salario_base + pluses
        
        meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
                'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
        
        total_año = 0
        
        for i in range(12):
            # Salario base del mes
            self.tabla_calendario.setItem(i, 0, QTableWidgetItem(meses[i]))
            self.tabla_calendario.setItem(i, 1, QTableWidgetItem(f"€ {salario_mensual:.2f}"))
            
            # Verificar si hay paga extra este mes
            paga_extra_mes = 0
            if not self.radio_prorrateadas.isChecked():
                for paga in self.pagas_extras_config:
                    if paga['mes'] == i + 1:
                        importe_base = salario_base * paga['porcentaje_base'] / 100
                        importe_pluses = pluses if paga['incluir_pluses'] else 0
                        paga_extra_mes += importe_base + importe_pluses
                        
            if self.radio_prorrateadas.isChecked():
                # En prorrateo, agregar la parte proporcional
                paga_extra_mes = salario_mensual * 2 / 12  # 2 pagas extras / 12 meses
                self.tabla_calendario.setItem(i, 2, QTableWidgetItem(f"€ {paga_extra_mes:.2f} (prorr.)"))
            else:
                self.tabla_calendario.setItem(i, 2, QTableWidgetItem(f"€ {paga_extra_mes:.2f}"))
                
            # Total del mes
            total_mes = salario_mensual + paga_extra_mes
            total_año += total_mes
            self.tabla_calendario.setItem(i, 3, QTableWidgetItem(f"€ {total_mes:.2f}"))
            
            # Colorear filas con pagas extras
            if paga_extra_mes > 0 and not self.radio_prorrateadas.isChecked():
                for col in range(4):
                    self.tabla_calendario.item(i, col).setBackground(QColor(255, 235, 205))
                    
    def cargar_desde_convenio(self):
        """Carga configuración de pagas desde convenio colectivo"""
        from PyQt5.QtWidgets import QDialog, QListWidget, QListWidgetItem
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Cargar desde Convenio")
        dialog.setModal(True)
        
        layout = QVBoxLayout(dialog)
        
        # Lista de convenios predefinidos
        lista = QListWidget()
        
        convenios = [
            {
                'nombre': 'Convenio Metal - 2 pagas extras',
                'pagas': [
                    {'concepto': 'Paga de Verano', 'mes': 7, 'porcentaje_base': 100, 'incluir_pluses': True},
                    {'concepto': 'Paga de Navidad', 'mes': 12, 'porcentaje_base': 100, 'incluir_pluses': True}
                ]
            },
            {
                'nombre': 'Convenio Hostelería - 3 pagas extras',
                'pagas': [
                    {'concepto': 'Paga de Beneficios', 'mes': 3, 'porcentaje_base': 100, 'incluir_pluses': False},
                    {'concepto': 'Paga de Verano', 'mes': 7, 'porcentaje_base': 100, 'incluir_pluses': True},
                    {'concepto': 'Paga de Navidad', 'mes': 12, 'porcentaje_base': 100, 'incluir_pluses': True}
                ]
            },
            {
                'nombre': 'Convenio Construcción - 2 pagas + gratificación',
                'pagas': [
                    {'concepto': 'Gratificación Marzo', 'mes': 3, 'porcentaje_base': 50, 'incluir_pluses': False},
                    {'concepto': 'Paga de Verano', 'mes': 6, 'porcentaje_base': 100, 'incluir_pluses': True},
                    {'concepto': 'Paga de Navidad', 'mes': 12, 'porcentaje_base': 100, 'incluir_pluses': True}
                ]
            },
            {
                'nombre': 'Sector Público - 2 pagas completas',
                'pagas': [
                    {'concepto': 'Paga Extra Junio', 'mes': 6, 'porcentaje_base': 100, 'incluir_pluses': True},
                    {'concepto': 'Paga Extra Diciembre', 'mes': 12, 'porcentaje_base': 100, 'incluir_pluses': True}
                ]
            }
        ]
        
        for convenio in convenios:
            item = QListWidgetItem(convenio['nombre'])
            item.setData(Qt.UserRole, convenio['pagas'])
            lista.addItem(item)
            
        layout.addWidget(QLabel("Seleccione un convenio:"))
        layout.addWidget(lista)
        
        # Botones
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, dialog
        )
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)
        
        if dialog.exec_() == QDialog.Accepted:
            item = lista.currentItem()
            if item:
                self.pagas_extras_config = item.data(Qt.UserRole)
                self.radio_personalizado.setChecked(True)
                self.actualizar_tabla_pagas()
                self.calcular_pagas()
                
                QMessageBox.information(
                    self,
                    "Convenio cargado",
                    f"Se ha cargado la configuración: {item.text()}"
                )
                
    def actualizar_grafico(self):
        """Actualiza el gráfico según el tipo seleccionado"""
        self.figure.clear()
        tipo = self.combo_grafico.currentText()
        
        if tipo == "Distribución mensual":
            self.grafico_distribucion_mensual()
        elif tipo == "Comparación 12 vs 14 pagas":
            self.grafico_comparacion_pagas()
        elif tipo == "Flujo de caja anual":
            self.grafico_flujo_caja()
        elif tipo == "Impacto fiscal":
            self.grafico_impacto_fiscal()
            
        self.canvas.draw()
        
    def grafico_distribucion_mensual(self):
        """Genera gráfico de distribución mensual de pagos"""
        ax = self.figure.add_subplot(111)
        
        meses = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun',
                'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
        
        salario_base = self.spin_salario_base.value()
        pluses = self.spin_pluses.value()
        salario_mensual = salario_base + pluses
        
        # Preparar datos
        salarios = [salario_mensual] * 12
        extras = [0] * 12
        
        if not self.radio_prorrateadas.isChecked():
            for paga in self.pagas_extras_config:
                mes_idx = paga['mes'] - 1
                importe_base = salario_base * paga['porcentaje_base'] / 100
                importe_pluses = pluses if paga['incluir_pluses'] else 0
                extras[mes_idx] += importe_base + importe_pluses
        else:
            # En prorrateo, distribuir uniformemente
            prorrateo_mensual = salario_mensual * 2 / 12
            extras = [prorrateo_mensual] * 12
            
        # Crear gráfico de barras apiladas
        x = np.arange(len(meses))
        width = 0.6
        
        p1 = ax.bar(x, salarios, width, label='Salario mensual', color='#2196F3')
        p2 = ax.bar(x, extras, width, bottom=salarios, label='Paga extra', color='#4CAF50')
        
        ax.set_ylabel('Importe (€)')
        ax.set_title('Distribución Mensual de Pagos')
        ax.set_xticks(x)
        ax.set_xticklabels(meses)
        ax.legend()
        ax.grid(True, alpha=0.3, axis='y')
        
        # Añadir valores totales
        for i in range(len(meses)):
            total = salarios[i] + extras[i]
            if extras[i] > 0:
                ax.text(i, total + 50, f'{total:.0f}€', ha='center', va='bottom', fontsize=9)
                
    def grafico_comparacion_pagas(self):
        """Compara sistema de 12 vs 14 pagas"""
        ax = self.figure.add_subplot(111)
        
        salario_base = self.spin_salario_base.value()
        pluses = self.spin_pluses.value()
        salario_mensual = salario_base + pluses
        
        # Calcular totales
        total_14_pagas = salario_mensual * 14
        total_12_pagas_prorrateo = salario_mensual * 14  # Mismo total anual
        mensual_14_pagas = salario_mensual
        mensual_12_pagas = total_12_pagas_prorrateo / 12
        
        # Datos para el gráfico
        categorias = ['14 Pagas\n(Mensual)', '12 Pagas\n(Mensual)', '14 Pagas\n(Anual)', '12 Pagas\n(Anual)']
        valores = [mensual_14_pagas, mensual_12_pagas, total_14_pagas, total_12_pagas_prorrateo]
        colores = ['#2196F3', '#4CAF50', '#2196F3', '#4CAF50']
        
        bars = ax.bar(categorias[:2], valores[:2], color=colores[:2], alpha=0.7)
        
        # Añadir valores
        for bar, valor in zip(bars, valores[:2]):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'€{valor:.0f}', ha='center', va='bottom')
                   
        ax.set_ylabel('Importe (€)')
        ax.set_title('Comparación: 12 Pagas Prorrateadas vs 14 Pagas')
        ax.grid(True, alpha=0.3, axis='y')
        
        # Añadir tabla comparativa
        ax2 = self.figure.add_subplot(122)
        ax2.axis('tight')
        ax2.axis('off')
        
        tabla_data = [
            ['Concepto', '14 Pagas', '12 Pagas'],
            ['Mensual regular', f'€ {mensual_14_pagas:.2f}', f'€ {mensual_12_pagas:.2f}'],
            ['Pagas extras', '2 pagas completas', 'Prorrateadas'],
            ['Total anual', f'€ {total_14_pagas:.2f}', f'€ {total_12_pagas_prorrateo:.2f}'],
            ['Diferencia mensual', '-', f'€ {mensual_12_pagas - mensual_14_pagas:+.2f}']
        ]
        
        tabla = ax2.table(cellText=tabla_data, loc='center', cellLoc='center')
        tabla.auto_set_font_size(False)
        tabla.set_fontsize(9)
        tabla.scale(1, 1.5)
        
        # Colorear encabezado
        for i in range(3):
            tabla[(0, i)].set_facecolor('#CCCCCC')
            
    def grafico_flujo_caja(self):
        """Genera gráfico de flujo de caja anual"""
        ax = self.figure.add_subplot(111)
        
        meses = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun',
                'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
        
        salario_base = self.spin_salario_base.value()
        pluses = self.spin_pluses.value()
        salario_mensual = salario_base + pluses
        
        # Calcular flujo acumulado
        flujo_mensual = []
        flujo_acumulado = []
        acumulado = 0
        
        for i in range(12):
            ingreso_mes = salario_mensual
            
            # Añadir pagas extras si corresponde
            if not self.radio_prorrateadas.isChecked():
                for paga in self.pagas_extras_config:
                    if paga['mes'] == i + 1:
                        importe_base = salario_base * paga['porcentaje_base'] / 100
                        importe_pluses = pluses if paga['incluir_pluses'] else 0
                        ingreso_mes += importe_base + importe_pluses
            else:
                # En prorrateo
                ingreso_mes += salario_mensual * 2 / 12
                
            flujo_mensual.append(ingreso_mes)
            acumulado += ingreso_mes
            flujo_acumulado.append(acumulado)
            
        # Graficar
        x = range(12)
        ax.plot(x, flujo_acumulado, 'b-o', linewidth=2, label='Ingresos acumulados')
        
        # Marcar meses con pagas extras
        for i, paga in enumerate(self.pagas_extras_config):
            mes_idx = paga['mes'] - 1
            ax.plot(mes_idx, flujo_acumulado[mes_idx], 'ro', markersize=10)
            ax.annotate(paga['concepto'], 
                       xy=(mes_idx, flujo_acumulado[mes_idx]),
                       xytext=(10, 20), textcoords='offset points',
                       fontsize=8, ha='left',
                       bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7),
                       arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))
                       
        ax.set_xlabel('Mes')
        ax.set_ylabel('Ingresos Acumulados (€)')
        ax.set_title('Flujo de Caja Anual')
        ax.set_xticks(x)
        ax.set_xticklabels(meses)
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        # Añadir línea de tendencia
        z = np.polyfit(x, flujo_acumulado, 1)
        p = np.poly1d(z)
        ax.plot(x, p(x), "r--", alpha=0.5, label='Tendencia')
        
    def grafico_impacto_fiscal(self):
        """Muestra el impacto fiscal de las diferentes modalidades"""
        ax = self.figure.add_subplot(111)
        
        salario_base = self.spin_salario_base.value()
        pluses = self.spin_pluses.value()
        total_anual = (salario_base + pluses) * 14
        
        # Tramos IRPF simplificados (ejemplo)
        tramos = [
            (12450, 0.19),
            (20200, 0.24),
            (35200, 0.30),
            (60000, 0.37),
            (300000, 0.45)
        ]
        
        # Calcular IRPF para diferentes escenarios
        escenarios = []
        
        # 14 pagas
        irpf_14_pagas = self.calcular_irpf_estimado(total_anual, tramos)
        neto_14_pagas = total_anual - irpf_14_pagas
        escenarios.append(('14 pagas', total_anual, irpf_14_pagas, neto_14_pagas))
        
        # 12 pagas prorrateadas
        irpf_12_pagas = self.calcular_irpf_estimado(total_anual, tramos)
        neto_12_pagas = total_anual - irpf_12_pagas
        escenarios.append(('12 pagas\nprorrateadas', total_anual, irpf_12_pagas, neto_12_pagas))
        
        # Preparar datos para el gráfico
        nombres = [e[0] for e in escenarios]
        brutos = [e[1] for e in escenarios]
        irpf = [e[2] for e in escenarios]
        netos = [e[3] for e in escenarios]
        
        x = np.arange(len(nombres))
        width = 0.35
        
        # Gráfico de barras
        p1 = ax.bar(x, netos, width, label='Salario neto', color='#4CAF50')
        p2 = ax.bar(x, irpf, width, bottom=netos, label='IRPF', color='#f44336')
        
        ax.set_ylabel('Importe (€)')
        ax.set_title('Impacto Fiscal de las Modalidades de Pago')
        ax.set_xticks(x)
        ax.set_xticklabels(nombres)
        ax.legend()
        ax.grid(True, alpha=0.3, axis='y')
        
        # Añadir porcentajes
        for i in range(len(nombres)):
            porcentaje_irpf = (irpf[i] / brutos[i] * 100)
            ax.text(i, brutos[i] + 500, f'{porcentaje_irpf:.1f}%', 
                   ha='center', va='bottom', fontsize=9)
                   
        # Añadir nota
        ax.text(0.5, -0.15, 'Nota: Cálculo simplificado del IRPF sin deducciones personales',
               transform=ax.transAxes, ha='center', fontsize=8, style='italic')
               
    def calcular_irpf_estimado(self, base_imponible, tramos):
        """Calcula el IRPF estimado según los tramos"""
        irpf_total = 0
        base_restante = base_imponible
        limite_anterior = 0
        
        for limite, tipo in tramos:
            if base_restante <= 0:
                break
                
            base_tramo = min(base_restante, limite - limite_anterior)
            irpf_total += base_tramo * tipo
            base_restante -= base_tramo
            limite_anterior = limite
            
        return irpf_total
        
    def simular_escenarios(self):
        """Simula diferentes escenarios de pagas extras"""
        from PyQt5.QtWidgets import QDialog, QTableWidget
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Simulación de Escenarios")
        dialog.setModal(True)
        dialog.resize(900, 400)
        
        layout = QVBoxLayout(dialog)
        
        # Tabla de escenarios
        tabla = QTableWidget()
        tabla.setColumnCount(7)
        tabla.setHorizontalHeaderLabels([
            'Escenario', 'Nº Pagas', 'Mensual Regular', 'Total Extras',
            'Total Anual', 'Mensual Efectivo', 'Variabilidad'
        ])
        
        salario_base = self.spin_salario_base.value()
        pluses = self.spin_pluses.value()
        salario_mensual = salario_base + pluses
        
        # Definir escenarios
        escenarios = [
            {
                'nombre': '12 pagas prorrateadas',
                'num_pagas': 12,
                'extras': 0,
                'distribucion': 'Uniforme'
            },
            {
                'nombre': '14 pagas (estándar)',
                'num_pagas': 14,
                'extras': 2,
                'distribucion': 'Variable'
            },
            {
                'nombre': '15 pagas (3 extras)',
                'num_pagas': 15,
                'extras': 3,
                'distribucion': 'Variable'
            },
            {
                'nombre': '16 pagas (4 extras)',
                'num_pagas': 16,
                'extras': 4,
                'distribucion': 'Muy variable'
            }
        ]
        
        tabla.setRowCount(len(escenarios))
        
        for i, escenario in enumerate(escenarios):
            # Calcular valores
            if escenario['extras'] == 0:
                # Prorrateado
                total_anual = salario_mensual * 14
                mensual_regular = total_anual / 12
                total_extras = 0
            else:
                # Con pagas extras
                total_extras = salario_mensual * escenario['extras']
                total_anual = (salario_mensual * 12) + total_extras
                mensual_regular = salario_mensual
                
            mensual_efectivo = total_anual / 12
            
            # Llenar tabla
            tabla.setItem(i, 0, QTableWidgetItem(escenario['nombre']))
            tabla.setItem(i, 1, QTableWidgetItem(str(escenario['num_pagas'])))
            tabla.setItem(i, 2, QTableWidgetItem(f"€ {mensual_regular:.2f}"))
            tabla.setItem(i, 3, QTableWidgetItem(f"€ {total_extras:.2f}"))
            tabla.setItem(i, 4, QTableWidgetItem(f"€ {total_anual:.2f}"))
            tabla.setItem(i, 5, QTableWidgetItem(f"€ {mensual_efectivo:.2f}"))
            tabla.setItem(i, 6, QTableWidgetItem(escenario['distribucion']))
            
            # Colorear según variabilidad
            if escenario['distribucion'] == 'Uniforme':
                color = QColor(200, 230, 201)
            elif escenario['distribucion'] == 'Variable':
                color = QColor(255, 235, 205)
            else:
                color = QColor(255, 205, 210)
                
            for col in range(7):
                tabla.item(i, col).setBackground(color)
                
        layout.addWidget(tabla)
        
        # Añadir resumen
        resumen = QTextEdit()
        resumen.setMaximumHeight(100)
        resumen.setReadOnly(True)
        
        texto_resumen = "=== RESUMEN DE ESCENARIOS ===\n\n"
        texto_resumen += "• 12 pagas prorrateadas: Mayor estabilidad mensual, mismo total anual\n"
        texto_resumen += "• 14 pagas: Sistema tradicional, picos en verano y navidad\n"
        texto_resumen += "• Más de 14 pagas: Mayor variabilidad, planificación más compleja\n"
        texto_resumen += "\nRecomendación: Considerar necesidades de liquidez y preferencias personales"
        
        resumen.setText(texto_resumen)
        layout.addWidget(resumen)
        
        # Botón cerrar
        btn_cerrar = QPushButton("Cerrar")
        btn_cerrar.clicked.connect(dialog.accept)
        layout.addWidget(btn_cerrar)
        
        dialog.exec_()
        
    def generar_calendario_pagos(self):
        """Genera un calendario detallado de pagos"""
        archivo, _ = QFileDialog.getSaveFileName(
            self,
            'Guardar calendario de pagos',
            f'calendario_pagos_{datetime.now().year}.xlsx',
            'Excel (*.xlsx);;PDF (*.pdf)'
        )
        
        if archivo:
            if archivo.endswith('.xlsx'):
                self.exportar_calendario_excel(archivo)
            else:
                QMessageBox.information(
                    self,
                    "Función en desarrollo",
                    "La exportación a PDF se implementará próximamente."
                )
                
    def exportar_calendario_excel(self, archivo):
        """Exporta el calendario de pagos a Excel"""
        try:
            # Preparar datos
            calendario_data = []
            
            salario_base = self.spin_salario_base.value()
            pluses = self.spin_pluses.value()
            salario_mensual = salario_base + pluses
            
            meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
                    'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
            
            for i, mes in enumerate(meses):
                registro = {
                    'Mes': mes,
                    'Salario Base': salario_base,
                    'Pluses': pluses,
                    'Total Mensual': salario_mensual
                }
                
                # Verificar pagas extras
                paga_extra_total = 0
                conceptos_extra = []
                
                if not self.radio_prorrateadas.isChecked():
                    for paga in self.pagas_extras_config:
                        if paga['mes'] == i + 1:
                            importe_base = salario_base * paga['porcentaje_base'] / 100
                            importe_pluses = pluses if paga['incluir_pluses'] else 0
                            paga_extra_total += importe_base + importe_pluses
                            conceptos_extra.append(paga['concepto'])
                else:
                    paga_extra_total = salario_mensual * 2 / 12
                    conceptos_extra = ['Prorrateo pagas extras']
                    
                registro['Paga Extra'] = paga_extra_total
                registro['Concepto Extra'] = ', '.join(conceptos_extra) if conceptos_extra else '-'
                registro['Total a Percibir'] = salario_mensual + paga_extra_total
                
                calendario_data.append(registro)
                
            df_calendario = pd.DataFrame(calendario_data)
            
            # Crear resumen
            resumen_data = {
                'Concepto': [
                    'Total Anual Bruto',
                    'Salario Base Anual',
                    'Pluses Anuales',
                    'Total Pagas Extras',
                    'Promedio Mensual',
                    'Número de Pagas'
                ],
                'Importe': [
                    df_calendario['Total a Percibir'].sum(),
                    salario_base * 12,
                    pluses * 12,
                    df_calendario['Paga Extra'].sum(),
                    df_calendario['Total a Percibir'].sum() / 12,
                    12 + len(self.pagas_extras_config)
                ]
            }
            
            df_resumen = pd.DataFrame(resumen_data)
            
            # Guardar en Excel
            with pd.ExcelWriter(archivo, engine='openpyxl') as writer:
                df_calendario.to_excel(writer, sheet_name='Calendario Mensual', index=False)
                df_resumen.to_excel(writer, sheet_name='Resumen Anual', index=False)
                
                # Si hay pagas extras configuradas, agregar hoja de detalle
                if self.pagas_extras_config:
                    extras_data = []
                    for paga in self.pagas_extras_config:
                        extras_data.append({
                            'Concepto': paga['concepto'],
                            'Mes': meses[paga['mes']-1],
                            'Base de Cálculo': f"{paga['porcentaje_base']}% del salario base",
                            'Incluye Pluses': 'Sí' if paga['incluir_pluses'] else 'No',
                            'Importe': salario_base * paga['porcentaje_base'] / 100 + 
                                     (pluses if paga['incluir_pluses'] else 0)
                        })
                    df_extras = pd.DataFrame(extras_data)
                    df_extras.to_excel(writer, sheet_name='Detalle Pagas Extras', index=False)
                    
            QMessageBox.information(
                self,
                'Exportación exitosa',
                f'El calendario de pagos se ha exportado correctamente a:\n{archivo}'
            )
            
        except Exception as e:
            QMessageBox.critical(
                self,
                'Error al exportar',
                f'Error al exportar el calendario:\n{str(e)}'
            )
            
    def exportar_analisis(self):
        """Exporta un análisis completo de las pagas extras"""
        archivo, _ = QFileDialog.getSaveFileName(
            self,
            'Exportar análisis',
            'analisis_pagas_extras.xlsx',
            'Excel (*.xlsx)'
        )
        
        if archivo:
            self.exportar_calendario_excel(archivo)  # Reutilizamos la función