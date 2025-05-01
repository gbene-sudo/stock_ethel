import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                               QTableView, QPushButton, QDialog, QFormLayout, QLineEdit,
                               QComboBox, QMessageBox, QLabel, QHeaderView)
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtCore import Qt, QSortFilterProxyModel

# Assuming models and CRUD are available and correctly implemented
from models import Barril
from CRUD import (actualizar_barril, obtener_barriles, borrar_barril, crear_barril,
                  order_by_id, filtro_por_id, filtro_por_litros, filtro_por_estado,
                  filtro_por_tipo_y_estado)


TIPOS_VALIDOS = ["Wheat", "Hoppy", "Summer", "Irish", "Porter"]
ESTADOS_VALIDOS = ["Lleno", "Entregado", "Latas", "Bar", "Incompleto", "Vacio"]
CAPACIDADES_VALIDOS = [10, 15, 20, 30, 50]

class BarrelModel(QStandardItemModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setHorizontalHeaderLabels(["ID", "Tipo", "Capacidad (L)", "Estado"])

    def set_data(self, barriles):
        self.setRowCount(0)  # Clear existing rows
        for barril in barriles:
            row_items = [
                QStandardItem(str(barril.id)),
                QStandardItem(barril.tipo),
                QStandardItem(str(barril.capacidad)),
                QStandardItem(barril.estado)
            ]
            self.appendRow(row_items)

        # Make cells not editable
        for row in range(self.rowCount()):
            for col in range(self.columnCount()):
                self.item(row, col).setEditable(False)


class AddBarrelDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Cargar Nuevo Barril")
        self.setGeometry(100, 100, 300, 250)

        layout = QFormLayout()

        self.tipo_combo = QComboBox()
        self.tipo_combo.addItems(TIPOS_VALIDOS)
        layout.addRow("Tipo:", self.tipo_combo)

        self.capacidad_combo = QComboBox()
        self.capacidad_combo.addItems(map(str, CAPACIDADES_VALIDOS))
        layout.addRow("Capacidad (L):", self.capacidad_combo)

        self.estado_combo = QComboBox()
        self.estado_combo.addItems(ESTADOS_VALIDOS)
        layout.addRow("Estado:", self.estado_combo)

        self.save_button = QPushButton("Guardar")
        self.save_button.clicked.connect(self.save_barril)
        layout.addRow(self.save_button)

        self.setLayout(layout)

    def save_barril(self):
        tipo = self.tipo_combo.currentText()
        capacidad = int(self.capacidad_combo.currentText())
        estado = self.estado_combo.currentText()

        if tipo not in TIPOS_VALIDOS:
            QMessageBox.showerror("Error", f"Tipo inválido. Debe ser uno de: {', '.join(TIPOS_VALIDOS)}")
            return

        if capacidad not in CAPACIDADES_VALIDOS:
             QMessageBox.showerror("Error",
                                     f"Capacidad inválida. Debe ser una de: {', '.join(map(str, CAPACIDADES_VALIDOS))} litros.")
             return

        if estado not in ESTADOS_VALIDOS:
            QMessageBox.showerror("Error", f"Estado inválido. Debe ser uno de: {', '.join(ESTADOS_VALIDOS)}")
            return

        crear_barril(tipo, capacidad, estado)
        QMessageBox.information(self, "Éxito", f"Barril '{tipo}' creado correctamente.")
        self.parent().load_barriles() # Refresh the main table
        self.accept()


class SearchBarrelDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Buscar Barril por ID")
        self.setGeometry(100, 100, 250, 150)

        layout = QFormLayout()

        self.id_input = QLineEdit()
        layout.addRow("Ingrese el ID del Barril:", self.id_input)

        self.search_button = QPushButton("Buscar")
        self.search_button.clicked.connect(self.search_barril)
        layout.addRow(self.search_button)

        self.setLayout(layout)

    def search_barril(self):
        barril_id_text = self.id_input.text()

        if not barril_id_text:
            QMessageBox.warning(self, "Campos vacíos", "Ingrese un ID.")
            return

        try:
            barril_id = int(barril_id_text)
        except ValueError:
            QMessageBox.critical(self, "Error", "El ID debe ser un número.")
            return

        barril = filtro_por_id(barril_id)

        if barril:
            self.show_barrel_details(barril)
            self.accept()
        else:
            QMessageBox.information(self, "No encontrado", f"No se encontró el barril con ID {barril_id}.")

    def show_barrel_details(self, barril):
        detail_dialog = QDialog(self)
        detail_dialog.setWindowTitle(f"Detalle del Barril ID {barril.id}")
        detail_dialog.setGeometry(150, 150, 300, 250)

        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"ID: {barril.id}"))
        layout.addWidget(QLabel(f"Tipo: {barril.tipo}"))
        layout.addWidget(QLabel(f"Capacidad (L): {barril.capacidad}"))
        layout.addWidget(QLabel(f"Estado: {barril.estado}"))

        close_button = QPushButton("Cerrar")
        close_button.clicked.connect(detail_dialog.accept)
        layout.addWidget(close_button)

        detail_dialog.setLayout(layout)
        detail_dialog.exec()


