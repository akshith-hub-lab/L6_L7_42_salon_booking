"""Property-based fuzz tests for all public booking input parsers."""

from hypothesis import given, settings, strategies as st

from salon_booking import duration_average, parse_booking, payable_bill


FUZZ_SETTINGS = settings(max_examples=250, deadline=None)
FUZZ_INPUT = st.one_of(st.text(), st.none(), st.integers(), st.floats(allow_nan=True))


@FUZZ_SETTINGS
@given(FUZZ_INPUT)
def test_parse_booking_handles_arbitrary_input(value):
    try:
        service, minutes = parse_booking(value)
    except ValueError:
        return
    assert isinstance(value, str)
    assert service and service == service.title()
    assert minutes >= 0


@FUZZ_SETTINGS
@given(FUZZ_INPUT)
def test_duration_average_handles_arbitrary_input(value):
    try:
        result = duration_average(value)
    except ValueError:
        return
    assert isinstance(value, str)
    assert isinstance(result, int)
    assert result >= 0


@FUZZ_SETTINGS
@given(FUZZ_INPUT)
def test_payable_bill_handles_arbitrary_input(value):
    try:
        result = payable_bill(value)
    except ValueError:
        return
    assert isinstance(value, str)
    assert result >= 0


@FUZZ_SETTINGS
@given(st.text(min_size=1).filter(lambda s: s.strip() and ":" not in s),
       st.floats(min_value=0, max_value=10000, allow_nan=False, allow_infinity=False))
def test_parse_booking_valid_values(service, minutes):
    parsed_service, parsed_minutes = parse_booking(f"{service}:{minutes}")
    assert parsed_service == service.strip().title()
    assert parsed_minutes == minutes


@FUZZ_SETTINGS
@given(st.lists(st.integers(min_value=0, max_value=100000), min_size=1, max_size=30))
def test_duration_average_matches_reference(values):
    encoded = ",".join(map(str, values))
    assert duration_average(encoded) == sum(values) // len(values)


@FUZZ_SETTINGS
@given(st.floats(min_value=0, max_value=100000, allow_nan=False, allow_infinity=False),
       st.floats(min_value=0, max_value=100000, allow_nan=False, allow_infinity=False))
def test_payable_bill_never_goes_below_zero(bill, discount):
    assert payable_bill(f"{bill}|{discount}") == round(max(bill * 1.18 - discount, 0), 2)
