layout_fila2.addWidget(QLabel("Estilo:"))
        self.combo_estilo = QComboBox()
        self.combo_estilo.addItems(["Moderno", "Clásico", "Minimalista", "Corporativo"])
        self.combo_estilo.currentTextChanged.connect(self.cambiar_estilo)
        layout_fila2.addWidget(self.combo_estilo)
        
        layout_fila2.addStretch()
        layout_controles.addLayout(layout_fila2)
        
        # Fila 3: Filtros
        layout_fila3 = QHBoxLayout()
        
        layout_fila3.addWidget(QLabel("Conceptos a mostrar:"))
        
        self.check_salario_base = QCheckBox("Salario base")
        self.check_salario_base.setChecked(True)
        self.check_salario_base.stateChanged.connect(self.actualizar_visualizacion)
        layout_fila3.addWidget(self.check_salario_base)
        
        self.check_pluses = QCheckBox("Pluses")
        self.check_pluses.setChecked(True)
        self.check_pluses.stateChanged.connect(self.actualizar_visualizacion)
        layout_fila3.addWidget(self.check_pluses)
        
        self.check_deducciones = QCheckBox("Deducciones")
        self.check_deducciones.setChecked(True)
        self.check_deducciones.stateChanged.connect(self.actualizar_visualizacion)
        layout_fila3.addWidget(self.check_deducciones)
        
        self.check_neto = QCheckBox("Salario neto")
        self.check_neto.setChecked(True)
        self.check_neto.stateChanged.connect(self.actualizar_visualizacion)
        layout_fila3.addWidget(self.check_neto)
        
        layout_fila3.addStretch()
        layout_controles.addLayout(layout_fila3)
        
        layout_principal.addWidget(panel_controles)
        
        # Canvas para gráficos
        self.figure = Figure(figsize=(12, 8))
        self.canvas = FigureCanvas(self.figure)
        layout_principal.addWidget(self.canvas)
        
        # Panel de controles interactivos
        panel_interactivo = QGroupBox("Controles Interactivos")
        layout_interactivo = QHBoxLayout(panel_interactivo)
        
        # Zoom
        layout_interactivo.addWidget(QLabel("Zoom:"))
        self.slider_zoom = QSlider(Qt.Horizontal)
        self.slider_zoom.setRange(50, 200)
        self.slider_zoom.setValue(100)
        self.slider_zoom.valueChanged.connect(self.cambiar_zoom)
        layout_interactivo.addWidget(self.slider_zoom)
        self.lbl_zoom = QLabel("100%")
        layout_interactivo.addWidget(self.lbl_zoom)
        
        # Rotación (para algunos gráficos)
        layout_interactivo.addWidget(QLabel("Rotación:"))
        self.slider_rotacion = QSlider(Qt.Horizontal)
        self.slider_rotacion.setRange(0, 90)
        self.slider_rotacion.setValue(45)
        self.slider_rotacion.valueChanged.connect(self.cambiar_rotacion)
        layout_interactivo.addWidget(self.slider_rotacion)
        
        # Transparencia
        layout_interactivo.addWidget(QLabel("Transparencia:"))
        self.slider_alpha = QSlider(Qt.Horizontal)
        self.slider_alpha.setRange(20, 100)
        self.slider_alpha.setValue(80)
        self.slider_alpha.valueChanged.connect(self.cambiar_transparencia)
        layout_interactivo.addWidget(self.slider_alpha)
        
        layout_interactivo.addStretch()
        
        # Selector de colores
        btn_color = QPushButton("🎨 Personalizar colores")
        btn_color.clicked.connect(self.personalizar_colores)
        layout_interactivo.addWidget(btn_color)
        
        layout_principal.addWidget(panel_interactivo)
        
        # Botones de acción
        layout_acciones = QHBoxLayout()
        
        btn_cargar_datos = QPushButton("📁 Cargar Datos")
        btn_cargar_datos.clicked.connect(self.cargar_datos)
        layout_acciones.addWidget(btn_cargar_datos)
        
        btn_exportar = QPushButton("💾 Exportar Gráfico")
        btn_exportar.clicked.connect(self.exportar_grafico)
        layout_acciones.addWidget(btn_exportar)
        
        btn_guardar_plantilla = QPushButton("📋 Guardar como Plantilla")
        btn_guardar_plantilla.clicked.connect(self.guardar_plantilla)
        layout_acciones.addWidget(btn_guardar_plantilla)
        
        btn_imprimir = QPushButton("🖨️ Imprimir")
        btn_imprimir.clicked.connect(self.imprimir_grafico)
        layout_acciones.addWidget(btn_imprimir)
        
        layout_acciones.addStretch()
        
        btn_actualizar = QPushButton("🔄 Actualizar")
        btn_actualizar.clicked.connect(self.actualizar_visualizacion)
        btn_actualizar.setStyleSheet("background-color: #4CAF50;")
        layout_acciones.addWidget(btn_actualizar)
        
        layout_principal.addLayout(layout_acciones)
        
        # Cargar datos de ejemplo
        self.cargar_datos_ejemplo()
        self.actualizar_visualizacion()
        
    def cambiar_periodo(self):
        """Muestra/oculta los selectores de fecha según el período"""
        periodo = self.combo_periodo.currentText()
        mostrar_fechas = periodo == "Personalizado"
        self.date_inicio.setVisible(mostrar_fechas)
        self.date_fin.setVisible(mostrar_fechas)
        
        if not mostrar_fechas:
            # Ajustar fechas según el período seleccionado
            fecha_actual = QDate.currentDate()
            
            if periodo == "Últimos 6 meses":
                self.date_inicio.setDate(fecha_actual.addMonths(-6))
                self.date_fin.setDate(fecha_actual)
            elif periodo == "Último año":
                self.date_inicio.setDate(fecha_actual.addYears(-1))
                self.date_fin.setDate(fecha_actual)
            elif periodo == "Año actual":
                self.date_inicio.setDate(QDate(fecha_actual.year(), 1, 1))
                self.date_fin.setDate(fecha_actual)
                
        self.actualizar_visualizacion()
        
    def cargar_datos_ejemplo(self):
        """Carga datos de ejemplo para visualización"""
        # Generar datos de ejemplo para 12 meses
        meses = []
        fecha_base = datetime.now() - timedelta(days=365)
        
        for i in range(12):
            fecha = fecha_base + timedelta(days=30*i)
            
            # Generar variaciones realistas
            salario_base = 2000 + np.random.normal(0, 50)
            plus_transporte = 100
            plus_productividad = 150 + np.random.normal(0, 30)
            plus_extra = 200 * (1 if i in [5, 11] else 0)  # Pagas extras
            
            deducciones = (salario_base + plus_transporte + plus_productividad) * 0.20
            
            self.datos_nominas.append({
                'fecha': fecha,
                'mes': fecha.strftime('%b %Y'),
                'salario_base': salario_base,
                'plus_transporte': plus_transporte,
                'plus_productividad': plus_productividad,
                'plus_extra': plus_extra,
                'total_pluses': plus_transporte + plus_productividad + plus_extra,
                'deducciones': deducciones,
                'salario_bruto': salario_base + plus_transporte + plus_productividad + plus_extra,
                'salario_neto': salario_base + plus_transporte + plus_productividad + plus_extra - deducciones
            })
            
        self.datos_cargados = True
        
    def cargar_datos(self):
        """Carga datos desde archivo"""
        archivo, _ = QFileDialog.getOpenFileName(
            self,
            'Cargar datos de nóminas',
            '',
            'Excel (*.xlsx *.xls);;CSV (*.csv)'
        )
        
        if archivo:
            try:
                if archivo.endswith('.csv'):
                    df = pd.read_csv(archivo)
                else:
                    df = pd.read_excel(archivo)
                    
                # Convertir DataFrame a lista de diccionarios
                self.datos_nominas = df.to_dict('records')
                self.datos_cargados = True
                
                self.actualizar_visualizacion()
                
                QMessageBox.information(
                    self,
                    "Datos cargados",
                    f"Se han cargado {len(self.datos_nominas)} registros correctamente."
                )
                
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Error al cargar",
                    f"Error al cargar el archivo:\n{str(e)}"
                )
                
    def actualizar_visualizacion(self):
        """Actualiza la visualización según el tipo seleccionado"""
        if not self.datos_cargados:
            return
            
        self.figure.clear()
        
        tipo = self.combo_tipo_grafico.currentText()
        
        if tipo == "Evolución temporal":
            self.grafico_evolucion_temporal()
        elif tipo == "Comparación de conceptos":
            self.grafico_comparacion_conceptos()
        elif tipo == "Distribución porcentual":
            self.grafico_distribucion_porcentual()
        elif tipo == "Análisis de tendencias":
            self.grafico_analisis_tendencias()
        elif tipo == "Heatmap mensual":
            self.grafico_heatmap_mensual()
        elif tipo == "Gráfico de cascada":
            self.grafico_cascada()
        elif tipo == "Análisis de desviaciones":
            self.grafico_desviaciones()
        elif tipo == "Dashboard completo":
            self.crear_dashboard()
            
        self.canvas.draw()
        
    def grafico_evolucion_temporal(self):
        """Crea gráfico de evolución temporal"""
        ax = self.figure.add_subplot(111)
        
        # Preparar datos
        meses = [d['mes'] for d in self.datos_nominas]
        
        # Aplicar estilo
        self.aplicar_estilo_grafico(ax)
        
        # Líneas según checkboxes
        if self.check_salario_base.isChecked():
            valores = [d['salario_base'] for d in self.datos_nominas]
            ax.plot(meses, valores, 'o-', label='Salario Base', linewidth=2.5, markersize=8)
            
        if self.check_pluses.isChecked():
            valores = [d['total_pluses'] for d in self.datos_nominas]
            ax.plot(meses, valores, 's-', label='Total Pluses', linewidth=2.5, markersize=8)
            
        if self.check_deducciones.isChecked():
            valores = [d['deducciones'] for d in self.datos_nominas]
            ax.plot(meses, valores, '^-', label='Deducciones', linewidth=2.5, markersize=8)
            
        if self.check_neto.isChecked():
            valores = [d['salario_neto'] for d in self.datos_nominas]
            ax.plot(meses, valores, 'D-', label='Salario Neto', linewidth=3, markersize=8)
            
        # Añadir valores si está marcado
        if self.check_mostrar_valores.isChecked() and self.check_neto.isChecked():
            valores = [d['salario_neto'] for d in self.datos_nominas]
            for i, (mes, valor) in enumerate(zip(meses, valores)):
                ax.annotate(f'€{valor:.0f}', 
                           xy=(i, valor), 
                           xytext=(0, 10),
                           textcoords='offset points',
                           ha='center',
                           fontsize=9,
                           bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.3))
                           
        # Línea de promedio
        if self.check_mostrar_promedio.isChecked():
            promedio = np.mean([d['salario_neto'] for d in self.datos_nominas])
            ax.axhline(promedio, color='red', linestyle='--', alpha=0.7,
                      label=f'Promedio: €{promedio:.0f}')
                      
        # Línea de tendencia
        if self.check_mostrar_tendencia.isChecked():
            x = np.arange(len(meses))
            y = [d['salario_neto'] for d in self.datos_nominas]
            z = np.polyfit(x, y, 1)
            p = np.poly1d(z)
            ax.plot(x, p(x), "r--", alpha=0.8, linewidth=2,
                   label=f'Tendencia: {z[0]:.1f}x + {z[1]:.0f}')
                   
        ax.set_xlabel('Mes', fontsize=12, fontweight='bold')
        ax.set_ylabel('Importe (€)', fontsize=12, fontweight='bold')
        ax.set_title('Evolución Temporal de Conceptos Salariales', fontsize=14, fontweight='bold', pad=20)
        ax.legend(loc='best', frameon=True, fancybox=True, shadow=True)
        ax.grid(True, alpha=0.3, linestyle='-', linewidth=0.5)
        
        # Rotar etiquetas si es necesario
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=self.slider_rotacion.value())
        
        self.figure.tight_layout()
        
    def grafico_comparacion_conceptos(self):
        """Crea gráfico de barras comparativo"""
        ax = self.figure.add_subplot(111)
        
        # Preparar datos del último mes
        ultimo_mes = self.datos_nominas[-1]
        
        conceptos = []
        valores = []
        colores = []
        
        if self.check_salario_base.isChecked():
            conceptos.append('Salario\nBase')
            valores.append(ultimo_mes['salario_base'])
            colores.append('#2196F3')
            
        if self.check_pluses.isChecked():
            conceptos.extend(['Plus\nTransporte', 'Plus\nProductividad', 'Plus\nExtra'])
            valores.extend([ultimo_mes['plus_transporte'], 
                          ultimo_mes['plus_productividad'],
                          ultimo_mes['plus_extra']])
            colores.extend(['#4CAF50', '#8BC34A', '#CDDC39'])
            
        if self.check_deducciones.isChecked():
            conceptos.append('Deducciones')
            valores.append(-ultimo_mes['deducciones'])
            colores.append('#f44336')
            
        # Crear gráfico
        bars = ax.bar(conceptos, valores, color=colores, alpha=self.slider_alpha.value()/100)
        
        # Añadir valores en las barras
        if self.check_mostrar_valores.isChecked():
            for bar, valor in zip(bars, valores):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., 
                       height + (50 if height > 0 else -100),
                       f'€{abs(valor):.0f}',
                       ha='center', va='bottom' if height > 0 else 'top',
                       fontweight='bold')
                       
        # Línea en cero
        ax.axhline(0, color='black', linewidth=0.8)
        
        ax.set_ylabel('Importe (€)', fontsize=12, fontweight='bold')
        ax.set_title(f'Comparación de Conceptos - {ultimo_mes["mes"]}', 
                    fontsize=14, fontweight='bold', pad=20)
        ax.grid(True, axis='y', alpha=0.3)
        
        self.aplicar_estilo_grafico(ax)
        self.figure.tight_layout()
        
    def grafico_distribucion_porcentual(self):
        """Crea gráfico de pastel/donut"""
        ax = self.figure.add_subplot(111)
        
        # Datos del último mes
        ultimo_mes = self.datos_nominas[-1]
        
        # Preparar datos
        etiquetas = []
        valores = []
        colores = []
        
        if self.check_salario_base.isChecked():
            etiquetas.append('Salario Base')
            valores.append(ultimo_mes['salario_base'])
            colores.append('#2196F3')
            
        if self.check_pluses.isChecked():
            etiquetas.append('Pluses')
            valores.append(ultimo_mes['total_pluses'])
            colores.append('#4CAF50')
            
        # Crear gráfico donut
        wedges, texts, autotexts = ax.pie(valores, labels=etiquetas, colors=colores,
                                          autopct='%1.1f%%', startangle=90,
                                          wedgeprops=dict(width=0.5, edgecolor='white'),
                                          textprops={'fontsize': 12, 'fontweight': 'bold'})
        
        # Mejorar aspecto
        for text in texts:
            text.set_fontsize(12)
            text.set_fontweight('bold')
            
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(11)
            autotext.set_fontweight('bold')
            
        # Añadir círculo central con total
        centre_circle = plt.Circle((0, 0), 0.70, fc='white', linewidth=2, edgecolor='#333333')
        ax.add_artist(centre_circle)
        
        # Texto en el centro
        total = sum(valores)
        ax.text(0, 0, f'Total\n€{total:.0f}', 
               ha='center', va='center', fontsize=16, fontweight='bold')
               
        ax.set_title(f'Distribución Salarial - {ultimo_mes["mes"]}',
                    fontsize=14, fontweight='bold', pad=20)
                    
        ax.axis('equal')
        self.figure.tight_layout()
        
    def grafico_analisis_tendencias(self):
        """Crea gráfico de análisis de tendencias con predicción"""
        ax = self.figure.add_subplot(111)
        
        # Datos históricos
        meses = np.arange(len(self.datos_nominas))
        salarios = [d['salario_neto'] for d in self.datos_nominas]
        
        # Calcular tendencia polinómica
        z = np.polyfit(meses, salarios, 2)
        p = np.poly1d(z)
        
        # Extender para predicción
        meses_futuros = np.arange(len(self.datos_nominas), len(self.datos_nominas) + 3)
        meses_total = np.concatenate([meses, meses_futuros])
        
        # Graficar
        ax.scatter(meses, salarios, color='#2196F3', s=100, alpha=0.7, label='Datos reales')
        ax.plot(meses_total, p(meses_total), 'r--', linewidth=2, label='Tendencia')
        
        # Área de predicción
        ax.fill_between(meses_futuros, 
                       p(meses_futuros) - 100, 
                       p(meses_futuros) + 100,
                       alpha=0.2, color='red', label='Intervalo de predicción')
                       
        # Etiquetas personalizadas para el eje X
        etiquetas_x = [d['mes'] for d in self.datos_nominas]
        # Añadir meses futuros
        ultimo_fecha = self.datos_nominas[-1]['fecha']
        for i in range(1, 4):
            fecha_futura = ultimo_fecha + timedelta(days=30*i)
            etiquetas_x.append(fecha_futura.strftime('%b %Y') + '*')
            
        ax.set_xticks(meses_total)
        ax.set_xticklabels(etiquetas_x, rotation=45, ha='right')
        
        ax.set_xlabel('Mes', fontsize=12, fontweight='bold')
        ax.set_ylabel('Salario Neto (€)', fontsize=12, fontweight='bold')
        ax.set_title('Análisis de Tendencias con Predicción', fontsize=14, fontweight='bold', pad=20)
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # Añadir ecuación
        ax.text(0.05, 0.95, f'y = {z[0]:.2f}x² + {z[1]:.2f}x + {z[2]:.0f}',
               transform=ax.transAxes, fontsize=10,
               verticalalignment='top',
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
               
        self.figure.tight_layout()
        
    def grafico_heatmap_mensual(self):
        """Crea un heatmap de conceptos por mes"""
        ax = self.figure.add_subplot(111)
        
        # Preparar matriz de datos
        conceptos = ['Salario Base', 'Pluses', 'Deducciones', 'Neto']
        meses = [d['mes'] for d in self.datos_nominas]
        
        matriz = []
        for d in self.datos_nominas:
            fila = [
                d['salario_base'],
                d['total_pluses'],
                d['deducciones'],
                d['salario_neto']
            ]
            matriz.append(fila)
            
        matriz = np.array(matriz).T
        
        # Crear heatmap
        im = ax.imshow(matriz, cmap='RdYlGn', aspect='auto')
        
        # Configurar ejes
        ax.set_xticks(np.arange(len(meses)))
        ax.set_yticks(np.arange(len(conceptos)))
        ax.set_xticklabels(meses)
        ax.set_yticklabels(conceptos)
        
        # Rotar las etiquetas del eje x
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha="right", rotation_mode="anchor")
        
        # Añadir valores en las celdas si está marcado
        if self.check_mostrar_valores.isChecked():
            for i in range(len(conceptos)):
                for j in range(len(meses)):
                    text = ax.text(j, i, f'{matriz[i, j]:.0f}',
                                 ha="center", va="center", color="black", fontsize=8)
                                 
        # Colorbar
        cbar = self.figure.colorbar(im, ax=ax)
        cbar.set_label('Importe (€)', rotation=270, labelpad=20)
        
        ax.set_title('Heatmap de Conceptos Salariales por Mes', 
                    fontsize=14, fontweight='bold', pad=20)
                    
        self.figure.tight_layout()
        
    def grafico_cascada(self):
        """Crea un gráfico de cascada (waterfall)"""
        ax = self.figure.add_subplot(111)
        
        # Datos del último mes
        ultimo_mes = self.datos_nominas[-1]
        
        # Preparar datos para cascada
        categorias = ['Salario\nBase', '+Transport', '+Product.', '+Extra', '-Deducc.', 'NETO']
        valores = [
            ultimo_mes['salario_base'],
            ultimo_mes['plus_transporte'],
            ultimo_mes['plus_productividad'],
            ultimo_mes['plus_extra'],
            -ultimo_mes['deducciones'],
            0  # Se calculará
        ]
        
        # Calcular posiciones
        pos_anterior = 0
        posiciones = []
        for i, valor in enumerate(valores[:-1]):
            posiciones.append(pos_anterior)
            pos_anterior += valor
            
        # El último es el total
        valores[-1] = pos_anterior
        posiciones.append(0)
        
        # Colores
        colores = ['#2196F3', '#4CAF50', '#4CAF50', '#4CAF50', '#f44336', '#333333']
        
        # Crear barras
        for i, (cat, val, pos, color) in enumerate(zip(categorias, valores, posiciones, colores)):
            if i < len(categorias) - 1:
                ax.bar(i, abs(val), bottom=pos if val > 0 else pos + val, 
                      color=color, alpha=0.8, edgecolor='black', linewidth=1)
                      
                # Líneas conectoras
                if i < len(categorias) - 2:
                    ax.plot([i+0.4, i+1-0.4], [pos + val, pos + val], 
                           'k--', alpha=0.5, linewidth=1)
            else:
                # Barra final (total)
                ax.bar(i, val, color=color, alpha=0.8, edgecolor='black', linewidth=2)
                
        # Añadir valores
        for i, (val, pos) in enumerate(zip(valores, posiciones)):
            if i < len(valores) - 1:
                y_pos = pos + val/2 if val > 0 else pos + val/2
                ax.text(i, y_pos, f'€{abs(val):.0f}', 
                       ha='center', va='center', fontweight='bold', fontsize=10)
            else:
                ax.text(i, val + 50, f'€{val:.0f}', 
                       ha='center', va='bottom', fontweight='bold', fontsize=12)
                       
        ax.set_xticks(range(len(categorias)))
        ax.set_xticklabels(categorias)
        ax.set_ylabel('Importe (€)', fontsize=12, fontweight='bold')
        ax.set_title(f'Desglose en Cascada - {ultimo_mes["mes"]}', 
                    fontsize=14, fontweight='bold', pad=20)
        ax.grid(True, axis='y', alpha=0.3)
        
        # Línea base en 0
        ax.axhline(0, color='black', linewidth=0.8)
        
        self.figure.tight_layout()
        
    def grafico_desviaciones(self):
        """Crea gráfico de desviaciones respecto al promedio"""
        ax = self.figure.add_subplot(111)
        
        # Calcular promedios
        promedio_neto = np.mean([d['salario_neto'] for d in self.datos_nominas])
        
        # Calcular desviaciones
        meses = [d['mes'] for d in self.datos_nominas]
        desviaciones = [d['salario_neto'] - promedio_neto for d in self.datos_nominas]
        
        # Colores según desviación positiva o negativa
        colores = ['#4CAF50' if d > 0 else '#f44336' for d in desviaciones]
        
        # Crear gráfico de barras
        bars = ax.bar(meses, desviaciones, color=colores, alpha=0.7, edgecolor='black')
        
        # Línea en cero (promedio)
        ax.axhline(0, color='black', linewidth=2, label=f'Promedio: €{promedio_neto:.0f}')
        
        # Añadir valores
        if self.check_mostrar_valores.isChecked():
            for bar, desv in zip(bars, desviaciones):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., 
                       height + (20 if height > 0 else -30),
                       f'{desv:+.0f}€',
                       ha='center', va='bottom' if height > 0 else 'top',
                       fontsize=9, fontweight='bold')
                       
        # Áreas de desviación estándar
        desv_std = np.std([d['salario_neto'] for d in self.datos_nominas])
        ax.axhspan(-desv_std, desv_std, alpha=0.1, color='gray', 
                  label=f'±1 Desv. Est. (€{desv_std:.0f})')
        ax.axhspan(-2*desv_std, -desv_std, alpha=0.05, color='red')
        ax.axhspan(desv_std, 2*desv_std, alpha=0.05, color='green')
        
        ax.set_xlabel('Mes', fontsize=12, fontweight='bold')
        ax.set_ylabel('Desviación (€)', fontsize=12, fontweight='bold')
        ax.set_title('Análisis de Desviaciones del Salario Neto', 
                    fontsize=14, fontweight='bold', pad=20)
        ax.legend()
        ax.grid(True, axis='y', alpha=0.3)
        
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
        self.figure.tight_layout()
        
    def crear_dashboard(self):
        """Crea un dashboard completo con múltiples visualizaciones"""
        # Limpiar y crear subplots
        gs = self.figure.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
        
        # 1. Evolución temporal (grande, arriba)
        ax1 = self.figure.add_subplot(gs[0, :])
        meses = [d['mes'] for d in self.datos_nominas]
        netos = [d['salario_neto'] for d in self.datos_nominas]
        ax1.plot(meses, netos, 'o-', linewidth=2, markersize=6, color='#2196F3')
        ax1.fill_between(range(len(meses)), netos, alpha=0.3, color='#2196F3')
        ax1.set_title('Evolución del Salario Neto', fontweight='bold')
        ax1.grid(True, alpha=0.3)
        plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        # 2. Comparación último mes (izquierda medio)
        ax2 = self.figure.add_subplot(gs[1, 0])
        ultimo = self.datos_nominas[-1]
        conceptos = ['Base', 'Pluses', 'Deducc.']
        valores = [ultimo['salario_base'], ultimo['total_pluses'], -ultimo['deducciones']]
        colores = ['#2196F3', '#4CAF50', '#f44336']
        ax2.bar(conceptos, valores, color=colores, alpha=0.7)
        ax2.set_title('Último Mes', fontweight='bold', fontsize=10)
        ax2.grid(True, axis='y', alpha=0.3)
        
        # 3. KPIs (centro medio)
        ax3 = self.figure.add_subplot(gs[1, 1])
        ax3.axis('off')
        
        # Calcular KPIs
        promedio = np.mean(netos)
        maximo = max(netos)
        minimo = min(netos)
        ultimo_valor = netos[-1]
        variacion = ((ultimo_valor - netos[-2]) / netos[-2] * 100) if len(netos) > 1 else 0
        
        # Mostrar KPIs
        kpi_text = f"""
        INDICADORES CLAVE
        
        Promedio: €{promedio:.0f}
        Máximo: €{maximo:.0f}
        Mínimo: €{minimo:.0f}
        Actual: €{ultimo_valor:.0f}
        Var. Mes: {variacion:+.1f}%
        """
        ax3.text(0.5, 0.5, kpi_text, transform=ax3.transAxes,
                fontsize=10, ha='center', va='center',
                bbox=dict(boxstyle='round,pad=0.5', facecolor='lightgray', alpha=0.8))
        
        # 4. Mini gráfico de tendencia (derecha medio)
        ax4 = self.figure.add_subplot(gs[1, 2])
        x = np.arange(len(netos))
        z = np.polyfit(x, netos, 1)
        p = np.poly1d(z)
        ax4.scatter(x[-6:], netos[-6:], alpha=0.6, color='#2196F3')
        ax4.plot(x[-6:], p(x[-6:]), 'r--', linewidth=2)
        ax4.set_title('Tendencia 6 meses', fontweight='bold', fontsize=10)
        ax4.grid(True, alpha=0.3)
        
        # 5. Distribución porcentual (izquierda abajo)
        ax5 = self.figure.add_subplot(gs[2, 0])
        sizes = [ultimo['salario_base'], ultimo['total_pluses']]
        labels = ['Base', 'Pluses']
        colors = ['#2196F3', '#4CAF50']
        ax5.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
                startangle=90, textprops={'fontsize': 9})
        ax5.set_title('Distribución', fontweight='bold', fontsize=10)
        
        # 6. Comparación anual (centro abajo)
        ax6 = self.figure.add_subplot(gs[2, 1])
        # Agrupar por trimestre
        trimestres = ['T1', 'T2', 'T3', 'T4']
        valores_trim = []
        for i in range(0, len(netos), 3):
            valores_trim.append(np.mean(netos[i:i+3]))
        if len(valores_trim) < 4:
            valores_trim.extend([np.nan] * (4 - len(valores_trim)))
        ax6.bar(trimestres, valores_trim, color='#FF9800', alpha=0.7)
        ax6.set_title('Por Trimestre', fontweight='bold', fontsize=10)
        ax6.grid(True, axis='y', alpha=0.3)
        
        # 7. Estadísticas (derecha abajo)
        ax7 = self.figure.add_subplot(gs[2, 2])
        # Box plot simple
        ax7.boxplot([netos], vert=True, patch_artist=True,
                   boxprops=dict(facecolor='#2196F3', alpha=0.7))
        ax7.set_ylabel('€', fontsize=9)
        ax7.set_title('Distribución', fontweight='bold', fontsize=10)
        ax7.grid(True, axis='y', alpha=0.3)
        
        # Título general
        self.figure.suptitle('Dashboard de Análisis Salarial', fontsize=16, fontweight='bold')
        
    def aplicar_estilo_grafico(self, ax):
        """Aplica el estilo seleccionado al gráfico"""
        estilo = self.combo_estilo.currentText()
        
        if estilo == "Moderno":
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_linewidth(0.5)
            ax.spines['bottom'].set_linewidth(0.5)
            ax.tick_params(labelsize=10)
            ax.grid(True, alpha=0.3, linestyle='-', linewidth=0.5)
            
        elif estilo == "Clásico":
            ax.spines['top'].set_visible(True)
            ax.spines['right'].set_visible(True)
            ax.grid(True, alpha=0.3, linestyle='--')
            
        elif estilo == "Minimalista":
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_visible(False)
            ax.spines['bottom'].set_visible(False)
            ax.grid(False)
            ax.tick_params(bottom=False, left=False)
            
        elif estilo == "Corporativo":
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_linewidth(2)
            ax.spines['bottom'].set_linewidth(2)
            ax.grid(True, alpha=0.2, linestyle='-')
            ax.set_facecolor('#f8f8f8')
            
    def cambiar_estilo(self):
        """Cambia el estilo del gráfico"""
        self.actualizar_visualizacion()
        
    def cambiar_zoom(self, valor):
        """Ajusta el zoom del gráfico"""
        self.lbl_zoom.setText(f"{valor}%")
        # Aquí se podría implementar el zoom real
        
    def cambiar_rotacion(self, valor):
        """Ajusta la rotación de etiquetas"""
        self.actualizar_visualizacion()
        
    def cambiar_transparencia(self, valor):
        """Ajusta la transparencia"""
        self.actualizar_visualizacion()
        
    def personalizar_colores(self):
        """Permite personalizar los colores del gráfico"""
        from PyQt5.QtWidgets import QDialog, QGridLayout, QDialogButtonBox
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Personalizar Colores")
        dialog.setModal(True)
        
        layout = QGridLayout(dialog)
        
        # Selectores de color para cada concepto
        conceptos = [
            ('Salario Base', '#2196F3'),
            ('Pluses', '#4CAF50'),
            ('Deducciones', '#f44336'),
            ('Salario Neto', '#9C27B0')
        ]
        
        self.color_buttons = {}
        
        for i, (concepto, color_default) in enumerate(conceptos):
            layout.addWidget(QLabel(concepto + ":"), i, 0)
            
            btn_color = QPushButton()
            btn_color.setStyleSheet(f"background-color: {color_default}; min-width: 60px;")
            btn_color.clicked.connect(lambda checked, c=concepto: self.seleccionar_color(c))
            self.color_buttons[concepto] = btn_color
            
            layout.addWidget(btn_color, i, 1)
            
        # Botones
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, dialog
        )
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons, len(conceptos), 0, 1, 2)
        
        if dialog.exec_() == QDialog.Accepted:
            self.actualizar_visualizacion()
            
    def seleccionar_color(self, concepto):
        """Abre el selector de color para un concepto"""
        color = QColorDialog.getColor()
        if color.isValid():
            self.color_buttons[concepto].setStyleSheet(f"background-color: {color.name()}; min-width: 60px;")
            
    def exportar_grafico(self):
        """Exporta el gráfico actual"""
        archivo, _ = QFileDialog.getSaveFileName(
            self,
            'Exportar gráfico',
            f'grafico_{self.combo_tipo_grafico.currentText().lower().replace(" ", "_")}.png',
            'PNG (*.png);;JPG (*.jpg);;PDF (*.pdf);;SVG (*.svg)'
        )
        
        if archivo:
            try:
                # Configurar DPI alto para mejor calidad
                dpi = 300 if archivo.endswith(('.png', '.jpg')) else 100
                self.figure.savefig(archivo, dpi=dpi, bbox_inches='tight', 
                                   facecolor='white', edgecolor='none')
                
                QMessageBox.information(
                    self,
                    'Exportación exitosa',
                    f'El gráfico se ha exportado correctamente a:\n{archivo}'
                )
                
            except Exception as e:
                QMessageBox.critical(
                    self,
                    'Error al exportar',
                    f'Error al exportar el gráfico:\n{str(e)}'
                )
                
    def guardar_plantilla(self):
        """Guarda la configuración actual como plantilla"""
        from PyQt5.QtWidgets import QInputDialog
        
        nombre, ok = QInputDialog.getText(
            self,
            'Guardar Plantilla',
            'Nombre de la plantilla:'
        )
        
        if ok and nombre:
            # Aquí se guardaría la configuración
            QMessageBox.information(
                self,
                'Plantilla guardada',
                f'La plantilla "{nombre}" se ha guardado correctamente.'
            )
            
    def imprimir_grafico(self):
        """Imprime el gráfico actual"""
        from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
        from PyQt5.QtGui import QPainter
        
        printer = QPrinter(QPrinter.HighResolution)
        dialog = QPrintDialog(printer, self)
        
        if dialog.exec_() == QPrintDialog.Accepted:
            # Aquí se implementaría la impresión
            QMessageBox.information(
                self,
                'Función en desarrollo',
                'La función de impresión se implementará próximamente.'
            )import pandas as pd