class UpdateBarrelDialog(QDialog):
    def __init__(self, barril, parent=None):
        super().__init__(parent)
        self.barril = barril
        self.setWindowTitle(f"Actualizar Barril ID {barril.id}")
        self.setGeometry(100, 100, 300, 250)

        layout = QFormLayout()

        self.tipo_combo = QComboBox()
        self.tipo_combo.addItems(TIPOS_VALIDOS)
        self.tipo_combo.setCurrentText(barril.tipo)
        layout.addRow("Tipo:", self.tipo_combo)

        self.capacidad_combo = QComboBox()
        self.capacidad_combo.addItems(map(str, CAPACIDADES_VALIDOS))
        self.capacidad_combo.setCurrentText(str(barril.capacidad))
        layout.addRow("Capacidad (L):", self.capacidad_combo)

        self.estado_combo = QComboBox()
        self.estado_combo.addItems(ESTADOS_VALIDOS)
        self.estado_combo.setCurrentText(barril.estado)
        layout.addRow("Estado:", self.estado_combo)

        self.save_button = QPushButton("Guardar Cambios")
        self.save_button.clicked.connect(self.save_changes)
        layout.addRow(self.save_button)

        self.setLayout(layout)

    def save_changes(self):
        nuevo_tipo = self.tipo_combo.currentText()
        nueva_capacidad = int(self.capacidad_combo.currentText())
        nuevo_estado = self.estado_combo.currentText()

        if nuevo_tipo not in TIPOS_VALIDOS:
            QMessageBox.critical(self, "Error", f"Tipo inválido. Debe ser uno de: {', '.join(TIPOS_VALIDOS)}")
            return

        if nueva_capacidad not in CAPACIDADES_VALIDOS:
             QMessageBox.critical(self, "Error",
                                     f"Capacidad inválida. Debe ser una de: {', '.join(map(str, CAPACIDADES_VALIDOS))}")
             return

        if nuevo_estado not in ESTADOS_VALIDOS:
            QMessageBox.critical(self, "Error", f"Estado inválido. Debe ser uno de: {', '.join(ESTADOS_VALIDOS)}")
            return

        actualizar_barril(self.barril.id, nuevo_tipo, nuevo_estado, nueva_capacidad)
        QMessageBox.information(self, "Éxito", "Barril actualizado correctamente.")
        self.parent().load_barriles() # Refresh the main table
        self.accept()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cervecería Ethel")
        self.setGeometry(100, 100, 800, 500)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QHBoxLayout(self.central_widget)

        # Table View
        self.model = BarrelModel()
        self.proxy_model = QSortFilterProxyModel()
        self.proxy_model.setSourceModel(self.model)

        self.table_view = QTableView()
        self.table_view.setModel(self.proxy_model)
        self.table_view.setSortingEnabled(True)
        self.table_view.horizontalHeader().sectionClicked.connect(self.on_header_click)

        # Set column widths
        header = self.table_view.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.Stretch)

        self.layout.addWidget(self.table_view, 1)

        # Buttons Layout
        self.buttons_layout = QVBoxLayout()

        self.btn_cargar = QPushButton("Cargar Barril")
        self.btn_cargar.clicked.connect(self.open_add_dialog)
        self.buttons_layout.addWidget(self.btn_cargar)

        self.btn_busqueda = QPushButton("Buscar Barril")
        self.btn_busqueda.clicked.connect(self.open_search_dialog)
        self.buttons_layout.addWidget(self.btn_busqueda)

        self.btn_eliminar = QPushButton("Eliminar Barril")
        self.btn_eliminar.clicked.connect(self.delete_barrel)
        self.buttons_layout.addWidget(self.btn_eliminar)

        self.btn_actualizar = QPushButton("Actualizar Barril")
        self.btn_actualizar.clicked.connect(self.open_update_dialog)
        self.buttons_layout.addWidget(self.btn_actualizar)

        self.buttons_layout.addStretch() # Add stretch to push buttons to top
        self.layout.addLayout(self.buttons_layout)

        self.load_barriles()
        self.apply_styles()

    def apply_styles(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QTableView {
                background-color: #ffffff;
                alternate-background-color: #e0e0e0;
                selection-background-color: #a8a8a8;
                selection-color: #ffffff;
                border: 1px solid #d0d0d0;
                gridline-color: #d0d0d0;
            }
            QTableView::item {
                padding: 5px;
            }
            QHeaderView::section {
                background-color: #4a4a4a;
                color: #ffffff;
                padding: 5px;
                border: 1px solid #d0d0d0;
            }
            QPushButton {
                background-color: #5cb85c;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 5px;
                margin-bottom: 5px;
            }
            QPushButton:hover {
                background-color: #4cae4c;
            }
            QPushButton:pressed {
                background-color: #398439;
            }
            QDialog {
                background-color: #f9f9f9;
            }
            QFormLayout .QLabel {
                font-weight: bold;
            }
            QLineEdit, QComboBox {
                padding: 5px;
                border: 1px solid #d0d0d0;
                border-radius: 3px;
            }
        """)


    def load_barriles(self, barriles_list=None):
        if barriles_list is None:
            barriles_list = obtener_barriles()
        self.model.set_data(barriles_list)

    def on_header_click(self, logical_index):
        # This is handled by QSortFilterProxyModel when sorting is enabled on QTableView
        # No explicit sorting logic needed here, just ensure it's enabled
        pass

    def open_add_dialog(self):
        dialog = AddBarrelDialog(self)
        dialog.exec()

    def open_search_dialog(self):
        dialog = SearchBarrelDialog(self)
        dialog.exec()

    def delete_barrel(self):
        selected_indexes = self.table_view.selectionModel().selectedRows()
        if not selected_indexes:
            QMessageBox.warning(self, "Atención", "Seleccione un barril para eliminar.")
            return

        # Get the original index from the proxy model
        source_index = self.proxy_model.mapToSource(selected_indexes[0])
        barril_id_item = self.model.item(source_index.row(), 0)
        barril_id = int(barril_id_item.text())

        confirmacion = QMessageBox.question(self, "Eliminar", "¿Está seguro de eliminar este barril?",
                                            QMessageBox.Yes | QMessageBox.No)
        if confirmacion == QMessageBox.Yes:
            borrar_barril(barril_id)
            self.load_barriles()
            QMessageBox.information(self, "Éxito", "Barril eliminado.")

    def open_update_dialog(self):
        selected_indexes = self.table_view.selectionModel().selectedRows()
        if not selected_indexes:
            QMessageBox.warning(self, "Atención", "Seleccione un barril para actualizar.")
            return

        # Get the original index from the proxy model
        source_index = self.proxy_model.mapToSource(selected_indexes[0])
        barril_id_item = self.model.item(source_index.row(), 0)
        barril_id = int(barril_id_item.text())

        barril_to_update = filtro_por_id(barril_id) # Fetch the full barrel object
        if barril_to_update:
            dialog = UpdateBarrelDialog(barril_to_update, self)
            dialog.exec()
        else:
            QMessageBox.critical(self, "Error", "No se pudo obtener la información del barril para actualizar.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())