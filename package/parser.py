import re
from numpy import *  # required for parses to parse math functions e.g sin(), cos()

class Parser:
    """
       A class for parsing and evaluating mathematical expressions.

       This class provides methods to parse expressions, check their validity, and convert them into lambda functions for evaluation.

       Attributes:
           None
       """
    def __init__(self):
        ...

    # float, float e.g 123.123, 123.123
    def parse_two_floats(self, input_string: str) -> [float, float]:
        """
                Parses an input string containing two floats separated by a comma.

                Args:
                    input_string (str): The input string to be parsed.

                Returns:
                    [float, float]: A list of two floats extracted from the input string.

                Raises:
                    None
        """
        check = re.match("^-?(0|[1-9]\d*)(\.\d*)? *, *-?(0|[1-9]\d*)(\.\d*)?", input_string)
        if check:
            return [float(x) for x in input_string.split(",")]
        return False

    def check_expression_string_two_params(self, input_string: str) -> bool:
        """
                Checks the validity of an expression string with two parameters.

                Args:
                    input_string (str): The expression string to be checked.

                Returns:
                    bool: True if the expression is valid, False otherwise.

                Raises:
                    None
        """

        if 't' not in input_string.replace('', ' ').split(' '):
            input_string += " + t*0"

        if 'v' not in input_string.replace('', ' ').split(' '):
            input_string += " + v*0"

        input_string = input_string.replace('^', '**')

        try:
            parsed_string = lambda t, v: eval(input_string)
            t = 0.456456
            v = 0.3326
            a = parsed_string(t, v)
        except Exception:
            return False
        return True

    def parse_expression_string_to_lambda_two_params(self, input_string: str):
        """
              Parses an expression string with two parameters into a lambda function.

              Args:
                  input_string (str): The expression string to be parsed.

              Returns:
                  function: A lambda function that represents the parsed expression.

              Raises:
                  SyntaxError: If the input string is not a correct math input or contains variables other than 't' and 'v'.
        """
        if 't' not in input_string.replace('', ' ').split(' '):
            input_string += " + t*0"

        if 'v' not in input_string.replace('', ' ').split(' '):
            input_string += " + v*0"

        input_string = input_string.replace('^', '**')

        if self.check_expression_string_two_params(input_string):
            parsed_string = lambda t, v: eval(input_string)

        else:
            raise SyntaxError("Given statement is not correct math input, or has other variables than t and v")

        return parsed_string

    # TODO vvv
    def check_expression_string(self, input_string: str) -> bool:
        """
                Checks the validity of an expression string with one parameter.

                Args:
                    input_string (str): The expression string to be checked.

                Returns:
                    bool: True if the expression is valid, False otherwise.

                Raises:
                    None
        """

        if 't' not in input_string.replace('', ' ').split(' '):
            input_string += " + t*0"

        try:
            parsed_string = lambda t: eval(input_string)
            t = 0.456456
            a = parsed_string(t)
        except Exception:
            return False
        return True


    def parse_expression_string_to_lambda(self, input_string: str):
        """
                  Parses an expression string with one parameter into a lambda function.

                  Args:
                      input_string (str): The expression string to be parsed.

                   Returns:
                      function: A lambda function that represents the parsed expression.

                   Raises:
                      SyntaxError: If the input string is not a correct math input or contains variables other than 't'
        """
        if 't' not in input_string.replace('', ' ').split(' '):
            input_string += " + t*0"

        input_string = input_string.replace('^', '**')

        if self.check_expression_string(input_string):
            parsed_string = lambda t: eval(input_string)
        else:
            raise SyntaxError("Given statement is not correct math input, or has other variables than t")

        return parsed_string
