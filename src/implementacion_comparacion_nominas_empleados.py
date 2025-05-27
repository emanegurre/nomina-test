btn_editar = QPushButton("✏️ Editar")
        btn_editar.clicked.connect(self.editar_empleado)
        layout_botones.addWidget(btn_editar)
        
        btn_eliminar = QPushButton("❌ Eliminar")
        btn_eliminar.clicked.connect(self.eliminar_empleado)
        layout_botones.addWidget(btn_eliminar)
        
        layout_empleados.addLayout(layout_botones)
        
        # Lista de empleados
        self.lista_empleados = QListWidget()
        self.lista_empleados.setSelectionMode(QListWidget.MultiSelection)
        layout_empleados.addWidget(self.lista_empleados)
        
        # Botones de importación
        layout_importar = QHBoxLayout()
        
        btn_importar_excel = QPushButton("📊 Importar Excel")
        btn_importar_excel.clicked.connect(self.importar_excel)
        layout_importar.addWidget(btn_importar_excel)
        
        btn_cargar_ejemplo = QPushButton("📋 Cargar Ejemplo")
        btn_cargar_ejemplo.clicked.connect(self.cargar_datos_ejemplo)
        layout_importar.addWidget(btn_cargar_ejemplo)
        
        layout_empleados.addLayout(layout_importar)
        
        # Panel derecho - Comparación y análisis
        panel_comparacion = QWidget()
        layout_comparacion = QVBoxLayout(panel_comparacion)
        
        # Controles de comparación
        panel_controles = QGroupBox("Opciones de Comparación")
        layout_controles = QVBoxLayout(panel_controles)
        
        # Tipo de comparación
        layout_tipo = QHBoxLayout()
        layout_tipo.addWidget(QLabel("Tipo de comparación:"))
        
        self.combo_tipo_comparacion = QComboBox()
        self.combo_tipo_comparacion.addItems([
            "Comparación general",
            "Por departamento",
            "Por rango salarial",
            "Por antigüedad",
            "Análisis de equidad"
        ])
        layout_tipo.addWidget(self.combo_tipo_comparacion)
        
        layout_tipo.addStretch()
        
        btn_comparar = QPushButton("🔍 Comparar Seleccionados")
        btn_comparar.clicked.connect(self.realizar_comparacion)
        btn_comparar.setStyleSheet("background-color: #FF9800; font-weight: bold;")
        layout_tipo.addWidget(btn_comparar)
        
        layout_controles.addLayout(layout_tipo)
        
        # Filtros
        layout_filtros = QHBoxLayout()
        
        self.check_salario_base = QCheckBox("Salario base")
        self.check_salario_base.setChecked(True)
        layout_filtros.addWidget(self.check_salario_base)
        
        self.check_pluses = QCheckBox("Pluses")
        self.check_pluses.setChecked(True)
        layout_filtros.addWidget(self.check_pluses)
        
        self.check_deducciones = QCheckBox("Deducciones")
        self.check_deducciones.setChecked(True)
        layout_filtros.addWidget(self.check_deducciones)
        
        self.check_neto = QCheckBox("Salario neto")
        self.check_neto.setChecked(True)
        layout_filtros.addWidget(self.check_neto)
        
        layout_filtros.addStretch()
        layout_controles.addLayout(layout_filtros)
        
        layout_comparacion.addWidget(panel_controles)
        
        # Tabla de comparación
        self.tabla_comparacion = QTableWidget()
        layout_comparacion.addWidget(self.tabla_comparacion)
        
        # Panel de estadísticas
        panel_estadisticas = QGroupBox("Estadísticas")
        layout_estadisticas = QVBoxLayout(panel_estadisticas)
        
        self.texto_estadisticas = QTextEdit()
        self.texto_estadisticas.setMaximumHeight(150)
        self.texto_estadisticas.setReadOnly(True)
        layout_estadisticas.addWidget(self.texto_estadisticas)
        
        layout_comparacion.addWidget(panel_estadisticas)
        
        # Agregar paneles al splitter
        splitter.addWidget(panel_empleados)
        splitter.addWidget(panel_comparacion)
        splitter.setSizes([300, 700])
        
        layout_principal.addWidget(splitter)
        
        # Panel de gráficos
        panel_graficos = QGroupBox("Visualización")
        layout_graficos = QVBoxLayout(panel_graficos)
        
        # Canvas para gráficos
        self.figure = Figure(figsize=(12, 4))
        self.canvas = FigureCanvas(self.figure)
        layout_graficos.addWidget(self.canvas)
        
        # Controles de gráfico
        layout_controles_grafico = QHBoxLayout()
        
        layout_controles_grafico.addWidget(QLabel("Tipo de gráfico:"))
        self.combo_tipo_grafico = QComboBox()
        self.combo_tipo_grafico.addItems([
            "Comparación de barras",
            "Distribución salarial",
            "Análisis por departamento",
            "Tendencias",
            "Matriz de equidad"
        ])
        self.combo_tipo_grafico.currentTextChanged.connect(self.actualizar_grafico)
        layout_controles_grafico.addWidget(self.combo_tipo_grafico)
        
        layout_controles_grafico.addStretch()
        layout_graficos.addLayout(layout_controles_grafico)
        
        layout_principal.addWidget(panel_graficos)
        
        # Botones de acción
        layout_acciones = QHBoxLayout()
        
        btn_informe_equidad = QPushButton("📊 Informe de Equidad")
        btn_informe_equidad.clicked.connect(self.generar_informe_equidad)
        layout_acciones.addWidget(btn_informe_equidad)
        
        btn_exportar = QPushButton("💾 Exportar Comparación")
        btn_exportar.clicked.connect(self.exportar_comparacion)
        layout_acciones.addWidget(btn_exportar)
        
        btn_politica_salarial = QPushButton("📋 Análisis Política Salarial")
        btn_politica_salarial.clicked.connect(self.analizar_politica_salarial)
        layout_acciones.addWidget(btn_politica_salarial)
        
        layout_acciones.addStretch()
        
        layout_principal.addLayout(layout_acciones)
        
    def agregar_empleado(self):
        """Agrega un nuevo empleado"""
        from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QFormLayout, QSpinBox
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Agregar Empleado")
        dialog.setModal(True)
        
        layout = QFormLayout(dialog)
        
        # Campos del formulario
        input_nombre = QLineEdit()
        layout.addRow("Nombre:", input_nombre)
        
        input_departamento = QLineEdit()
        layout.addRow("Departamento:", input_departamento)
        
        input_puesto = QLineEdit()
        layout.addRow("Puesto:", input_puesto)
        
        input_salario = QDoubleSpinBox()
        input_salario.setRange(0, 99999)
        input_salario.setDecimals(2)
        input_salario.setValue(2000)
        layout.addRow("Salario base:", input_salario)
        
        # Pluses comunes
        input_transporte = QDoubleSpinBox()
        input_transporte.setRange(0, 9999)
        input_transporte.setDecimals(2)
        input_transporte.setValue(100)
        layout.addRow("Plus transporte:", input_transporte)
        
        input_productividad = QDoubleSpinBox()
        input_productividad.setRange(0, 9999)
        input_productividad.setDecimals(2)
        layout.addRow("Plus productividad:", input_productividad)
        
        # Antigüedad
        input_antiguedad = QSpinBox()
        input_antiguedad.setRange(0, 50)
        layout.addRow("Años antigüedad:", input_antiguedad)
        
        # Botones
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, dialog
        )
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addRow(buttons)
        
        if dialog.exec_() == QDialog.Accepted:
            nombre = input_nombre.text()
            if nombre and nombre not in self.empleados:
                # Crear empleado
                empleado = EmpleadoData(
                    nombre,
                    input_departamento.text(),
                    input_puesto.text()
                )
                
                empleado.salario_base = input_salario.value()
                
                # Agregar pluses
                if input_transporte.value() > 0:
                    empleado.pluses['Transporte'] = input_transporte.value()
                if input_productividad.value() > 0:
                    empleado.pluses['Productividad'] = input_productividad.value()
                    
                # Calcular plus antigüedad
                if input_antiguedad.value() > 0:
                    plus_antiguedad = empleado.salario_base * 0.03 * input_antiguedad.value()
                    empleado.pluses['Antigüedad'] = plus_antiguedad
                    
                empleado.datos_adicionales['antiguedad'] = input_antiguedad.value()
                
                # Agregar a la lista
                self.empleados[nombre] = empleado
                self.actualizar_lista_empleados()
                
                QMessageBox.information(
                    self,
                    "Empleado agregado",
                    f"Se ha agregado el empleado {nombre} correctamente."
                )
            else:
                QMessageBox.warning(
                    self,
                    "Error",
                    "Debe especificar un nombre único para el empleado."
                )
                
    def editar_empleado(self):
        """Edita el empleado seleccionado"""
        items = self.lista_empleados.selectedItems()
        if not items:
            QMessageBox.warning(self, "Sin selección", "Seleccione un empleado para editar.")
            return
            
        # Por simplicidad, editamos el primer seleccionado
        nombre = items[0].text().split(' - ')[0]
        empleado = self.empleados.get(nombre)
        
        if not empleado:
            return
            
        # Aquí se abriría un diálogo similar al de agregar pero con los datos precargados
        QMessageBox.information(
            self,
            "Función en desarrollo",
            f"La edición del empleado {nombre} se implementará próximamente."
        )
        
    def eliminar_empleado(self):
        """Elimina los empleados seleccionados"""
        items = self.lista_empleados.selectedItems()
        if not items:
            QMessageBox.warning(self, "Sin selección", "Seleccione empleados para eliminar.")
            return
            
        respuesta = QMessageBox.question(
            self,
            "Confirmar eliminación",
            f"¿Está seguro de eliminar {len(items)} empleado(s)?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if respuesta == QMessageBox.Yes:
            for item in items:
                nombre = item.text().split(' - ')[0]
                if nombre in self.empleados:
                    del self.empleados[nombre]
                    
            self.actualizar_lista_empleados()
            
    def actualizar_lista_empleados(self):
        """Actualiza la lista visual de empleados"""
        self.lista_empleados.clear()
        
        for nombre, empleado in sorted(self.empleados.items()):
            texto = f"{nombre} - {empleado.departamento} - €{empleado.get_salario_total():.2f}"
            self.lista_empleados.addItem(texto)
            
    def cargar_datos_ejemplo(self):
        """Carga datos de ejemplo"""
        empleados_ejemplo = [
            {
                'nombre': 'Juan García',
                'departamento': 'Ventas',
                'puesto': 'Comercial',
                'salario_base': 1800,
                'pluses': {'Transporte': 100, 'Productividad': 200, 'Comisiones': 300},
                'antiguedad': 3
            },
            {
                'nombre': 'María López',
                'departamento': 'Administración',
                'puesto': 'Administrativa',
                'salario_base': 1600,
                'pluses': {'Transporte': 100, 'Idiomas': 150},
                'antiguedad': 5
            },
            {
                'nombre': 'Carlos Martín',
                'departamento': 'IT',
                'puesto': 'Desarrollador',
                'salario_base': 2500,
                'pluses': {'Transporte': 100, 'Disponibilidad': 200},
                'antiguedad': 2
            },
            {
                'nombre': 'Ana Rodríguez',
                'departamento': 'Ventas',
                'puesto': 'Jefa de Ventas',
                'salario_base': 2800,
                'pluses': {'Transporte': 100, 'Responsabilidad': 400, 'Objetivos': 300},
                'antiguedad': 7
            },
            {
                'nombre': 'Pedro Sánchez',
                'departamento': 'Producción',
                'puesto': 'Operario',
                'salario_base': 1500,
                'pluses': {'Transporte': 100, 'Turnicidad': 250, 'Peligrosidad': 100},
                'antiguedad': 10
            }
        ]
        
        self.empleados.clear()
        
        for datos in empleados_ejemplo:
            empleado = EmpleadoData(
                datos['nombre'],
                datos['departamento'],
                datos['puesto']
            )
            
            empleado.salario_base = datos['salario_base']
            empleado.pluses = datos['pluses'].copy()
            
            # Calcular plus antigüedad
            antiguedad = datos['antiguedad']
            if antiguedad > 0:
                plus_antiguedad = empleado.salario_base * 0.03 * antiguedad
                empleado.pluses['Antigüedad'] = plus_antiguedad
                
            empleado.datos_adicionales['antiguedad'] = antiguedad
            
            # Estimar deducciones
            total_bruto = empleado.get_salario_total()
            empleado.deducciones['Seg. Social'] = total_bruto * 0.0635
            empleado.deducciones['IRPF'] = total_bruto * 0.15
            
            self.empleados[datos['nombre']] = empleado
            
        self.actualizar_lista_empleados()
        
        QMessageBox.information(
            self,
            "Datos cargados",
            f"Se han cargado {len(empleados_ejemplo)} empleados de ejemplo."
        )
        
    def importar_excel(self):
        """Importa empleados desde Excel"""
        archivo, _ = QFileDialog.getOpenFileName(
            self,
            'Importar empleados',
            '',
            'Excel (*.xlsx *.xls)'
        )
        
        if archivo:
            try:
                df = pd.read_excel(archivo)
                
                # Verificar columnas mínimas requeridas
                columnas_requeridas = ['Nombre', 'Salario Base']
                if not all(col in df.columns for col in columnas_requeridas):
                    QMessageBox.warning(
                        self,
                        "Formato incorrecto",
                        f"El archivo debe contener al menos las columnas: {', '.join(columnas_requeridas)}"
                    )
                    return
                    
                # Importar empleados
                empleados_importados = 0
                
                for _, row in df.iterrows():
                    nombre = str(row['Nombre'])
                    if nombre and nombre not in self.empleados:
                        empleado = EmpleadoData(
                            nombre,
                            str(row.get('Departamento', '')),
                            str(row.get('Puesto', ''))
                        )
                        
                        empleado.salario_base = float(row['Salario Base'])
                        
                        # Buscar columnas de pluses
                        for col in df.columns:
                            if col.startswith('Plus '):
                                concepto = col.replace('Plus ', '')
                                valor = float(row[col]) if pd.notna(row[col]) else 0
                                if valor > 0:
                                    empleado.pluses[concepto] = valor
                                    
                        self.empleados[nombre] = empleado
                        empleados_importados += 1
                        
                self.actualizar_lista_empleados()
                
                QMessageBox.information(
                    self,
                    "Importación completada",
                    f"Se han importado {empleados_importados} empleados."
                )
                
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Error al importar",
                    f"Error al importar el archivo:\n{str(e)}"
                )
                
    def realizar_comparacion(self):
        """Realiza la comparación de los empleados seleccionados"""
        # Obtener empleados seleccionados
        items = self.lista_empleados.selectedItems()
        if len(items) < 2:
            QMessageBox.warning(
                self,
                "Selección insuficiente",
                "Seleccione al menos 2 empleados para comparar."
            )
            return
            
        empleados_seleccionados = []
        for item in items:
            nombre = item.text().split(' - ')[0]
            if nombre in self.empleados:
                empleados_seleccionados.append(self.empleados[nombre])
                
        tipo_comparacion = self.combo_tipo_comparacion.currentText()
        
        if tipo_comparacion == "Comparación general":
            self.comparacion_general(empleados_seleccionados)
        elif tipo_comparacion == "Por departamento":
            self.comparacion_por_departamento()
        elif tipo_comparacion == "Por rango salarial":
            self.comparacion_por_rango()
        elif tipo_comparacion == "Análisis de equidad":
            self.analisis_equidad()
            
        self.actualizar_grafico()
        
    def comparacion_general(self, empleados):
        """Realiza una comparación general de los empleados"""
        # Configurar tabla
        columnas = ['Empleado', 'Departamento', 'Puesto']
        
        if self.check_salario_base.isChecked():
            columnas.append('Salario Base')
        if self.check_pluses.isChecked():
            columnas.append('Total Pluses')
        if self.check_deducciones.isChecked():
            columnas.append('Deducciones')
        if self.check_neto.isChecked():
            columnas.append('Salario Neto')
            
        columnas.extend(['Total Bruto', 'Diferencia'])
        
        self.tabla_comparacion.setColumnCount(len(columnas))
        self.tabla_comparacion.setHorizontalHeaderLabels(columnas)
        self.tabla_comparacion.setRowCount(len(empleados))
        
        # Calcular salario promedio para la diferencia
        salarios_totales = [emp.get_salario_total() for emp in empleados]
        salario_promedio = sum(salarios_totales) / len(salarios_totales)
        
        # Llenar tabla
        for i, empleado in enumerate(empleados):
            col = 0
            
            # Datos básicos
            self.tabla_comparacion.setItem(i, col, QTableWidgetItem(empleado.nombre))
            col += 1
            
            self.tabla_comparacion.setItem(i, col, QTableWidgetItem(empleado.departamento))
            col += 1
            
            self.tabla_comparacion.setItem(i, col, QTableWidgetItem(empleado.puesto))
            col += 1
            
            # Datos salariales
            if self.check_salario_base.isChecked():
                self.tabla_comparacion.setItem(i, col, QTableWidgetItem(f"€ {empleado.salario_base:.2f}"))
                col += 1
                
            if self.check_pluses.isChecked():
                total_pluses = sum(empleado.pluses.values())
                self.tabla_comparacion.setItem(i, col, QTableWidgetItem(f"€ {total_pluses:.2f}"))
                col += 1
                
            if self.check_deducciones.isChecked():
                total_deducciones = sum(empleado.deducciones.values())
                self.tabla_comparacion.setItem(i, col, QTableWidgetItem(f"€ {total_deducciones:.2f}"))
                col += 1
                
            if self.check_neto.isChecked():
                salario_neto = empleado.get_salario_neto()
                self.tabla_comparacion.setItem(i, col, QTableWidgetItem(f"€ {salario_neto:.2f}"))
                col += 1
                
            # Total y diferencia
            total_bruto = empleado.get_salario_total()
            self.tabla_comparacion.setItem(i, col, QTableWidgetItem(f"€ {total_bruto:.2f}"))
            col += 1
            
            diferencia = total_bruto - salario_promedio
            porcentaje_dif = (diferencia / salario_promedio * 100) if salario_promedio > 0 else 0
            
            item_dif = QTableWidgetItem(f"€ {diferencia:+.2f} ({porcentaje_dif:+.1f}%)")
            
            # Colorear según diferencia
            if diferencia > 0:
                item_dif.setBackground(QColor(200, 230, 201))
            else:
                item_dif.setBackground(QColor(255, 205, 210))
                
            self.tabla_comparacion.setItem(i, col, item_dif)
            
        # Actualizar estadísticas
        self.actualizar_estadisticas(empleados)
        
    def actualizar_estadisticas(self, empleados):
        """Actualiza el panel de estadísticas"""
        if not empleados:
            return
            
        salarios = [emp.get_salario_total() for emp in empleados]
        
        estadisticas = "=== ESTADÍSTICAS DE LA COMPARACIÓN ===\n\n"
        estadisticas += f"Empleados comparados: {len(empleados)}\n"
        estadisticas += f"Salario promedio: € {np.mean(salarios):.2f}\n"
        estadisticas += f"Salario mediano: € {np.median(salarios):.2f}\n"
        estadisticas += f"Salario máximo: € {max(salarios):.2f} ({empleados[salarios.index(max(salarios))].nombre})\n"
        estadisticas += f"Salario mínimo: € {min(salarios):.2f} ({empleados[salarios.index(min(salarios))].nombre})\n"
        estadisticas += f"Desviación estándar: € {np.std(salarios):.2f}\n"
        estadisticas += f"Rango salarial: € {max(salarios) - min(salarios):.2f}\n"
        
        # Análisis de equidad
        coef_variacion = (np.std(salarios) / np.mean(salarios) * 100) if np.mean(salarios) > 0 else 0
        estadisticas += f"\nCoeficiente de variación: {coef_variacion:.1f}%\n"
        
        if coef_variacion < 15:
            estadisticas += "✅ Buena equidad salarial"
        elif coef_variacion < 25:
            estadisticas += "⚠️ Equidad salarial moderada"
        else:
            estadisticas += "❌ Baja equidad salarial"
            
        self.texto_estadisticas.setText(estadisticas)
        
    def comparacion_por_departamento(self):
        """Compara empleados agrupados por departamento"""
        # Agrupar por departamento
        departamentos = {}
        for empleado in self.empleados.values():
            dept = empleado.departamento or "Sin departamento"
            if dept not in departamentos:
                departamentos[dept] = []
            departamentos[dept].append(empleado)
            
        # Configurar tabla
        self.tabla_comparacion.setColumnCount(6)
        self.tabla_comparacion.setHorizontalHeaderLabels([
            'Departamento', 'Nº Empleados', 'Salario Promedio',
            'Salario Máximo', 'Salario Mínimo', 'Desv. Estándar'
        ])
        self.tabla_comparacion.setRowCount(len(departamentos))
        
        # Llenar tabla
        for i, (dept, empleados) in enumerate(sorted(departamentos.items())):
            salarios = [emp.get_salario_total() for emp in empleados]
            
            self.tabla_comparacion.setItem(i, 0, QTableWidgetItem(dept))
            self.tabla_comparacion.setItem(i, 1, QTableWidgetItem(str(len(empleados))))
            self.tabla_comparacion.setItem(i, 2, QTableWidgetItem(f"€ {np.mean(salarios):.2f}"))
            self.tabla_comparacion.setItem(i, 3, QTableWidgetItem(f"€ {max(salarios):.2f}"))
            self.tabla_comparacion.setItem(i, 4, QTableWidgetItem(f"€ {min(salarios):.2f}"))
            self.tabla_comparacion.setItem(i, 5, QTableWidgetItem(f"€ {np.std(salarios):.2f}"))
            
    def comparacion_por_rango(self):
        """Compara empleados por rangos salariales"""
        # Definir rangos
        rangos = [
            (0, 1500, "Menos de €1,500"),
            (1500, 2000, "€1,500 - €2,000"),
            (2000, 2500, "€2,000 - €2,500"),
            (2500, 3000, "€2,500 - €3,000"),
            (3000, float('inf'), "Más de €3,000")
        ]
        
        # Clasificar empleados
        empleados_por_rango = {rango[2]: [] for rango in rangos}
        
        for empleado in self.empleados.values():
            salario = empleado.get_salario_total()
            for min_sal, max_sal, etiqueta in rangos:
                if min_sal <= salario < max_sal:
                    empleados_por_rango[etiqueta].append(empleado)
                    break
                    
        # Configurar tabla
        self.tabla_comparacion.setColumnCount(5)
        self.tabla_comparacion.setHorizontalHeaderLabels([
            'Rango Salarial', 'Nº Empleados', '% del Total',
            'Salario Promedio', 'Departamentos'
        ])
        
        filas_con_datos = [r for r in rangos if empleados_por_rango[r[2]]]
        self.tabla_comparacion.setRowCount(len(filas_con_datos))
        
        total_empleados = len(self.empleados)
        
        # Llenar tabla
        row = 0
        for min_sal, max_sal, etiqueta in rangos:
            empleados = empleados_por_rango[etiqueta]
            if not empleados:
                continue
                
            num_empleados = len(empleados)
            porcentaje = (num_empleados / total_empleados * 100) if total_empleados > 0 else 0
            salarios = [emp.get_salario_total() for emp in empleados]
            promedio = np.mean(salarios)
            
            # Departamentos únicos
            departamentos = set(emp.departamento for emp in empleados if emp.departamento)
            dept_text = ", ".join(sorted(departamentos)) or "N/A"
            
            self.tabla_comparacion.setItem(row, 0, QTableWidgetItem(etiqueta))
            self.tabla_comparacion.setItem(row, 1, QTableWidgetItem(str(num_empleados)))
            self.tabla_comparacion.setItem(row, 2, QTableWidgetItem(f"{porcentaje:.1f}%"))
            self.tabla_comparacion.setItem(row, 3, QTableWidgetItem(f"€ {promedio:.2f}"))
            self.tabla_comparacion.setItem(row, 4, QTableWidgetItem(dept_text))
            
            row += 1
            
    def analisis_equidad(self):
        """Realiza un análisis de equidad salarial"""
        # Este es un análisis simplificado
        # En la práctica, debería considerar factores como género, edad, etc.
        
        # Agrupar por características similares (departamento y antigüedad similar)
        grupos = {}
        
        for empleado in self.empleados.values():
            dept = empleado.departamento or "Sin dept"
            antiguedad = empleado.datos_adicionales.get('antiguedad', 0)
            
            # Crear grupos por rangos de antigüedad
            if antiguedad < 2:
                grupo_ant = "0-2 años"
            elif antiguedad < 5:
                grupo_ant = "2-5 años"
            elif antiguedad < 10:
                grupo_ant = "5-10 años"
            else:
                grupo_ant = "10+ años"
                
            clave = f"{dept} - {grupo_ant}"
            
            if clave not in grupos:
                grupos[clave] = []
            grupos[clave].append(empleado)
            
        # Configurar tabla
        self.tabla_comparacion.setColumnCount(6)
        self.tabla_comparacion.setHorizontalHeaderLabels([
            'Grupo', 'Empleados', 'Salario Promedio', 
            'Desv. Estándar', 'Coef. Variación', 'Estado'
        ])
        self.tabla_comparacion.setRowCount(len(grupos))
        
        # Analizar cada grupo
        for i, (grupo, empleados) in enumerate(sorted(grupos.items())):
            if len(empleados) < 2:
                continue
                
            salarios = [emp.get_salario_total() for emp in empleados]
            promedio = np.mean(salarios)
            desviacion = np.std(salarios)
            coef_variacion = (desviacion / promedio * 100) if promedio > 0 else 0
            
            # Determinar estado
            if coef_variacion < 10:
                estado = "✅ Excelente"
                color = QColor(200, 230, 201)
            elif coef_variacion < 20:
                estado = "👍 Bueno"
                color = QColor(255, 235, 205)
            elif coef_variacion < 30:
                estado = "⚠️ Regular"
                color = QColor(255, 224, 178)
            else:
                estado = "❌ Revisar"
                color = QColor(255, 205, 210)
                
            self.tabla_comparacion.setItem(i, 0, QTableWidgetItem(grupo))
            self.tabla_comparacion.setItem(i, 1, QTableWidgetItem(str(len(empleados))))
            self.tabla_comparacion.setItem(i, 2, QTableWidgetItem(f"€ {promedio:.2f}"))
            self.tabla_comparacion.setItem(i, 3, QTableWidgetItem(f"€ {desviacion:.2f}"))
            self.tabla_comparacion.setItem(i, 4, QTableWidgetItem(f"{coef_variacion:.1f}%"))
            
            item_estado = QTableWidgetItem(estado)
            item_estado.setBackground(color)
            self.tabla_comparacion.setItem(i, 5, item_estado)
            
    def actualizar_grafico(self):
        """Actualiza el gráfico según el tipo seleccionado"""
        self.figure.clear()
        tipo = self.combo_tipo_grafico.currentText()
        
        if tipo == "Comparación de barras":
            self.grafico_comparacion_barras()
        elif tipo == "Distribución salarial":
            self.grafico_distribucion_salarial()
        elif tipo == "Análisis por departamento":
            self.grafico_por_departamento()
        elif tipo == "Tendencias":
            self.grafico_tendencias()
        elif tipo == "Matriz de equidad":
            self.grafico_matriz_equidad()
            
        self.canvas.draw()
        
    def grafico_comparacion_barras(self):
        """Genera gráfico de barras comparativo"""
        ax = self.figure.add_subplot(111)
        
        # Obtener empleados seleccionados
        items = self.lista_empleados.selectedItems()
        if not items:
            # Si no hay selección, mostrar todos
            empleados = list(self.empleados.values())
        else:
            empleados = []
            for item in items:
                nombre = item.text().split(' - ')[0]
                if nombre in self.empleados:
                    empleados.append(self.empleados[nombre])
                    
        if not empleados:
            return
            
        # Preparar datos
        nombres = [emp.nombre for emp in empleados]
        salarios_base = [emp.salario_base for emp in empleados]
        pluses = [sum(emp.pluses.values()) for emp in empleados]
        deducciones = [sum(emp.deducciones.values()) for emp in empleados]
        
        x = np.arange(len(nombres))
        width = 0.25
        
        # Crear barras
        bars1 = ax.bar(x - width, salarios_base, width, label='Salario Base', color='#2196F3')
        bars2 = ax.bar(x, pluses, width, label='Pluses', color='#4CAF50')
        bars3 = ax.bar(x + width, deducciones, width, label='Deducciones', color='#f44336')
        
        ax.set_xlabel('Empleados')
        ax.set_ylabel('Importe (€)')
        ax.set_title('Comparación de Componentes Salariales')
        ax.set_xticks(x)
        ax.set_xticklabels(nombres, rotation=45, ha='right')
        ax.legend()
        ax.grid(True, alpha=0.3, axis='y')
        
        # Añadir valores en las barras
        def autolabel(bars):
            for bar in bars:
                height = bar.get_height()
                ax.annotate(f'{height:.0f}',
                           xy=(bar.get_x() + bar.get_width() / 2, height),
                           xytext=(0, 3),
                           textcoords="offset points",
                           ha='center', va='bottom',
                           fontsize=8)
                           
        autolabel(bars1)
        autolabel(bars2)
        autolabel(bars3)
        
        self.figure.tight_layout()
        
    def grafico_distribucion_salarial(self):
        """Genera gráfico de distribución salarial"""
        ax = self.figure.add_subplot(121)
        
        # Histograma
        salarios = [emp.get_salario_total() for emp in self.empleados.values()]
        
        ax.hist(salarios, bins=10, color='#2196F3', alpha=0.7, edgecolor='black')
        ax.set_xlabel('Salario Total (€)')
        ax.set_ylabel('Número de Empleados')
        ax.set_title('Distribución Salarial')
        ax.grid(True, alpha=0.3, axis='y')
        
        # Añadir líneas de estadísticas
        mean_sal = np.mean(salarios)
        median_sal = np.median(salarios)
        
        ax.axvline(mean_sal, color='red', linestyle='--', linewidth=2, label=f'Media: €{mean_sal:.0f}')
        ax.axvline(median_sal, color='green', linestyle='--', linewidth=2, label=f'Mediana: €{median_sal:.0f}')
        ax.legend()
        
        # Box plot
        ax2 = self.figure.add_subplot(122)
        
        # Datos por departamento
        dept_data = {}
        for emp in self.empleados.values():
            dept = emp.departamento or "Sin dept"
            if dept not in dept_data:
                dept_data[dept] = []
            dept_data[dept].append(emp.get_salario_total())
            
        # Crear box plot
        data_to_plot = list(dept_data.values())
        labels = list(dept_data.keys())
        
        bp = ax2.boxplot(data_to_plot, labels=labels, patch_artist=True)
        
        # Colorear cajas
        colors = ['#2196F3', '#4CAF50', '#FF9800', '#f44336', '#9C27B0']
        for patch, color in zip(bp['boxes'], colors * len(bp['boxes'])):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)
            
        ax2.set_ylabel('Salario Total (€)')
        ax2.set_title('Distribución por Departamento')
        ax2.tick_params(axis='x', rotation=45)
        ax2.grid(True, alpha=0.3, axis='y')
        
        self.figure.tight_layout()
        
    def grafico_por_departamento(self):
        """Genera gráfico de análisis por departamento"""
        ax = self.figure.add_subplot(111)
        
        # Agrupar por departamento
        dept_stats = {}
        for emp in self.empleados.values():
            dept = emp.departamento or "Sin departamento"
            if dept not in dept_stats:
                dept_stats[dept] = {
                    'salarios': [],
                    'empleados': []
                }
            dept_stats[dept]['salarios'].append(emp.get_salario_total())
            dept_stats[dept]['empleados'].append(emp)
            
        # Calcular estadísticas
        departamentos = []
        promedios = []
        num_empleados = []
        
        for dept, data in sorted(dept_stats.items()):
            departamentos.append(dept)
            promedios.append(np.mean(data['salarios']))
            num_empleados.append(len(data['empleados']))
            
        # Crear gráfico de barras con tamaño variable
        x = np.arange(len(departamentos))
        
        # Normalizar tamaños para el ancho de las barras
        max_empleados = max(num_empleados) if num_empleados else 1
        widths = [0.3 + (n / max_empleados) * 0.5 for n in num_empleados]
        
        bars = ax.bar(x, promedios, color='#2196F3', alpha=0.7)
        
        # Ajustar ancho de cada barra
        for bar, width, n in zip(bars, widths, num_empleados):
            bar.set_width(width)
            # Añadir número de empleados
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'€{height:.0f}\n({n} emp.)',
                   ha='center', va='bottom', fontsize=9)
                   
        ax.set_xlabel('Departamento')
        ax.set_ylabel('Salario Promedio (€)')
        ax.set_title('Análisis Salarial por Departamento')
        ax.set_xticks(x)
        ax.set_xticklabels(departamentos, rotation=45, ha='right')
        ax.grid(True, alpha=0.3, axis='y')
        
        # Línea de promedio general
        promedio_general = np.mean([emp.get_salario_total() for emp in self.empleados.values()])
        ax.axhline(promedio_general, color='red', linestyle='--', 
                  label=f'Promedio general: €{promedio_general:.0f}')
        ax.legend()
        
        self.figure.tight_layout()
        
    def grafico_tendencias(self):
        """Genera gráfico de tendencias (simulado)"""
        ax = self.figure.add_subplot(111)
        
        # Simular evolución temporal
        meses = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun']
        
        # Para cada empleado seleccionado, simular tendencia
        items = self.lista_empleados.selectedItems()
        if not items:
            items = [self.lista_empleados.item(i) for i in range(min(3, self.lista_empleados.count()))]
            
        for item in items:
            nombre = item.text().split(' - ')[0]
            if nombre in self.empleados:
                empleado = self.empleados[nombre]
                salario_base = empleado.get_salario_total()
                
                # Simular variación mensual
                variacion = np.random.normal(0, 50, len(meses))
                salarios = [salario_base + sum(variacion[:i+1]) for i in range(len(meses))]
                
                ax.plot(meses, salarios, '-o', label=nombre, linewidth=2)
                
        ax.set_xlabel('Mes')
        ax.set_ylabel('Salario Total (€)')
        ax.set_title('Tendencias Salariales (Simulación)')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        self.figure.tight_layout()
        
    def grafico_matriz_equidad(self):
        """Genera una matriz de equidad salarial"""
        ax = self.figure.add_subplot(111)
        
        # Crear matriz de comparación
        empleados_lista = list(self.empleados.values())
        n_empleados = len(empleados_lista)
        
        if n_empleados > 10:
            # Limitar a los primeros 10 para legibilidad
            empleados_lista = empleados_lista[:10]
            n_empleados = 10
            
        matriz = np.zeros((n_empleados, n_empleados))
        
        for i in range(n_empleados):
            for j in range(n_empleados):
                sal_i = empleados_lista[i].get_salario_total()
                sal_j = empleados_lista[j].get_salario_total()
                # Ratio salarial
                matriz[i, j] = (sal_i / sal_j) if sal_j > 0 else 1
                
        # Crear heatmap
        im = ax.imshow(matriz, cmap='RdYlGn', aspect='auto', vmin=0.5, vmax=1.5)
        
        # Configurar ejes
        nombres = [emp.nombre.split()[0] for emp in empleados_lista]  # Solo primer nombre
        ax.set_xticks(np.arange(n_empleados))
        ax.set_yticks(np.arange(n_empleados))
        ax.set_xticklabels(nombres, rotation=45, ha='right')
        ax.set_yticklabels(nombres)
        
        # Añadir valores en las celdas
        for i in range(n_empleados):
            for j in range(n_empleados):
                text = ax.text(j, i, f'{matriz[i, j]:.2f}',
                             ha="center", va="center", color="black", fontsize=8)
                             
        ax.set_title('Matriz de Equidad Salarial (Ratios)')
        
        # Añadir colorbar
        cbar = self.figure.colorbar(im, ax=ax)
        cbar.set_label('Ratio Salarial', rotation=270, labelpad=15)
        
        self.figure.tight_layout()
        
    def generar_informe_equidad(self):
        """Genera un informe detallado de equidad salarial"""
        from PyQt5.QtWidgets import QDialog, QTextEdit, QPushButton
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Informe de Equidad Salarial")
        dialog.setModal(True)
        dialog.resize(800, 600)
        
        layout = QVBoxLayout(dialog)
        
        # Área de texto para el informe
        texto_informe = QTextEdit()
        texto_informe.setReadOnly(True)
        
        # Generar informe
        informe = self.crear_informe_equidad()
        texto_informe.setHtml(informe)
        
        layout.addWidget(texto_informe)
        
        # Botones
        layout_botones = QHBoxLayout()
        
        btn_exportar = QPushButton("📄 Exportar a PDF")
        btn_exportar.clicked.connect(lambda: self.exportar_informe_pdf(informe))
        layout_botones.addWidget(btn_exportar)
        
        btn_cerrar = QPushButton("Cerrar")
        btn_cerrar.clicked.connect(dialog.accept)
        layout_botones.addWidget(btn_cerrar)
        
        layout.addLayout(layout_botones)
        
        dialog.exec_()
        
    def crear_informe_equidad(self):
        """Crea el contenido del informe de equidad"""
        html = """
        <html>
        <head>
            <style>
                body { font-family: Arial, sans-serif; }
                h1 { color: #2196F3; }
                h2 { color: #4CAF50; }
                table { border-collapse: collapse; width: 100%; margin: 20px 0; }
                th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                th { background-color: #f2f2f2; }
                .good { background-color: #c8e6c9; }
                .warning { background-color: #fff3cd; }
                .bad { background-color: #f8d7da; }
            </style>
        </head>
        <body>
        """
        
        html += "<h1>Informe de Equidad Salarial</h1>"
        html += f"<p><strong>Fecha:</strong> {datetime.now().strftime('%d/%m/%Y')}</p>"
        html += f"<p><strong>Total empleados analizados:</strong> {len(self.empleados)}</p>"
        
        # Resumen general
        salarios = [emp.get_salario_total() for emp in self.empleados.values()]
        
        html += "<h2>1. Resumen General</h2>"
        html += "<table>"
        html += "<tr><th>Métrica</th><th>Valor</th></tr>"
        html += f"<tr><td>Salario promedio</td><td>€ {np.mean(salarios):.2f}</td></tr>"
        html += f"<tr><td>Salario mediano</td><td>€ {np.median(salarios):.2f}</td></tr>"
        html += f"<tr><td>Desviación estándar</td><td>€ {np.std(salarios):.2f}</td></tr>"
        html += f"<tr><td>Rango salarial</td><td>€ {min(salarios):.2f} - € {max(salarios):.2f}</td></tr>"
        
        coef_var = (np.std(salarios) / np.mean(salarios) * 100) if np.mean(salarios) > 0 else 0
        clase = 'good' if coef_var < 20 else 'warning' if coef_var < 30 else 'bad'
        html += f"<tr class='{clase}'><td>Coeficiente de variación</td><td>{coef_var:.1f}%</td></tr>"
        html += "</table>"
        
        # Análisis por departamento
        html += "<h2>2. Análisis por Departamento</h2>"
        html += "<table>"
        html += "<tr><th>Departamento</th><th>Empleados</th><th>Salario Promedio</th><th>Desv. Est.</th><th>Estado</th></tr>"
        
        dept_stats = {}
        for emp in self.empleados.values():
            dept = emp.departamento or "Sin departamento"
            if dept not in dept_stats:
                dept_stats[dept] = []
            dept_stats[dept].append(emp.get_salario_total())
            
        for dept, salarios_dept in sorted(dept_stats.items()):
            promedio = np.mean(salarios_dept)
            desviacion = np.std(salarios_dept)
            cv = (desviacion / promedio * 100) if promedio > 0 else 0
            
            if cv < 15:
                estado = "✅ Excelente"
                clase = "good"
            elif cv < 25:
                estado = "⚠️ Moderado"
                clase = "warning"
            else:
                estado = "❌ Revisar"
                clase = "bad"
                
            html += f"<tr class='{clase}'>"
            html += f"<td>{dept}</td>"
            html += f"<td>{len(salarios_dept)}</td>"
            html += f"<td>€ {promedio:.2f}</td>"
            html += f"<td>€ {desviacion:.2f}</td>"
            html += f"<td>{estado}</td>"
            html += "</tr>"
            
        html += "</table>"
        
        # Recomendaciones
        html += "<h2>3. Recomendaciones</h2>"
        html += "<ul>"
        
        if coef_var > 30:
            html += "<li><strong>Alta disparidad salarial detectada.</strong> Se recomienda revisar la política salarial.</li>"
            
        # Verificar si hay departamentos con alta variación
        for dept, salarios_dept in dept_stats.items():
            if len(salarios_dept) > 1:
                cv_dept = (np.std(salarios_dept) / np.mean(salarios_dept) * 100) if np.mean(salarios_dept) > 0 else 0
                if cv_dept > 25:
                    html += f"<li>El departamento <strong>{dept}</strong> presenta alta variación salarial ({cv_dept:.1f}%). Revisar criterios de compensación.</li>"
                    
        html += "<li>Establecer bandas salariales claras por puesto y nivel.</li>"
        html += "<li>Realizar revisiones salariales periódicas (al menos anuales).</li>"
        html += "<li>Documentar criterios objetivos para incrementos y promociones.</li>"
        html += "</ul>"
        
        html += "</body></html>"
        
        return html
        
    def exportar_informe_pdf(self, html_content):
        """Exporta el informe a PDF"""
        QMessageBox.information(
            self,
            "Función en desarrollo",
            "La exportación a PDF se implementará próximamente.\n"
            "Por ahora, puede copiar el contenido del informe."
        )
        
    def exportar_comparacion(self):
        """Exporta la comparación actual a Excel"""
        archivo, _ = QFileDialog.getSaveFileName(
            self,
            'Exportar comparación',
            'comparacion_empleados.xlsx',
            'Excel (*.xlsx)'
        )
        
        if archivo:
            try:
                # Crear DataFrame desde la tabla de comparación
                datos = []
                columnas = []
                
                # Obtener encabezados
                for col in range(self.tabla_comparacion.columnCount()):
                    header = self.tabla_comparacion.horizontalHeaderItem(col)
                    columnas.append(header.text() if header else f'Columna {col}')
                    
                # Obtener datos
                for row in range(self.tabla_comparacion.rowCount()):
                    fila = []
                    for col in range(self.tabla_comparacion.columnCount()):
                        item = self.tabla_comparacion.item(row, col)
                        fila.append(item.text() if item else '')
                    datos.append(fila)
                    
                df_comparacion = pd.DataFrame(datos, columns=columnas)
                
                # Crear resumen de empleados
                resumen_data = []
                for nombre, emp in self.empleados.items():
                    resumen_data.append({
                        'Nombre': nombre,
                        'Departamento': emp.departamento,
                        'Puesto': emp.puesto,
                        'Salario Base': emp.salario_base,
                        'Total Pluses': sum(emp.pluses.values()),
                        'Total Deducciones': sum(emp.deducciones.values()),
                        'Salario Bruto': emp.get_salario_total(),
                        'Salario Neto Estimado': emp.get_salario_neto()
                    })
                    
                df_resumen = pd.DataFrame(resumen_data)
                
                # Guardar en Excel
                with pd.ExcelWriter(archivo, engine='openpyxl') as writer:
                    df_comparacion.to_excel(writer, sheet_name='Comparación', index=False)
                    df_resumen.to_excel(writer, sheet_name='Resumen Empleados', index=False)
                    
                    # Agregar hoja de estadísticas
                    stats_text = self.texto_estadisticas.toPlainText()
                    df_stats = pd.DataFrame({'Estadísticas': [stats_text]})
                    df_stats.to_excel(writer, sheet_name='Estadísticas', index=False)
                    
                QMessageBox.information(
                    self,
                    'Exportación exitosa',
                    f'La comparación se ha exportado correctamente a:\n{archivo}'
                )
                
            except Exception as e:
                QMessageBox.critical(
                    self,
                    'Error al exportar',
                    f'Error al exportar la comparación:\n{str(e)}'
                )
                
    def analizar_politica_salarial(self):
        """Analiza la política salarial de la empresa"""
        QMessageBox.information(
            self,
            "Análisis de Política Salarial",
            "Esta función analizará:\n\n"
            "• Coherencia en las bandas salariales\n"
            "• Competitividad con el mercado\n"
            "• Cumplimiento de convenios\n"
            "• Recomendaciones de mejora\n\n"
            "Función en desarrollo."
        )import pandas as pd
