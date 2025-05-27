import pandas as pd
import numpy as np
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                            QTableWidget, QTableWidgetItem, QLabel, QComboBox,
                            QGroupBox, QCalendarWidget, QListWidget, QLineEdit,
                            QMessageBox, QFileDialog, QTextEdit, QCheckBox,
                            QSpinBox, QDateEdit, QDialog, QDialogButtonBox,
                            QFormLayout, QListWidgetItem, QSplitter)
from PyQt5.QtCore import Qt, QDate, QDateTime, pyqtSignal
from PyQt5.QtGui import QColor, QFont, QTextCharFormat, QBrush
from datetime import datetime, timedelta
import calendar
import json

class CalendarioLaboralWidget(QWidget):
    # Señal para notificar cambios en el calendario
    calendario_actualizado = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        self.festivos = {}
        self.vacaciones = []
        self.turnos = {}
        self.jornada_laboral = {
            'lunes': 8, 'martes': 8, 'miércoles': 8, 
            'jueves': 8, 'viernes': 8, 'sábado': 0, 'domingo': 0
        }
        self.initUI()
        
    def initUI(self):
        layout_principal = QVBoxLayout(self)
        
        # Splitter principal
        splitter = QSplitter(Qt.Horizontal)
        
        # Panel izquierdo - Calendario
        panel_calendario = QWidget()
        layout_calendario = QVBoxLayout(panel_calendario)
        
        # Controles del calendario
        layout_controles = QHBoxLayout()
        
        self.combo_year = QComboBox()
        years = list(range(2020, 2031))
        self.combo_year.addItems([str(y) for y in years])
        self.combo_year.setCurrentText(str(datetime.now().year))
        self.combo_year.currentTextChanged.connect(self.actualizar_vista_calendario)
        layout_controles.addWidget(QLabel("Año:"))
        layout_controles.addWidget(self.combo_year)
        
        layout_controles.addStretch()
        
        btn_festivos_nacionales = QPushButton("🏛️ Cargar Festivos Nacionales")
        btn_festivos_nacionales.clicked.connect(self.cargar_festivos_nacionales)
        layout_controles.addWidget(btn_festivos_nacionales)
        
        layout_calendario.addLayout(layout_controles)
        
        # Widget del calendario
        self.calendario = QCalendarWidget()
        self.calendario.setMinimumHeight(300)
        self.calendario.clicked.connect(self.fecha_seleccionada)
        layout_calendario.addWidget(self.calendario)
        
        # Leyenda
        layout_leyenda = QHBoxLayout()
        
        leyendas = [
            ("⬜", "Laborable", QColor(255, 255, 255)),
            ("🟥", "Festivo", QColor(255, 200, 200)),
            ("🟦", "Vacaciones", QColor(200, 200, 255)),
            ("🟨", "Turno especial", QColor(255, 255, 200))
        ]
        
        for simbolo, texto, color in leyendas:
            lbl_simbolo = QLabel(simbolo)
            lbl_simbolo.setStyleSheet(f"background-color: {color.name()}; padding: 5px;")
            layout_leyenda.addWidget(lbl_simbolo)
            layout_leyenda.addWidget(QLabel(texto))
            layout_leyenda.addStretch()
            
        layout_calendario.addLayout(layout_leyenda)
        
        # Panel derecho - Configuración
        panel_config = QWidget()
        layout_config = QVBoxLayout(panel_config)
        
        # Pestañas de configuración
        from PyQt5.QtWidgets import QTabWidget
        self.tabs_config = QTabWidget()
        
        # Tab 1: Festivos
        self.tab_festivos = QWidget()
        self.setup_tab_festivos()
        self.tabs_config.addTab(self.tab_festivos, "🎉 Festivos")
        
        # Tab 2: Vacaciones
        self.tab_vacaciones = QWidget()
        self.setup_tab_vacaciones()
        self.tabs_config.addTab(self.tab_vacaciones, "🏖️ Vacaciones")
        
        # Tab 3: Turnos
        self.tab_turnos = QWidget()
        self.setup_tab_turnos()
        self.tabs_config.addTab(self.tab_turnos, "📅 Turnos")
        
        # Tab 4: Jornada
        self.tab_jornada = QWidget()
        self.setup_tab_jornada()
        self.tabs_config.addTab(self.tab_jornada, "⏰ Jornada")
        
        layout_config.addWidget(self.tabs_config)
        
        # Agregar paneles al splitter
        splitter.addWidget(panel_calendario)
        splitter.addWidget(panel_config)
        splitter.setSizes([500, 500])
        
        layout_principal.addWidget(splitter)
        
        # Panel inferior - Resumen
        panel_resumen = QGroupBox("Resumen del Calendario")
        layout_resumen = QVBoxLayout(panel_resumen)
        
        self.texto_resumen = QTextEdit()
        self.texto_resumen.setMaximumHeight(100)
        self.texto_resumen.setReadOnly(True)
        layout_resumen.addWidget(self.texto_resumen)
        
        layout_principal.addWidget(panel_resumen)
        
        # Botones de acción
        layout_acciones = QHBoxLayout()
        
        btn_exportar = QPushButton("📊 Exportar Calendario")
        btn_exportar.clicked.connect(self.exportar_calendario)
        layout_acciones.addWidget(btn_exportar)
        
        btn_importar = QPushButton("📁 Importar Calendario")
        btn_importar.clicked.connect(self.importar_calendario)
        layout_acciones.addWidget(btn_importar)
        
        btn_calcular_horas = QPushButton("🧮 Calcular Horas Mes")
        btn_calcular_horas.clicked.connect(self.calcular_horas_mes)
        layout_acciones.addWidget(btn_calcular_horas)
        
        layout_acciones.addStretch()
        
        btn_limpiar = QPushButton("🗑️ Limpiar Todo")
        btn_limpiar.clicked.connect(self.limpiar_calendario)
        layout_acciones.addWidget(btn_limpiar)
        
        layout_principal.addLayout(layout_acciones)
        
        # Actualizar vista inicial
        self.actualizar_vista_calendario()
        self.actualizar_resumen()
        
    def setup_tab_festivos(self):
        """Configura la pestaña de festivos"""
        layout = QVBoxLayout(self.tab_festivos)
        
        # Botones de gestión
        layout_botones = QHBoxLayout()
        
        btn_agregar = QPushButton("➕ Agregar Festivo")
        btn_agregar.clicked.connect(self.agregar_festivo)
        layout_botones.addWidget(btn_agregar)
        
        btn_eliminar = QPushButton("❌ Eliminar Seleccionado")
        btn_eliminar.clicked.connect(self.eliminar_festivo)
        layout_botones.addWidget(btn_eliminar)
        
        layout_botones.addStretch()
        layout.addLayout(layout_botones)
        
        # Lista de festivos
        self.lista_festivos = QListWidget()
        layout.addWidget(self.lista_festivos)
        
        # Opciones de festivos predefinidos
        layout_predefinidos = QHBoxLayout()
        
        btn_festivos_comunidad = QPushButton("🏛️ Festivos Comunidad")
        btn_festivos_comunidad.clicked.connect(self.cargar_festivos_comunidad)
        layout_predefinidos.addWidget(btn_festivos_comunidad)
        
        btn_festivos_locales = QPushButton("🏘️ Festivos Locales")
        btn_festivos_locales.clicked.connect(self.cargar_festivos_locales)
        layout_predefinidos.addWidget(btn_festivos_locales)
        
        layout.addLayout(layout_predefinidos)
        
    def setup_tab_vacaciones(self):
        """Configura la pestaña de vacaciones"""
        layout = QVBoxLayout(self.tab_vacaciones)
        
        # Información de días disponibles
        layout_info = QHBoxLayout()
        
        layout_info.addWidget(QLabel("Días totales:"))
        self.spin_dias_totales = QSpinBox()
        self.spin_dias_totales.setRange(0, 50)
        self.spin_dias_totales.setValue(22)
        layout_info.addWidget(self.spin_dias_totales)
        
        layout_info.addWidget(QLabel("Días usados:"))
        self.lbl_dias_usados = QLabel("0")
        self.lbl_dias_usados.setStyleSheet("font-weight: bold; color: #2196F3;")
        layout_info.addWidget(self.lbl_dias_usados)
        
        layout_info.addWidget(QLabel("Días restantes:"))
        self.lbl_dias_restantes = QLabel("22")
        self.lbl_dias_restantes.setStyleSheet("font-weight: bold; color: #4CAF50;")
        layout_info.addWidget(self.lbl_dias_restantes)
        
        layout_info.addStretch()
        layout.addLayout(layout_info)
        
        # Botones de gestión
        layout_botones = QHBoxLayout()
        
        btn_agregar_periodo = QPushButton("➕ Agregar Periodo")
        btn_agregar_periodo.clicked.connect(self.agregar_periodo_vacaciones)
        layout_botones.addWidget(btn_agregar_periodo)
        
        btn_eliminar_periodo = QPushButton("❌ Eliminar Seleccionado")
        btn_eliminar_periodo.clicked.connect(self.eliminar_periodo_vacaciones)
        layout_botones.addWidget(btn_eliminar_periodo)
        
        layout_botones.addStretch()
        layout.addLayout(layout_botones)
        
        # Lista de periodos de vacaciones
        self.lista_vacaciones = QListWidget()
        layout.addWidget(self.lista_vacaciones)
        
        # Sugerencias
        btn_sugerir_vacaciones = QPushButton("💡 Sugerir Mejores Fechas")
        btn_sugerir_vacaciones.clicked.connect(self.sugerir_vacaciones)
        layout.addWidget(btn_sugerir_vacaciones)
        
    def setup_tab_turnos(self):
        """Configura la pestaña de turnos"""
        layout = QVBoxLayout(self.tab_turnos)
        
        # Configuración de turnos
        layout_config = QHBoxLayout()
        
        layout_config.addWidget(QLabel("Tipo de turno:"))
        self.combo_tipo_turno = QComboBox()
        self.combo_tipo_turno.addItems([
            "Turno fijo",
            "Turno rotativo 2x2",
            "Turno rotativo 3x3",
            "Turno personalizado"
        ])
        layout_config.addWidget(self.combo_tipo_turno)
        
        btn_aplicar_turno = QPushButton("✅ Aplicar Turno")
        btn_aplicar_turno.clicked.connect(self.aplicar_turno)
        layout_config.addWidget(btn_aplicar_turno)
        
        layout_config.addStretch()
        layout.addLayout(layout_config)
        
        # Tabla de turnos
        self.tabla_turnos = QTableWidget()
        self.tabla_turnos.setColumnCount(3)
        self.tabla_turnos.setHorizontalHeaderLabels(['Semana', 'Turno', 'Horas'])
        layout.addWidget(self.tabla_turnos)
        
        # Panel de turno personalizado
        self.panel_turno_personalizado = QGroupBox("Configurar Turno Personalizado")
        layout_personalizado = QVBoxLayout(self.panel_turno_personalizado)
        
        # Aquí se pueden agregar controles para configurar turnos personalizados
        layout_personalizado.addWidget(QLabel("Configure los días y horarios del turno"))
        
        self.panel_turno_personalizado.setVisible(False)
        layout.addWidget(self.panel_turno_personalizado)
        
        self.combo_tipo_turno.currentTextChanged.connect(
            lambda t: self.panel_turno_personalizado.setVisible(t == "Turno personalizado")
        )
        
    def setup_tab_jornada(self):
        """Configura la pestaña de jornada laboral"""
        layout = QVBoxLayout(self.tab_jornada)
        
        # Jornada semanal
        group_semanal = QGroupBox("Jornada Semanal")
        layout_semanal = QVBoxLayout(group_semanal)
        
        self.spinboxes_jornada = {}
        dias_semana = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
        
        for dia in dias_semana:
            layout_dia = QHBoxLayout()
            layout_dia.addWidget(QLabel(f"{dia}:"))
            
            spin = QSpinBox()
            spin.setRange(0, 24)
            spin.setValue(self.jornada_laboral.get(dia.lower(), 0))
            spin.valueChanged.connect(self.actualizar_resumen_jornada)
            self.spinboxes_jornada[dia.lower()] = spin
            layout_dia.addWidget(spin)
            
            layout_dia.addWidget(QLabel("horas"))
            layout_dia.addStretch()
            
            layout_semanal.addLayout(layout_dia)
            
        layout.addWidget(group_semanal)
        
        # Resumen jornada
        group_resumen = QGroupBox("Resumen")
        layout_resumen_jornada = QVBoxLayout(group_resumen)
        
        self.lbl_horas_semanales = QLabel("Horas semanales: 40")
        self.lbl_horas_semanales.setFont(QFont('Arial', 12, QFont.Bold))
        layout_resumen_jornada.addWidget(self.lbl_horas_semanales)
        
        self.lbl_horas_mensuales = QLabel("Horas mensuales (aprox): 173")
        layout_resumen_jornada.addWidget(self.lbl_horas_mensuales)
        
        self.lbl_horas_anuales = QLabel("Horas anuales (aprox): 2080")
        layout_resumen_jornada.addWidget(self.lbl_horas_anuales)
        
        layout.addWidget(group_resumen)
        
        # Plantillas de jornada
        layout_plantillas = QHBoxLayout()
        
        btn_jornada_completa = QPushButton("Jornada Completa (40h)")
        btn_jornada_completa.clicked.connect(lambda: self.aplicar_plantilla_jornada('completa'))
        layout_plantillas.addWidget(btn_jornada_completa)
        
        btn_media_jornada = QPushButton("Media Jornada (20h)")
        btn_media_jornada.clicked.connect(lambda: self.aplicar_plantilla_jornada('media'))
        layout_plantillas.addWidget(btn_media_jornada)
        
        btn_jornada_intensiva = QPushButton("Jornada Intensiva")
        btn_jornada_intensiva.clicked.connect(lambda: self.aplicar_plantilla_jornada('intensiva'))
        layout_plantillas.addWidget(btn_jornada_intensiva)
        
        layout.addLayout(layout_plantillas)
        
        layout.addStretch()
        
        # Actualizar resumen inicial
        self.actualizar_resumen_jornada()
        
    def fecha_seleccionada(self, date):
        """Maneja la selección de una fecha en el calendario"""
        fecha_str = date.toString("yyyy-MM-dd")
        
        # Mostrar información de la fecha seleccionada
        info = f"Fecha seleccionada: {date.toString('dd/MM/yyyy')}\n"
        
        if fecha_str in self.festivos:
            info += f"Festivo: {self.festivos[fecha_str]}\n"
            
        # Verificar si es vacaciones
        for periodo in self.vacaciones:
            inicio = QDate.fromString(periodo['inicio'], "yyyy-MM-dd")
            fin = QDate.fromString(periodo['fin'], "yyyy-MM-dd")
            if inicio <= date <= fin:
                info += f"Vacaciones: {periodo['descripcion']}\n"
                break
                
        # Verificar día de la semana
        dia_semana = date.dayOfWeek()
        dias = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
        info += f"Día: {dias[dia_semana-1]}\n"
        
        # Horas de trabajo
        horas = self.jornada_laboral.get(dias[dia_semana-1].lower(), 0)
        info += f"Horas laborables: {horas}\n"
        
        QMessageBox.information(self, "Información del día", info)
        
    def agregar_festivo(self):
        """Agrega un nuevo festivo"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Agregar Festivo")
        dialog.setModal(True)
        
        layout = QFormLayout(dialog)
        
        # Fecha
        date_edit = QDateEdit()
        date_edit.setCalendarPopup(True)
        date_edit.setDate(QDate.currentDate())
        layout.addRow("Fecha:", date_edit)
        
        # Descripción
        input_descripcion = QLineEdit()
        layout.addRow("Descripción:", input_descripcion)
        
        # Tipo
        combo_tipo = QComboBox()
        combo_tipo.addItems(["Nacional", "Autonómico", "Local", "Empresa"])
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
            fecha = date_edit.date()
            fecha_str = fecha.toString("yyyy-MM-dd")
            descripcion = input_descripcion.text()
            tipo = combo_tipo.currentText()
            
            if descripcion:
                self.festivos[fecha_str] = descripcion
                
                # Agregar a la lista
                item_text = f"{fecha.toString('dd/MM/yyyy')} - {descripcion} ({tipo})"
                self.lista_festivos.addItem(item_text)
                
                # Actualizar calendario
                self.actualizar_vista_calendario()
                self.actualizar_resumen()
                
                # Emitir señal
                self.calendario_actualizado.emit(self.obtener_datos_calendario())
            else:
                QMessageBox.warning(self, "Error", "Debe especificar una descripción")
                
    def eliminar_festivo(self):
        """Elimina el festivo seleccionado"""
        item = self.lista_festivos.currentItem()
        if item:
            # Extraer fecha del texto del item
            fecha_texto = item.text().split(' - ')[0]
            fecha = QDate.fromString(fecha_texto, "dd/MM/yyyy")
            fecha_str = fecha.toString("yyyy-MM-dd")
            
            # Eliminar del diccionario
            if fecha_str in self.festivos:
                del self.festivos[fecha_str]
                
            # Eliminar de la lista
            self.lista_festivos.takeItem(self.lista_festivos.currentRow())
            
            # Actualizar vista
            self.actualizar_vista_calendario()
            self.actualizar_resumen()
            
    def cargar_festivos_nacionales(self):
        """Carga los festivos nacionales predefinidos"""
        año = int(self.combo_year.currentText())
        
        # Festivos nacionales de España (ejemplo)
        festivos_nacionales = {
            f"{año}-01-01": "Año Nuevo",
            f"{año}-01-06": "Reyes Magos",
            f"{año}-05-01": "Día del Trabajador",
            f"{año}-08-15": "Asunción de la Virgen",
            f"{año}-10-12": "Día de la Hispanidad",
            f"{año}-11-01": "Todos los Santos",
            f"{año}-12-06": "Día de la Constitución",
            f"{año}-12-08": "Inmaculada Concepción",
            f"{año}-12-25": "Navidad"
        }
        
        # Agregar festivos móviles (Semana Santa)
        # Aquí se podría calcular las fechas exactas de Semana Santa
        
        for fecha, descripcion in festivos_nacionales.items():
            self.festivos[fecha] = descripcion
            fecha_qdate = QDate.fromString(fecha, "yyyy-MM-dd")
            item_text = f"{fecha_qdate.toString('dd/MM/yyyy')} - {descripcion} (Nacional)"
            
            # Evitar duplicados
            items_existentes = [self.lista_festivos.item(i).text() 
                              for i in range(self.lista_festivos.count())]
            if item_text not in items_existentes:
                self.lista_festivos.addItem(item_text)
                
        self.actualizar_vista_calendario()
        self.actualizar_resumen()
        
        QMessageBox.information(
            self,
            "Festivos cargados",
            f"Se han cargado {len(festivos_nacionales)} festivos nacionales."
        )
        
    def cargar_festivos_comunidad(self):
        """Carga festivos de la comunidad autónoma"""
        # Aquí se implementaría la carga de festivos específicos de cada comunidad
        QMessageBox.information(
            self,
            "Función en desarrollo",
            "La carga de festivos por comunidad autónoma se implementará próximamente."
        )
        
    def cargar_festivos_locales(self):
        """Carga festivos locales"""
        # Aquí se implementaría la carga de festivos locales
        QMessageBox.information(
            self,
            "Función en desarrollo",
            "La carga de festivos locales se implementará próximamente."
        )
        
    def agregar_periodo_vacaciones(self):
        """Agrega un periodo de vacaciones"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Agregar Periodo de Vacaciones")
        dialog.setModal(True)
        
        layout = QFormLayout(dialog)
        
        # Fecha inicio
        date_inicio = QDateEdit()
        date_inicio.setCalendarPopup(True)
        date_inicio.setDate(QDate.currentDate())
        layout.addRow("Fecha inicio:", date_inicio)
        
        # Fecha fin
        date_fin = QDateEdit()
        date_fin.setCalendarPopup(True)
        date_fin.setDate(QDate.currentDate().addDays(7))
        layout.addRow("Fecha fin:", date_fin)
        
        # Descripción
        input_descripcion = QLineEdit("Vacaciones")
        layout.addRow("Descripción:", input_descripcion)
        
        # Botones
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, dialog
        )
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addRow(buttons)
        
        if dialog.exec_() == QDialog.Accepted:
            inicio = date_inicio.date()
            fin = date_fin.date()
            
            if inicio > fin:
                QMessageBox.warning(self, "Error", "La fecha de inicio debe ser anterior a la de fin")
                return
                
            # Calcular días
            dias = inicio.daysTo(fin) + 1
            
            # Verificar días disponibles
            dias_usados = sum(p['dias'] for p in self.vacaciones)
            dias_totales = self.spin_dias_totales.value()
            
            if dias_usados + dias > dias_totales:
                QMessageBox.warning(
                    self,
                    "Sin días suficientes",
                    f"No hay suficientes días de vacaciones.\n"
                    f"Disponibles: {dias_totales - dias_usados}\n"
                    f"Solicitados: {dias}"
                )
                return
                
            periodo = {
                'inicio': inicio.toString("yyyy-MM-dd"),
                'fin': fin.toString("yyyy-MM-dd"),
                'dias': dias,
                'descripcion': input_descripcion.text()
            }
            
            self.vacaciones.append(periodo)
            
            # Agregar a la lista
            item_text = f"{inicio.toString('dd/MM/yyyy')} - {fin.toString('dd/MM/yyyy')} ({dias} días)"
            self.lista_vacaciones.addItem(item_text)
            
            # Actualizar contadores
            self.actualizar_contador_vacaciones()
            self.actualizar_vista_calendario()
            self.actualizar_resumen()
            
    def eliminar_periodo_vacaciones(self):
        """Elimina el periodo de vacaciones seleccionado"""
        row = self.lista_vacaciones.currentRow()
        if row >= 0:
            # Eliminar de la lista de datos
            del self.vacaciones[row]
            
            # Eliminar de la lista visual
            self.lista_vacaciones.takeItem(row)
            
            # Actualizar todo
            self.actualizar_contador_vacaciones()
            self.actualizar_vista_calendario()
            self.actualizar_resumen()
            
    def actualizar_contador_vacaciones(self):
        """Actualiza el contador de días de vacaciones"""
        dias_usados = sum(p['dias'] for p in self.vacaciones)
        dias_totales = self.spin_dias_totales.value()
        dias_restantes = dias_totales - dias_usados
        
        self.lbl_dias_usados.setText(str(dias_usados))
        self.lbl_dias_restantes.setText(str(dias_restantes))
        
        # Cambiar color si no quedan días
        if dias_restantes < 0:
            self.lbl_dias_restantes.setStyleSheet("font-weight: bold; color: #f44336;")
        elif dias_restantes < 5:
            self.lbl_dias_restantes.setStyleSheet("font-weight: bold; color: #ff9800;")
        else:
            self.lbl_dias_restantes.setStyleSheet("font-weight: bold; color: #4CAF50;")
            
    def sugerir_vacaciones(self):
        """Sugiere las mejores fechas para vacaciones"""
        año = int(self.combo_year.currentText())
        
        # Buscar puentes y periodos óptimos
        sugerencias = []
        
        # Analizar festivos para encontrar puentes
        for fecha_str, descripcion in self.festivos.items():
            fecha = QDate.fromString(fecha_str, "yyyy-MM-dd")
            dia_semana = fecha.dayOfWeek()
            
            # Si es martes o jueves, sugerir puente
            if dia_semana == 2:  # Martes
                sugerencias.append({
                    'inicio': fecha.addDays(-1),
                    'fin': fecha,
                    'dias': 2,
                    'motivo': f"Puente de {descripcion} (Lunes-Martes)"
                })
            elif dia_semana == 4:  # Jueves
                sugerencias.append({
                    'inicio': fecha,
                    'fin': fecha.addDays(1),
                    'dias': 2,
                    'motivo': f"Puente de {descripcion} (Jueves-Viernes)"
                })
                
        # Mostrar sugerencias
        if sugerencias:
            mensaje = "Sugerencias de vacaciones para optimizar puentes:\n\n"
            for sug in sugerencias[:5]:  # Mostrar máximo 5 sugerencias
                mensaje += f"• {sug['inicio'].toString('dd/MM')} - {sug['fin'].toString('dd/MM')}: "
                mensaje += f"{sug['motivo']} ({sug['dias']} días)\n"
                
            QMessageBox.information(self, "Sugerencias de Vacaciones", mensaje)
        else:
            QMessageBox.information(
                self,
                "Sin sugerencias",
                "No se encontraron oportunidades de puentes para este año."
            )
            
    def aplicar_turno(self):
        """Aplica el turno seleccionado"""
        tipo_turno = self.combo_tipo_turno.currentText()
        
        # Aquí se implementaría la lógica de turnos
        QMessageBox.information(
            self,
            "Función en desarrollo",
            f"La aplicación de turnos '{tipo_turno}' se implementará próximamente."
        )
        
    def actualizar_resumen_jornada(self):
        """Actualiza el resumen de la jornada laboral"""
        # Calcular horas semanales
        horas_semanales = sum(spin.value() for spin in self.spinboxes_jornada.values())
        
        # Actualizar jornada_laboral
        for dia, spin in self.spinboxes_jornada.items():
            self.jornada_laboral[dia] = spin.value()
            
        # Calcular aproximaciones
        horas_mensuales = horas_semanales * 4.33
        horas_anuales = horas_semanales * 52
        
        # Actualizar labels
        self.lbl_horas_semanales.setText(f"Horas semanales: {horas_semanales}")
        self.lbl_horas_mensuales.setText(f"Horas mensuales (aprox): {horas_mensuales:.0f}")
        self.lbl_horas_anuales.setText(f"Horas anuales (aprox): {horas_anuales:.0f}")
        
        # Actualizar resumen general
        self.actualizar_resumen()
        
    def aplicar_plantilla_jornada(self, tipo):
        """Aplica una plantilla de jornada predefinida"""
        plantillas = {
            'completa': {
                'lunes': 8, 'martes': 8, 'miércoles': 8,
                'jueves': 8, 'viernes': 8, 'sábado': 0, 'domingo': 0
            },
            'media': {
                'lunes': 4, 'martes': 4, 'miércoles': 4,
                'jueves': 4, 'viernes': 4, 'sábado': 0, 'domingo': 0
            },
            'intensiva': {
                'lunes': 7, 'martes': 7, 'miércoles': 7,
                'jueves': 7, 'viernes': 7, 'sábado': 0, 'domingo': 0
            }
        }
        
        if tipo in plantillas:
            for dia, horas in plantillas[tipo].items():
                self.spinboxes_jornada[dia].setValue(horas)
                
    def actualizar_vista_calendario(self):
        """Actualiza la vista del calendario con los festivos y vacaciones"""
        # Limpiar formato
        self.calendario.setDateTextFormat(QDate(), QTextCharFormat())
        
        # Formato para festivos
        formato_festivo = QTextCharFormat()
        formato_festivo.setBackground(QBrush(QColor(255, 200, 200)))
        
        # Formato para vacaciones
        formato_vacaciones = QTextCharFormat()
        formato_vacaciones.setBackground(QBrush(QColor(200, 200, 255)))
        
        # Aplicar formato a festivos
        for fecha_str in self.festivos:
            fecha = QDate.fromString(fecha_str, "yyyy-MM-dd")
            self.calendario.setDateTextFormat(fecha, formato_festivo)
            
        # Aplicar formato a vacaciones
        for periodo in self.vacaciones:
            inicio = QDate.fromString(periodo['inicio'], "yyyy-MM-dd")
            fin = QDate.fromString(periodo['fin'], "yyyy-MM-dd")
            
            fecha_actual = inicio
            while fecha_actual <= fin:
                self.calendario.setDateTextFormat(fecha_actual, formato_vacaciones)
                fecha_actual = fecha_actual.addDays(1)
                
    def actualizar_resumen(self):
        """Actualiza el resumen del calendario"""
        año = int(self.combo_year.currentText())
        
        # Calcular estadísticas
        total_festivos = len([f for f in self.festivos if f.startswith(str(año))])
        total_dias_vacaciones = sum(p['dias'] for p in self.vacaciones 
                                   if p['inicio'].startswith(str(año)))
        
        # Calcular días y horas laborables del año
        dias_laborables = 0
        horas_laborables = 0
        
        fecha = QDate(año, 1, 1)
        while fecha.year() == año:
            fecha_str = fecha.toString("yyyy-MM-dd")
            dia_semana = fecha.dayOfWeek()
            
            # Verificar si es laborable
            es_laborable = True
            
            # Verificar si es festivo
            if fecha_str in self.festivos:
                es_laborable = False
                
            # Verificar si es vacaciones
            for periodo in self.vacaciones:
                inicio = QDate.fromString(periodo['inicio'], "yyyy-MM-dd")
                fin = QDate.fromString(periodo['fin'], "yyyy-MM-dd")
                if inicio <= fecha <= fin:
                    es_laborable = False
                    break
                    
            # Si es laborable, sumar días y horas
            if es_laborable:
                dias_semana_nombres = ['lunes', 'martes', 'miércoles', 'jueves', 
                                      'viernes', 'sábado', 'domingo']
                horas_dia = self.jornada_laboral.get(dias_semana_nombres[dia_semana-1], 0)
                if horas_dia > 0:
                    dias_laborables += 1
                    horas_laborables += horas_dia
                    
            fecha = fecha.addDays(1)
            
        # Crear resumen
        resumen = f"=== RESUMEN CALENDARIO {año} ===\n\n"
        resumen += f"Días laborables: {dias_laborables}\n"
        resumen += f"Horas laborables totales: {horas_laborables}\n"
        resumen += f"Festivos: {total_festivos}\n"
        resumen += f"Días de vacaciones: {total_dias_vacaciones}\n"
        resumen += f"Promedio horas/mes: {horas_laborables/12:.1f}\n"
        
        self.texto_resumen.setText(resumen)
        
    def calcular_horas_mes(self):
        """Calcula las horas laborables del mes actual"""
        fecha_actual = self.calendario.selectedDate()
        if not fecha_actual.isValid():
            fecha_actual = QDate.currentDate()
            
        mes = fecha_actual.month()
        año = fecha_actual.year()
        
        # Calcular días y horas del mes
        dias_laborables = 0
        horas_laborables = 0
        festivos_mes = []
        vacaciones_mes = []
        
        # Iterar por todos los días del mes
        dias_en_mes = calendar.monthrange(año, mes)[1]
        
        for dia in range(1, dias_en_mes + 1):
            fecha = QDate(año, mes, dia)
            fecha_str = fecha.toString("yyyy-MM-dd")
            dia_semana = fecha.dayOfWeek()
            
            # Verificar si es laborable
            es_laborable = True
            
            # Verificar festivos
            if fecha_str in self.festivos:
                es_laborable = False
                festivos_mes.append(f"{dia:02d} - {self.festivos[fecha_str]}")
                
            # Verificar vacaciones
            for periodo in self.vacaciones:
                inicio = QDate.fromString(periodo['inicio'], "yyyy-MM-dd")
                fin = QDate.fromString(periodo['fin'], "yyyy-MM-dd")
                if inicio <= fecha <= fin:
                    es_laborable = False
                    if periodo['descripcion'] not in vacaciones_mes:
                        vacaciones_mes.append(periodo['descripcion'])
                    break
                    
            # Si es laborable, calcular horas
            if es_laborable:
                dias_semana_nombres = ['lunes', 'martes', 'miércoles', 'jueves', 
                                      'viernes', 'sábado', 'domingo']
                horas_dia = self.jornada_laboral.get(dias_semana_nombres[dia_semana-1], 0)
                if horas_dia > 0:
                    dias_laborables += 1
                    horas_laborables += horas_dia
                    
        # Mostrar resultado
        meses_nombres = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
                        'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
        
        mensaje = f"=== CÁLCULO DE HORAS - {meses_nombres[mes-1].upper()} {año} ===\n\n"
        mensaje += f"Días laborables: {dias_laborables}\n"
        mensaje += f"Horas laborables: {horas_laborables}\n\n"
        
        if festivos_mes:
            mensaje += "Festivos:\n"
            for festivo in festivos_mes:
                mensaje += f"  • {festivo}\n"
            mensaje += "\n"
            
        if vacaciones_mes:
            mensaje += "Vacaciones:\n"
            for vacacion in vacaciones_mes:
                mensaje += f"  • {vacacion}\n"
                
        QMessageBox.information(self, "Cálculo de Horas del Mes", mensaje)
        
    def exportar_calendario(self):
        """Exporta el calendario a un archivo"""
        archivo, _ = QFileDialog.getSaveFileName(
            self,
            'Exportar calendario',
            f'calendario_{self.combo_year.currentText()}.json',
            'JSON (*.json);;Excel (*.xlsx)'
        )
        
        if archivo:
            if archivo.endswith('.json'):
                self.exportar_json(archivo)
            elif archivo.endswith('.xlsx'):
                self.exportar_excel(archivo)
                
    def exportar_json(self, archivo):
        """Exporta el calendario a JSON"""
        try:
            datos = {
                'año': self.combo_year.currentText(),
                'festivos': self.festivos,
                'vacaciones': self.vacaciones,
                'jornada_laboral': self.jornada_laboral,
                'turnos': self.turnos
            }
            
            with open(archivo, 'w', encoding='utf-8') as f:
                json.dump(datos, f, ensure_ascii=False, indent=2)
                
            QMessageBox.information(
                self,
                'Exportación exitosa',
                f'El calendario se ha exportado correctamente a:\n{archivo}'
            )
            
        except Exception as e:
            QMessageBox.critical(
                self,
                'Error al exportar',
                f'Error al exportar el calendario:\n{str(e)}'
            )
            
    def exportar_excel(self, archivo):
        """Exporta el calendario a Excel"""
        try:
            # Crear DataFrames
            # Festivos
            festivos_data = []
            for fecha_str, descripcion in self.festivos.items():
                fecha = QDate.fromString(fecha_str, "yyyy-MM-dd")
                festivos_data.append({
                    'Fecha': fecha.toString('dd/MM/yyyy'),
                    'Descripción': descripcion,
                    'Día Semana': fecha.toString('dddd')
                })
            df_festivos = pd.DataFrame(festivos_data)
            
            # Vacaciones
            vacaciones_data = []
            for periodo in self.vacaciones:
                vacaciones_data.append({
                    'Inicio': QDate.fromString(periodo['inicio'], "yyyy-MM-dd").toString('dd/MM/yyyy'),
                    'Fin': QDate.fromString(periodo['fin'], "yyyy-MM-dd").toString('dd/MM/yyyy'),
                    'Días': periodo['dias'],
                    'Descripción': periodo['descripcion']
                })
            df_vacaciones = pd.DataFrame(vacaciones_data)
            
            # Jornada laboral
            jornada_data = []
            for dia, horas in self.jornada_laboral.items():
                jornada_data.append({
                    'Día': dia.capitalize(),
                    'Horas': horas
                })
            df_jornada = pd.DataFrame(jornada_data)
            
            # Resumen anual
            año = int(self.combo_year.currentText())
            resumen_mensual = []
            
            for mes in range(1, 13):
                dias_mes = calendar.monthrange(año, mes)[1]
                dias_laborables = 0
                horas_mes = 0
                
                for dia in range(1, dias_mes + 1):
                    fecha = QDate(año, mes, dia)
                    fecha_str = fecha.toString("yyyy-MM-dd")
                    
                    if fecha_str not in self.festivos:
                        es_vacaciones = False
                        for periodo in self.vacaciones:
                            inicio = QDate.fromString(periodo['inicio'], "yyyy-MM-dd")
                            fin = QDate.fromString(periodo['fin'], "yyyy-MM-dd")
                            if inicio <= fecha <= fin:
                                es_vacaciones = True
                                break
                                
                        if not es_vacaciones:
                            dia_semana = fecha.dayOfWeek()
                            dias_nombres = ['lunes', 'martes', 'miércoles', 'jueves',
                                          'viernes', 'sábado', 'domingo']
                            horas = self.jornada_laboral.get(dias_nombres[dia_semana-1], 0)
                            if horas > 0:
                                dias_laborables += 1
                                horas_mes += horas
                                
                meses_nombres = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
                               'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
                
                resumen_mensual.append({
                    'Mes': meses_nombres[mes-1],
                    'Días Laborables': dias_laborables,
                    'Horas Laborables': horas_mes
                })
                
            df_resumen = pd.DataFrame(resumen_mensual)
            
            # Guardar en Excel
            with pd.ExcelWriter(archivo, engine='openpyxl') as writer:
                df_resumen.to_excel(writer, sheet_name='Resumen', index=False)
                df_festivos.to_excel(writer, sheet_name='Festivos', index=False)
                df_vacaciones.to_excel(writer, sheet_name='Vacaciones', index=False)
                df_jornada.to_excel(writer, sheet_name='Jornada', index=False)
                
            QMessageBox.information(
                self,
                'Exportación exitosa',
                f'El calendario se ha exportado correctamente a:\n{archivo}'
            )
            
        except Exception as e:
            QMessageBox.critical(
                self,
                'Error al exportar',
                f'Error al exportar el calendario:\n{str(e)}'
            )
            
    def importar_calendario(self):
        """Importa un calendario desde archivo"""
        archivo, _ = QFileDialog.getOpenFileName(
            self,
            'Importar calendario',
            '',
            'JSON (*.json)'
        )
        
        if archivo:
            try:
                with open(archivo, 'r', encoding='utf-8') as f:
                    datos = json.load(f)
                    
                # Cargar datos
                self.festivos = datos.get('festivos', {})
                self.vacaciones = datos.get('vacaciones', [])
                self.jornada_laboral = datos.get('jornada_laboral', self.jornada_laboral)
                self.turnos = datos.get('turnos', {})
                
                # Actualizar año si es necesario
                año_importado = datos.get('año', str(datetime.now().year))
                index = self.combo_year.findText(año_importado)
                if index >= 0:
                    self.combo_year.setCurrentIndex(index)
                    
                # Actualizar listas y controles
                self.actualizar_listas()
                self.actualizar_controles_jornada()
                self.actualizar_vista_calendario()
                self.actualizar_resumen()
                
                QMessageBox.information(
                    self,
                    'Importación exitosa',
                    'El calendario se ha importado correctamente.'
                )
                
            except Exception as e:
                QMessageBox.critical(
                    self,
                    'Error al importar',
                    f'Error al importar el calendario:\n{str(e)}'
                )
                
    def actualizar_listas(self):
        """Actualiza las listas de festivos y vacaciones"""
        # Limpiar listas
        self.lista_festivos.clear()
        self.lista_vacaciones.clear()
        
        # Actualizar lista de festivos
        for fecha_str, descripcion in sorted(self.festivos.items()):
            fecha = QDate.fromString(fecha_str, "yyyy-MM-dd")
            item_text = f"{fecha.toString('dd/MM/yyyy')} - {descripcion}"
            self.lista_festivos.addItem(item_text)
            
        # Actualizar lista de vacaciones
        for periodo in self.vacaciones:
            inicio = QDate.fromString(periodo['inicio'], "yyyy-MM-dd")
            fin = QDate.fromString(periodo['fin'], "yyyy-MM-dd")
            item_text = f"{inicio.toString('dd/MM/yyyy')} - {fin.toString('dd/MM/yyyy')} ({periodo['dias']} días)"
            self.lista_vacaciones.addItem(item_text)
            
        # Actualizar contador de vacaciones
        self.actualizar_contador_vacaciones()
        
    def actualizar_controles_jornada(self):
        """Actualiza los controles de jornada laboral"""
        for dia, spin in self.spinboxes_jornada.items():
            spin.setValue(self.jornada_laboral.get(dia, 0))
            
    def limpiar_calendario(self):
        """Limpia todos los datos del calendario"""
        respuesta = QMessageBox.question(
            self,
            'Confirmar limpieza',
            '¿Está seguro de que desea limpiar todo el calendario?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if respuesta == QMessageBox.Yes:
            self.festivos = {}
            self.vacaciones = []
            self.turnos = {}
            
            # Limpiar listas
            self.lista_festivos.clear()
            self.lista_vacaciones.clear()
            self.tabla_turnos.setRowCount(0)
            
            # Actualizar vistas
            self.actualizar_contador_vacaciones()
            self.actualizar_vista_calendario()
            self.actualizar_resumen()
            
            QMessageBox.information(self, 'Calendario limpiado', 'Se han eliminado todos los datos del calendario.')
            
    def obtener_datos_calendario(self):
        """Obtiene los datos del calendario para compartir con otros módulos"""
        return {
            'festivos': self.festivos,
            'vacaciones': self.vacaciones,
            'jornada_laboral': self.jornada_laboral,
            'turnos': self.turnos,
            'año': int(self.combo_year.currentText())
        }