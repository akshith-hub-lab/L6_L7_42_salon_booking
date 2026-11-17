"""Input validation helpers for the salon booking exercise."""

import math


def _finite_number(value, field):
    """Parse a finite, non-negative number from user supplied text."""
    try:
        number = float(value.strip())
    except (AttributeError, TypeError, ValueError) as exc:
        raise ValueError(f"{field} must be a number") from exc
    if not math.isfinite(number) or number < 0:
        raise ValueError(f"{field} must be a finite, non-negative number")
    return number


def parse_booking(text):
    """Parse service:minutes and return a normalized service and duration."""
    if not isinstance(text, str):
        raise ValueError("booking must be text in the form service:minutes")
    parts = text.split(":")
    if len(parts) != 2:
        raise ValueError("booking must contain exactly one ':' separator")
    service, duration = (part.strip() for part in parts)
    if not service:
        raise ValueError("service name cannot be empty")
    minutes = _finite_number(duration, "duration")
    return service.title(), minutes


def duration_average(durations_csv):
    """Return the floor of the average of comma-separated durations."""
    if not isinstance(durations_csv, str):
        raise ValueError("durations must be comma-separated text")
    fields = durations_csv.split(",")
    if any(not field.strip() for field in fields):
        raise ValueError("provide one or more comma-separated durations")

    values = []
    for field in fields:
        value = field.strip()
        if not value.isdecimal():
            raise ValueError("durations must be non-negative whole numbers")
        values.append(int(value))
    return sum(values) // len(values)


def payable_bill(text):
    """Apply 18% tax and a discount, never returning a negative bill."""
    if not isinstance(text, str):
        raise ValueError("bill must be text in the form amount|discount")
    parts = text.split("|")
    if len(parts) != 2:
        raise ValueError("bill must contain exactly one '|' separator")
    bill = _finite_number(parts[0], "bill")
    discount = _finite_number(parts[1], "discount")
    total = bill * 1.18 - discount
    if not math.isfinite(total):
        raise ValueError("calculated bill is outside the supported range")
    return round(max(total, 0.0), 2)


def _run_prompt(prompt, function, label):
    try:
        print(label, function(input(prompt)))
    except ValueError as exc:
        print(f"Invalid input: {exc}")


def main():
    print("==== Running parse_booking ====")
    _run_prompt("Enter service:duration in min (e.g. haircut:45): ", parse_booking,
                "Service and Duration:")

    print("\n==== Running duration_average ====")
    _run_prompt("Enter durations as CSV (e.g. 30,45,60): ", duration_average,
                "Average Duration:")

    print("\n==== Running payable_bill ====")
    _run_prompt("Enter bill|discount (e.g. 800|100): ", payable_bill,
                "Payable Bill:")


if __name__ == "__main__":
    main()