import numpy as np
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                            QTableWidget, QTableWidgetItem, QLabel, QComboBox,
                            QGroupBox, QLineEdit, QDoubleSpinBox, QCheckBox,
                            QMessageBox, QFileDialog, QTextEdit, QListWidget,
                            QListWidgetItem, QSplitter)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QColor, QFont
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class EmpleadoData:
    """Clase para almacenar datos de un empleado"""
    def __init__(self, nombre, departamento="", puesto=""):
        self.nombre = nombre
        self.departamento = departamento
        self.puesto = puesto
        self.salario_base = 0
        self.pluses = {}
        self.deducciones = {}
        self.datos_adicionales = {}
        
    def get_salario_total(self):
        """Calcula el salario total del empleado"""
        total_pluses = sum(self.pluses.values())
        total_deducciones = sum(self.deducciones.values())
        return self.salario_base + total_pluses - total_deducciones
        
    def get_salario_neto(self):
        """Calcula el salario neto estimado"""
        bruto = self.get_salario_total()
        # Estimación simplificada de retenciones
        if bruto <= 1000:
            retencion = 0.10
        elif bruto <= 2000:
            retencion = 0.15
        elif bruto <= 3000:
            retencion = 0.20
        else:
            retencion = 0.25
        return bruto * (1 - retencion)

class ComparacionEmpleadosWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.empleados = {}
        self.initUI()
        
    def initUI(self):
        layout_principal = QVBoxLayout(self)
        
        # Splitter principal
        splitter = QSplitter(Qt.Horizontal)
        
        # Panel izquierdo - Gestión de empleados
        panel_empleados = QWidget()
        layout_empleados = QVBoxLayout(panel_empleados)
        
        # Título
        lbl_empleados = QLabel("Empleados")
        lbl_empleados.setFont(QFont('Arial', 12, QFont.Bold))
        layout_empleados.addWidget(lbl_empleados)
        
        # Botones de gestión
        layout_botones = QHBoxLayout()
        
        btn_agregar = QPushButton("➕ Agregar")
        btn_agregar.clicked.connect(self.agregar_empleado)
        layout_botones.addWidget(btn_agregar)
        
        btn_editar = QPushButton("✏️ Editar")
        btn