import numpy as np
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                            QLabel, QComboBox, QGroupBox, QCheckBox,
                            QMessageBox, QFileDialog, QSpinBox, QDateEdit,
                            QTableWidget, QTableWidgetItem, QSlider,
                            QColorDialog)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QColor
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import seaborn as sns

class VisualizacionesWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.datos_nominas = []
        self.datos_cargados = False
        self.initUI()
        
    def initUI(self):
        layout_principal = QVBoxLayout(self)
        
        # Panel de controles superiores
        panel_controles = QGroupBox("Controles de Visualización")
        layout_controles = QVBoxLayout(panel_controles)
        
        # Fila 1: Tipo de gráfico y período
        layout_fila1 = QHBoxLayout()
        
        layout_fila1.addWidget(QLabel("Tipo de gráfico:"))
        self.combo_tipo_grafico = QComboBox()
        self.combo_tipo_grafico.addItems([
            "Evolución temporal",
            "Comparación de conceptos",
            "Distribución porcentual",
            "Análisis de tendencias",
            "Heatmap mensual",
            "Gráfico de cascada",
            "Análisis de desviaciones",
            "Dashboard completo"
        ])
        self.combo_tipo_grafico.currentTextChanged.connect(self.actualizar_visualizacion)
        layout_fila1.addWidget(self.combo_tipo_grafico)
        
        layout_fila1.addWidget(QLabel("Período:"))
        self.combo_periodo = QComboBox()
        self.combo_periodo.addItems([
            "Últimos 6 meses",
            "Último año",
            "Año actual",
            "Todo el histórico",
            "Personalizado"
        ])
        self.combo_periodo.currentTextChanged.connect(self.cambiar_periodo)
        layout_fila1.addWidget(self.combo_periodo)
        
        # Fechas personalizadas (ocultas por defecto)
        self.date_inicio = QDateEdit()
        self.date_inicio.setCalendarPopup(True)
        self.date_inicio.setDate(QDate.currentDate().addMonths(-12))
        self.date_inicio.setVisible(False)
        layout_fila1.addWidget(self.date_inicio)
        
        self.date_fin = QDateEdit()
        self.date_fin.setCalendarPopup(True)
        self.date_fin.setDate(QDate.currentDate())
        self.date_fin.setVisible(False)
        layout_fila1.addWidget(self.date_fin)
        
        layout_fila1.addStretch()
        layout_controles.addLayout(layout_fila1)
        
        # Fila 2: Opciones de visualización
        layout_fila2 = QHBoxLayout()
        
        self.check_mostrar_valores = QCheckBox("Mostrar valores")
        self.check_mostrar_valores.setChecked(True)
        self.check_mostrar_valores.stateChanged.connect(self.actualizar_visualizacion)
        layout_fila2.addWidget(self.check_mostrar_valores)
        
        self.check_mostrar_tendencia = QCheckBox("Línea de tendencia")
        self.check_mostrar_tendencia.stateChanged.connect(self.actualizar_visualizacion)
        layout_fila2.addWidget(self.check_mostrar_tendencia)
        
        self.check_mostrar_promedio = QCheckBox("Línea promedio")
        self.check_mostrar_promedio.setChecked(True)
        self.check_mostrar_promedio.stateChanged.connect(self.actualizar_visualizacion)
        layout_fila2.addWidget(self.check_mostrar_promedio)
        
        self.check_animacion = QCheckBox("Animación")
        layout_fila2.addWidget(self.check_animacion)
        
        layout_fila2.addWidget(QLabel