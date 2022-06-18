# -*- Python Version: 2.7 -*-
# -*- coding: utf-8 -*-

"""Descriptors for validating and cleaning user-input into Grasshopper Components.

Basic Usage:
------------

class ZeroNotAllowedValidator(Validated): # Subclass from Validated
    def validate(self, name,  new_value, old_value):
        if new_value == 0:
            raise ValueError("Input for for '{}' may not be 0!".format(name))
        else:
            return new_value

class MyClassWithValidation(object):
    example = ZeroNotAllowedValidator(storage_name="example") # Class Attribute

>>> obj = MyClassWithValidation()
>>> obj.example = 0
>>> ValueError: Input for 'example' may not be 0!
"""


class Validated(object):
    """Base class for all Validator objects. Ensure all children have a 'validate' method.

    During __set__ the subclass's .validate() method will be run using the input value. Cleaning
    and type-checking or any other type of validation should take place within this method.
    The .validate() method should raise a ValueError if the input does not meet the specification.
    """

    def __init__(self, storage_name):
        self.storage_name = storage_name  # normally the same as the Class Attribute

    def __set__(self, instance, value):
        """Set the value on the instance. Runs a .validate() method on self to 
        allow for subclasses to implement custom input validation.

        Arguments:
        ----------
            * instance: The descriptor class variable.
            * value: The value to validate and set.
        """
        value = self.validate(
            name=self.storage_name,
            new_value=value,
            old_value=instance.__dict__.get(self.storage_name, None)
        )
        instance.__dict__[self.storage_name] = value

    def __get__(self, instance, owner):
        """
        Arguments:
        ---------
            * instance: The descriptor class variable.
            * owner: The Class which has the descriptor as a class variable.
        """
        return instance.__dict__[self.storage_name]

    def validate(self, name,  new_value, old_value):
        """Return validated input value, or raise an error.

        Arguments:
        ---------
            * name: The Class-Attribute's name. Mostly used for Error messages.
            * new_value: The new value to validate.
            * old_value: The original value of the descriptor, sometimes useful 
                for returning if 'new_value' is None, or similar.
        """
        raise NotImplementedError(
            "Error: Must implement the .validated() method on subclass of Validated.")

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

        # No spaces, no leading or trailing whitespace
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


class Float(Validated):
    """A Floating Point value of any value (positive or negative)"""

    def validate(self, name, new_value, old_value):
        if new_value is None:
            return old_value

        try:
            new_value = float(new_value)
        except:
            raise ValueError("Error: input {} of type: {} is not allowed."
                             "Supply float only.".format(
                                 new_value, type(new_value)))

        return new_value


class FloatNonZero(Validated):
    """A Floating Point value which is not allowed to be zero."""
    tolerance = 0.0001

    def validate(self, name, new_value, old_value):
        if new_value is None:
            return old_value

        try:
            new_value = float(new_value)
        except:
            raise ValueError("Error: input {} of type: {} is not allowed."
                             "Supply float values only.".format(
                                 new_value, type(new_value)))

        if new_value - 0.0 < self.tolerance:
            raise ValueError(
                "Error: input for '{}' cannot be zero.".format(name))

        return new_value


class FloatPositiveValue(Validated):
    """A Floating Point value which is not allowed to be negative"""

    def validate(self, name, new_value, old_value):
        if new_value is None:
            return old_value

        try:
            new_value = float(new_value)
        except:
            raise ValueError("Error: input {} of type: {} is not allowed."
                             "Supply float values only.".format(
                                 new_value, type(new_value)))

        if new_value < 0:
            raise ValueError(
                "Error: input for '{}' cannot be negative.".format(name))

        return new_value
