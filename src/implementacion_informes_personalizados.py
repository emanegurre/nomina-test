import pandas as pd
import numpy as np
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                            QLabel, QComboBox, QGroupBox, QCheckBox,
                            QMessageBox, QFileDialog, QListWidget, QTextEdit,
                            QDateEdit, QTableWidget, QTableWidgetItem,
                            QSplitter, QTreeWidget, QTreeWidgetItem,
                            QProgressBar)
from PyQt5.QtCore import Qt, QDate, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QIcon, QColor
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
import os

class GeneradorInformeThread(QThread):
    """Thread para generar informes sin bloquear la interfaz"""
    progreso = pyqtSignal(int)
    estado = pyqtSignal(str)
    completado = pyqtSignal(str)
    error = pyqtSignal(str)
    
    def __init__(self, tipo_informe, configuracion, datos):
        super().__init__()
        self.tipo_informe = tipo_informe
        self.configuracion = configuracion
        self.datos = datos
        
    def run(self):
        try:
            self.estado.emit("Iniciando generación del informe...")
            self.progreso.emit(10)
            
            if self.tipo_informe == "Resumen Ejecutivo":
                archivo = self.generar_resumen_ejecutivo()
            elif self.tipo_informe == "Análisis Detallado":
                archivo = self.generar_analisis_detallado()
            elif self.tipo_informe == "Comparativo Mensual":
                archivo = self.generar_comparativo_mensual()
            elif self.tipo_informe == "Informe Anual":
                archivo = self.generar_informe_anual()
            elif self.tipo_informe == "Análisis de Costes":
                archivo = self.generar_analisis_costes()
            elif self.tipo_informe == "Personalizado":
                archivo = self.generar_informe_personalizado()
                
            self.progreso.emit(100)
            self.completado.emit(archivo)
            
        except Exception as e:
            self.error.emit(str(e))
            
    def generar_resumen_ejecutivo(self):
        """Genera un resumen ejecutivo"""
        self.estado.emit("Generando resumen ejecutivo...")
        self.progreso.emit(30)
        
        # Aquí iría la lógica real de generación
        # Por ahora, simulamos el proceso
        import time
        time.sleep(1)
        
        self.progreso.emit(70)
        
        # Retornar archivo generado
        return "resumen_ejecutivo.pdf"
        
    def generar_analisis_detallado(self):
        """Genera un análisis detallado"""
        self.estado.emit("Generando análisis detallado...")
        # Implementación similar
        return "analisis_detallado.pdf"
        
    def generar_comparativo_mensual(self):
        """Genera comparativo mensual"""
        return "comparativo_mensual.pdf"
        
    def generar_informe_anual(self):
        """Genera informe anual"""
        return "informe_anual.pdf"
        
    def generar_analisis_costes(self):
        """Genera análisis de costes"""
        return "analisis_costes.pdf"
        
    def generar_informe_personalizado(self):
        """Genera informe personalizado"""
        return "informe_personalizado.pdf"

class InformesWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.plantillas_informe = {}
        self.datos_disponibles = {}
        self.initUI()
        
    def initUI(self):
        layout_principal = QVBoxLayout(self)
        
        # Splitter principal
        splitter = QSplitter(Qt.Horizontal)
        
        # Panel izquierdo - Configuración
        panel_config = QWidget()
        layout_config = QVBoxLayout(panel_config)
        
        # Tipo de informe
        grupo_tipo = QGroupBox("Tipo de Informe")
        layout_tipo = QVBoxLayout(grupo_tipo)
        
        self.combo_tipo_informe = QComboBox()
        self.combo_tipo_informe.addItems([
            "Resumen Ejecutivo",
            "Análisis Detallado",
            "Comparativo Mensual",
            "Informe Anual",
            "Análisis de Costes",
            "Informe de Equidad",
            "Dashboard Gerencial",
            "Personalizado"
        ])
        self.combo_tipo_informe.currentTextChanged.connect(self.cambiar_tipo_informe)
        layout_tipo.addWidget(self.combo_tipo_informe)
        
        self.texto_descripcion = QTextEdit()
        self.texto_descripcion.setMaximumHeight(80)
        self.texto_descripcion.setReadOnly(True)
        self.actualizar_descripcion()
        layout_tipo.addWidget(self.texto_descripcion)
        
        layout_config.addWidget(grupo_tipo)
        
        # Período
        grupo_periodo = QGroupBox("Período del Informe")
        layout_periodo = QVBoxLayout(grupo_periodo)
        
        layout_fechas = QHBoxLayout()
        layout_fechas.addWidget(QLabel("Desde:"))
        self.date_desde = QDateEdit()
        self.date_desde.setCalendarPopup(True)
        self.date_desde.setDate(QDate.currentDate().addMonths(-12))
        layout_fechas.addWidget(self.date_desde)
        
        layout_fechas.addWidget(QLabel("Hasta:"))
        self.date_hasta = QDateEdit()
        self.date_hasta.setCalendarPopup(True)
        self.date_hasta.setDate(QDate.currentDate())
        layout_fechas.addWidget(self.date_hasta)
        
        layout_periodo.addLayout(layout_fechas)
        
        # Atajos de período
        layout_atajos = QHBoxLayout()
        btn_mes_actual = QPushButton("Mes Actual")
        btn_mes_actual.clicked.connect(lambda: self.establecer_periodo('mes'))
        layout_atajos.addWidget(btn_mes_actual)
        
        btn_trimestre = QPushButton("Trimestre")
        btn_trimestre.clicked.connect(lambda: self.establecer_periodo('trimestre'))
        layout_atajos.addWidget(btn_trimestre)
        
        btn_año = QPushButton("Año")
        btn_año.clicked.connect(lambda: self.establecer_periodo('año'))
        layout_atajos.addWidget(btn_año)
        
        layout_periodo.addLayout(layout_atajos)
        
        layout_config.addWidget(grupo_periodo)
        
        # Secciones a incluir
        grupo_secciones = QGroupBox("Secciones a Incluir")
        layout_secciones = QVBoxLayout(grupo_secciones)
        
        self.check_portada = QCheckBox("Portada")
        self.check_portada.setChecked(True)
        layout_secciones.addWidget(self.check_portada)
        
        self.check_indice = QCheckBox("Índice")
        self.check_indice.setChecked(True)
        layout_secciones.addWidget(self.check_indice)
        
        self.check_resumen = QCheckBox("Resumen Ejecutivo")
        self.check_resumen.setChecked(True)
        layout_secciones.addWidget(self.check_resumen)
        
        self.check_graficos = QCheckBox("Gráficos y Visualizaciones")
        self.check_graficos.setChecked(True)
        layout_secciones.addWidget(self.check_graficos)
        
        self.check_tablas = QCheckBox("Tablas Detalladas")
        self.check_tablas.setChecked(True)
        layout_secciones.addWidget(self.check_tablas)
        
        self.check_conclusiones = QCheckBox("Conclusiones")
        self.check_conclusiones.setChecked(True)
        layout_secciones.addWidget(self.check_conclusiones)
        
        self.check_anexos = QCheckBox("Anexos")
        layout_secciones.addWidget(self.check_anexos)
        
        layout_config.addWidget(grupo_secciones)
        
        # Formato de salida
        grupo_formato = QGroupBox("Formato de Salida")
        layout_formato = QVBoxLayout(grupo_formato)
        
        self.combo_formato = QComboBox()
        self.combo_formato.addItems(["PDF", "Word", "Excel", "HTML", "PowerPoint"])
        layout_formato.addWidget(self.combo_formato)
        
        self.check_enviar_email = QCheckBox("Enviar por email al generar")
        layout_formato.addWidget(self.check_enviar_email)
        
        layout_config.addWidget(grupo_formato)
        
        # Panel derecho - Vista previa y datos
        panel_derecho = QWidget()
        layout_derecho = QVBoxLayout(panel_derecho)
        
        # Datos disponibles
        grupo_datos = QGroupBox("Datos Disponibles")
        layout_datos = QVBoxLayout(grupo_datos)
        
        self.tree_datos = QTreeWidget()
        self.tree_datos.setHeaderLabel("Fuentes de Datos")
        self.cargar_arbol_datos()
        layout_datos.addWidget(self.tree_datos)
        
        layout_botones_datos = QHBoxLayout()
        btn_cargar_datos = QPushButton("📁 Cargar Datos")
        btn_cargar_datos.clicked.connect(self.cargar_datos)
        layout_botones_datos.addWidget(btn_cargar_datos)
        
        btn_actualizar = QPushButton("🔄 Actualizar")
        btn_actualizar.clicked.connect(self.actualizar_datos)
        layout_botones_datos.addWidget(btn_actualizar)
        
        layout_datos.addLayout(layout_botones_datos)
        
        layout_derecho.addWidget(grupo_datos)
        
        # Vista previa
        grupo_preview = QGroupBox("Vista Previa")
        layout_preview = QVBoxLayout(grupo_preview)
        
        self.texto_preview = QTextEdit()
        self.texto_preview.setReadOnly(True)
        layout_preview.addWidget(self.texto_preview)
        
        layout_derecho.addWidget(grupo_preview)
        
        # Agregar paneles al splitter
        splitter.addWidget(panel_config)
        splitter.addWidget(panel_derecho)
        splitter.setSizes([400, 600])
        
        layout_principal.addWidget(splitter)
        
        # Barra de progreso
        self.barra_progreso = QProgressBar()
        self.barra_progreso.setVisible(False)
        layout_principal.addWidget(self.barra_progreso)
        
        # Estado
        self.lbl_estado = QLabel("Listo para generar informes")
        self.lbl_estado.setStyleSheet("color: gray;")
        layout_principal.addWidget(self.lbl_estado)
        
        # Botones de acción
        layout_acciones = QHBoxLayout()
        
        btn_plantillas = QPushButton("📋 Gestionar Plantillas")
        btn_plantillas.clicked.connect(self.gestionar_plantillas)
        layout_acciones.addWidget(btn_plantillas)
        
        btn_programar = QPushButton("⏰ Programar Generación")
        btn_programar.clicked.connect(self.programar_generacion)
        layout_acciones.addWidget(btn_programar)
        
        btn_historial = QPushButton("📚 Ver Historial")
        btn_historial.clicked.connect(self.ver_historial)
        layout_acciones.addWidget(btn_historial)
        
        layout_acciones.addStretch()
        
        btn_preview = QPushButton("👁️ Actualizar Vista Previa")
        btn_preview.clicked.connect(self.actualizar_vista_previa)
        layout_acciones.addWidget(btn_preview)
        
        btn_generar = QPushButton("📄 Generar Informe")
        btn_generar.clicked.connect(self.generar_informe)
        btn_generar.setStyleSheet("background-color: #4CAF50; font-weight: bold; padding: 8px 16px;")
        layout_acciones.addWidget(btn_generar)
        
        layout_principal.addLayout(layout_acciones)
        
        # Cargar datos de ejemplo
        self.cargar_datos_ejemplo()
        
    def cambiar_tipo_informe(self):
        """Actualiza la configuración según el tipo de informe"""
        self.actualizar_descripcion()
        self.actualizar_secciones_disponibles()
        self.actualizar_vista_previa()
        
    def actualizar_descripcion(self):
        """Actualiza la descripción del tipo de informe"""
        descripciones = {
            "Resumen Ejecutivo": "Informe conciso con los puntos clave y métricas principales para la dirección.",
            "Análisis Detallado": "Análisis completo con todos los datos, gráficos y tablas detalladas.",
            "Comparativo Mensual": "Comparación mes a mes de los principales indicadores salariales.",
            "Informe Anual": "Resumen anual completo con evolución, tendencias y proyecciones.",
            "Análisis de Costes": "Desglose detallado de costes laborales por departamento y concepto.",
            "Informe de Equidad": "Análisis de equidad salarial y cumplimiento de políticas.",
            "Dashboard Gerencial": "Panel visual con KPIs y métricas clave para toma de decisiones.",
            "Personalizado": "Configure su propio informe seleccionando las secciones deseadas."
        }
        
        tipo = self.combo_tipo_informe.currentText()
        self.texto_descripcion.setText(descripciones.get(tipo, ""))
        
    def actualizar_secciones_disponibles(self):
        """Habilita/deshabilita secciones según el tipo de informe"""
        tipo = self.combo_tipo_informe.currentText()
        
        if tipo == "Resumen Ejecutivo":
            self.check_portada.setChecked(True)
            self.check_indice.setChecked(False)
            self.check_resumen.setChecked(True)
            self.check_graficos.setChecked(True)
            self.check_tablas.setChecked(False)
            self.check_conclusiones.setChecked(True)
            self.check_anexos.setChecked(False)
            
        elif tipo == "Análisis Detallado":
            # Marcar todas las secciones
            for check in [self.check_portada, self.check_indice, self.check_resumen,
                         self.check_graficos, self.check_tablas, self.check_conclusiones,
                         self.check_anexos]:
                check.setChecked(True)
                
        elif tipo == "Dashboard Gerencial":
            self.check_portada.setChecked(False)
            self.check_indice.setChecked(False)
            self.check_resumen.setChecked(False)
            self.check_graficos.setChecked(True)
            self.check_tablas.setChecked(False)
            self.check_conclusiones.setChecked(False)
            self.check_anexos.setChecked(False)
            
    def establecer_periodo(self, periodo):
        """Establece el período según el atajo seleccionado"""
        fecha_actual = QDate.currentDate()
        
        if periodo == 'mes':
            self.date_desde.setDate(QDate(fecha_actual.year(), fecha_actual.month(), 1))
            self.date_hasta.setDate(fecha_actual)
            
        elif periodo == 'trimestre':
            mes_trimestre = ((fecha_actual.month() - 1) // 3) * 3 + 1
            self.date_desde.setDate(QDate(fecha_actual.year(), mes_trimestre, 1))
            self.date_hasta.setDate(fecha_actual)
            
        elif periodo == 'año':
            self.date_desde.setDate(QDate(fecha_actual.year(), 1, 1))
            self.date_hasta.setDate(fecha_actual)
            
    def cargar_arbol_datos(self):
        """Carga el árbol de fuentes de datos disponibles"""
        self.tree_datos.clear()
        
        # Nóminas
        item_nominas = QTreeWidgetItem(self.tree_datos, ["📊 Nóminas"])
        QTreeWidgetItem(item_nominas, ["12 archivos cargados"])
        QTreeWidgetItem(item_nominas, ["Período: Ene 2024 - Dic 2024"])
        
        # Empleados
        item_empleados = QTreeWidgetItem(self.tree_datos, ["👥 Empleados"])
        QTreeWidgetItem(item_empleados, ["Total: 45 empleados"])
        QTreeWidgetItem(item_empleados, ["5 departamentos"])
        
        # Calendario
        item_calendario = QTreeWidgetItem(self.tree_datos, ["📅 Calendario Laboral"])
        QTreeWidgetItem(item_calendario, ["Año 2024 configurado"])
        QTreeWidgetItem(item_calendario, ["14 festivos"])
        
        # Configuración
        item_config = QTreeWidgetItem(self.tree_datos, ["⚙️ Configuración"])
        QTreeWidgetItem(item_config, ["Pagas extras: 2"])
        QTreeWidgetItem(item_config, ["Incrementos: 3%"])
        
        self.tree_datos.expandAll()
        
    def cargar_datos(self):
        """Carga datos para el informe"""
        archivo, _ = QFileDialog.getOpenFileName(
            self,
            'Cargar datos',
            '',
            'Excel (*.xlsx *.xls);;CSV (*.csv);;JSON (*.json)'
        )
        
        if archivo:
            # Aquí se cargarían los datos reales
            QMessageBox.information(
                self,
                "Datos cargados",
                f"Se han cargado los datos desde:\n{archivo}"
            )
            
            self.cargar_arbol_datos()
            
    def actualizar_datos(self):
        """Actualiza los datos disponibles"""
        self.cargar_arbol_datos()
        self.lbl_estado.setText("Datos actualizados")
        
    def cargar_datos_ejemplo(self):
        """Carga datos de ejemplo para demostración"""
        # Simular datos cargados
        self.datos_disponibles = {
            'nominas': self.generar_datos_nominas_ejemplo(),
            'empleados': self.generar_datos_empleados_ejemplo(),
            'departamentos': ['Ventas', 'Administración', 'IT', 'Producción', 'RRHH']
        }
        
    def generar_datos_nominas_ejemplo(self):
        """Genera datos de nóminas de ejemplo"""
        datos = []
        fecha_base = datetime.now() - timedelta(days=365)
        
        for i in range(12):
            fecha = fecha_base + timedelta(days=30*i)
            datos.append({
                'fecha': fecha,
                'mes': fecha.strftime('%B %Y'),
                'total_devengos': 95000 + np.random.normal(0, 5000),
                'total_deducciones': 19000 + np.random.normal(0, 1000),
                'liquido_total': 76000 + np.random.normal(0, 4000),
                'num_empleados': 45
            })
            
        return datos
        
    def generar_datos_empleados_ejemplo(self):
        """Genera datos de empleados de ejemplo"""
        departamentos = ['Ventas', 'Administración', 'IT', 'Producción', 'RRHH']
        empleados = []
        
        for i in range(45):
            empleados.append({
                'id': i + 1,
                'nombre': f'Empleado {i + 1}',
                'departamento': np.random.choice(departamentos),
                'salario_base': 1500 + np.random.randint(0, 2000),
                'antiguedad': np.random.randint(0, 15)
            })
            
        return empleados
        
    def actualizar_vista_previa(self):
        """Actualiza la vista previa del informe"""
        tipo = self.combo_tipo_informe.currentText()
        
        # Generar estructura del informe
        estructura = f"<h2>Vista Previa: {tipo}</h2>\n"
        estructura += f"<p><b>Período:</b> {self.date_desde.date().toString('dd/MM/yyyy')} - "
        estructura += f"{self.date_hasta.date().toString('dd/MM/yyyy')}</p>\n"
        estructura += "<hr>\n"
        
        estructura += "<h3>Contenido del Informe:</h3>\n<ol>\n"
        
        if self.check_portada.isChecked():
            estructura += "<li>Portada</li>\n"
            
        if self.check_indice.isChecked():
            estructura += "<li>Índice</li>\n"
            
        if self.check_resumen.isChecked():
            estructura += "<li>Resumen Ejecutivo\n<ul>\n"
            estructura += "<li>Indicadores clave</li>\n"
            estructura += "<li>Principales hallazgos</li>\n"
            estructura += "<li>Recomendaciones</li>\n"
            estructura += "</ul></li>\n"
            
        if self.check_graficos.isChecked():
            estructura += "<li>Gráficos y Visualizaciones\n<ul>\n"
            estructura += "<li>Evolución temporal</li>\n"
            estructura += "<li>Distribución por departamento</li>\n"
            estructura += "<li>Análisis de tendencias</li>\n"
            estructura += "</ul></li>\n"
            
        if self.check_tablas.isChecked():
            estructura += "<li>Tablas Detalladas\n<ul>\n"
            estructura += "<li>Desglose por empleado</li>\n"
            estructura += "<li>Comparativas mensuales</li>\n"
            estructura += "<li>Resumen de conceptos</li>\n"
            estructura += "</ul></li>\n"
            
        if self.check_conclusiones.isChecked():
            estructura += "<li>Conclusiones y Recomendaciones</li>\n"
            
        if self.check_anexos.isChecked():
            estructura += "<li>Anexos\n<ul>\n"
            estructura += "<li>Datos fuente</li>\n"
            estructura += "<li>Metodología</li>\n"
            estructura += "<li>Glosario</li>\n"
            estructura += "</ul></li>\n"
            
        estructura += "</ol>\n"
        
        # Estadísticas
        estructura += "<hr>\n<h3>Estadísticas del Informe:</h3>\n"
        estructura += f"<p>• Páginas estimadas: {self.estimar_paginas()}</p>\n"
        estructura += f"<p>• Gráficos: {self.contar_graficos()}</p>\n"
        estructura += f"<p>• Tablas: {self.contar_tablas()}</p>\n"
        estructura += f"<p>• Formato: {self.combo_formato.currentText()}</p>\n"
        
        self.texto_preview.setHtml(estructura)
        
    def estimar_paginas(self):
        """Estima el número de páginas del informe"""
        paginas = 0
        
        if self.check_portada.isChecked():
            paginas += 1
        if self.check_indice.isChecked():
            paginas += 1
        if self.check_resumen.isChecked():
            paginas += 2
        if self.check_graficos.isChecked():
            paginas += 4
        if self.check_tablas.isChecked():
            paginas += 3
        if self.check_conclusiones.isChecked():
            paginas += 1
        if self.check_anexos.isChecked():
            paginas += 2
            
        return paginas
        
    def contar_graficos(self):
        """Cuenta el número de gráficos a incluir"""
        if not self.check_graficos.isChecked():
            return 0
            
        tipo = self.combo_tipo_informe.currentText()
        
        graficos = {
            "Resumen Ejecutivo": 3,
            "Análisis Detallado": 8,
            "Comparativo Mensual": 5,
            "Informe Anual": 10,
            "Análisis de Costes": 6,
            "Dashboard Gerencial": 12,
            "Personalizado": 4
        }
        
        return graficos.get(tipo, 4)
        
    def contar_tablas(self):
        """Cuenta el número de tablas a incluir"""
        if not self.check_tablas.isChecked():
            return 0
            
        tipo = self.combo_tipo_informe.currentText()
        
        tablas = {
            "Resumen Ejecutivo": 2,
            "Análisis Detallado": 6,
            "Comparativo Mensual": 4,
            "Informe Anual": 8,
            "Análisis de Costes": 5,
            "Dashboard Gerencial": 1,
            "Personalizado": 3
        }
        
        return tablas.get(tipo, 3)
        
    def generar_informe(self):
        """Genera el informe con la configuración actual"""
        # Validar datos
        if not self.datos_disponibles:
            QMessageBox.warning(
                self,
                "Sin datos",
                "No hay datos cargados para generar el informe."
            )
            return
            
        # Confirmar generación
        tipo = self.combo_tipo_informe.currentText()
        formato = self.combo_formato.currentText()
        
        respuesta = QMessageBox.question(
            self,
            "Confirmar generación",
            f"¿Desea generar el informe '{tipo}' en formato {formato}?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.Yes
        )
        
        if respuesta == QMessageBox.No:
            return
            
        # Preparar configuración
        configuracion = {
            'tipo': tipo,
            'formato': formato,
            'periodo': {
                'desde': self.date_desde.date(),
                'hasta': self.date_hasta.date()
            },
            'secciones': {
                'portada': self.check_portada.isChecked(),
                'indice': self.check_indice.isChecked(),
                'resumen': self.check_resumen.isChecked(),
                'graficos': self.check_graficos.isChecked(),
                'tablas': self.check_tablas.isChecked(),
                'conclusiones': self.check_conclusiones.isChecked(),
                'anexos': self.check_anexos.isChecked()
            }
        }
        
        # Mostrar barra de progreso
        self.barra_progreso.setVisible(True)
        self.barra_progreso.setValue(0)
        
        # Crear thread para generar el informe
        self.thread_generador = GeneradorInformeThread(
            tipo,
            configuracion,
            self.datos_disponibles
        )
        
        self.thread_generador.progreso.connect(self.actualizar_progreso)
        self.thread_generador.estado.connect(self.actualizar_estado)
        self.thread_generador.completado.connect(self.informe_generado)
        self.thread_generador.error.connect(self.error_generacion)
        
        self.thread_generador.start()
        
    def actualizar_progreso(self, valor):
        """Actualiza la barra de progreso"""
        self.barra_progreso.setValue(valor)
        
    def actualizar_estado(self, mensaje):
        """Actualiza el mensaje de estado"""
        self.lbl_estado.setText(mensaje)
        
    def informe_generado(self, archivo):
        """Maneja cuando el informe se ha generado exitosamente"""
        self.barra_progreso.setVisible(False)
        self.lbl_estado.setText("Informe generado exitosamente")
        
        # Si está marcado enviar por email
        if self.check_enviar_email.isChecked():
            self.enviar_informe_email(archivo)
        else:
            # Preguntar si desea abrir el archivo
            respuesta = QMessageBox.question(
                self,
                "Informe generado",
                f"El informe se ha generado correctamente.\n\n{archivo}\n\n¿Desea abrirlo ahora?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.Yes
            )
            
            if respuesta == QMessageBox.Yes:
                os.startfile(archivo)
                
    def error_generacion(self, mensaje_error):
        """Maneja errores en la generación"""
        self.barra_progreso.setVisible(False)
        self.lbl_estado.setText("Error al generar el informe")
        
        QMessageBox.critical(
            self,
            "Error",
            f"Error al generar el informe:\n\n{mensaje_error}"
        )
        
    def enviar_informe_email(self, archivo):
        """Envía el informe por email"""
        from PyQt5.QtWidgets import QDialog, QFormLayout, QLineEdit, QDialogButtonBox
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Enviar Informe por Email")
        dialog.setModal(True)
        
        layout = QFormLayout(dialog)
        
        input_destinatario = QLineEdit()
        layout.addRow("Destinatario:", input_destinatario)
        
        input_asunto = QLineEdit(f"Informe {self.combo_tipo_informe.currentText()}")
        layout.addRow("Asunto:", input_asunto)
        
        input_mensaje = QTextEdit()
        input_mensaje.setPlainText(
            f"Adjunto el informe '{self.combo_tipo_informe.currentText()}' "
            f"correspondiente al período {self.date_desde.date().toString('dd/MM/yyyy')} - "
            f"{self.date_hasta.date().toString('dd/MM/yyyy')}.\n\n"
            "Saludos cordiales."
        )
        layout.addRow("Mensaje:", input_mensaje)
        
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, dialog
        )
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addRow(buttons)
        
        if dialog.exec_() == QDialog.Accepted:
            # Aquí se implementaría el envío real del email
            QMessageBox.information(
                self,
                "Email enviado",
                f"El informe se ha enviado correctamente a:\n{input_destinatario.text()}"
            )
            
    def gestionar_plantillas(self):
        """Abre el gestor de plantillas de informes"""
        from PyQt5.QtWidgets import QDialog, QListWidget, QListWidgetItem
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Gestionar Plantillas de Informes")
        dialog.setModal(True)
        dialog.resize(600, 400)
        
        layout = QVBoxLayout(dialog)
        
        # Lista de plantillas
        lista = QListWidget()
        
        plantillas_ejemplo = [
            "Informe Mensual Estándar",
            "Reporte Ejecutivo Trimestral",
            "Análisis Anual Completo",
            "Dashboard KPIs Mensuales",
            "Informe de Costes Departamental"
        ]
        
        for plantilla in plantillas_ejemplo:
            item = QListWidgetItem(f"📄 {plantilla}")
            lista.addItem(item)
            
        layout.addWidget(lista)
        
        # Botones
        layout_botones = QHBoxLayout()
        
        btn_nueva = QPushButton("➕ Nueva Plantilla")
        layout_botones.addWidget(btn_nueva)
        
        btn_editar = QPushButton("✏️ Editar")
        layout_botones.addWidget(btn_editar)
        
        btn_eliminar = QPushButton("❌ Eliminar")
        layout_botones.addWidget(btn_eliminar)
        
        btn_duplicar = QPushButton("📋 Duplicar")
        layout_botones.addWidget(btn_duplicar)
        
        layout_botones.addStretch()
        
        btn_cerrar = QPushButton("Cerrar")
        btn_cerrar.clicked.connect(dialog.accept)
        layout_botones.addWidget(btn_cerrar)
        
        layout.addLayout(layout_botones)
        
        dialog.exec_()
        
    def programar_generacion(self):
        """Programa la generación automática de informes"""
        from PyQt5.QtWidgets import QDialog, QTimeEdit, QSpinBox
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Programar Generación Automática")
        dialog.setModal(True)
        
        layout = QVBoxLayout(dialog)
        
        # Frecuencia
        layout_frecuencia = QHBoxLayout()
        layout_frecuencia.addWidget(QLabel("Generar informe:"))
        
        combo_frecuencia = QComboBox()
        combo_frecuencia.addItems([
            "Diariamente",
            "Semanalmente",
            "Mensualmente",
            "Trimestralmente",
            "Anualmente"
        ])
        layout_frecuencia.addWidget(combo_frecuencia)
        
        layout.addLayout(layout_frecuencia)
        
        # Día específico
        layout_dia = QHBoxLayout()
        layout_dia.addWidget(QLabel("Día del mes:"))
        
        spin_dia = QSpinBox()
        spin_dia.setRange(1, 31)
        spin_dia.setValue(1)
        layout_dia.addWidget(spin_dia)
        
        layout.addLayout(layout_dia)
        
        # Hora
        layout_hora = QHBoxLayout()
        layout_hora.addWidget(QLabel("Hora:"))
        
        time_hora = QTimeEdit()
        time_hora.setDisplayFormat("HH:mm")
        layout_hora.addWidget(time_hora)
        
        layout.addLayout(layout_hora)
        
        # Opciones adicionales
        check_email = QCheckBox("Enviar automáticamente por email")
        layout.addWidget(check_email)
        
        check_archivo = QCheckBox("Guardar en carpeta compartida")
        layout.addWidget(check_archivo)
        
        # Botones
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, dialog
        )
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)
        
        if dialog.exec_() == QDialog.Accepted:
            QMessageBox.information(
                self,
                "Programación guardada",
                f"Se ha programado la generación automática del informe "
                f"{combo_frecuencia.currentText().lower()}."
            )
            
    def ver_historial(self):
        """Muestra el historial de informes generados"""
        from PyQt5.QtWidgets import QDialog, QTableWidget
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Historial de Informes")
        dialog.setModal(True)
        dialog.resize(800, 400)
        
        layout = QVBoxLayout(dialog)
        
        # Tabla de historial
        tabla = QTableWidget()
        tabla.setColumnCount(5)
        tabla.setHorizontalHeaderLabels([
            'Fecha', 'Tipo', 'Período', 'Formato', 'Estado'
        ])
        
        # Datos de ejemplo
        historial = [
            ('25/01/2025 10:30', 'Resumen Ejecutivo', 'Enero 2025', 'PDF', '✅ Completado'),
            ('01/01/2025 09:00', 'Informe Anual', 'Año 2024', 'Excel', '✅ Completado'),
            ('15/12/2024 14:15', 'Comparativo Mensual', 'Dic 2024', 'Word', '✅ Completado'),
            ('01/12/2024 08:00', 'Análisis de Costes', 'Nov 2024', 'PDF', '✅ Completado'),
            ('15/11/2024 11:30', 'Dashboard Gerencial', 'Nov 2024', 'HTML', '❌ Error')
        ]
        
        tabla.setRowCount(len(historial))
        
        for i, (fecha, tipo, periodo, formato, estado) in enumerate(historial):
            tabla.setItem(i, 0, QTableWidgetItem(fecha))
            tabla.setItem(i, 1, QTableWidgetItem(tipo))
            tabla.setItem(i, 2, QTableWidgetItem(periodo))
            tabla.setItem(i, 3, QTableWidgetItem(formato))
            
            item_estado = QTableWidgetItem(estado)
            if '✅' in estado:
                item_estado.setBackground(QColor(200, 230, 201))
            else:
                item_estado.setBackground(QColor(255, 205, 210))
            tabla.setItem(i, 4, item_estado)
            
        layout.addWidget(tabla)
        
        # Botones
        layout_botones = QHBoxLayout()
        
        btn_abrir = QPushButton("📄 Abrir")
        layout_botones.addWidget(btn_abrir)
        
        btn_reenviar = QPushButton("📧 Reenviar")
        layout_botones.addWidget(btn_reenviar)
        
        btn_eliminar = QPushButton("🗑️ Eliminar")
        layout_botones.addWidget(btn_eliminar)
        
        layout_botones.addStretch()
        
        btn_cerrar = QPushButton("Cerrar")
        btn_cerrar.clicked.connect(dialog.accept)
        layout_botones.addWidget(btn_cerrar)
        
        layout.addLayout(layout_botones)
        
        dialog.exec_()