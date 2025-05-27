# Concepto
        self.tabla_conceptos.setItem(row, 1, QTableWidgetItem(concepto))
        
        # Tipo
        item_tipo = QTableWidgetItem(tipo)
        if tipo == "Devengo":
            item_tipo.setBackground(QColor(200, 230, 201))
        else:
            item_tipo.setBackground(QColor(255, 205, 210))
        self.tabla_conceptos.setItem(row, 2, item_tipo)
        
        # Base
        self.tabla_conceptos.setItem(row, 3, QTableWidgetItem(f"{base:.2f}"))
        
        # Cantidad
        self.tabla_conceptos.setItem(row, 4, QTableWidgetItem(f"{cantidad:.4f}"))
        
        # Importe
        item_importe = QTableWidgetItem(f"{importe:.2f}")
        if importe < 0:
            item_importe.setForeground(QColor(244, 67, 54))
        else:
            item_importe.setForeground(QColor(76, 175, 80))
        self.tabla_conceptos.setItem(row, 5, item_importe)
        
        # Botón eliminar
        btn_eliminar = QPushButton("❌")
        btn_eliminar.clicked.connect(lambda: self.eliminar_concepto(row))
        self.tabla_conceptos.setCellWidget(row, 6, btn_eliminar)
        
    def eliminar_concepto(self, row):
        """Elimina un concepto de la tabla"""
        # Buscar la fila actual del botón
        for i in range(self.tabla_conceptos.rowCount()):
            btn = self.tabla_conceptos.cellWidget(i, 6)
            if btn and btn.clicked == self.sender().clicked:
                self.tabla_conceptos.removeRow(i)
                break
        self.calcular_totales()
        
    def eliminar_concepto_seleccionado(self):
        """Elimina el concepto seleccionado con la tecla Delete"""
        row = self.tabla_conceptos.currentRow()
        if row >= 0:
            self.tabla_conceptos.removeRow(row)
            self.calcular_totales()
            
    def menu_contextual(self, position):
        """Muestra menú contextual en la tabla"""
        menu = QMenu()
        
        # Acciones del menú
        accion_editar = QAction("✏️ Editar", self)
        accion_editar.triggered.connect(self.editar_concepto)
        menu.addAction(accion_editar)
        
        accion_duplicar = QAction("📋 Duplicar", self)
        accion_duplicar.triggered.connect(self.duplicar_concepto)
        menu.addAction(accion_duplicar)
        
        menu.addSeparator()
        
        accion_eliminar = QAction("❌ Eliminar", self)
        accion_eliminar.triggered.connect(self.eliminar_concepto_seleccionado)
        menu.addAction(accion_eliminar)
        
        menu.exec_(self.tabla_conceptos.viewport().mapToGlobal(position))
        
    def editar_concepto(self):
        """Edita el concepto seleccionado"""
        row = self.tabla_conceptos.currentRow()
        if row < 0:
            return
            
        # Hacer las celdas editables temporalmente
        for col in range(5):  # Columnas 0-4 son editables
            item = self.tabla_conceptos.item(row, col)
            if item:
                item.setFlags(item.flags() | Qt.ItemIsEditable)
                
        # Conectar señal para recalcular al terminar de editar
        self.tabla_conceptos.itemChanged.connect(self.concepto_editado)
        
    def concepto_editado(self, item):
        """Maneja cuando se edita un concepto"""
        # Desconectar la señal
        self.tabla_conceptos.itemChanged.disconnect(self.concepto_editado)
        
        # Recalcular el importe
        row = item.row()
        try:
            base = float(self.tabla_conceptos.item(row, 3).text())
            cantidad = float(self.tabla_conceptos.item(row, 4).text())
            tipo = self.tabla_conceptos.item(row, 2).text()
            
            if cantidad <= 1:
                importe = base * cantidad
            else:
                importe = cantidad
                
            if tipo == "Deducción":
                importe = -abs(importe)
                
            self.tabla_conceptos.item(row, 5).setText(f"{importe:.2f}")
            
        except ValueError:
            pass
            
        self.calcular_totales()
        
    def duplicar_concepto(self):
        """Duplica el concepto seleccionado"""
        row = self.tabla_conceptos.currentRow()
        if row < 0:
            return
            
        # Obtener datos del concepto
        codigo = self.tabla_conceptos.item(row, 0).text()
        concepto = self.tabla_conceptos.item(row, 1).text() + " (copia)"
        tipo = self.tabla_conceptos.item(row, 2).text()
        base = float(self.tabla_conceptos.item(row, 3).text())
        cantidad = float(self.tabla_conceptos.item(row, 4).text())
        importe = float(self.tabla_conceptos.item(row, 5).text())
        
        # Agregar el duplicado
        self.agregar_concepto_tabla(codigo, concepto, tipo, base, cantidad, importe)
        self.calcular_totales()
        
    def agregar_conceptos_multiples(self):
        """Permite agregar múltiples conceptos de una vez"""
        from PyQt5.QtWidgets import QDialog, QTableWidget, QDialogButtonBox
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Agregar Múltiples Conceptos")
        dialog.setModal(True)
        dialog.resize(800, 400)
        
        layout = QVBoxLayout(dialog)
        
        # Instrucciones
        instrucciones = QLabel("Seleccione los conceptos que desea agregar:")
        layout.addWidget(instrucciones)
        
        # Tabla de conceptos disponibles
        tabla = QTableWidget()
        tabla.setColumnCount(4)
        tabla.setHorizontalHeaderLabels(['Seleccionar', 'Código', 'Concepto', 'Tipo'])
        
        # Conceptos predefinidos
        conceptos_disponibles = [
            ('020', 'Antigüedad', 'Devengo'),
            ('021', 'Plus Nocturnidad', 'Devengo'),
            ('022', 'Plus Peligrosidad', 'Devengo'),
            ('023', 'Plus Convenio', 'Devengo'),
            ('024', 'Horas Extraordinarias', 'Devengo'),
            ('025', 'Gratificación', 'Devengo'),
            ('026', 'Comisiones', 'Devengo'),
            ('027', 'Incentivos', 'Devengo'),
            ('028', 'Plus Idiomas', 'Devengo'),
            ('029', 'Plus Disponibilidad', 'Devengo'),
            ('102', 'Desempleo', 'Deducción'),
            ('103', 'Formación Profesional', 'Deducción'),
            ('104', 'Horas Extra Fuerza Mayor', 'Deducción'),
            ('202', 'Anticipo', 'Deducción'),
            ('203', 'Préstamo Empresa', 'Deducción'),
            ('204', 'Embargo', 'Deducción'),
            ('205', 'Cuota Sindical', 'Deducción')
        ]
        
        tabla.setRowCount(len(conceptos_disponibles))
        
        for i, (codigo, concepto, tipo) in enumerate(conceptos_disponibles):
            # Checkbox
            check = QCheckBox()
            widget = QWidget()
            layout_check = QHBoxLayout(widget)
            layout_check.addWidget(check)
            layout_check.setAlignment(Qt.AlignCenter)
            layout_check.setContentsMargins(0, 0, 0, 0)
            tabla.setCellWidget(i, 0, widget)
            
            # Datos
            tabla.setItem(i, 1, QTableWidgetItem(codigo))
            tabla.setItem(i, 2, QTableWidgetItem(concepto))
            tabla.setItem(i, 3, QTableWidgetItem(tipo))
            
        layout.addWidget(tabla)
        
        # Botones
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, dialog
        )
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)
        
        if dialog.exec_() == QDialog.Accepted:
            # Agregar conceptos seleccionados
            for i in range(tabla.rowCount()):
                widget = tabla.cellWidget(i, 0)
                if widget:
                    check = widget.findChild(QCheckBox)
                    if check and check.isChecked():
                        codigo = tabla.item(i, 1).text()
                        concepto = tabla.item(i, 2).text()
                        tipo = tabla.item(i, 3).text()
                        
                        # Valores por defecto
                        base = 0.0
                        cantidad = 1.0
                        importe = 0.0
                        
                        self.agregar_concepto_tabla(codigo, concepto, tipo, base, cantidad, importe)
                        
            self.calcular_totales()
            
    def importar_conceptos(self):
        """Importa conceptos desde un archivo"""
        archivo, _ = QFileDialog.getOpenFileName(
            self,
            'Importar conceptos',
            '',
            'CSV (*.csv);;Excel (*.xlsx *.xls)'
        )
        
        if archivo:
            try:
                if archivo.endswith('.csv'):
                    df = pd.read_csv(archivo)
                else:
                    df = pd.read_excel(archivo)
                    
                # Verificar columnas requeridas
                columnas_requeridas = ['Codigo', 'Concepto', 'Tipo', 'Base', 'Cantidad']
                if not all(col in df.columns for col in columnas_requeridas):
                    QMessageBox.warning(
                        self,
                        "Formato incorrecto",
                        f"El archivo debe contener las columnas: {', '.join(columnas_requeridas)}"
                    )
                    return
                    
                # Importar conceptos
                for _, row in df.iterrows():
                    codigo = str(row['Codigo'])
                    concepto = str(row['Concepto'])
                    tipo = str(row['Tipo'])
                    base = float(row['Base'])
                    cantidad = float(row['Cantidad'])
                    
                    # Calcular importe
                    if cantidad <= 1:
                        importe = base * cantidad
                    else:
                        importe = cantidad
                        
                    if tipo == "Deducción":
                        importe = -abs(importe)
                        
                    self.agregar_concepto_tabla(codigo, concepto, tipo, base, cantidad, importe)
                    
                self.calcular_totales()
                
                QMessageBox.information(
                    self,
                    "Importación exitosa",
                    f"Se han importado {len(df)} conceptos correctamente."
                )
                
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Error al importar",
                    f"Error al importar el archivo:\n{str(e)}"
                )
                
    def limpiar_tabla(self):
        """Limpia todos los conceptos de la tabla"""
        respuesta = QMessageBox.question(
            self,
            "Confirmar limpieza",
            "¿Está seguro de que desea eliminar todos los conceptos?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if respuesta == QMessageBox.Yes:
            self.tabla_conceptos.setRowCount(0)
            self.calcular_totales()
            
    def calcular_totales(self):
        """Calcula y actualiza todos los totales"""
        total_devengos = 0
        total_deducciones = 0
        salario_base = 0
        complementos = 0
        seg_social = 0
        irpf = 0
        
        # Recorrer la tabla
        for row in range(self.tabla_conceptos.rowCount()):
            tipo = self.tabla_conceptos.item(row, 2).text()
            concepto = self.tabla_conceptos.item(row, 1).text()
            importe = float(self.tabla_conceptos.item(row, 5).text())
            
            if tipo == "Devengo":
                total_devengos += importe
                
                if "base" in concepto.lower() or "salario" in concepto.lower():
                    salario_base += importe
                else:
                    complementos += importe
                    
            else:  # Deducción
                total_deducciones += abs(importe)
                
                if "social" in concepto.lower() or "s.s." in concepto.lower():
                    seg_social += abs(importe)
                elif "irpf" in concepto.lower():
                    irpf += abs(importe)
                    
        # Calcular líquido
        liquido = total_devengos - total_deducciones
        
        # Actualizar labels
        self.lbl_total_devengos.setText(f"Total Devengos: € {total_devengos:.2f}")
        self.lbl_salario_base.setText(f"Salario Base: € {salario_base:.2f}")
        self.lbl_complementos.setText(f"Complementos: € {complementos:.2f}")
        
        self.lbl_total_deducciones.setText(f"Total Deducciones: € {total_deducciones:.2f}")
        self.lbl_seg_social.setText(f"Seg. Social: € {seg_social:.2f}")
        self.lbl_irpf.setText(f"IRPF: € {irpf:.2f}")
        
        self.lbl_liquido.setText(f"LÍQUIDO A PERCIBIR: € {liquido:.2f}")
        self.lbl_base_cotizacion.setText(f"Base Cotización: € {total_devengos:.2f}")
        self.lbl_base_irpf.setText(f"Base IRPF: € {total_devengos:.2f}")
        
        # Actualizar datos actuales
        self.datos_actuales = {
            'empleado': self.input_empleado.text(),
            'departamento': self.input_departamento.text(),
            'fecha': self.date_nomina.date().toString("yyyy-MM-dd"),
            'tipo_nomina': self.combo_tipo_nomina.currentText(),
            'total_devengos': total_devengos,
            'total_deducciones': total_deducciones,
            'liquido': liquido,
            'conceptos': self.obtener_conceptos_tabla()
        }
        
    def obtener_conceptos_tabla(self):
        """Obtiene todos los conceptos de la tabla como lista"""
        conceptos = []
        
        for row in range(self.tabla_conceptos.rowCount()):
            concepto = {
                'codigo': self.tabla_conceptos.item(row, 0).text(),
                'descripcion': self.tabla_conceptos.item(row, 1).text(),
                'tipo': self.tabla_conceptos.item(row, 2).text(),
                'base': float(self.tabla_conceptos.item(row, 3).text()),
                'cantidad': float(self.tabla_conceptos.item(row, 4).text()),
                'importe': float(self.tabla_conceptos.item(row, 5).text())
            }
            conceptos.append(concepto)
            
        return conceptos
        
    def validar_automaticamente(self):
        """Realiza validaciones automáticas de la nómina"""
        errores = []
        advertencias = []
        
        # Validar que hay conceptos
        if self.tabla_conceptos.rowCount() == 0:
            errores.append("No hay conceptos en la nómina")
            
        # Validar que hay al menos un devengo
        tiene_devengo = False
        for row in range(self.tabla_conceptos.rowCount()):
            if self.tabla_conceptos.item(row, 2).text() == "Devengo":
                tiene_devengo = True
                break
                
        if not tiene_devengo:
            errores.append("La nómina debe tener al menos un devengo")
            
        # Validar porcentajes de cotización
        total_devengos = sum(float(self.tabla_conceptos.item(row, 5).text()) 
                           for row in range(self.tabla_conceptos.rowCount())
                           if self.tabla_conceptos.item(row, 2).text() == "Devengo")
                           
        seg_social = sum(abs(float(self.tabla_conceptos.item(row, 5).text()))
                        for row in range(self.tabla_conceptos.rowCount())
                        if "social" in self.tabla_conceptos.item(row, 1).text().lower())
                        
        if total_devengos > 0:
            porcentaje_ss = (seg_social / total_devengos) * 100
            if porcentaje_ss < 4 or porcentaje_ss > 7:
                advertencias.append(f"El porcentaje de Seg. Social ({porcentaje_ss:.2f}%) parece inusual")
                
        # Validar IRPF
        irpf = sum(abs(float(self.tabla_conceptos.item(row, 5).text()))
                  for row in range(self.tabla_conceptos.rowCount())
                  if "irpf" in self.tabla_conceptos.item(row, 1).text().lower())
                  
        if total_devengos > 0:
            porcentaje_irpf = (irpf / total_devengos) * 100
            if porcentaje_irpf < 2:
                advertencias.append(f"El porcentaje de IRPF ({porcentaje_irpf:.2f}%) parece muy bajo")
            elif porcentaje_irpf > 45:
                advertencias.append(f"El porcentaje de IRPF ({porcentaje_irpf:.2f}%) parece muy alto")
                
        # Validar datos del empleado
        if not self.input_empleado.text():
            errores.append("Falta el nombre del empleado")
            
        # Mostrar resultados
        if errores or advertencias:
            mensaje = ""
            
            if errores:
                mensaje += "ERRORES:\n"
                for error in errores:
                    mensaje += f"❌ {error}\n"
                mensaje += "\n"
                
            if advertencias:
                mensaje += "ADVERTENCIAS:\n"
                for advertencia in advertencias:
                    mensaje += f"⚠️ {advertencia}\n"
                    
            QMessageBox.warning(self, "Resultado de la validación", mensaje)
            
            # Actualizar checks
            self.check_validacion_importes.setChecked(len(errores) == 0)
            self.check_validacion_calculos.setChecked(True)
            self.check_validacion_normativa.setChecked(len(advertencias) == 0)
        else:
            QMessageBox.information(
                self,
                "Validación exitosa",
                "✅ La nómina ha pasado todas las validaciones correctamente."
            )
            
            # Marcar todos los checks
            self.check_validacion_importes.setChecked(True)
            self.check_validacion_calculos.setChecked(True)
            self.check_validacion_normativa.setChecked(True)
            
    def mostrar_vista_previa(self):
        """Muestra una vista previa de la nómina"""
        from PyQt5.QtWidgets import QDialog
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Vista Previa de Nómina")
        dialog.setModal(True)
        dialog.resize(600, 800)
        
        layout = QVBoxLayout(dialog)
        
        # Crear HTML de la nómina
        html = self.generar_html_nomina()
        
        # Mostrar en QTextEdit
        vista = QTextEdit()
        vista.setReadOnly(True)
        vista.setHtml(html)
        layout.addWidget(vista)
        
        # Botones
        layout_botones = QHBoxLayout()
        
        btn_imprimir = QPushButton("🖨️ Imprimir")
        btn_imprimir.clicked.connect(lambda: self.imprimir_nomina(html))
        layout_botones.addWidget(btn_imprimir)
        
        btn_cerrar = QPushButton("Cerrar")
        btn_cerrar.clicked.connect(dialog.accept)
        layout_botones.addWidget(btn_cerrar)
        
        layout.addLayout(layout_botones)
        
        dialog.exec_()
        
    def generar_html_nomina(self):
        """Genera el HTML de la nómina"""
        html = """
        <html>
        <head>
            <style>
                body { font-family: Arial, sans-serif; }
                .header { background-color: #f0f0f0; padding: 20px; margin-bottom: 20px; }
                h1 { color: #2196F3; margin: 0; }
                h2 { color: #4CAF50; }
                table { width: 100%; border-collapse: collapse; margin: 20px 0; }
                th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                th { background-color: #f2f2f2; font-weight: bold; }
                .devengo { background-color: #e8f5e9; }
                .deduccion { background-color: #ffebee; }
                .total { font-weight: bold; font-size: 1.1em; }
                .liquido { background-color: #e3f2fd; font-size: 1.2em; }
                .footer { margin-top: 40px; padding-top: 20px; border-top: 2px solid #ccc; }
            </style>
        </head>
        <body>
        """
        
        # Encabezado
        html += f"""
        <div class="header">
            <h1>NÓMINA</h1>
            <p><strong>Empleado:</strong> {self.input_empleado.text()}</p>
            <p><strong>Departamento:</strong> {self.input_departamento.text()}</p>
            <p><strong>Fecha:</strong> {self.date_nomina.date().toString('dd/MM/yyyy')}</p>
            <p><strong>Tipo:</strong> {self.combo_tipo_nomina.currentText()}</p>
        </div>
        """
        
        # Tabla de conceptos
        html += """
        <h2>Detalle de Conceptos</h2>
        <table>
            <tr>
                <th>Código</th>
                <th>Concepto</th>
                <th>Base</th>
                <th>Cantidad</th>
                <th>Importe</th>
            </tr>
        """
        
        # Devengos
        total_devengos = 0
        for row in range(self.tabla_conceptos.rowCount()):
            if self.tabla_conceptos.item(row, 2).text() == "Devengo":
                codigo = self.tabla_conceptos.item(row, 0).text()
                concepto = self.tabla_conceptos.item(row, 1).text()
                base = self.tabla_conceptos.item(row, 3).text()
                cantidad = self.tabla_conceptos.item(row, 4).text()
                importe = float(self.tabla_conceptos.item(row, 5).text())
                total_devengos += importe
                
                html += f"""
                <tr class="devengo">
                    <td>{codigo}</td>
                    <td>{concepto}</td>
                    <td>{base}</td>
                    <td>{cantidad}</td>
                    <td style="text-align: right;">€ {importe:.2f}</td>
                </tr>
                """
                
        html += f"""
        <tr class="total">
            <td colspan="4" style="text-align: right;">TOTAL DEVENGOS:</td>
            <td style="text-align: right;">€ {total_devengos:.2f}</td>
        </tr>
        """
        
        # Espacio
        html += '<tr><td colspan="5" style="border: none; height: 20px;"></td></tr>'
        
        # Deducciones
        total_deducciones = 0
        for row in range(self.tabla_conceptos.rowCount()):
            if self.tabla_conceptos.item(row, 2).text() == "Deducción":
                codigo = self.tabla_conceptos.item(row, 0).text()
                concepto = self.tabla_conceptos.item(row, 1).text()
                base = self.tabla_conceptos.item(row, 3).text()
                cantidad = self.tabla_conceptos.item(row, 4).text()
                importe = abs(float(self.tabla_conceptos.item(row, 5).text()))
                total_deducciones += importe
                
                html += f"""
                <tr class="deduccion">
                    <td>{codigo}</td>
                    <td>{concepto}</td>
                    <td>{base}</td>
                    <td>{cantidad}</td>
                    <td style="text-align: right;">€ {importe:.2f}</td>
                </tr>
                """
                
        html += f"""
        <tr class="total">
            <td colspan="4" style="text-align: right;">TOTAL DEDUCCIONES:</td>
            <td style="text-align: right;">€ {total_deducciones:.2f}</td>
        </tr>
        """
        
        # Líquido
        liquido = total_devengos - total_deducciones
        html += f"""
        <tr class="liquido">
            <td colspan="4" style="text-align: right;"><strong>LÍQUIDO A PERCIBIR:</strong></td>
            <td style="text-align: right;"><strong>€ {liquido:.2f}</strong></td>
        </tr>
        </table>
        """
        
        # Notas
        if self.texto_notas.toPlainText():
            html += f"""
            <div class="footer">
                <h3>Notas:</h3>
                <p>{self.texto_notas.toPlainText()}</p>
            </div>
            """
            
        html += "</body></html>"
        
        return html
        
    def imprimir_nomina(self, html):
        """Imprime la nómina"""
        from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
        from PyQt5.QtGui import QTextDocument
        
        printer = QPrinter(QPrinter.HighResolution)
        dialog = QPrintDialog(printer, self)
        
        if dialog.exec_() == QPrintDialog.Accepted:
            document = QTextDocument()
            document.setHtml(html)
            document.print_(printer)
            
    def guardar_nomina(self):
        """Guarda la nómina actual"""
        if not self.input_empleado.text():
            QMessageBox.warning(self, "Datos incompletos", "Debe especificar el nombre del empleado")
            return
            
        archivo, _ = QFileDialog.getSaveFileName(
            self,
            'Guardar nómina',
            f'nomina_{self.input_empleado.text()}_{self.date_nomina.date().toString("yyyyMM")}.json',
            'JSON (*.json);;Excel (*.xlsx)'
        )
        
        if archivo:
            try:
                # Actualizar datos actuales
                self.calcular_totales()
                
                if archivo.endswith('.json'):
                    # Guardar como JSON
                    with open(archivo, 'w', encoding='utf-8') as f:
                        json.dump(self.datos_actuales, f, ensure_ascii=False, indent=2)
                else:
                    # Guardar como Excel
                    df_conceptos = pd.DataFrame(self.datos_actuales['conceptos'])
                    df_resumen = pd.DataFrame([{
                        'Empleado': self.datos_actuales['empleado'],
                        'Fecha': self.datos_actuales['fecha'],
                        'Total Devengos': self.datos_actuales['total_devengos'],
                        'Total Deducciones': self.datos_actuales['total_deducciones'],
                        'Líquido': self.datos_actuales['liquido']
                    }])
                    
                    with pd.ExcelWriter(archivo, engine='openpyxl') as writer:
                        df_resumen.to_excel(writer, sheet_name='Resumen', index=False)
                        df_conceptos.to_excel(writer, sheet_name='Conceptos', index=False)
                        
                # Emitir señal
                self.datos_guardados.emit(self.datos_actuales)
                
                QMessageBox.information(
                    self,
                    'Guardado exitoso',
                    f'La nómina se ha guardado correctamente en:\n{archivo}'
                )
                
            except Exception as e:
                QMessageBox.critical(
                    self,
                    'Error al guardar',
                    f'Error al guardar la nómina:\n{str(e)}'
                )
                
    def exportar_nomina(self):
        """Exporta la nómina a diferentes formatos"""
        from PyQt5.QtWidgets import QDialog, QRadioButton, QButtonGroup
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Exportar Nómina")
        dialog.setModal(True)
        
        layout = QVBoxLayout(dialog)
        
        # Opciones de formato
        layout.addWidget(QLabel("Seleccione el formato de exportación:"))
        
        grupo_formato = QButtonGroup()
        
        radio_pdf = QRadioButton("PDF")
        radio_pdf.setChecked(True)
        grupo_formato.addButton(radio_pdf)
        layout.addWidget(radio_pdf)
        
        radio_excel = QRadioButton("Excel")
        grupo_formato.addButton(radio_excel)
        layout.addWidget(radio_excel)
        
        radio_csv = QRadioButton("CSV")
        grupo_formato.addButton(radio_csv)
        layout.addWidget(radio_csv)
        
        radio_xml = QRadioButton("XML (formato SEPA)")
        grupo_formato.addButton(radio_xml)
        layout.addWidget(radio_xml)
        
        # Botones
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, dialog
        )
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)
        
        if dialog.exec_() == QDialog.Accepted:
            if radio_pdf.isChecked():
                self.exportar_pdf()
            elif radio_excel.isChecked():
                self.exportar_excel()
            elif radio_csv.isChecked():
                self.exportar_csv()
            elif radio_xml.isChecked():
                self.exportar_xml()
                
    def exportar_pdf(self):
        """Exporta la nómina a PDF"""
        archivo, _ = QFileDialog.getSaveFileName(
            self,
            'Exportar a PDF',
            f'nomina_{self.input_empleado.text()}_{self.date_nomina.date().toString("yyyyMM")}.pdf',
            'PDF (*.pdf)'
        )
        
        if archivo:
            try:
                from PyQt5.QtPrintSupport import QPrinter
                from PyQt5.QtGui import QTextDocument
                
                printer = QPrinter(QPrinter.HighResolution)
                printer.setOutputFormat(QPrinter.PdfFormat)
                printer.setOutputFileName(archivo)
                
                document = QTextDocument()
                document.setHtml(self.generar_html_nomina())
                document.print_(printer)
                
                QMessageBox.information(
                    self,
                    'Exportación exitosa',
                    f'La nómina se ha exportado a PDF:\n{archivo}'
                )
                
            except Exception as e:
                QMessageBox.critical(
                    self,
                    'Error al exportar',
                    f'Error al exportar a PDF:\n{str(e)}'
                )
                
    def exportar_excel(self):
        """Exporta la nómina a Excel"""
        archivo, _ = QFileDialog.getSaveFileName(
            self,
            'Exportar a Excel',
            f'nomina_{self.input_empleado.text()}_{self.date_nomina.date().toString("yyyyMM")}.xlsx',
            'Excel (*.xlsx)'
        )
        
        if archivo:
            self.guardar_nomina()  # Reutilizar la función existente
            
    def exportar_csv(self):
        """Exporta los conceptos a CSV"""
        archivo, _ = QFileDialog.getSaveFileName(
            self,
            'Exportar a CSV',
            f'conceptos_nomina_{self.date_nomina.date().toString("yyyyMM")}.csv',
            'CSV (*.csv)'
        )
        
        if archivo:
            try:
                conceptos = self.obtener_conceptos_tabla()
                df = pd.DataFrame(conceptos)
                df.to_csv(archivo, index=False, encoding='utf-8')
                
                QMessageBox.information(
                    self,
                    'Exportación exitosa',
                    f'Los conceptos se han exportado a CSV:\n{archivo}'
                )
                
            except Exception as e:
                QMessageBox.critical(
                    self,
                    'Error al exportar',
                    f'Error al exportar a CSV:\n{str(e)}'
                )
                
    def exportar_xml(self):
        """Exporta la nómina a formato XML"""
        QMessageBox.information(
            self,
            'Función en desarrollo',
            'La exportación a formato XML/SEPA se implementará próximamente.'
        )
        
    def nueva_entrada(self):
        """Crea una nueva entrada limpiando el formulario"""
        respuesta = QMessageBox.question(
            self,
            'Nueva entrada',
            '¿Desea guardar los cambios actuales antes de crear una nueva entrada?',
            QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
            QMessageBox.Cancel
        )
        
        if respuesta == QMessageBox.Cancel:
            return
        elif respuesta == QMessageBox.Yes:
            self.guardar_nomina()
            
        # Limpiar formulario
        self.input_empleado.clear()
        self.input_departamento.clear()
        self.date_nomina.setDate(QDate.currentDate())
        self.combo_tipo_nomina.setCurrentIndex(0)
        self.combo_plantilla.setCurrentIndex(0)
        self.tabla_conceptos.setRowCount(0)
        self.texto_notas.clear()
        
        # Desmarcar validaciones
        self.check_validacion_importes.setChecked(False)
        self.check_validacion_calculos.setChecked(False)
        self.check_validacion_normativa.setChecked(False)
        
        # Cargar plantilla básica si está seleccionada
        if self.combo_plantilla.currentText() == "Plantilla básica":
            self.cargar_plantilla_basica()
        else:
            self.calcular_totales()
            
    def cargar_plantilla(self):
        """Carga una plantilla seleccionada"""
        plantilla = self.combo_plantilla.currentText()
        
        if plantilla == "Nueva entrada":
            self.tabla_conceptos.setRowCount(0)
        elif plantilla == "Plantilla básica":
            self.cargar_plantilla_basica()
        elif plantilla == "Plantilla completa":
            self.cargar_plantilla_completa()
            
        self.calcular_totales()
        
    def cargar_plantilla_completa(self):
        """Carga una plantilla completa con más conceptos"""
        conceptos_completos = [
            ('001', 'Salario Base', 'Devengo', 2000.00, 1, 2000.00),
            ('010', 'Plus Transporte', 'Devengo', 100.00, 1, 100.00),
            ('011', 'Plus Productividad', 'Devengo', 150.00, 1, 150.00),
            ('020', 'Antigüedad', 'Devengo', 60.00, 1, 60.00),
            ('023', 'Plus Convenio', 'Devengo', 80.00, 1, 80.00),
            ('101', 'Contingencias Comunes', 'Deducción', 2390.00, 0.047, -112.33),
            ('102', 'Desempleo', 'Deducción', 2390.00, 0.0155, -37.05),
            ('103', 'Formación Profesional', 'Deducción', 2390.00, 0.001, -2.39),
            ('201', 'IRPF', 'Deducción', 2390.00, 0.15, -358.50)
        ]
        
        self.tabla_conceptos.setRowCount(0)
        
        for concepto in conceptos_completos:
            self.agregar_concepto_tabla(*concepto)
            
    def guardar_como_plantilla(self):
        """Guarda la configuración actual como plantilla"""
        from PyQt5.QtWidgets import QInputDialog
        
        nombre, ok = QInputDialog.getText(
            self,
            'Guardar Plantilla',
            'Nombre de la plantilla:'
        )
        
        if ok and nombre:
            # Obtener conceptos actuales
            conceptos = self.obtener_conceptos_tabla()
            
            # Guardar en el diccionario de plantillas
            self.plantillas[nombre] = conceptos
            
            # Agregar al combo si no existe
            if self.combo_plantilla.findText(nombre) == -1:
                self.combo_plantilla.addItem(nombre)
                
            # Guardar plantillas en archivo
            try:
                with open('plantillas_nomina.json', 'w', encoding='utf-8') as f:
                    json.dump(self.plantillas, f, ensure_ascii=False, indent=2)
                    
                QMessageBox.information(
                    self,
                    'Plantilla guardada',
                    f'La plantilla "{nombre}" se ha guardado correctamente.'
                )
                
            except Exception as e:
                QMessageBox.warning(
                    self,
                    'Error al guardar',
                    f'No se pudo guardar la plantilla:\n{str(e)}'
                )import pandas as pd
