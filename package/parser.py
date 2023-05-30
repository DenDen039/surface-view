import re
from numpy import *  # required for parses to parse math functions e.g sin(), cos()

class Parser:
    def __init__(self):
        ...

    # float, float e.g 123.123, 123.123
    def parse_two_floats(self, input_string: str) -> [float, float]:
        check = re.match("^-?(0|[1-9]\d*)(\.\d*)? *, *-?(0|[1-9]\d*)(\.\d*)?", input_string)
        if check:
            return [float(x) for x in input_string.split(",")]
        return False

    def check_expression_string_two_params(self, input_string: str) -> bool:

        if 't' not in input_string.replace('', ' ').split(' '):
            input_string += " + t*0"

        if 'v' not in input_string.replace('', ' ').split(' '):
            input_string += " + v*0"

        try:
            parsed_string = lambda t, v: eval(input_string)
            t = 0.456456
            v = 0.3326
            a = parsed_string(t, v)
            print(parsed_string)
        except Exception:
            return False
        return True

    def parse_expression_string_to_lambda_two_params(self, input_string: str):
        if 't' not in input_string.replace('', ' ').split(' '):
            input_string += " + t*0"

        if 'v' not in input_string.replace('', ' ').split(' '):
            input_string += " + v*0"

        if self.check_expression_string_two_params(input_string):
            parsed_string = lambda t, v: eval(input_string)
            print(f"parsed string: {parsed_string(1,1)}")
        else:
            raise SyntaxError("Given statement is not correct math input, or has other variables than t and v")

        return parsed_string

    # TODO vvv
    def check_expression_string(self, input_string: str) -> bool:

        if 't' not in input_string.replace('', ' ').split(' '):
            input_string += " + t*0"

        try:
            parsed_string = lambda t: eval(input_string)
            t = 0.456456
            a = parsed_string(t)
            print(parsed_string)
        except NameError:
            return False
        return True


    def parse_expression_string_to_lambda(self, input_string: str):
        if 't' not in input_string.replace('', ' ').split(' '):
            input_string += " + t*0"

        if self.check_expression_string(input_string):
            parsed_string = lambda t: eval(input_string)
        else:
            raise SyntaxError("Given statement is not correct math input, or has other variables than t")

        return parsed_string
