"""A collection of matchers for various number types."""

# pylint: disable=too-few-public-methods
from decimal import Decimal

from h_matchers.matcher.core import Matcher


class AnyNumber(Matcher):
    _types = (int, float, complex, Decimal)
    _type_description = "number"

    def __init__(self):
        self.conditions = []

        super().__init__("dummy", self.assert_equal_to)

    def assert_equal_to(self, other):
        # Ints are also booleans
        # pylint: disable=compare-to-zero
        assert other is not True and other is not False, "Not a boolean"

        # Check it's the right type
        assert isinstance(other, self._types)

        # Apply all the different conditions
        for label, test in self.conditions:
            assert test(other), label

        return True

    def truthy(self):
        return self._add_condition("falsy", bool)

    def falsy(self):
        return self._add_condition("falsy", lambda other: not bool(other))

    def _add_condition(self, description, test):
        self.conditions.append((description, test))
        return self

    def __str__(self):
        parts = [self._type_description]
        for condition_label, _ in self.conditions:
            parts.append(condition_label)

        return f"** any {', '.join(parts)} **"


class AnyInt(AnyNumber):
    """Matches any integer."""

    _types = (int,)
    _type_description = "integer"

    def less_than(self, value):
        return self._add_condition(f"<{value}", lambda other: other < value)

    def less_than_or_equal_to(self, value):
        return self._add_condition(f">={value}", lambda other: other <= value)

    def greater_than(self, value):
        return self._add_condition(f">{value}", lambda other: other > value)

    def greater_than_or_equal_to(self, value):
        return self._add_condition(f">={value}", lambda other: other >= value)

    def multiple_of(self, value):
        return self._add_condition(
            f"multiple of {value}", lambda other: not other % value
        )

    def even(self):
        return self.multiple_of(2)

    def odd(self):
        return self._add_condition("odd", lambda other: other % 2 == 1)

    def __lt__(self, value):
        return self.less_than(value)

    def __le__(self, value):
        return self.less_than_or_equal_to(value)

    def __gt__(self, value):
        return self.greater_than(value)

    def __ge__(self, value):
        return self.greater_than_or_equal_to(value)


class AnyReal(AnyInt):
    """Matches any real number."""

    _types = (int, float, Decimal)
    # We're going to refer to this as just a "number" as it's what we're going
    # to work on 99.9% of the time
    _type_description = "number"

    def approximately(self, value, error_factor=0.05):
        return self._add_condition(
            f"~ {value} ({error_factor})",
            lambda other: abs(value - other) <= error_factor * float(value),
        )


class AnyFloat(AnyReal):
    """Matches any float."""

    _types = (float,)
    _type_description = "float"


class AnyDecimal(AnyReal):
    """Matches any Decimal."""

    _types = (Decimal,)
    _type_description = "decimal"


class AnyComplex(AnyNumber):
    """Matches any complex number."""

    _types = (complex,)
    _type_description = "complex"
