# L6_L7_42 - Salon Booking

## Lab 7: Fuzz Testing

This lab uses Hypothesis to fuzz three salon booking input parsers, identify edge cases, and verify defensive validation.

### Files

| File | Description |
| --- | --- |
| salon_booking.py | Validated booking, duration-average, and bill functions plus a safe interactive demo. |
| test_salon_booking.py | Hypothesis tests for arbitrary inputs, valid input properties, and business rules. |
| requirements.txt | Test dependencies. |

Install and run from this directory:

    python -m pip install -r requirements.txt
    python -m pytest -q
    python salon_booking.py

Malformed values raise a clear ValueError from the functions. The interactive demo reports the validation error and continues instead of crashing.
