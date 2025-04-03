""" Модуль реализующий внутреннюю логику и связывающий компоненты View и Model"""

from datetime import datetime, timedelta
from typing import Any

from ..models.expense import Expense
from bookkeeper.models.budget import Budget
from bookkeeper.models.category import Category


class Presenter:
    """Связь компонентов View и Model"""
    def __init__(self, view: Any, cat_view: Any, cat_repo: Any,
                 exp_repo: Any, budget_repo: Any) -> None:
        self.view = view
        self.cat_view = cat_view
        self.exp_repo = exp_repo
        self.cat_repo = cat_repo
        self.budget_repo = budget_repo
        self.exp_data = self.exp_repo.get_all()
        self.cat_data = self.cat_repo.get_all()
        self.budget_data = self.budget_repo.get_all()
        self.b_day = self.budget_data[0].budget
        self.b_week = self.budget_data[1].budget
        self.b_month = self.budget_data[2].budget
        self.view.on_expense_add_button_clicked(
            self.handle_expense_add_button_clicked
        )
        self.view.on_expense_delete_button_clicked(
            self.handle_expense_delete_button_clicked
        )
        self.view.on_expense_change_button_clicked(
            self.handle_expense_change_button_clicked
        )
        self.view.on_budget_change_button_clicked(
            self.handle_budget_change_button_clicked
        )
        self.view.on_category_edit_button_clicked(
            self.handle_category_edit_button_clicked
        )
        self.cat_view.on_category_add_button_clicked(
            self.handle_category_add_button_clicked
        )
        self.cat_view.on_category_delete_button_clicked(
            self.handle_category_delete_button_clicked
        )
        self.cat_view.on_category_change_button_clicked(
            self.handle_category_change_button_clicked
        )

    def update_expense_data(self) -> None:
        """Обновляет отображаемую таблицу расходов в соответствии с базой данных"""
        self.exp_data = self.exp_repo.get_all()
        if self.exp_data:
            for exp in self.exp_data:
                for cat in self.cat_data:
                    if cat.pk == exp.category:
                        exp.category = cat.name
                        break
            self.view.set_expense_table(self.exp_data)

    def update_budget_data(self) -> None:
        """Обновляет отображаемую таблицу бюджета в соответствии с базой данных"""
        self.exp_data = self.exp_repo.get_all()
        day, week, month = 0, 0, 0
        today = datetime.now()
        for expense in self.exp_data:
            if expense.expense_date >= f'{(today - timedelta(days=1)):%Y-%m-%d}':
                day += expense.amount
            if expense.expense_date >= f'{(today - timedelta(days=7)):%Y-%m-%d}':
                week += expense.amount
            if expense.expense_date >= f'{(today - timedelta(days=30)):%Y-%m-%d}':
                month += expense.amount
        self.budget_repo.update(Budget(amount=day,
                                       time="День", budget=self.b_day, pk=1))
        self.budget_repo.update(Budget(amount=week,
                                       time="Неделя", budget=self.b_week, pk=2))
        self.budget_repo.update(Budget(amount=month,
                                       time="Месяц", budget=self.b_month, pk=3))
        self.view.set_budget_table(self.budget_repo.get_all())

    def update_category_data(self) -> None:
        """Обновляет отображаемую таблицу расходов в соответствии с базой данных"""
        self.cat_data = self.cat_repo.get_all()
        if self.cat_data:
            for cat in self.cat_data:
                for sub_cat in self.cat_data:
                    if sub_cat.parent == cat.pk:
                        sub_cat.parent = cat.name
            self.cat_view.set_category_table(self.cat_data)
            self.cat_view.set_category_dropdown(self.cat_data)
            self.view.set_category_dropdown(self.cat_data)

    def show(self) -> None:
        """Вызывает отображение главного окна"""
        self.view.show()
        self.update_expense_data()
        self.update_budget_data()
        self.view.set_category_dropdown(self.cat_data)

    def handle_expense_add_button_clicked(self) -> None:
        """
        При нажатии на кнопку "Добавить" добавляет в базу данных
        соответствующую запись и вызывает обновление таблиц
        """
        cat_pk = self.view.get_selected_cat()
        amount = self.view.get_amount()
        comment = self.view.get_comment()
        date = self.view.get_selected_date()
        exp = Expense(int(amount), cat_pk, expense_date=date, comment=comment)
        self.exp_repo.add(exp)
        self.update_expense_data()
        self.update_budget_data()

    def handle_expense_delete_button_clicked(self) -> None:
        """
        При нажатии на кнопку "Удалить" удаляет из базы данных
        соответствующие записи и вызывает обновление таблиц.
        Удаление последней записи из таблицы отображается
        только при перезапуске программы
        """
        selected = self.view.get_selected(self.exp_repo.get_all())
        if selected:
            for pk in selected:
                self.exp_repo.delete(pk)
            self.update_expense_data()
            self.update_budget_data()

    def handle_expense_change_button_clicked(self) -> None:
        """
        При нажатии на кнопку "Изменить" заменяет в базе данных
        соответствующую запись и вызывает обновление таблиц.
        """
        cat_pk = self.view.get_selected_cat()
        amount = self.view.get_amount()
        comment = self.view.get_comment()
        date = self.view.get_selected_date()
        select = self.view.get_selected(self.exp_repo.get_all())
        if select:
            exp = Expense(amount, cat_pk, expense_date=date,
                          comment=comment, pk=select[0])
            self.exp_repo.update(exp)
            self.update_expense_data()
            self.update_budget_data()

    def handle_budget_change_button_clicked(self) -> None:
        """
        При нажатии на кнопку "Изменить Бюджет" изменяет бюджет
        на определенный промежуток времени.
        """
        budget_sum = self.view.get_amount()
        select = self.view.get_selected(self.budget_repo.get_all())
        if select:
            select = select[0]
            if select == 1:
                self.b_day = budget_sum
            elif select == 2:
                self.b_week = budget_sum
            elif select == 3:
                self.b_month = budget_sum
        self.update_budget_data()

    def handle_category_edit_button_clicked(self) -> None:
        """
        При нажатии на кнопку "Редактировать Категории"
        открывает соответствующее окно
        """
        self.update_category_data()
        self.cat_view.show()

    def handle_category_add_button_clicked(self) -> None:
        """
        При нажатии на кнопку "Добавить" в окне категорий
        добавляет в базу данных соответствующую запись
        и вызывает обновление выпадающего списка категорий
        и таблицы категорий
        """
        new_cat_name = self.cat_view.get_cat_name()
        parent_cat_pk = self.cat_view.get_selected_cat()
        cat = Category(name=new_cat_name, parent=parent_cat_pk)
        self.cat_repo.add(cat)
        self.update_category_data()

    def handle_category_delete_button_clicked(self) -> None:
        """
        При нажатии на кнопку "Удалить" в окне категорий
        удаляет из базы данных соответствующую запись
        и вызывает обновление выпадающего списка категорий
        и таблицы категорий
        """
        selected = self.cat_view.get_selected(self.cat_repo.get_all())
        if selected:
            for pk in selected:
                self.cat_repo.delete(pk)
        self.update_category_data()

    def handle_category_change_button_clicked(self) -> None:
        """
        При нажатии на кнопку "Изменить" в окне категорий
        заменяет в базе данных соответствующую запись
        и вызывает обновление выпадающего списка категорий
        и таблицы категорий
        """
        new_cat_name = self.cat_view.get_cat_name()
        parent_cat_pk = self.cat_view.get_selected_cat()
        select = self.cat_view.get_selected(self.cat_repo.get_all())
        if select:
            cat = Category(name=new_cat_name, parent=parent_cat_pk, pk=select[0])
            self.cat_repo.update(cat)
            self.update_category_data()