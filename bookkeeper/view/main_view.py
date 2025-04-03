"""Главное окно """

from typing import Any
# pylint: disable= no-name-in-module, c-extension-no-member
# Ошибки связанные с Qt
from PySide6 import QtWidgets, QtCore
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QVBoxLayout, QLabel, QWidget,\
    QGridLayout, QComboBox, QLineEdit, QPushButton

from bookkeeper.view.table_model import TableModel


class MainWindow(QtWidgets.QMainWindow):
    """Главное окно"""

    def __init__(self) -> None:
        super().__init__()

        self.item_model = None

        self.setFixedSize(600, 800)

        self.setWindowTitle("Программа для ведения бюджета")

        self.layout = QVBoxLayout()  # type: ignore

        self.layout.addWidget(QLabel('Последние расходы'))  # type: ignore

        self.expenses_grid = QtWidgets.QTableView()
        self.layout.addWidget(self.expenses_grid)  # type: ignore

        self.layout.addWidget(QLabel('Бюджет'))  # type: ignore

        self.budget_grid = QtWidgets.QTableView()
        self.layout.addWidget(self.budget_grid)  # type: ignore

        self.bottom_controls = QGridLayout()

        self.bottom_controls.addWidget(QLabel('Сумма'), 0, 0)
        self.amount_line_edit = QLineEdit()
        self.bottom_controls.addWidget(self.amount_line_edit, 0, 1)

        self.bottom_controls.addWidget(QLabel('Дата покупки'), 1, 0)
        self.date_input = DateWidget()
        self.bottom_controls.addWidget(self.date_input, 1, 1)

        self.bottom_controls.addWidget(QLabel('Категория'), 2, 0)
        self.category_dropdown = QComboBox()
        self.bottom_controls.addWidget(self.category_dropdown, 2, 1)

        self.bottom_controls.addWidget(QLabel('Комментарий'), 3, 0)
        self.comment_line_edit = QLineEdit()
        self.bottom_controls.addWidget(self.comment_line_edit, 3, 1)

        self.expense_change_button = QPushButton('Изменить')
        self.bottom_controls.addWidget(self.expense_change_button, 4, 0)
        self.expense_change_button.setToolTip(
            'Веди все параметры, потом выдели строку, '
            'которую нужно заменить и нажми эту кнопку\n'
            'Чтобы выделить строку нажми на ее номер')

        self.expense_add_button = QPushButton('Добавить')
        self.bottom_controls.addWidget(self.expense_add_button, 4, 1)

        self.expense_delete_button = QPushButton('Удалить')
        self.bottom_controls.addWidget(self.expense_delete_button, 4, 2)
        self.expense_delete_button.setToolTip(
            'Выдели строки, которые хочешь удалить и нажми эту кнопку\n'
            'Чтобы выделить строки нажимай на их номера')

        self.budget_change_button = QPushButton('Изменить \n Бюджет')
        self.bottom_controls.addWidget(self.budget_change_button, 0, 2)
        self.budget_change_button.setToolTip(
            'Введи в поле "Сумма" новый бюджет\n'
            'Выдели строку в которой хочешь заменить бюджет\n'
            'Чтобы выделить строку нажми на ее номер')

        self.category_edit_button = QPushButton('Редактировать \n Категории')
        self.bottom_controls.addWidget(self.category_edit_button, 2, 2)
        self.category_edit_button.setToolTip(
            'Нажми, если хочешь изменить список категорий')

        self.bottom_widget = QWidget()
        self.bottom_widget.setLayout(self.bottom_controls)

        self.layout.addWidget(self.bottom_widget)  # type: ignore

        self.widget = QWidget()
        self.widget.setLayout(self.layout)  # type: ignore

        self.setCentralWidget(self.widget)

    def set_expense_table(self, data: list[Any]) -> None:
        """Создает таблицу расходов"""
        if data:
            self.item_model = TableModel(data)  # type: ignore
            self.expenses_grid.setModel(self.item_model)  # type: ignore
            self.expenses_grid.setColumnHidden(4, True)
            self.expenses_grid.setColumnWidth(1, 120)
            self.expenses_grid.setColumnWidth(3, 240)

    def set_budget_table(self, data: list[Any]) -> None:
        """Создает таблицу бюджета"""
        if data:
            self.item_model = TableModel(data)  # type: ignore
            self.budget_grid.setModel(self.item_model)  # type: ignore
            self.budget_grid.setColumnHidden(3, True)
            for num in range(3):
                self.budget_grid.setColumnWidth(num, (600-40)//3)
                self.budget_grid.setRowHeight(1, 30)
            self.budget_grid.setMaximumHeight(120)

    def set_category_dropdown(self, data: list[Any]) -> None:
        """Отвечает за выпадающий список категорий"""
        self.category_dropdown.clear()
        for obj in data:
            self.category_dropdown.addItem(obj.name, obj.pk)

    def on_expense_add_button_clicked(self, slot: Any) -> None:
        """Отвечает за вызов определенной функции при нажатии кнопки "Добавить" """
        self.expense_add_button.clicked.connect(slot)  # type: ignore

    def on_expense_delete_button_clicked(self, slot: Any) -> None:
        """Отвечает за вызов определенной функции при нажатии кнопки "Удалить" """
        self.expense_delete_button.clicked.connect(slot)  # type: ignore

    def on_expense_change_button_clicked(self, slot: Any) -> None:
        """Отвечает за вызов определенной функции при нажатии кнопки "Изменить" """
        self.expense_change_button.clicked.connect(slot)  # type: ignore

    def on_budget_change_button_clicked(self, slot: Any) -> None:
        """Отвечает за вызов определенной функции при нажатии кнопки "Изменить Бюджет" """
        self.budget_change_button.clicked.connect(slot)  # type: ignore

    def on_category_edit_button_clicked(self, slot: Any) -> None:
        """Отвечает за вызов определенной функции при нажатии кнопки
         "Редактировать категории" """
        self.category_edit_button.clicked.connect(slot)  # type: ignore

    def get_amount(self) -> float:
        """Возвращает введенную пользователем сумму"""
        return int(self.amount_line_edit.text())

    def get_comment(self) -> str:
        """Возвращает напечатанный пользователем комментарий"""
        return str(self.comment_line_edit.text())

    def get_selected_cat(self) -> int:
        """Возвращает выбранную категорию"""
        return int(
            self.category_dropdown.itemData(self.category_dropdown.currentIndex())
        )

    def get_selected_date(self) -> str:
        """Возвращает выбранную дату"""
        return f'{(self.date_input.dateTime().toPython()):%Y-%m-%d}'

    def __get_selected_row_indices_expense(self) -> list[int]:
        """Возвращает индексы выбранных мышкой строк
        из таблицы Последних расходов"""
        list_of_index = \
            list(set([qmi.row() for qmi
                      in self.expenses_grid.selectionModel().selection().indexes()]))
        return list_of_index

    def __get_selected_row_indices_budget(self) -> list[int]:
        """Возвращает индексы выбранных мышкой строк
         из таблицы бюджета"""
        list_of_index = \
            list(set([qmi.row() for qmi
                      in self.budget_grid.selectionModel().selection().indexes()]))
        return list_of_index

    def get_selected(self, data: list[Any]) -> list[int] | None:
        """Возвращает список pk объектов, находящихся в строках выделенных мышкой"""
        self.item_model = TableModel(data)      # type: ignore
        data_type = str(type(data[0]))
        idx = None
        if data_type == "<class 'bookkeeper.models.expense.Expense'>":
            idx = self.__get_selected_row_indices_expense()
        elif data_type == "<class 'bookkeeper.models.budget.Budget'>":
            idx = self.__get_selected_row_indices_budget()
        if not idx:
            return None
        return [self.item_model._data[i].pk for i in idx]       # type: ignore


class DateWidget(QtWidgets.QDateEdit):
    """
    Виджет выбора даты в виде календаря
    """
    def __init__(self, date: QtCore.QDate = QtCore.QDate.currentDate()) -> None:
        super().__init__(date)
        self.setCalendarPopup(True)
        self.setDisplayFormat('dd.MM.yyyy')
        calendar = self.calendarWidget()
        calendar.setFirstDayOfWeek(Qt.DayOfWeek.Monday)
        calendar.setGridVisible(True)