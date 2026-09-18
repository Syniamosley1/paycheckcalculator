"""Basic weekly paycheck calculator."""


def calculate_pay(hours_worked: float, hourly_rate: float) -> float:
    """Return weekly gross pay using regular pay only."""
    if hours_worked < 0 or hourly_rate < 0:
        raise ValueError("Hours worked and hourly rate must be non-negative.")
    return hours_worked * hourly_rate


if __name__ == "__main__":
    hours = float(input("Hours worked: "))
    rate = float(input("Hourly rate: "))
    print(f"Weekly gross pay: ${calculate_pay(hours, rate):,.2f}")
