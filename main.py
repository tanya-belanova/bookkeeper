"""Модуль запуска программы"""

# pylint: disable= no-name-in-module
# Ошибки связанные с Qt
import sys
from PySide6.QtWidgets import QApplication

from bookkeeper.view.main_view import MainWindow
from bookkeeper.view.categories_view import CategoryView
from bookkeeper.presenter.presenter import Presenter
from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense
from bookkeeper.models.budget import Budget
from bookkeeper.repository.sqlite_repository import SQLiteRepository
from bookkeeper.utils import read_tree


DB_NAME = 'test9.db'

if __name__ == '__main__':

    app = QApplication(sys.argv)

    view = MainWindow()
    cat_view = CategoryView()

    category_repo = SQLiteRepository[Category](DB_NAME, Category)
    expense_repo = SQLiteRepository[Expense](DB_NAME, Expense)
    budget_repo = SQLiteRepository[Budget](DB_NAME, Budget)

    if not category_repo.get_all():
        cats = '''
                продукты
                развлечения
                транспорт
                книги
                одежда
                товары для дома
                лекарства
                рестораны
                '''.splitlines()
        Category.create_from_tree(read_tree(cats), category_repo)

    if not budget_repo.get_all():
        budget_repo.add(Budget(amount=0, time="День", budget=1000))
        budget_repo.add(Budget(amount=0, time="Неделя", budget=7000))
        budget_repo.add(Budget(amount=0, time="Месяц", budget=30000))

    window = Presenter(view, cat_view, category_repo, expense_repo, budget_repo)
    window.show()
    app.exec()