"""Окно редактирования категорий"""

from typing import Any
# pylint: disable= no-name-in-module, c-extension-no-member
# Ошибки связанные с Qt
from PySide6 import QtWidgets
from PySide6.QtWidgets import QVBoxLayout, QLabel, QWidget,\
    QGridLayout, QComboBox, QLineEdit, QPushButton

from bookkeeper.view.table_model import TableModel


class CategoryView(QtWidgets.QMainWindow):
    """Главное окно"""

    def __init__(self,) -> None:
        super().__init__()

        self.item_model = None

        self.setFixedSize(450, 500)

        self.setWindowTitle("Редактирование списка категорий")

        self.layout = QVBoxLayout()  # type: ignore

        self.layout.addWidget(QLabel('Список категорий'))       # type: ignore

        self.category_grid = QtWidgets.QTableView()
        self.layout.addWidget(self.category_grid)       # type: ignore

        self.bottom_controls = QGridLayout()

        self.bottom_controls.addWidget(QLabel('Новая подкатегория'), 0, 0)
        self.cat_name_line_edit = QLineEdit()
        self.bottom_controls.addWidget(self.cat_name_line_edit, 0, 1)

        self.bottom_controls.addWidget(QLabel('Категория'), 2, 0)
        self.category_dropdown = QComboBox()
        self.bottom_controls.addWidget(self.category_dropdown, 2, 1)

        self.category_change_button = QPushButton('Изменить')
        self.bottom_controls.addWidget(self.category_change_button, 3, 0)
        self.category_change_button.setToolTip(
            'Веди название подкатегории и выбери ее родительскую категорию,\n '
            'потом выдели строку, которую нужно заменить и нажми эту кнопку\n'
            'Чтобы выделить строку нажми на ее номер')

        self.category_add_button = QPushButton('Добавить')
        self.bottom_controls.addWidget(self.category_add_button, 3, 1)

        self.category_delete_button = QPushButton('Удалить')
        self.bottom_controls.addWidget(self.category_delete_button, 3, 2)
        self.category_delete_button.setToolTip(
            'Выдели строки, которые хочешь удалить и нажми эту кнопку\n'
            'Чтобы выделить строки нажимай на их номера')

        self.bottom_category_widget = QWidget()
        self.bottom_category_widget.setLayout(self.bottom_controls)

        self.layout.addWidget(self.bottom_category_widget)      # type: ignore

        self.widget = QWidget()
        self.widget.setLayout(self.layout)  # type: ignore

        self.setCentralWidget(self.widget)

    def set_category_table(self, data: list[Any]) -> None:
        """Создает таблицу категорий"""
        if data:
            self.item_model = TableModel(data)  # type: ignore
            self.category_grid.setModel(self.item_model)    # type: ignore
            self.category_grid.hideColumn(2)
            self.category_grid.setColumnWidth(0, 200)
            self.category_grid.setColumnWidth(1, 200)

    def set_category_dropdown(self, data: list[Any]) -> None:
        """Отвечает за выпадающий список категорий"""
        self.category_dropdown.clear()
        for obj in data:
            self.category_dropdown.addItem(obj.name, obj.pk)

    def on_category_add_button_clicked(self, slot: Any) -> None:
        """Отвечает за вызов определенной функции при нажатии кнопки "Добавить" """
        self.category_add_button.clicked.connect(slot)      # type: ignore

    def on_category_delete_button_clicked(self, slot: Any) -> None:
        """Отвечает за вызов определенной функции при нажатии кнопки "Удалить" """
        self.category_delete_button.clicked.connect(slot)       # type: ignore

    def on_category_change_button_clicked(self, slot: Any) -> None:
        """Отвечает за вызов определенной функции при нажатии кнопки "Изменить" """
        self.category_change_button.clicked.connect(slot)       # type: ignore

    def get_cat_name(self) -> str:
        """Возвращает введенное пользователем имя подкатегории"""
        return self.cat_name_line_edit.text()

    def get_selected_cat(self) -> int:
        """Возвращает выбранную категорию"""
        return int(
            self.category_dropdown.itemData(self.category_dropdown.currentIndex())
        )

    def __get_selected_row_indices_category(self) -> list[int]:
        """Возвращает индексы выбранных мышкой строк
        из таблицы Последних расходов"""
        list_of_index = \
            list(set([qmi.row() for qmi
                      in self.category_grid.selectionModel().selection().indexes()]))
        return list_of_index

    def get_selected(self, data: list[Any]) -> list[int] | None:
        """Возвращает список pk объектов, находящихся в строках выделенных мышкой"""
        self.item_model = TableModel(data)  # type: ignore
        idx = self.__get_selected_row_indices_category()
        if not idx:
            return None
        return [self.item_model._data[i].pk for i in idx]       # type: ignore