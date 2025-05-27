# 💰 Comparador de Nóminas

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![PyQt5](https://img.shields.io/badge/PyQt5-5.15+-green.svg)](https://pypi.org/project/PyQt5/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Software profesional para Windows 11 que permite comparar nóminas, saldos y tiempos de nómina. Facilita la detección de errores, análisis de desviaciones y predicción de nóminas futuras.

## 🚀 Características Principales

- ✅ **Comparación automática** de nóminas, saldos y tiempos
- 📅 **Calendario laboral** personalizable
- 💰 **Cálculo de precio por hora** y desglose de pluses
- 🔮 **Predicción de nóminas** basada en el calendario laboral
- 📈 **Gestión de incrementos salariales** y pagas extras
- 👥 **Comparación entre nóminas** de diferentes empleados
- 📊 **Visualizaciones gráficas** y generación de informes
- ✏️ **Entrada manual de datos** para simulaciones

## 📸 Capturas de Pantalla

![Interfaz Principal](assets/screenshots/main_interface.png)
*Interfaz principal del programa*

![Comparación de Nóminas](assets/screenshots/comparison.png)
*Módulo de comparación de nóminas*

## 🛠️ Requisitos del Sistema

- **Sistema Operativo**: Windows 11 (compatible con Windows 10)
- **Python**: 3.8 o superior
- **Memoria RAM**: 4GB mínimo (8GB recomendado)
- **Espacio en disco**: 200MB

## 📦 Instalación

### Opción 1: Ejecutar desde el código fuente

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/TU_USUARIO/comparador-nominas.git
   cd comparador-nominas
   ```

2. **Crear entorno virtual** (recomendado)
   ```bash
   python -m venv venv
   
   # En Windows
   venv\Scripts\activate
   
   # En Linux/Mac
   source venv/bin/activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Ejecutar el programa**
   ```bash
   python src/interfaz_usuario.py
   ```

### Opción 2: Usar el instalador (Windows)

1. Descarga el instalador desde [Releases](https://github.com/TU_USUARIO/comparador-nominas/releases)
2. Ejecuta `ComparadorNominas_Setup.exe`
3. Sigue las instrucciones del instalador

## 🎮 Uso Básico

### 1. Importar Nóminas
- Haz clic en "📁 Cargar Nóminas"
- Selecciona archivos PDF o Excel
- El programa extraerá automáticamente los datos

### 2. Comparar Nóminas
- Selecciona el tipo de comparación
- Ajusta el umbral de desviación
- Haz clic en "🔍 Comparar"

### 3. Generar Informes
- Ve a la pestaña "📋 Informes"
- Selecciona el tipo de informe
- Configura el período
- Haz clic en "📄 Generar Informe"

## 🔧 Configuración

### Calendario Laboral
1. Ve a la pestaña "📅 Calendario"
2. Configura festivos nacionales y locales
3. Añade tus períodos de vacaciones
4. Guarda la configuración

### Pagas Extras
1. Ve a la pestaña "💸 Pagas Extras"
2. Elige entre 12 o 14 pagas
3. Configura las fechas de pago
4. Simula diferentes escenarios

## 📚 Documentación

- [Guía de Usuario](docs/guia_usuario.md) - Manual completo para usuarios
- [Documentación Técnica](docs/documentacion_tecnica.md) - Para desarrolladores
- [Ejemplos](ejemplos/) - Archivos de ejemplo para pruebas

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Por favor:

1. Fork el proyecto
2. Crea tu rama de características (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 🐛 Reportar Problemas

Si encuentras algún problema, por favor [abre un issue](https://github.com/TU_USUARIO/comparador-nominas/issues) con:
- Descripción detallada del problema
- Pasos para reproducirlo
- Capturas de pantalla (si aplica)
- Versión del programa y sistema operativo

## 📝 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## 👨‍💻 Autor

**Tu Nombre**
- GitHub: [@TU_USUARIO](https://github.com/TU_USUARIO)
- LinkedIn: [Tu Perfil](https://linkedin.com/in/tu-perfil)

## 🙏 Agradecimientos

- Gracias a todos los que han contribuido al proyecto
- Iconos por [Font Awesome](https://fontawesome.com)
- Framework UI por [PyQt5](https://www.riverbankcomputing.com/software/pyqt/)

---

⭐ Si te gusta este proyecto, ¡dale una estrella en GitHub!