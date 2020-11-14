#!python3.10

from typing import Optional


def safe_input_int(prompt: str,
                   positiveOnly: bool = True,
                   minimumValue: Optional[int] = None) -> int:
    """Take an integer value as input, safely, from the user. Guaranteed to return an integer value to the provided spec.

    Args:
        prompt (str): the string prompt to give the user before the input prompt.
        positiveOnly (bool): whether the integer should be positive (not including 0). Defaults to True.
        minimumValue: (Optional[int]): the minimum value of the integer. If not supplied, no minimum value. Defaults to None.

    Returns:
        int: the safe integer value provided by the user.
    """
    def is_above_or_equal_to_minimum_if_minimum_exists(value: int) -> bool:
        """Check if given `value` is above or equal to the minimum value

        Args:
            value (int): the value to compare to `minimumValue`

        Returns:
            bool: `True` if greater than or equal to `minimumValue`, or if `minimumValue` is `None`, `False` otherwise
        """

        if minimumValue is not None:
            return value >= minimumValue
        else:
            return True

    integerInput: int

    while True:
        unsanitisedInput = input(prompt)
        try:
            # try to cast the un-sanitized input to an integer
            integerInput = int(unsanitisedInput)
        except ValueError as _:
            # user inputted an invalid integer value.
            print("Invalid input. Please enter a" +
                  (" positive" if positiveOnly else "n") + " integer value.")
        else:
            positiveValid: bool = True
            # no exception, input is a valid integer.
            # check if satisfies positiveOnly parameter
            if positiveOnly:
                if integerInput > 0:
                    # the value is positive. woohoo!
                    pass
                else:
                    # the value is not positive, not satisfying the 'positive' requirement of the input.
                    print("The input must be positive. Please try again.")
                    positiveValid = False

            if positiveValid:
                if is_above_or_equal_to_minimum_if_minimum_exists(integerInput):
                    # the value is above or equal to the minimum value if it exists. woohoo!
                    # value satisfies all requirements completely. safe to return.
                    return integerInput
                else:
                    # the value is below the minimum value specified... oops
                    print(
                        "The given input is below the minimum value of {}. Please try again."
                        .format(str(minimumValue)))
