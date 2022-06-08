# -*- Python Version: 2.7 -*-
# -*- coding: utf-8 -*-

"""Descriptors for validating and cleaning user-input in Grasshopper Components."""


class Validated(object):
    """Base class for all Validator objects. Ensure all children have a 'validate' method."""

    def __init__(self, storage_name):
        self.storage_name = storage_name

    def __set__(self, instance, value):
        """Set the value on the instance. Not, the 'instance' is the class-attribute."""
        value = self.validate(
            name=self.storage_name,
            new_value=value,
            old_value=instance.__dict__.get(self.storage_name, None)
        )
        instance.__dict__[self.storage_name] = value

    def __get__(self, instance, owner):
        return instance.__dict__[self.storage_name]

    def validate(self, name,  new_value, old_value):
        """return validated input value, or raise an error."""
        raise NotImplementedError("Error: Must implement Validated method on subclass.")

    def __str__(self):
        return "Validated[{}](storage_name={})".format(self.__class__.__name__, self.storage_name)


class NotNone(Validated):
    """A value which may not be None."""

    def validate(self, name, new_value, old_value):
        if new_value is not None:
            return new_value

        if old_value is not None:
            return old_value

        raise ValueError("Error: value for {} may not be None.".format(name))


class HBName(Validated):
    """A String which is valid as an HB-Room or HB-Model display name."""

    def validate(self, name, new_value, old_value):
        if new_value is None:
            return old_value

        new_value = str(new_value).strip().replace(" ", "_")

        if not new_value:
            raise ValueError("Error: input for {} cannot be blank.".format(name))

        return new_value


class IntegerNonZero(Validated):
    """An Integer value which is not allowed to be zero."""

    def validate(self, name, new_value, old_value):
        if new_value is None:
            return old_value

        try:
            new_value = int(new_value)
        except:
            raise ValueError("Error: input {} of type: {} is not allowed."
                             "Supply positive integer only.".format(
                                 new_value, type(new_value)))

        if new_value < 1:
            raise ValueError(
                "Error: input for '{}' cannot be zero or negative.".format(name))

        return new_value


class FloatNonZero(Validated):
    """A Floating Point value which is not allowed to be zero."""

    def validate(self, name, new_value, old_value):
        if new_value is None:
            return old_value

        try:
            new_value = float(new_value)
        except:
            raise ValueError("Error: input {} of type: {} is not allowed."
                             "Supply positive integer only.".format(
                                 new_value, type(new_value)))

        if new_value <= 0.0:
            raise ValueError(
                "Error: input for '{}' cannot be zero or negative.".format(name))

        return new_value
