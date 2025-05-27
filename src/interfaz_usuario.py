import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QPushButton, QLabel, QMenuBar, QMenu,
                            QAction, QStatusBar, QTabWidget, QMessageBox,
                            QFileDialog, QSplitter)
from PyQt5.QtCore import Qt, QSettings
from PyQt5.QtGui import QIcon, QFont

# Importar los módulos del programa
from implementacion_comparacion import ComparacionWidget
from implementacion_precio_hora import PrecioHoraWidget
from implementacion_prediccion_nomina import PrediccionNominaWidget
from implementacion_calendario_laboral import CalendarioLaboralWidget
from implementacion_incrementos_salariales import IncrementosSalarialesWidget
from implementacion_pagas_extras import PagasExtrasWidget
from implementacion_comparacion_nominas_empleados import ComparacionEmpleadosWidget
from implementacion_visualizaciones_graficas import VisualizacionesWidget
from implementacion_entrada_manual_datos import EntradaManualWidget
from implementacion_informes_personalizados import InformesWidget

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings = QSettings('ComparadorNominas', 'MainWindow')
        self.initUI()
        self.cargar_configuracion()
        
    def initUI(self):
        # Configuración de la ventana principal
        self.setWindowTitle('Comparador de Nóminas - Versión 1.0')
        self.setGeometry(100, 100, 1400, 800)
        
        # Widget central
        widget_central = QWidget()
        self.setCentralWidget(widget_central)
        
        # Layout principal
        layout_principal = QVBoxLayout(widget_central)
        
        # Crear el widget de pestañas
        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.West)
        
        # Crear las pestañas para cada módulo
        self.crear_pestanas()
        
        # Añadir las pestañas al layout principal
        layout_principal.addWidget(self.tabs)
        
        # Crear menú
        self.crear_menu()
        
        # Crear barra de estado
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage('Listo para trabajar')
        
        # Aplicar estilos
        self.aplicar_estilos()
        
    def crear_pestanas(self):
        """Crea todas las pestañas del programa"""
        # Pestaña de Comparación
        self.comparacion_widget = ComparacionWidget()
        self.tabs.addTab(self.comparacion_widget, "📊 Comparación")
        
        # Pestaña de Precio por Hora
        self.precio_hora_widget = PrecioHoraWidget()
        self.tabs.addTab(self.precio_hora_widget, "💰 Precio/Hora")
        
        # Pestaña de Predicción
        self.prediccion_widget = PrediccionNominaWidget()
        self.tabs.addTab(self.prediccion_widget, "🔮 Predicción")
        
        # Pestaña de Calendario Laboral
        self.calendario_widget = CalendarioLaboralWidget()
        self.tabs.addTab(self.calendario_widget, "📅 Calendario")
        
        # Pestaña de Incrementos Salariales
        self.incrementos_widget = IncrementosSalarialesWidget()
        self.tabs.addTab(self.incrementos_widget, "📈 Incrementos")
        
        # Pestaña de Pagas Extras
        self.pagas_extras_widget = PagasExtrasWidget()
        self.tabs.addTab(self.pagas_extras_widget, "💸 Pagas Extras")
        
        # Pestaña de Comparación entre Empleados
        self.comparacion_empleados_widget = ComparacionEmpleadosWidget()
        self.tabs.addTab(self.comparacion_empleados_widget, "👥 Comparar Empleados")
        
        # Pestaña de Visualizaciones
        self.visualizaciones_widget = VisualizacionesWidget()
        self.tabs.addTab(self.visualizaciones_widget, "📈 Gráficos")
        
        # Pestaña de Entrada Manual
        self.entrada_manual_widget = EntradaManualWidget()
        self.tabs.addTab(self.entrada_manual_widget, "✏️ Entrada Manual")
        
        # Pestaña de Informes
        self.informes_widget = InformesWidget()
        self.tabs.addTab(self.informes_widget, "📋 Informes")
        
    def crear_menu(self):
        """Crea el menú de la aplicación"""
        menubar = self.menuBar()
        
        # Menú Archivo
        menu_archivo = menubar.addMenu('&Archivo')
        
        # Acción Abrir
        accion_abrir = QAction('&Abrir archivos...', self)
        accion_abrir.setShortcut('Ctrl+O')
        accion_abrir.setStatusTip('Abrir archivos de nóminas')
        accion_abrir.triggered.connect(self.abrir_archivos)
        menu_archivo.addAction(accion_abrir)
        
        # Acción Guardar
        accion_guardar = QAction('&Guardar proyecto', self)
        accion_guardar.setShortcut('Ctrl+S')
        accion_guardar.setStatusTip('Guardar proyecto actual')
        accion_guardar.triggered.connect(self.guardar_proyecto)
        menu_archivo.addAction(accion_guardar)
        
        menu_archivo.addSeparator()
        
        # Acción Salir
        accion_salir = QAction('&Salir', self)
        accion_salir.setShortcut('Ctrl+Q')
        accion_salir.setStatusTip('Salir de la aplicación')
        accion_salir.triggered.connect(self.close)
        menu_archivo.addAction(accion_salir)
        
        # Menú Herramientas
        menu_herramientas = menubar.addMenu('&Herramientas')
        
        # Acción Configuración
        accion_configuracion = QAction('&Configuración', self)
        accion_configuracion.setStatusTip('Configurar la aplicación')
        accion_configuracion.triggered.connect(self.mostrar_configuracion)
        menu_herramientas.addAction(accion_configuracion)
        
        # Acción Limpiar datos
        accion_limpiar = QAction('&Limpiar datos', self)
        accion_limpiar.setStatusTip('Limpiar todos los datos cargados')
        accion_limpiar.triggered.connect(self.limpiar_datos)
        menu_herramientas.addAction(accion_limpiar)
        
        # Menú Ayuda
        menu_ayuda = menubar.addMenu('A&yuda')
        
        # Acción Manual de Usuario
        accion_manual = QAction('&Manual de Usuario', self)
        accion_manual.setShortcut('F1')
        accion_manual.setStatusTip('Ver el manual de usuario')
        accion_manual.triggered.connect(self.mostrar_manual)
        menu_ayuda.addAction(accion_manual)
        
        # Acción Acerca de
        accion_acerca = QAction('&Acerca de...', self)
        accion_acerca.setStatusTip('Información sobre la aplicación')
        accion_acerca.triggered.connect(self.mostrar_acerca_de)
        menu_ayuda.addAction(accion_acerca)
        
    def aplicar_estilos(self):
        """Aplica estilos CSS a la aplicación"""
        estilo = """
        QMainWindow {
            background-color: #f5f5f5;
        }
        
        QTabWidget::pane {
            border: 1px solid #cccccc;
            background-color: white;
        }
        
        QTabWidget::tab-bar {
            alignment: left;
        }
        
        QTabBar::tab {
            background-color: #e0e0e0;
            padding: 10px 20px;
            margin: 2px;
            border-radius: 4px;
            min-height: 40px;
            font-size: 12px;
        }
        
        QTabBar::tab:selected {
            background-color: #4CAF50;
            color: white;
            font-weight: bold;
        }
        
        QTabBar::tab:hover {
            background-color: #45a049;
            color: white;
        }
        
        QPushButton {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: bold;
        }
        
        QPushButton:hover {
            background-color: #45a049;
        }
        
        QPushButton:pressed {
            background-color: #3d8b40;
        }
        
        QStatusBar {
            background-color: #333333;
            color: white;
            font-size: 12px;
        }
        
        QMenuBar {
            background-color: #333333;
            color: white;
        }
        
        QMenuBar::item:selected {
            background-color: #4CAF50;
        }
        
        QMenu {
            background-color: white;
            border: 1px solid #cccccc;
        }
        
        QMenu::item:selected {
            background-color: #4CAF50;
            color: white;
        }
        """
        self.setStyleSheet(estilo)
        
    def abrir_archivos(self):
        """Abre archivos de nóminas"""
        archivos, _ = QFileDialog.getOpenFileNames(
            self, 
            'Abrir archivos de nóminas',
            '',
            'Archivos soportados (*.pdf *.xlsx *.xls);;PDF (*.pdf);;Excel (*.xlsx *.xls)'
        )
        
        if archivos:
            self.statusBar.showMessage(f'Cargando {len(archivos)} archivos...')
            # Aquí se procesarían los archivos
            # Por ahora solo mostramos un mensaje
            QMessageBox.information(
                self,
                'Archivos cargados',
                f'Se han seleccionado {len(archivos)} archivos para procesar.'
            )
            self.statusBar.showMessage('Archivos cargados correctamente')
            
    def guardar_proyecto(self):
        """Guarda el proyecto actual"""
        archivo, _ = QFileDialog.getSaveFileName(
            self,
            'Guardar proyecto',
            '',
            'Proyecto Comparador (*.cmp)'
        )
        
        if archivo:
            # Aquí se guardaría el proyecto
            self.statusBar.showMessage('Proyecto guardado correctamente')
            
    def mostrar_configuracion(self):
        """Muestra la ventana de configuración"""
        QMessageBox.information(
            self,
            'Configuración',
            'Ventana de configuración en desarrollo...'
        )
        
    def limpiar_datos(self):
        """Limpia todos los datos cargados"""
        respuesta = QMessageBox.question(
            self,
            'Confirmar limpieza',
            '¿Está seguro de que desea limpiar todos los datos cargados?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if respuesta == QMessageBox.Yes:
            # Aquí se limpiarían los datos
            self.statusBar.showMessage('Datos limpiados')
            
    def mostrar_manual(self):
        """Muestra el manual de usuario"""
        # Intentar abrir el archivo de documentación
        doc_path = os.path.join('docs', 'guia_usuario.md')
        if os.path.exists(doc_path):
            os.startfile(doc_path)
        else:
            QMessageBox.information(
                self,
                'Manual de Usuario',
                'El manual de usuario no está disponible.\nPor favor, consulte la documentación en línea.'
            )
            
    def mostrar_acerca_de(self):
        """Muestra información sobre la aplicación"""
        QMessageBox.about(
            self,
            'Acerca de Comparador de Nóminas',
            '<h2>Comparador de Nóminas</h2>'
            '<p>Versión 1.0</p>'
            '<p>Software para comparar nóminas, saldos y tiempos de nómina.</p>'
            '<p>Facilita la detección de errores, análisis de desviaciones '
            'y predicción de nóminas futuras.</p>'
            '<br>'
            '<p>© 2024 - Todos los derechos reservados</p>'
        )
        
    def cargar_configuracion(self):
        """Carga la configuración guardada"""
        # Restaurar geometría de la ventana
        geometry = self.settings.value('geometry')
        if geometry:
            self.restoreGeometry(geometry)
            
    def closeEvent(self, event):
        """Evento al cerrar la aplicación"""
        # Guardar configuración
        self.settings.setValue('geometry', self.saveGeometry())
        
        # Confirmar salida
        respuesta = QMessageBox.question(
            self,
            'Confirmar salida',
            '¿Está seguro de que desea salir?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if respuesta == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

def main():
    app = QApplication(sys.argv)
    app.setApplicationName('Comparador de Nóminas')
    app.setOrganizationName('ComparadorNominas')
    
    # Configurar el icono de la aplicación si existe
    if os.path.exists('icon.ico'):
        app.setWindowIcon(QIcon('icon.ico'))
    
    ventana = VentanaPrincipal()
    ventana.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()