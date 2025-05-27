import pandas as pd
import numpy as np
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                            QTableWidget, QTableWidgetItem, QLabel, QComboBox,
                            QGroupBox, QSplitter, QTextEdit, QFileDialog,
                            QMessageBox, QProgressBar, QSpinBox, QDoubleSpinBox)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QColor, QFont
import PyPDF2
import re
from datetime import datetime

class ProcesadorArchivos(QThread):
    """Thread para procesar archivos sin bloquear la interfaz"""
    progreso = pyqtSignal(int)
    resultado = pyqtSignal(dict)
    error = pyqtSignal(str)
    
    def __init__(self, archivos):
        super().__init__()
        self.archivos = archivos
        
    def run(self):
        try:
            datos = []
            total_archivos = len(self.archivos)
            
            for i, archivo in enumerate(self.archivos):
                if archivo.endswith('.pdf'):
                    datos_pdf = self.procesar_pdf(archivo)
                    if datos_pdf:
                        datos.append(datos_pdf)
                elif archivo.endswith(('.xlsx', '.xls')):
                    datos_excel = self.procesar_excel(archivo)
                    if datos_excel:
                        datos.append(datos_excel)
                        
                progreso_actual = int((i + 1) / total_archivos * 100)
                self.progreso.emit(progreso_actual)
                
            self.resultado.emit({'datos': datos})
            
        except Exception as e:
            self.error.emit(str(e))
            
    def procesar_pdf(self, archivo):
        """Procesa archivos PDF de nóminas"""
        try:
            with open(archivo, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                texto_completo = ""
                
                for pagina in pdf_reader.pages:
                    texto_completo += pagina.extract_text()
                
                # Extraer datos relevantes del PDF
                datos = self.extraer_datos_nomina(texto_completo)
                datos['archivo'] = archivo
                datos['tipo'] = 'PDF'
                
                return datos
                
        except Exception as e:
            print(f"Error procesando PDF {archivo}: {str(e)}")
            return None
            
    def procesar_excel(self, archivo):
        """Procesa archivos Excel"""
        try:
            df = pd.read_excel(archivo)
            
            # Intentar identificar la estructura del Excel
            datos = {
                'archivo': archivo,
                'tipo': 'Excel',
                'dataframe': df
            }
            
            # Buscar columnas típicas de nóminas
            columnas_nomina = ['salario', 'sueldo', 'total', 'neto', 'bruto']
            columnas_encontradas = [col for col in df.columns if any(palabra in col.lower() for palabra in columnas_nomina)]
            
            if columnas_encontradas:
                datos['columnas_nomina'] = columnas_encontradas
                
            return datos
            
        except Exception as e:
            print(f"Error procesando Excel {archivo}: {str(e)}")
            return None
            
    def extraer_datos_nomina(self, texto):
        """Extrae datos relevantes del texto de una nómina"""
        datos = {
            'periodo': '',
            'salario_bruto': 0.0,
            'salario_neto': 0.0,
            'deducciones': 0.0,
            'horas_trabajadas': 0.0,
            'conceptos': []
        }
        
        # Patrones de búsqueda (estos se pueden personalizar según el formato de las nóminas)
        patrones = {
            'periodo': r'(?:periodo|período|mes)[\s:]+([a-zA-Z]+\s+\d{4})',
            'salario_bruto': r'(?:bruto|total\s+devengado)[\s:]+(?:€\s*)?(\d+[.,]\d{2})',
            'salario_neto': r'(?:neto|líquido|a\s+percibir)[\s:]+(?:€\s*)?(\d+[.,]\d{2})',
            'horas': r'(?:horas\s+trabajadas|horas)[\s:]+(\d+[.,]?\d*)'
        }
        
        for clave, patron in patrones.items():
            coincidencia = re.search(patron, texto, re.IGNORECASE)
            if coincidencia:
                if clave in ['salario_bruto', 'salario_neto']:
                    valor = coincidencia.group(1).replace(',', '.')
                    datos[clave] = float(valor)
                elif clave == 'horas':
                    datos['horas_trabajadas'] = float(coincidencia.group(1).replace(',', '.'))
                else:
                    datos[clave] = coincidencia.group(1)
                    
        # Calcular deducciones
        if datos['salario_bruto'] > 0 and datos['salario_neto'] > 0:
            datos['deducciones'] = datos['salario_bruto'] - datos['salario_neto']
            
        return datos

class ComparacionWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.datos_cargados = []
        self.initUI()
        
    def initUI(self):
        layout_principal = QVBoxLayout(self)
        
        # Barra de herramientas
        layout_herramientas = QHBoxLayout()
        
        btn_cargar_nominas = QPushButton('📁 Cargar Nóminas')
        btn_cargar_nominas.clicked.connect(self.cargar_nominas)
        layout_herramientas.addWidget(btn_cargar_nominas)
        
        btn_cargar_saldos = QPushButton('💰 Cargar Saldos')
        btn_cargar_saldos.clicked.connect(self.cargar_saldos)
        layout_herramientas.addWidget(btn_cargar_saldos)
        
        btn_cargar_tiempos = QPushButton('⏱️ Cargar Tiempos')
        btn_cargar_tiempos.clicked.connect(self.cargar_tiempos)
        layout_herramientas.addWidget(btn_cargar_tiempos)
        
        layout_herramientas.addStretch()
        
        btn_comparar = QPushButton('🔍 Comparar')
        btn_comparar.clicked.connect(self.realizar_comparacion)
        btn_comparar.setStyleSheet('background-color: #ff9800;')
        layout_herramientas.addWidget(btn_comparar)
        
        layout_principal.addLayout(layout_herramientas)
        
        # Barra de progreso
        self.barra_progreso = QProgressBar()
        self.barra_progreso.setVisible(False)
        layout_principal.addWidget(self.barra_progreso)
        
        # Splitter para dividir la vista
        splitter = QSplitter(Qt.Horizontal)
        
        # Panel izquierdo - Datos cargados
        panel_izquierdo = QWidget()
        layout_izquierdo = QVBoxLayout(panel_izquierdo)
        
        lbl_datos = QLabel('Datos Cargados:')
        lbl_datos.setFont(QFont('Arial', 10, QFont.Bold))
        layout_izquierdo.addWidget(lbl_datos)
        
        self.tabla_datos = QTableWidget()
        self.tabla_datos.setColumnCount(4)
        self.tabla_datos.setHorizontalHeaderLabels(['Archivo', 'Tipo', 'Periodo', 'Estado'])
        layout_izquierdo.addWidget(self.tabla_datos)
        
        # Panel derecho - Resultados de comparación
        panel_derecho = QWidget()
        layout_derecho = QVBoxLayout(panel_derecho)
        
        # Selector de tipo de comparación
        layout_tipo_comparacion = QHBoxLayout()
        layout_tipo_comparacion.addWidget(QLabel('Tipo de comparación:'))
        
        self.combo_tipo = QComboBox()
        self.combo_tipo.addItems([
            'Comparación mensual',
            'Comparación anual',
            'Análisis de tendencias',
            'Detección de anomalías'
        ])
        layout_tipo_comparacion.addWidget(self.combo_tipo)
        
        # Umbral de desviación
        layout_tipo_comparacion.addWidget(QLabel('Umbral desviación (%):'))
        self.spin_umbral = QDoubleSpinBox()
        self.spin_umbral.setRange(0, 100)
        self.spin_umbral.setValue(5.0)
        self.spin_umbral.setSingleStep(0.5)
        layout_tipo_comparacion.addWidget(self.spin_umbral)
        
        layout_derecho.addLayout(layout_tipo_comparacion)
        
        # Tabla de resultados
        lbl_resultados = QLabel('Resultados de Comparación:')
        lbl_resultados.setFont(QFont('Arial', 10, QFont.Bold))
        layout_derecho.addWidget(lbl_resultados)
        
        self.tabla_resultados = QTableWidget()
        layout_derecho.addWidget(self.tabla_resultados)
        
        # Área de resumen
        lbl_resumen = QLabel('Resumen y Observaciones:')
        lbl_resumen.setFont(QFont('Arial', 10, QFont.Bold))
        layout_derecho.addWidget(lbl_resumen)
        
        self.texto_resumen = QTextEdit()
        self.texto_resumen.setMaximumHeight(150)
        layout_derecho.addWidget(self.texto_resumen)
        
        # Agregar paneles al splitter
        splitter.addWidget(panel_izquierdo)
        splitter.addWidget(panel_derecho)
        splitter.setSizes([400, 600])
        
        layout_principal.addWidget(splitter)
        
        # Botones de acción
        layout_acciones = QHBoxLayout()
        
        btn_exportar = QPushButton('📊 Exportar Resultados')
        btn_exportar.clicked.connect(self.exportar_resultados)
        layout_acciones.addWidget(btn_exportar)
        
        btn_generar_informe = QPushButton('📄 Generar Informe')
        btn_generar_informe.clicked.connect(self.generar_informe)
        layout_acciones.addWidget(btn_generar_informe)
        
        layout_acciones.addStretch()
        
        btn_limpiar = QPushButton('🗑️ Limpiar Todo')
        btn_limpiar.clicked.connect(self.limpiar_datos)
        btn_limpiar.setStyleSheet('background-color: #f44336;')
        layout_acciones.addWidget(btn_limpiar)
        
        layout_principal.addLayout(layout_acciones)
        
    def cargar_nominas(self):
        """Carga archivos de nóminas"""
        self.cargar_archivos('Nóminas')
        
    def cargar_saldos(self):
        """Carga archivos de saldos"""
        self.cargar_archivos('Saldos')
        
    def cargar_tiempos(self):
        """Carga archivos de tiempos"""
        self.cargar_archivos('Tiempos')
        
    def cargar_archivos(self, tipo):
        """Carga archivos del tipo especificado"""
        archivos, _ = QFileDialog.getOpenFileNames(
            self,
            f'Cargar archivos de {tipo}',
            '',
            'Archivos soportados (*.pdf *.xlsx *.xls);;PDF (*.pdf);;Excel (*.xlsx *.xls)'
        )
        
        if archivos:
            self.barra_progreso.setVisible(True)
            self.procesador = ProcesadorArchivos(archivos)
            self.procesador.progreso.connect(self.actualizar_progreso)
            self.procesador.resultado.connect(lambda r: self.archivos_procesados(r, tipo))
            self.procesador.error.connect(self.mostrar_error)
            self.procesador.start()
            
    def actualizar_progreso(self, valor):
        """Actualiza la barra de progreso"""
        self.barra_progreso.setValue(valor)
        
    def archivos_procesados(self, resultado, tipo):
        """Procesa los archivos cargados"""
        self.barra_progreso.setVisible(False)
        datos = resultado.get('datos', [])
        
        for dato in datos:
            dato['categoria'] = tipo
            self.datos_cargados.append(dato)
            
            # Agregar a la tabla
            row = self.tabla_datos.rowCount()
            self.tabla_datos.insertRow(row)
            
            # Obtener nombre del archivo sin ruta
            nombre_archivo = dato['archivo'].split('/')[-1].split('\\')[-1]
            
            self.tabla_datos.setItem(row, 0, QTableWidgetItem(nombre_archivo))
            self.tabla_datos.setItem(row, 1, QTableWidgetItem(tipo))
            self.tabla_datos.setItem(row, 2, QTableWidgetItem(dato.get('periodo', 'N/A')))
            self.tabla_datos.setItem(row, 3, QTableWidgetItem('✓ Cargado'))
            
            # Colorear la fila según el tipo
            colores = {
                'Nóminas': QColor(200, 230, 201),
                'Saldos': QColor(187, 222, 251),
                'Tiempos': QColor(255, 224, 178)
            }
            
            color = colores.get(tipo, QColor(255, 255, 255))
            for col in range(4):
                self.tabla_datos.item(row, col).setBackground(color)
                
        QMessageBox.information(
            self,
            'Archivos cargados',
            f'Se han cargado {len(datos)} archivos de {tipo} correctamente.'
        )
        
    def realizar_comparacion(self):
        """Realiza la comparación de los datos cargados"""
        if not self.datos_cargados:
            QMessageBox.warning(
                self,
                'Sin datos',
                'Por favor, cargue archivos antes de realizar la comparación.'
            )
            return
            
        tipo_comparacion = self.combo_tipo.currentText()
        umbral = self.spin_umbral.value()
        
        # Separar datos por categoría
        nominas = [d for d in self.datos_cargados if d['categoria'] == 'Nóminas']
        saldos = [d for d in self.datos_cargados if d['categoria'] == 'Saldos']
        tiempos = [d for d in self.datos_cargados if d['categoria'] == 'Tiempos']
        
        # Realizar comparación según el tipo seleccionado
        if tipo_comparacion == 'Comparación mensual':
            self.comparacion_mensual(nominas, saldos, tiempos, umbral)
        elif tipo_comparacion == 'Comparación anual':
            self.comparacion_anual(nominas, saldos, tiempos, umbral)
        elif tipo_comparacion == 'Análisis de tendencias':
            self.analisis_tendencias(nominas, saldos, tiempos)
        elif tipo_comparacion == 'Detección de anomalías':
            self.detectar_anomalias(nominas, saldos, tiempos, umbral)
            
    def comparacion_mensual(self, nominas, saldos, tiempos, umbral):
        """Realiza comparación mensual de los datos"""
        self.tabla_resultados.clear()
        self.tabla_resultados.setColumnCount(6)
        self.tabla_resultados.setHorizontalHeaderLabels([
            'Concepto', 'Mes Anterior', 'Mes Actual', 'Diferencia', '% Variación', 'Estado'
        ])
        self.tabla_resultados.setRowCount(0)
        
        resumen = "=== COMPARACIÓN MENSUAL ===\n\n"
        
        # Comparar nóminas consecutivas
        if len(nominas) >= 2:
            nomina_anterior = nominas[-2]
            nomina_actual = nominas[-1]
            
            # Comparar salario bruto
            if 'salario_bruto' in nomina_anterior and 'salario_bruto' in nomina_actual:
                bruto_ant = nomina_anterior['salario_bruto']
                bruto_act = nomina_actual['salario_bruto']
                diferencia = bruto_act - bruto_ant
                porcentaje = (diferencia / bruto_ant * 100) if bruto_ant > 0 else 0
                
                row = self.tabla_resultados.rowCount()
                self.tabla_resultados.insertRow(row)
                self.tabla_resultados.setItem(row, 0, QTableWidgetItem('Salario Bruto'))
                self.tabla_resultados.setItem(row, 1, QTableWidgetItem(f'€ {bruto_ant:.2f}'))
                self.tabla_resultados.setItem(row, 2, QTableWidgetItem(f'€ {bruto_act:.2f}'))
                self.tabla_resultados.setItem(row, 3, QTableWidgetItem(f'€ {diferencia:.2f}'))
                self.tabla_resultados.setItem(row, 4, QTableWidgetItem(f'{porcentaje:.2f}%'))
                
                # Determinar estado
                if abs(porcentaje) > umbral:
                    estado = '⚠️ Desviación alta'
                    color = QColor(255, 193, 7)
                    resumen += f"⚠️ Alerta: Variación del {porcentaje:.2f}% en salario bruto\n"
                else:
                    estado = '✅ Normal'
                    color = QColor(76, 175, 80)
                    
                self.tabla_resultados.setItem(row, 5, QTableWidgetItem(estado))
                for col in range(6):
                    if self.tabla_resultados.item(row, col):
                        self.tabla_resultados.item(row, col).setBackground(color)
                        
            # Comparar salario neto
            if 'salario_neto' in nomina_anterior and 'salario_neto' in nomina_actual:
                neto_ant = nomina_anterior['salario_neto']
                neto_act = nomina_actual['salario_neto']
                diferencia = neto_act - neto_ant
                porcentaje = (diferencia / neto_ant * 100) if neto_ant > 0 else 0
                
                row = self.tabla_resultados.rowCount()
                self.tabla_resultados.insertRow(row)
                self.tabla_resultados.setItem(row, 0, QTableWidgetItem('Salario Neto'))
                self.tabla_resultados.setItem(row, 1, QTableWidgetItem(f'€ {neto_ant:.2f}'))
                self.tabla_resultados.setItem(row, 2, QTableWidgetItem(f'€ {neto_act:.2f}'))
                self.tabla_resultados.setItem(row, 3, QTableWidgetItem(f'€ {diferencia:.2f}'))
                self.tabla_resultados.setItem(row, 4, QTableWidgetItem(f'{porcentaje:.2f}%'))
                
                if abs(porcentaje) > umbral:
                    estado = '⚠️ Desviación alta'
                    color = QColor(255, 193, 7)
                else:
                    estado = '✅ Normal'
                    color = QColor(76, 175, 80)
                    
                self.tabla_resultados.setItem(row, 5, QTableWidgetItem(estado))
                for col in range(6):
                    if self.tabla_resultados.item(row, col):
                        self.tabla_resultados.item(row, col).setBackground(color)
                        
        # Comparar horas trabajadas si hay datos de tiempos
        if len(tiempos) >= 2:
            tiempo_anterior = tiempos[-2]
            tiempo_actual = tiempos[-1]
            
            if 'horas_trabajadas' in tiempo_anterior and 'horas_trabajadas' in tiempo_actual:
                horas_ant = tiempo_anterior['horas_trabajadas']
                horas_act = tiempo_actual['horas_trabajadas']
                diferencia = horas_act - horas_ant
                porcentaje = (diferencia / horas_ant * 100) if horas_ant > 0 else 0
                
                row = self.tabla_resultados.rowCount()
                self.tabla_resultados.insertRow(row)
                self.tabla_resultados.setItem(row, 0, QTableWidgetItem('Horas Trabajadas'))
                self.tabla_resultados.setItem(row, 1, QTableWidgetItem(f'{horas_ant:.1f} h'))
                self.tabla_resultados.setItem(row, 2, QTableWidgetItem(f'{horas_act:.1f} h'))
                self.tabla_resultados.setItem(row, 3, QTableWidgetItem(f'{diferencia:.1f} h'))
                self.tabla_resultados.setItem(row, 4, QTableWidgetItem(f'{porcentaje:.2f}%'))
                
                estado = '✅ Normal'
                color = QColor(76, 175, 80)
                
                self.tabla_resultados.setItem(row, 5, QTableWidgetItem(estado))
                for col in range(6):
                    if self.tabla_resultados.item(row, col):
                        self.tabla_resultados.item(row, col).setBackground(color)
                        
        resumen += f"\nTotal de elementos comparados: {self.tabla_resultados.rowCount()}\n"
        resumen += f"Umbral de desviación configurado: {umbral}%\n"
        
        self.texto_resumen.setText(resumen)
        
    def comparacion_anual(self, nominas, saldos, tiempos, umbral):
        """Realiza comparación anual de los datos"""
        self.tabla_resultados.clear()
        self.tabla_resultados.setColumnCount(5)
        self.tabla_resultados.setHorizontalHeaderLabels([
            'Concepto', 'Total Anual', 'Promedio Mensual', 'Máximo', 'Mínimo'
        ])
        self.tabla_resultados.setRowCount(0)
        
        resumen = "=== COMPARACIÓN ANUAL ===\n\n"
        
        # Analizar nóminas del año
        if nominas:
            salarios_brutos = [n.get('salario_bruto', 0) for n in nominas if 'salario_bruto' in n]
            salarios_netos = [n.get('salario_neto', 0) for n in nominas if 'salario_neto' in n]
            
            if salarios_brutos:
                total_bruto = sum(salarios_brutos)
                promedio_bruto = total_bruto / len(salarios_brutos)
                max_bruto = max(salarios_brutos)
                min_bruto = min(salarios_brutos)
                
                row = self.tabla_resultados.rowCount()
                self.tabla_resultados.insertRow(row)
                self.tabla_resultados.setItem(row, 0, QTableWidgetItem('Salario Bruto'))
                self.tabla_resultados.setItem(row, 1, QTableWidgetItem(f'€ {total_bruto:.2f}'))
                self.tabla_resultados.setItem(row, 2, QTableWidgetItem(f'€ {promedio_bruto:.2f}'))
                self.tabla_resultados.setItem(row, 3, QTableWidgetItem(f'€ {max_bruto:.2f}'))
                self.tabla_resultados.setItem(row, 4, QTableWidgetItem(f'€ {min_bruto:.2f}'))
                
                resumen += f"Salario bruto anual: € {total_bruto:.2f}\n"
                
            if salarios_netos:
                total_neto = sum(salarios_netos)
                promedio_neto = total_neto / len(salarios_netos)
                max_neto = max(salarios_netos)
                min_neto = min(salarios_netos)
                
                row = self.tabla_resultados.rowCount()
                self.tabla_resultados.insertRow(row)
                self.tabla_resultados.setItem(row, 0, QTableWidgetItem('Salario Neto'))
                self.tabla_resultados.setItem(row, 1, QTableWidgetItem(f'€ {total_neto:.2f}'))
                self.tabla_resultados.setItem(row, 2, QTableWidgetItem(f'€ {promedio_neto:.2f}'))
                self.tabla_resultados.setItem(row, 3, QTableWidgetItem(f'€ {max_neto:.2f}'))
                self.tabla_resultados.setItem(row, 4, QTableWidgetItem(f'€ {min_neto:.2f}'))
                
                resumen += f"Salario neto anual: € {total_neto:.2f}\n"
                
                # Calcular retenciones totales
                if salarios_brutos and salarios_netos:
                    total_retenciones = total_bruto - total_neto
                    porcentaje_retencion = (total_retenciones / total_bruto * 100) if total_bruto > 0 else 0
                    
                    row = self.tabla_resultados.rowCount()
                    self.tabla_resultados.insertRow(row)
                    self.tabla_resultados.setItem(row, 0, QTableWidgetItem('Retenciones'))
                    self.tabla_resultados.setItem(row, 1, QTableWidgetItem(f'€ {total_retenciones:.2f}'))
                    self.tabla_resultados.setItem(row, 2, QTableWidgetItem(f'{porcentaje_retencion:.2f}%'))
                    self.tabla_resultados.setItem(row, 3, QTableWidgetItem('-'))
                    self.tabla_resultados.setItem(row, 4, QTableWidgetItem('-'))
                    
                    resumen += f"Retenciones totales: € {total_retenciones:.2f} ({porcentaje_retencion:.2f}%)\n"
                    
        self.texto_resumen.setText(resumen)
        
    def analisis_tendencias(self, nominas, saldos, tiempos):
        """Analiza tendencias en los datos"""
        self.tabla_resultados.clear()
        self.tabla_resultados.setColumnCount(4)
        self.tabla_resultados.setHorizontalHeaderLabels([
            'Concepto', 'Tendencia', 'Variación Media', 'Proyección'
        ])
        self.tabla_resultados.setRowCount(0)
        
        resumen = "=== ANÁLISIS DE TENDENCIAS ===\n\n"
        
        # Analizar tendencia de salarios
        if len(nominas) >= 3:
            salarios_brutos = [n.get('salario_bruto', 0) for n in nominas if 'salario_bruto' in n]
            
            if len(salarios_brutos) >= 3:
                # Calcular tendencia
                variaciones = []
                for i in range(1, len(salarios_brutos)):
                    var = salarios_brutos[i] - salarios_brutos[i-1]
                    variaciones.append(var)
                    
                variacion_media = sum(variaciones) / len(variaciones)
                
                if variacion_media > 0:
                    tendencia = '📈 Ascendente'
                elif variacion_media < 0:
                    tendencia = '📉 Descendente'
                else:
                    tendencia = '➡️ Estable'
                    
                # Proyección simple
                ultimo_salario = salarios_brutos[-1]
                proyeccion = ultimo_salario + variacion_media
                
                row = self.tabla_resultados.rowCount()
                self.tabla_resultados.insertRow(row)
                self.tabla_resultados.setItem(row, 0, QTableWidgetItem('Salario Bruto'))
                self.tabla_resultados.setItem(row, 1, QTableWidgetItem(tendencia))
                self.tabla_resultados.setItem(row, 2, QTableWidgetItem(f'€ {variacion_media:.2f}'))
                self.tabla_resultados.setItem(row, 3, QTableWidgetItem(f'€ {proyeccion:.2f}'))
                
                resumen += f"Tendencia del salario bruto: {tendencia}\n"
                resumen += f"Variación media mensual: € {variacion_media:.2f}\n"
                resumen += f"Proyección próximo mes: € {proyeccion:.2f}\n"
                
        self.texto_resumen.setText(resumen)
        
    def detectar_anomalias(self, nominas, saldos, tiempos, umbral):
        """Detecta anomalías en los datos"""
        self.tabla_resultados.clear()
        self.tabla_resultados.setColumnCount(4)
        self.tabla_resultados.setHorizontalHeaderLabels([
            'Tipo', 'Descripción', 'Valor', 'Severidad'
        ])
        self.tabla_resultados.setRowCount(0)
        
        resumen = "=== DETECCIÓN DE ANOMALÍAS ===\n\n"
        anomalias_encontradas = 0
        
        # Detectar anomalías en salarios
        if len(nominas) >= 2:
            salarios_brutos = [n.get('salario_bruto', 0) for n in nominas if 'salario_bruto' in n]
            
            if salarios_brutos:
                promedio = sum(salarios_brutos) / len(salarios_brutos)
                desviacion = np.std(salarios_brutos)
                
                for i, salario in enumerate(salarios_brutos):
                    # Detectar valores atípicos (más de 2 desviaciones estándar)
                    if abs(salario - promedio) > 2 * desviacion:
                        row = self.tabla_resultados.rowCount()
                        self.tabla_resultados.insertRow(row)
                        self.tabla_resultados.setItem(row, 0, QTableWidgetItem('Salario atípico'))
                        self.tabla_resultados.setItem(row, 1, QTableWidgetItem(f'Mes {i+1}'))
                        self.tabla_resultados.setItem(row, 2, QTableWidgetItem(f'€ {salario:.2f}'))
                        self.tabla_resultados.setItem(row, 3, QTableWidgetItem('🔴 Alta'))
                        
                        # Colorear fila
                        for col in range(4):
                            if self.tabla_resultados.item(row, col):
                                self.tabla_resultados.item(row, col).setBackground(QColor(255, 193, 193))
                                
                        anomalias_encontradas += 1
                        
        resumen += f"Anomalías detectadas: {anomalias_encontradas}\n"
        resumen += f"Umbral de desviación: {umbral}%\n"
        
        if anomalias_encontradas == 0:
            resumen += "\n✅ No se detectaron anomalías significativas en los datos."
        else:
            resumen += f"\n⚠️ Se encontraron {anomalias_encontradas} anomalías que requieren revisión."
            
        self.texto_resumen.setText(resumen)
        
    def exportar_resultados(self):
        """Exporta los resultados a Excel"""
        if self.tabla_resultados.rowCount() == 0:
            QMessageBox.warning(self, 'Sin resultados', 'No hay resultados para exportar.')
            return
            
        archivo, _ = QFileDialog.getSaveFileName(
            self,
            'Exportar resultados',
            'comparacion_nominas.xlsx',
            'Excel (*.xlsx)'
        )
        
        if archivo:
            try:
                # Crear DataFrame desde la tabla
                datos = []
                for row in range(self.tabla_resultados.rowCount()):
                    fila = []
                    for col in range(self.tabla_resultados.columnCount()):
                        item = self.tabla_resultados.item(row, col)
                        fila.append(item.text() if item else '')
                    datos.append(fila)
                    
                columnas = []
                for col in range(self.tabla_resultados.columnCount()):
                    columnas.append(self.tabla_resultados.horizontalHeaderItem(col).text())
                    
                df = pd.DataFrame(datos, columns=columnas)
                
                # Guardar en Excel
                with pd.ExcelWriter(archivo, engine='openpyxl') as writer:
                    df.to_excel(writer, sheet_name='Comparación', index=False)
                    
                    # Agregar hoja de resumen
                    resumen_df = pd.DataFrame({
                        'Resumen': [self.texto_resumen.toPlainText()]
                    })
                    resumen_df.to_excel(writer, sheet_name='Resumen', index=False)
                    
                QMessageBox.information(
                    self,
                    'Exportación exitosa',
                    f'Los resultados se han exportado correctamente a:\n{archivo}'
                )
                
            except Exception as e:
                QMessageBox.critical(
                    self,
                    'Error al exportar',
                    f'Error al exportar los resultados:\n{str(e)}'
                )
                
    def generar_informe(self):
        """Genera un informe detallado"""
        QMessageBox.information(
            self,
            'Generar informe',
            'La función de generación de informes se implementará en el módulo de informes personalizados.'
        )
        
    def limpiar_datos(self):
        """Limpia todos los datos cargados"""
        respuesta = QMessageBox.question(
            self,
            'Confirmar limpieza',
            '¿Está seguro de que desea limpiar todos los datos?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if respuesta == QMessageBox.Yes:
            self.datos_cargados = []
            self.tabla_datos.setRowCount(0)
            self.tabla_resultados.setRowCount(0)
            self.texto_resumen.clear()
            QMessageBox.information(self, 'Datos limpiados', 'Todos los datos han sido eliminados.')
            
    def mostrar_error(self, mensaje):
        """Muestra un mensaje de error"""
        self.barra_progreso.setVisible(False)
        QMessageBox.critical(self, 'Error', f'Error al procesar archivos:\n{mensaje}')