"""
Базовые классы для отслеживания операционных метрик.
Фокус: бюджет, сроки, эффективность процессов.
"""

from datetime import datetime, timedelta
from typing import Optional, List


class BudgetTracker:
    """
    Трекер бюджетной дисциплины: план vs факт.
    
    Пример использования при управлении бюджетом 400+ млн ₽
    в условиях неопределённости (как в Университете Иннополис).
    """
    
    def __init__(self, planned_budget: float, name: str = "Project"):
        self.name = name
        self.planned_budget = planned_budget
        self.actual_spent = 0.0
        self.transactions: List[dict] = []
    
    def add_expense(self, amount: float, category: str, description: str = ""):
        """Добавить расход с привязкой к категории."""
        self.actual_spent += amount
        self.transactions.append({
            "date": datetime.now(),
            "amount": amount,
            "category": category,
            "description": description
        })
    
    def get_budget_variance(self) -> float:
        """Отклонение от плана в рублях (положительное = перерасход)."""
        return self.actual_spent - self.planned_budget
    
    def get_budget_utilization(self) -> float:
        """Процент использования бюджета."""
        if self.planned_budget == 0:
            return 0.0
        return (self.actual_spent / self.planned_budget) * 100
    
    def __repr__(self):
        return (
            f"BudgetTracker('{self.name}'): "
            f"план={self.planned_budget:,.0f} ₽, "
            f"факт={self.actual_spent:,.0f} ₽, "
            f"использовано={self.get_budget_utilization():.1f}%"
        )


class TimelineTracker:
    """
    Трекер соблюдения сроков: плановые даты vs фактическое выполнение.
    
    Полезен при построении процессов с нуля в условиях неопределённости.
    """
    
    def __init__(self, planned_end_date: datetime, name: str = "Milestone"):
        self.name = name
        self.planned_end_date = planned_end_date
        self.actual_end_date: Optional[datetime] = None
    
    def mark_completed(self, completion_date: Optional[datetime] = None):
        """Отметить завершение задачи."""
        self.actual_end_date = completion_date or datetime.now()
    
    def is_delayed(self) -> bool:
        """Проверить, есть ли задержка."""
        if self.actual_end_date is None:
            return datetime.now() > self.planned_end_date
        return self.actual_end_date > self.planned_end_date
    
    def get_delay_days(self) -> int:
        """Количество дней задержки (отрицательное = выполнено раньше)."""
        if self.actual_end_date is None:
            return (datetime.now() - self.planned_end_date).days
        return (self.actual_end_date - self.planned_end_date).days
    
    def __repr__(self):
        status = "в работе" if self.actual_end_date is None else "завершено"
        delay = f", задержка {self.get_delay_days()} дн." if self.is_delayed() else ""
        return f"TimelineTracker('{self.name}'): {status}{delay}"


if __name__ == "__main__":
    # Пример: отслеживание бюджета ИИ-института
    institute_budget = BudgetTracker(planned_budget=350_000_000, name="ИИ-институт МГУ")
    institute_budget.add_expense(120_000_000, "НИР", "Контракты с Сбером и Яндексом")
    institute_budget.add_expense(45_000_000, "ИТ-инфраструктура", "Серверы и лицензии")
    
    print(institute_budget)
    print(f"Отклонение от плана: {institute_budget.get_budget_variance():,.0f} ₽")
    
    # Пример: отслеживание сроков запуска университета
    uni_launch = TimelineTracker(
        planned_end_date=datetime(2020, 9, 1),
        name="Запуск Университета Иннополис"
    )
    uni_launch.mark_completed(datetime(2020, 8, 25))  # Запущен на 7 дней раньше!
    
    print(uni_launch)