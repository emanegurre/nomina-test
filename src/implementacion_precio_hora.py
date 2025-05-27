import pandas as pd
import numpy as np
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                            QTableWidget, QTableWidgetItem, QLabel, QComboBox,
                            QGroupBox, QLineEdit, QDoubleSpinBox, QSpinBox,
                            QMessageBox, QFileDialog, QCheckBox, QDateEdit)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QColor, QFont
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class PrecioHoraWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.datos_nomina = {}
        self.initUI()
        
    def initUI(self):
        layout_principal = QVBoxLayout(self)
        
        # Panel superior - Entrada de datos
        panel_entrada = QGroupBox("Datos de Entrada")
        layout_entrada = QVBoxLayout(panel_entrada)
        
        # Fila 1: Datos básicos
        layout_basicos = QHBoxLayout()
        
        # Salario bruto mensual
        layout_basicos.addWidget(QLabel("Salario Bruto Mensual (€):"))
        self.input_salario_bruto = QDoubleSpinBox()
        self.input_salario_bruto.setRange(0, 99999)
        self.input_salario_bruto.setDecimals(2)
        self.input_salario_bruto.setValue(2000)
        self.input_salario_bruto.valueChanged.connect(self.calcular_precio_hora)
        layout_basicos.addWidget(self.input_salario_bruto)
        
        # Horas mensuales
        layout_basicos.addWidget(QLabel("Horas Mensuales:"))
        self.input_horas_mes = QSpinBox()
        self.input_horas_mes.setRange(1, 300)
        self.input_horas_mes.setValue(160)
        self.input_horas_mes.valueChanged.connect(self.calcular_precio_hora)
        layout_basicos.addWidget(self.input_horas_mes)
        
        # Horas semanales
        layout_basicos.addWidget(QLabel("Horas Semanales:"))
        self.input_horas_semana = QSpinBox()
        self.input_horas_semana.setRange(1, 80)
        self.input_horas_semana.setValue(40)
        self.input_horas_semana.valueChanged.connect(self.actualizar_horas_mensuales)
        layout_basicos.addWidget(self.input_horas_semana)
        
        layout_entrada.addLayout(layout_basicos)
        
        # Fila 2: Pluses y complementos
        layout_pluses = QHBoxLayout()
        
        btn_agregar_plus = QPushButton("➕ Agregar Plus")
        btn_agregar_plus.clicked.connect(self.agregar_plus)
        layout_pluses.addWidget(btn_agregar_plus)
        
        layout_pluses.addStretch()
        
        layout_entrada.addLayout(layout_pluses)
        
        # Tabla de pluses
        self.tabla_pluses = QTableWidget()
        self.tabla_pluses.setColumnCount(5)
        self.tabla_pluses.setHorizontalHeaderLabels([
            'Concepto', 'Importe (€)', 'Tipo', 'Incluir', 'Eliminar'
        ])
        self.tabla_pluses.setMaximumHeight(150)
        layout_entrada.addWidget(self.tabla_pluses)
        
        # Agregar algunos pluses por defecto
        self.agregar_pluses_default()
        
        layout_principal.addWidget(panel_entrada)
        
        # Panel central - Resultados
        panel_resultados = QGroupBox("Resultados del Cálculo")
        layout_resultados = QVBoxLayout(panel_resultados)
        
        # Grid de resultados
        layout_grid_resultados = QHBoxLayout()
        
        # Columna 1: Precio por hora
        col1 = QVBoxLayout()
        
        self.lbl_precio_hora_bruto = QLabel("Precio/Hora Bruto: 0.00 €")
        self.lbl_precio_hora_bruto.setFont(QFont('Arial', 14, QFont.Bold))
        self.lbl_precio_hora_bruto.setStyleSheet("color: #2196F3;")
        col1.addWidget(self.lbl_precio_hora_bruto)
        
        self.lbl_precio_hora_neto = QLabel("Precio/Hora Neto: 0.00 €")
        self.lbl_precio_hora_neto.setFont(QFont('Arial', 12))
        col1.addWidget(self.lbl_precio_hora_neto)
        
        layout_grid_resultados.addLayout(col1)
        
        # Columna 2: Totales
        col2 = QVBoxLayout()
        
        self.lbl_total_pluses = QLabel("Total Pluses: 0.00 €")
        self.lbl_total_pluses.setFont(QFont('Arial', 12))
        col2.addWidget(self.lbl_total_pluses)
        
        self.lbl_salario_con_pluses = QLabel("Salario + Pluses: 0.00 €")
        self.lbl_salario_con_pluses.setFont(QFont('Arial', 12))
        col2.addWidget(self.lbl_salario_con_pluses)
        
        layout_grid_resultados.addLayout(col2)
        
        # Columna 3: Porcentajes
        col3 = QVBoxLayout()
        
        self.lbl_porcentaje_pluses = QLabel("Pluses sobre salario: 0.00%")
        self.lbl_porcentaje_pluses.setFont(QFont('Arial', 12))
        col3.addWidget(self.lbl_porcentaje_pluses)
        
        self.lbl_retencion_estimada = QLabel("Retención estimada: 0.00%")
        self.lbl_retencion_estimada.setFont(QFont('Arial', 12))
        col3.addWidget(self.lbl_retencion_estimada)
        
        layout_grid_resultados.addLayout(col3)
        
        layout_resultados.addLayout(layout_grid_resultados)
        
        # Tabla de desglose
        self.tabla_desglose = QTableWidget()
        self.tabla_desglose.setColumnCount(4)
        self.tabla_desglose.setHorizontalHeaderLabels([
            'Concepto', 'Importe', '€/Hora', '% del Total'
        ])
        layout_resultados.addWidget(self.tabla_desglose)
        
        layout_principal.addWidget(panel_resultados)
        
        # Panel inferior - Gráficos
        panel_graficos = QGroupBox("Visualización")
        layout_graficos = QVBoxLayout(panel_graficos)
        
        # Canvas para el gráfico
        self.figure = Figure(figsize=(10, 4))
        self.canvas = FigureCanvas(self.figure)
        layout_graficos.addWidget(self.canvas)
        
        layout_principal.addWidget(panel_graficos)
        
        # Botones de acción
        layout_acciones = QHBoxLayout()
        
        btn_cargar_nomina = QPushButton("📁 Cargar desde Nómina")
        btn_cargar_nomina.clicked.connect(self.cargar_desde_nomina)
        layout_acciones.addWidget(btn_cargar_nomina)
        
        btn_comparar_historico = QPushButton("📊 Comparar Histórico")
        btn_comparar_historico.clicked.connect(self.comparar_historico)
        layout_acciones.addWidget(btn_comparar_historico)
        
        btn_exportar = QPushButton("💾 Exportar Cálculo")
        btn_exportar.clicked.connect(self.exportar_calculo)
        layout_acciones.addWidget(btn_exportar)
        
        layout_acciones.addStretch()
        
        btn_limpiar = QPushButton("🗑️ Limpiar")
        btn_limpiar.clicked.connect(self.limpiar_datos)
        layout_acciones.addWidget(btn_limpiar)
        
        layout_principal.addLayout(layout_acciones)
        
        # Calcular valores iniciales
        self.calcular_precio_hora()
        
    def agregar_pluses_default(self):
        """Agrega algunos pluses comunes por defecto"""
        pluses_default = [
            ("Plus Transporte", 100.0, "Mensual"),
            ("Plus Productividad", 150.0, "Mensual"),
            ("Plus Convenio", 80.0, "Mensual"),
            ("Horas Extra", 200.0, "Variable")
        ]
        
        for concepto, importe, tipo in pluses_default:
            self.agregar_plus_tabla(concepto, importe, tipo, False)
            
    def agregar_plus_tabla(self, concepto, importe, tipo, incluir=True):
        """Agrega un plus a la tabla"""
        row = self.tabla_pluses.rowCount()
        self.tabla_pluses.insertRow(row)
        
        # Concepto
        self.tabla_pluses.setItem(row, 0, QTableWidgetItem(concepto))
        
        # Importe
        self.tabla_pluses.setItem(row, 1, QTableWidgetItem(f"{importe:.2f}"))
        
        # Tipo
        combo_tipo = QComboBox()
        combo_tipo.addItems(["Mensual", "Variable", "Anual"])
        combo_tipo.setCurrentText(tipo)
        combo_tipo.currentTextChanged.connect(self.calcular_precio_hora)
        self.tabla_pluses.setCellWidget(row, 2, combo_tipo)
        
        # Checkbox incluir
        checkbox = QCheckBox()
        checkbox.setChecked(incluir)
        checkbox.stateChanged.connect(self.calcular_precio_hora)
        widget_checkbox = QWidget()
        layout_checkbox = QHBoxLayout(widget_checkbox)
        layout_checkbox.addWidget(checkbox)
        layout_checkbox.setAlignment(Qt.AlignCenter)
        layout_checkbox.setContentsMargins(0, 0, 0, 0)
        self.tabla_pluses.setCellWidget(row, 3, widget_checkbox)
        
        # Botón eliminar
        btn_eliminar = QPushButton("❌")
        btn_eliminar.clicked.connect(lambda: self.eliminar_plus(row))
        self.tabla_pluses.setCellWidget(row, 4, btn_eliminar)
        
    def agregar_plus(self):
        """Muestra diálogo para agregar un nuevo plus"""
        from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QFormLayout
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Agregar Plus")
        dialog.setModal(True)
        
        layout = QFormLayout(dialog)
        
        # Campos del formulario
        input_concepto = QLineEdit()
        layout.addRow("Concepto:", input_concepto)
        
        input_importe = QDoubleSpinBox()
        input_importe.setRange(0, 9999)
        input_importe.setDecimals(2)
        layout.addRow("Importe (€):", input_importe)
        
        combo_tipo = QComboBox()
        combo_tipo.addItems(["Mensual", "Variable", "Anual"])
        layout.addRow("Tipo:", combo_tipo)
        
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
            importe = input_importe.value()
            tipo = combo_tipo.currentText()
            
            if concepto:
                self.agregar_plus_tabla(concepto, importe, tipo, True)
                self.calcular_precio_hora()
            else:
                QMessageBox.warning(self, "Error", "Debe especificar un concepto")
                
    def eliminar_plus(self, row):
        """Elimina un plus de la tabla"""
        # Buscar la fila actual del botón
        for i in range(self.tabla_pluses.rowCount()):
            btn = self.tabla_pluses.cellWidget(i, 4)
            if btn and btn.clicked == self.sender().clicked:
                self.tabla_pluses.removeRow(i)
                break
        self.calcular_precio_hora()
        
    def actualizar_horas_mensuales(self):
        """Actualiza las horas mensuales basándose en las semanales"""
        horas_semanales = self.input_horas_semana.value()
        horas_mensuales = horas_semanales * 4.33  # Promedio de semanas por mes
        self.input_horas_mes.setValue(int(horas_mensuales))
        
    def calcular_precio_hora(self):
        """Calcula el precio por hora y actualiza los resultados"""
        salario_bruto = self.input_salario_bruto.value()
        horas_mes = self.input_horas_mes.value()
        
        if horas_mes == 0:
            return
            
        # Calcular total de pluses
        total_pluses = 0
        pluses_incluidos = []
        
        for row in range(self.tabla_pluses.rowCount()):
            # Verificar si está incluido
            checkbox_widget = self.tabla_pluses.cellWidget(row, 3)
            if checkbox_widget:
                checkbox = checkbox_widget.findChild(QCheckBox)
                if checkbox and checkbox.isChecked():
                    concepto = self.tabla_pluses.item(row, 0).text()
                    importe_text = self.tabla_pluses.item(row, 1).text()
                    importe = float(importe_text)
                    
                    combo_tipo = self.tabla_pluses.cellWidget(row, 2)
                    tipo = combo_tipo.currentText() if combo_tipo else "Mensual"
                    
                    # Convertir a mensual si es necesario
                    if tipo == "Anual":
                        importe_mensual = importe / 12
                    else:
                        importe_mensual = importe
                        
                    total_pluses += importe_mensual
                    pluses_incluidos.append({
                        'concepto': concepto,
                        'importe': importe_mensual,
                        'tipo': tipo
                    })
                    
        # Calcular totales
        salario_con_pluses = salario_bruto + total_pluses
        precio_hora_bruto = salario_con_pluses / horas_mes
        
        # Estimar retención (simplificado)
        if salario_con_pluses <= 1000:
            retencion = 0.10
        elif salario_con_pluses <= 2000:
            retencion = 0.15
        elif salario_con_pluses <= 3000:
            retencion = 0.20
        else:
            retencion = 0.25
            
        salario_neto = salario_con_pluses * (1 - retencion)
        precio_hora_neto = salario_neto / horas_mes
        
        # Actualizar labels
        self.lbl_precio_hora_bruto.setText(f"Precio/Hora Bruto: {precio_hora_bruto:.2f} €")
        self.lbl_precio_hora_neto.setText(f"Precio/Hora Neto: {precio_hora_neto:.2f} €")
        self.lbl_total_pluses.setText(f"Total Pluses: {total_pluses:.2f} €")
        self.lbl_salario_con_pluses.setText(f"Salario + Pluses: {salario_con_pluses:.2f} €")
        
        porcentaje_pluses = (total_pluses / salario_bruto * 100) if salario_bruto > 0 else 0
        self.lbl_porcentaje_pluses.setText(f"Pluses sobre salario: {porcentaje_pluses:.2f}%")
        self.lbl_retencion_estimada.setText(f"Retención estimada: {retencion*100:.2f}%")
        
        # Actualizar tabla de desglose
        self.actualizar_desglose(salario_bruto, pluses_incluidos, salario_con_pluses, horas_mes)
        
        # Actualizar gráfico
        self.actualizar_grafico(salario_bruto, pluses_incluidos, total_pluses)
        
    def actualizar_desglose(self, salario_base, pluses, total, horas):
        """Actualiza la tabla de desglose"""
        self.tabla_desglose.setRowCount(0)
        
        # Salario base
        row = self.tabla_desglose.rowCount()
        self.tabla_desglose.insertRow(row)
        self.tabla_desglose.setItem(row, 0, QTableWidgetItem("Salario Base"))
        self.tabla_desglose.setItem(row, 1, QTableWidgetItem(f"{salario_base:.2f} €"))
        self.tabla_desglose.setItem(row, 2, QTableWidgetItem(f"{salario_base/horas:.2f} €/h"))
        porcentaje = (salario_base / total * 100) if total > 0 else 0
        self.tabla_desglose.setItem(row, 3, QTableWidgetItem(f"{porcentaje:.1f}%"))
        
        # Colorear fila
        for col in range(4):
            self.tabla_desglose.item(row, col).setBackground(QColor(200, 230, 201))
            
        # Pluses
        for plus in pluses:
            row = self.tabla_desglose.rowCount()
            self.tabla_desglose.insertRow(row)
            self.tabla_desglose.setItem(row, 0, QTableWidgetItem(plus['concepto']))
            self.tabla_desglose.setItem(row, 1, QTableWidgetItem(f"{plus['importe']:.2f} €"))
            self.tabla_desglose.setItem(row, 2, QTableWidgetItem(f"{plus['importe']/horas:.2f} €/h"))
            porcentaje = (plus['importe'] / total * 100) if total > 0 else 0
            self.tabla_desglose.setItem(row, 3, QTableWidgetItem(f"{porcentaje:.1f}%"))
            
            # Colorear según tipo
            color = QColor(187, 222, 251) if plus['tipo'] == "Mensual" else QColor(255, 224, 178)
            for col in range(4):
                self.tabla_desglose.item(row, col).setBackground(color)
                
        # Total
        row = self.tabla_desglose.rowCount()
        self.tabla_desglose.insertRow(row)
        self.tabla_desglose.setItem(row, 0, QTableWidgetItem("TOTAL"))
        self.tabla_desglose.setItem(row, 1, QTableWidgetItem(f"{total:.2f} €"))
        self.tabla_desglose.setItem(row, 2, QTableWidgetItem(f"{total/horas:.2f} €/h"))
        self.tabla_desglose.setItem(row, 3, QTableWidgetItem("100.0%"))
        
        # Formatear fila de total
        for col in range(4):
            item = self.tabla_desglose.item(row, col)
            item.setFont(QFont('Arial', 10, QFont.Bold))
            item.setBackground(QColor(158, 158, 158))
            
    def actualizar_grafico(self, salario_base, pluses, total_pluses):
        """Actualiza el gráfico de distribución"""
        self.figure.clear()
        
        # Crear subplots
        ax1 = self.figure.add_subplot(121)
        ax2 = self.figure.add_subplot(122)
        
        # Gráfico de pastel
        labels = ['Salario Base']
        sizes = [salario_base]
        colors = ['#4CAF50']
        
        for plus in pluses:
            labels.append(plus['concepto'])
            sizes.append(plus['importe'])
            colors.append('#2196F3' if plus['tipo'] == "Mensual" else '#FF9800')
            
        ax1.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        ax1.set_title('Distribución del Salario')
        
        # Gráfico de barras
        conceptos = ['Salario\nBase'] + [p['concepto'].replace(' ', '\n') for p in pluses]
        valores = [salario_base] + [p['importe'] for p in pluses]
        
        bars = ax2.bar(conceptos, valores, color=colors)
        ax2.set_ylabel('Importe (€)')
        ax2.set_title('Desglose de Conceptos')
        ax2.tick_params(axis='x', rotation=45)
        
        # Añadir valores en las barras
        for bar, valor in zip(bars, valores):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{valor:.0f}€', ha='center', va='bottom')
                    
        self.figure.tight_layout()
        self.canvas.draw()
        
    def cargar_desde_nomina(self):
        """Carga datos desde un archivo de nómina"""
        archivo, _ = QFileDialog.getOpenFileName(
            self,
            'Cargar nómina',
            '',
            'Archivos soportados (*.pdf *.xlsx *.xls);;PDF (*.pdf);;Excel (*.xlsx *.xls)'
        )
        
        if archivo:
            # Aquí se implementaría la lectura del archivo
            QMessageBox.information(
                self,
                'Función en desarrollo',
                'La carga automática desde nómina se implementará próximamente.\n'
                'Por ahora, introduzca los datos manualmente.'
            )
            
    def comparar_historico(self):
        """Compara el precio/hora histórico"""
        QMessageBox.information(
            self,
            'Función en desarrollo',
            'La comparación histórica se implementará próximamente.'
        )
        
    def exportar_calculo(self):
        """Exporta el cálculo actual"""
        archivo, _ = QFileDialog.getSaveFileName(
            self,
            'Exportar cálculo',
            'calculo_precio_hora.xlsx',
            'Excel (*.xlsx);;PDF (*.pdf)'
        )
        
        if archivo:
            if archivo.endswith('.xlsx'):
                self.exportar_excel(archivo)
            elif archivo.endswith('.pdf'):
                self.exportar_pdf(archivo)
                
    def exportar_excel(self, archivo):
        """Exporta a Excel"""
        try:
            # Crear DataFrame con los datos
            datos_resumen = {
                'Concepto': ['Salario Bruto Mensual', 'Horas Mensuales', 'Total Pluses',
                            'Salario + Pluses', 'Precio/Hora Bruto', 'Precio/Hora Neto'],
                'Valor': [
                    f"{self.input_salario_bruto.value():.2f} €",
                    f"{self.input_horas_mes.value()}",
                    self.lbl_total_pluses.text().split(': ')[1],
                    self.lbl_salario_con_pluses.text().split(': ')[1],
                    self.lbl_precio_hora_bruto.text().split(': ')[1],
                    self.lbl_precio_hora_neto.text().split(': ')[1]
                ]
            }
            
            df_resumen = pd.DataFrame(datos_resumen)
            
            # Crear DataFrame del desglose
            desglose_data = []
            for row in range(self.tabla_desglose.rowCount()):
                fila = []
                for col in range(self.tabla_desglose.columnCount()):
                    item = self.tabla_desglose.item(row, col)
                    fila.append(item.text() if item else '')
                desglose_data.append(fila)
                
            df_desglose = pd.DataFrame(
                desglose_data,
                columns=['Concepto', 'Importe', '€/Hora', '% del Total']
            )
            
            # Guardar en Excel
            with pd.ExcelWriter(archivo, engine='openpyxl') as writer:
                df_resumen.to_excel(writer, sheet_name='Resumen', index=False)
                df_desglose.to_excel(writer, sheet_name='Desglose', index=False)
                
            QMessageBox.information(
                self,
                'Exportación exitosa',
                f'El cálculo se ha exportado correctamente a:\n{archivo}'
            )
            
        except Exception as e:
            QMessageBox.critical(
                self,
                'Error al exportar',
                f'Error al exportar el cálculo:\n{str(e)}'
            )
            
    def exportar_pdf(self, archivo):
        """Exporta a PDF"""
        QMessageBox.information(
            self,
            'Función en desarrollo',
            'La exportación a PDF se implementará próximamente.'
        )
        
    def limpiar_datos(self):
        """Limpia todos los datos"""
        respuesta = QMessageBox.question(
            self,
            'Confirmar limpieza',
            '¿Está seguro de que desea limpiar todos los datos?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if respuesta == QMessageBox.Yes:
            self.input_salario_bruto.setValue(2000)
            self.input_horas_mes.setValue(160)
            self.input_horas_semana.setValue(40)
            self.tabla_pluses.setRowCount(0)
            self.agregar_pluses_default()
            self.calcular_precio_hora()