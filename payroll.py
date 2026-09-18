"""Payroll features for multiple employees, deductions, and CSV export."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from paycheck import calculate_pay


@dataclass(frozen=True)
class Employee:
    """Input data needed to calculate one employee's paycheck."""

    name: str
    hours_worked: float
    hourly_rate: float
    tax_rate: float = 0.0
    deductions: float = 0.0

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("Employee name cannot be empty.")
        if not 0 <= self.tax_rate <= 1:
            raise ValueError("Tax rate must be between 0 and 1.")
        if self.deductions < 0:
            raise ValueError("Deductions must be non-negative.")

    @property
    def gross_pay(self) -> float:
        """Calculate gross pay, including overtime."""
        return calculate_pay(self.hours_worked, self.hourly_rate)

    @property
    def taxes(self) -> float:
        """Calculate taxes as a fraction of gross pay."""
        return self.gross_pay * self.tax_rate

    @property
    def net_pay(self) -> float:
        """Calculate take-home pay after taxes and deductions."""
        return max(self.gross_pay - self.taxes - self.deductions, 0.0)


def calculate_payroll(employees: Iterable[Employee]) -> list[dict[str, float | str]]:
    """Return calculated payroll records for any number of employees."""
    return [
        {
            "employee": employee.name,
            "gross_pay": employee.gross_pay,
            "taxes": employee.taxes,
            "deductions": employee.deductions,
            "net_pay": employee.net_pay,
        }
        for employee in employees
    ]


def export_payroll_csv(
    employees: Iterable[Employee], output_file: str | Path = "payroll.csv"
) -> Path:
    """Export payroll records to a CSV file and return its path."""
    destination = Path(output_file)
    records = calculate_payroll(employees)
    fieldnames = ["employee", "gross_pay", "taxes", "deductions", "net_pay"]

    with destination.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(
            {
                key: value if key == "employee" else f"{value:.2f}"
                for key, value in record.items()
            }
            for record in records
        )

    return destination


if __name__ == "__main__":
    employees = [
        Employee("Riley Jack", 42, 20, tax_rate=0.20, deductions=15),
        Employee("Jordan Lee", 38, 22, tax_rate=0.18, deductions=10),
    ]
    file_path = export_payroll_csv(employees)
    print(f"Exported {len(employees)} employee paychecks to {file_path}")
