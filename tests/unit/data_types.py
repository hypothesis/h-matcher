"""Data types for testing the matchers"""
import enum


class _PrivateClass:
    """A dummy private class"""

    @classmethod
    def class_method(cls):
        """A dummy function"""

    def instance_method(self):
        """A dummy function"""


def _function():
    """A dummy function"""


PRIVATE_CLASS = _PrivateClass


class DataTypes(enum.Enum):
    """A collection of example data types to simplify writing unit-tests"""

    # The descriptions in the second position are mostly so Enum doesn't
    # equate things together and collapse our set of examples

    INT = (1, "integer")
    FALSY_INT = (0, "falsy integer")
    FLOAT = (1.0, "float")
    FALSY_FLOAT = (float(0), "falsy float")
    TRUE = (True, "true")
    FALSE = (False, "false")
    STRING = ("string", "string")
    FALSY_STRING = ("", "falsy string")

    # This stuff is covered by iteration over the Enum in parameters()
    # but coverage can't tell because they aren't directly referenced

    LAMBDA = (lambda: 1, "lambda")  # pragma: no cover
    CLASS_METHOD = (_PrivateClass.class_method, "class method")  # pragma: no cover
    INSTANCE_METHOD = (
        PRIVATE_CLASS.instance_method,
        "instance method",
    )  # pragma: no cover
    BUILTIN_METHOD = (print, "built in")  # pragma: no cover
    FUNCTION = (_function, "function")  # pragma: no cover

    CLASS = (_PrivateClass, "class")  # pragma: no cover
    CLASS_INSTANCE = (PRIVATE_CLASS, "class instance")  # pragma: no cover
    PACKAGE = (enum, "package")  # pragma: no cover

    @classmethod
    def parameters(cls, exact=None, exclude=None):
        exclude = set(exclude or [])
        exact = exact or cls

        return (example.value for example in exact if example not in exclude)


class Groups:
    FUNCTIONS = {
        DataTypes.LAMBDA,
        DataTypes.CLASS_METHOD,
        DataTypes.INSTANCE_METHOD,
        DataTypes.BUILTIN_METHOD,
        DataTypes.FUNCTION,
    }

    STRINGS = {DataTypes.STRING, DataTypes.FALSY_STRING}


DataTypes.Groups = Groups
