import pytest

from salon_booking import arrival_status, can_book, extra_time_charge


def test_extra_time_charge_branches():
    with pytest.raises(ValueError, match="unknown service"):
        extra_time_charge("nails", 30, "junior", False)

    with pytest.raises(ValueError, match="invalid duration"):
        extra_time_charge("haircut", -1, "junior", False)

    assert extra_time_charge("haircut", 30, "junior", False) == 0
    assert extra_time_charge("haircut", 46, "junior", True) == 10
    assert extra_time_charge("spa", 91, "junior", True) == 10
    assert extra_time_charge("haircut", 90, "senior", False) == 1080
    assert extra_time_charge("haircut", 91, "senior", False) == 1830
    assert extra_time_charge("haircut", 91, "stylist", False) == 1586


def test_can_book_branches():
    assert can_book(2, 1, True) is True
    assert can_book(3, 1, True) is False
    assert can_book(4, 2, False) is True
    assert can_book(5, 1, False) is False
    assert can_book(4, 3, False) is False


def test_arrival_status_branches():
    assert arrival_status(20, True, True) == "open"
    assert arrival_status(19, True, True) == "late"
    assert arrival_status(5, True, True) == "late"
    assert arrival_status(4, True, True) == "closed"

    assert arrival_status(5, False, False) == "open"
    assert arrival_status(4, False, False) == "late"
    assert arrival_status(-10, False, False) == "late"
    assert arrival_status(-11, False, False) == "closed"