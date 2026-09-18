"""Weekly paycheck calculator with overtime support."""


OVERTIME_THRESHOLD = 40.0
OVERTIME_MULTIPLIER = 1.5


def calculate_pay(
    hours_worked: float,
    hourly_rate: float,
    overtime_threshold: float = OVERTIME_THRESHOLD,
    overtime_multiplier: float = OVERTIME_MULTIPLIER,
) -> float:
    """Return gross weekly pay, including overtime after the threshold."""
    if hours_worked < 0 or hourly_rate < 0:
        raise ValueError("Hours worked and hourly rate must be non-negative.")
    if overtime_threshold < 0 or overtime_multiplier < 1:
        raise ValueError("Overtime settings are invalid.")

    regular_hours = min(hours_worked, overtime_threshold)
    overtime_hours = max(hours_worked - overtime_threshold, 0)
    return (regular_hours * hourly_rate) + (
        overtime_hours * hourly_rate * overtime_multiplier
    )


if __name__ == "__main__":
    hours = float(input("Hours worked: "))
    rate = float(input("Hourly rate: "))
    print(f"Weekly gross pay: ${calculate_pay(hours, rate):,.2f}")