import numpy as np
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                            QTableWidget, QTableWidgetItem, QLabel, QComboBox,
                            QGroupBox, QLineEdit, QDoubleSpinBox, QDateEdit,
                            QMessageBox, QFileDialog, QTextEdit, QCheckBox,
                            QHeaderView, QMenu, QAction, QSpinBox)
from PyQt5.QtCore import Qt, QDate, pyqtSignal
from PyQt5.QtGui import QColor, QFont, QKeySequence
import json
from datetime import datetime

class EntradaManualWidget(QWidget):
    # Señal para notificar cuando se guardan datos
    datos_guardados = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        self.datos_actuales = {}
        self.plantillas = {}
        self.initUI()
        
    def initUI(self):
        layout_principal = QVBoxLayout(self)
        
        # Panel superior - Información general
        panel_info = QGroupBox("Información General")
        layout_info = QVBoxLayout(panel_info)
        
        # Primera fila
        layout_fila1 = QHBoxLayout()
        
        layout_fila1.addWidget(QLabel("Empleado:"))
        self.input_empleado = QLineEdit()
        self.input_empleado.setPlaceholderText("Nombre del empleado")
        layout_fila1.addWidget(self.input_empleado)
        
        layout_fila1.addWidget(QLabel("Departamento:"))
        self.input_departamento = QLineEdit()
        self.input_departamento.setPlaceholderText("Departamento")
        layout_fila1.addWidget(self.input_departamento)
        
        layout_fila1.addWidget(QLabel("Fecha:"))
        self.date_nomina = QDateEdit()
        self.date_nomina.setCalendarPopup(True)
        self.date_nomina.setDate(QDate.currentDate())
        layout_fila1.addWidget(self.date_nomina)
        
        layout_info.addLayout(layout_fila1)
        
        # Segunda fila
        layout_fila2 = QHBoxLayout()
        
        layout_fila2.addWidget(QLabel("Tipo de nómina:"))
        self.combo_tipo_nomina = QComboBox()
        self.combo_tipo_nomina.addItems([
            "Nómina mensual",
            "Paga extra",
            "Finiquito",
            "Liquidación",
            "Atrasos",
            "Otros"
        ])
        layout_fila2.addWidget(self.combo_tipo_nomina)
        
        layout_fila2.addWidget(QLabel("Plantilla:"))
        self.combo_plantilla = QComboBox()
        self.combo_plantilla.addItems(["Nueva entrada", "Plantilla básica", "Plantilla completa"])
        self.combo_plantilla.currentTextChanged.connect(self.cargar_plantilla)
        layout_fila2.addWidget(self.combo_plantilla)
        
        btn_guardar_plantilla = QPushButton("💾 Guardar como plantilla")
        btn_guardar_plantilla.clicked.connect(self.guardar_como_plantilla)
        layout_fila2.addWidget(btn_guardar_plantilla)
        
        layout_fila2.addStretch()
        layout_info.addLayout(layout_fila2)
        
        layout_principal.addWidget(panel_info)
        
        # Panel central - Tabla de conceptos
        panel_conceptos = QGroupBox("Conceptos Salariales")
        layout_conceptos = QVBoxLayout(panel_conceptos)
        
        # Botones de gestión
        layout_botones = QHBoxLayout()
        
        btn_agregar_concepto = QPushButton("➕ Agregar Concepto")
        btn_agregar_concepto.clicked.connect(self.agregar_concepto)
        layout_botones.addWidget(btn_agregar_concepto)
        
        btn_agregar_multiple = QPushButton("➕➕ Agregar Múltiples")
        btn_agregar_multiple.clicked.connect(self.agregar_conceptos_multiples)
        layout_botones.addWidget(btn_agregar_multiple)
        
        btn_importar_conceptos = QPushButton("📁 Importar Conceptos")
        btn_importar_conceptos.clicked.connect(self.importar_conceptos)
        layout_botones.addWidget(btn_importar_conceptos)
        
        btn_limpiar_tabla = QPushButton("🗑️ Limpiar Todo")
        btn_limpiar_tabla.clicked.connect(self.limpiar_tabla)
        layout_botones.addWidget(btn_limpiar_tabla)
        
        layout_botones.addStretch()
        layout_conceptos.addLayout(layout_botones)
        
        # Tabla de conceptos
        self.tabla_conceptos = QTableWidget()
        self.tabla_conceptos.setColumnCount(7)
        self.tabla_conceptos.setHorizontalHeaderLabels([
            'Código', 'Concepto', 'Tipo', 'Base', 'Cantidad', 'Importe', 'Acciones'
        ])
        
        # Ajustar columnas
        header = self.tabla_conceptos.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(6, QHeaderView.Fixed)
        self.tabla_conceptos.setColumnWidth(6, 100)
        
        # Menú contextual
        self.tabla_conceptos.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tabla_conceptos.customContextMenuRequested.connect(self.menu_contextual)
        
        layout_conceptos.addWidget(self.tabla_conceptos)
        
        # Atajos de teclado
        layout_atajos = QHBoxLayout()
        lbl_atajos = QLabel("Atajos: Ctrl+N (Nuevo concepto) | Del (Eliminar) | Ctrl+D (Duplicar) | Ctrl+S (Guardar)")
        lbl_atajos.setStyleSheet("color: gray; font-size: 10px;")
        layout_atajos.addWidget(lbl_atajos)
        layout_conceptos.addLayout(layout_atajos)
        
        layout_principal.addWidget(panel_conceptos)
        
        # Panel de resumen y cálculos
        panel_resumen = QGroupBox("Resumen y Totales")
        layout_resumen = QHBoxLayout(panel_resumen)
        
        # Columna 1 - Devengos
        col_devengos = QVBoxLayout()
        
        self.lbl_total_devengos = QLabel("Total Devengos: € 0.00")
        self.lbl_total_devengos.setFont(QFont('Arial', 12, QFont.Bold))
        self.lbl_total_devengos.setStyleSheet("color: #4CAF50;")
        col_devengos.addWidget(self.lbl_total_devengos)
        
        self.lbl_salario_base = QLabel("Salario Base: € 0.00")
        col_devengos.addWidget(self.lbl_salario_base)
        
        self.lbl_complementos = QLabel("Complementos: € 0.00")
        col_devengos.addWidget(self.lbl_complementos)
        
        layout_resumen.addLayout(col_devengos)
        
        # Columna 2 - Deducciones
        col_deducciones = QVBoxLayout()
        
        self.lbl_total_deducciones = QLabel("Total Deducciones: € 0.00")
        self.lbl_total_deducciones.setFont(QFont('Arial', 12, QFont.Bold))
        self.lbl_total_deducciones.setStyleSheet("color: #f44336;")
        col_deducciones.addWidget(self.lbl_total_deducciones)
        
        self.lbl_seg_social = QLabel("Seg. Social: € 0.00")
        col_deducciones.addWidget(self.lbl_seg_social)
        
        self.lbl_irpf = QLabel("IRPF: € 0.00")
        col_deducciones.addWidget(self.lbl_irpf)
        
        layout_resumen.addLayout(col_deducciones)
        
        # Columna 3 - Líquido
        col_liquido = QVBoxLayout()
        
        self.lbl_liquido = QLabel("LÍQUIDO A PERCIBIR: € 0.00")
        self.lbl_liquido.setFont(QFont('Arial', 14, QFont.Bold))
        self.lbl_liquido.setStyleSheet("color: #2196F3;")
        col_liquido.addWidget(self.lbl_liquido)
        
        self.lbl_base_cotizacion = QLabel("Base Cotización: € 0.00")
        col_liquido.addWidget(self.lbl_base_cotizacion)
        
        self.lbl_base_irpf = QLabel("Base IRPF: € 0.00")
        col_liquido.addWidget(self.lbl_base_irpf)
        
        layout_resumen.addLayout(col_liquido)
        
        layout_principal.addWidget(panel_resumen)
        
        # Panel de validación y notas
        panel_validacion = QGroupBox("Validación y Notas")
        layout_validacion = QVBoxLayout(panel_validacion)
        
        # Checks de validación
        layout_checks = QHBoxLayout()
        
        self.check_validacion_importes = QCheckBox("Importes validados")
        layout_checks.addWidget(self.check_validacion_importes)
        
        self.check_validacion_calculos = QCheckBox("Cálculos verificados")
        layout_checks.addWidget(self.check_validacion_calculos)
        
        self.check_validacion_normativa = QCheckBox("Cumple normativa")
        layout_checks.addWidget(self.check_validacion_normativa)
        
        btn_validar_auto = QPushButton("🔍 Validar Automáticamente")
        btn_validar_auto.clicked.connect(self.validar_automaticamente)
        layout_checks.addWidget(btn_validar_auto)
        
        layout_checks.addStretch()
        layout_validacion.addLayout(layout_checks)
        
        # Área de notas
        self.texto_notas = QTextEdit()
        self.texto_notas.setMaximumHeight(80)
        self.texto_notas.setPlaceholderText("Notas u observaciones sobre esta nómina...")
        layout_validacion.addWidget(self.texto_notas)
        
        layout_principal.addWidget(panel_validacion)
        
        # Botones de acción principales
        layout_acciones = QHBoxLayout()
        
        btn_calcular = QPushButton("🧮 Calcular Totales")
        btn_calcular.clicked.connect(self.calcular_totales)
        btn_calcular.setStyleSheet("background-color: #FF9800;")
        layout_acciones.addWidget(btn_calcular)
        
        btn_vista_previa = QPushButton("👁️ Vista Previa")
        btn_vista_previa.clicked.connect(self.mostrar_vista_previa)
        layout_acciones.addWidget(btn_vista_previa)
        
        btn_guardar = QPushButton("💾 Guardar")
        btn_guardar.clicked.connect(self.guardar_nomina)
        btn_guardar.setStyleSheet("background-color: #4CAF50;")
        layout_acciones.addWidget(btn_guardar)
        
        btn_exportar = QPushButton("📊 Exportar")
        btn_exportar.clicked.connect(self.exportar_nomina)
        layout_acciones.addWidget(btn_exportar)
        
        layout_acciones.addStretch()
        
        btn_nueva = QPushButton("📄 Nueva Entrada")
        btn_nueva.clicked.connect(self.nueva_entrada)
        layout_acciones.addWidget(btn_nueva)
        
        layout_principal.addLayout(layout_acciones)
        
        # Configurar atajos de teclado
        self.configurar_atajos()
        
        # Cargar plantilla básica
        self.cargar_plantilla_basica()
        
    def configurar_atajos(self):
        """Configura atajos de teclado"""
        from PyQt5.QtWidgets import QShortcut
        
        # Ctrl+N: Nuevo concepto
        shortcut_nuevo = QShortcut(QKeySequence("Ctrl+N"), self)
        shortcut_nuevo.activated.connect(self.agregar_concepto)
        
        # Ctrl+S: Guardar
        shortcut_guardar = QShortcut(QKeySequence("Ctrl+S"), self)
        shortcut_guardar.activated.connect(self.guardar_nomina)
        
        # Del: Eliminar concepto seleccionado
        shortcut_eliminar = QShortcut(QKeySequence("Delete"), self)
        shortcut_eliminar.activated.connect(self.eliminar_concepto_seleccionado)
        
    def cargar_plantilla_basica(self):
        """Carga una plantilla básica de conceptos"""
        conceptos_basicos = [
            ('001', 'Salario Base', 'Devengo', 2000.00, 1, 2000.00),
            ('010', 'Plus Transporte', 'Devengo', 100.00, 1, 100.00),
            ('011', 'Plus Productividad', 'Devengo', 150.00, 1, 150.00),
            ('101', 'Seg. Social Trabajador', 'Deducción', 2250.00, 0.0635, -142.88),
            ('201', 'IRPF', 'Deducción', 2250.00, 0.15, -337.50)
        ]
        
        self.tabla_conceptos.setRowCount(0)
        
        for concepto in conceptos_basicos:
            self.agregar_concepto_tabla(*concepto)
            
        self.calcular_totales()
        
    def agregar_concepto(self):
        """Agrega un nuevo concepto a la tabla"""
        from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QFormLayout
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Agregar Concepto")
        dialog.setModal(True)
        
        layout = QFormLayout(dialog)
        
        # Campos del formulario
        input_codigo = QLineEdit()
        layout.addRow("Código:", input_codigo)
        
        input_concepto = QLineEdit()
        layout.addRow("Concepto:", input_concepto)
        
        combo_tipo = QComboBox()
        combo_tipo.addItems(["Devengo", "Deducción"])
        layout.addRow("Tipo:", combo_tipo)
        
        input_base = QDoubleSpinBox()
        input_base.setRange(0, 99999)
        input_base.setDecimals(2)
        layout.addRow("Base:", input_base)
        
        input_cantidad = QDoubleSpinBox()
        input_cantidad.setRange(0, 999)
        input_cantidad.setDecimals(4)
        input_cantidad.setValue(1)
        layout.addRow("Cantidad/Porcentaje:", input_cantidad)
        
        # Botones
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, dialog
        )
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addRow(buttons)
        
        if dialog.exec_() == QDialog.Accepted:
            codigo = input_codigo.text()
            concepto = input_concepto.text()
            tipo = combo_tipo.currentText()
            base = input_base.value()
            cantidad = input_cantidad.value()
            
            # Calcular importe
            if cantidad <= 1:  # Es un porcentaje
                importe = base * cantidad
            else:  # Es una cantidad fija
                importe = cantidad
                
            if tipo == "Deducción":
                importe = -abs(importe)
                
            self.agregar_concepto_tabla(codigo, concepto, tipo, base, cantidad, importe)
            self.calcular_totales()
            
    def agregar_concepto_tabla(self, codigo, concepto, tipo, base, cantidad, importe):
        """Agrega un concepto a la tabla"""
        row = self.tabla_conceptos.rowCount()
        self.tabla_conceptos.insertRow(row)
        
        # Código
        self.tabla_conceptos.setItem(row, 0, QTableWidgetItem(codigo))
        
        # Concepto
        self.tabla_conceptos.setItem(row, 1, QTableWidgetItem(