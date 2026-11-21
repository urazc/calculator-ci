"""Read a multiple-choice mathematics exam and print its answer key.

This program reuses arithmetic functions from the Week 7 calculator.py.
Keep calculator.py in the same directory.
"""
import importlib
import math
import re
from pathlib import Path

EXAM_FILE = Path(__file__).with_name("exam.uraz")
QUESTION = re.compile(
    r"^\s*(\d+)\.\s*[^:]+:\s*"
    r"(-?\d+(?:\.\d+)?)\s*([+*/-])\s*"
    r"(-?\d+(?:\.\d+)?)\s*$"
)
OPTION = re.compile(r"^\s*([ABCD])\.\s*(-?\d+(?:\.\d+)?)\s*$")
FUNCTION_NAMES = {
    "+": ("add", "addition", "add_numbers", "sum_numbers"),
    "-": ("subtract", "subtraction", "sub", "subtract_numbers"),
    "*": ("multiply", "multiplication", "mul", "multiply_numbers"),
    "/": ("divide", "division", "div", "divide_numbers"),
}

def calculate(calculator, left, operator, right):
    if operator == "/" and right == 0:
        raise ZeroDivisionError("Division by zero in exam question")
    for name in FUNCTION_NAMES[operator]:
        function = getattr(calculator, name, None)
        if callable(function):
            return float(function(left, right))
    raise RuntimeError(
        f"calculator.py has no recognised function for '{operator}'. "
        f"Expected one of: {', '.join(FUNCTION_NAMES[operator])}. "
        "Please check the Week 7 calculator interface."
    )

def parse_exam(path):
    questions = []
    current = None
    for line_number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line:
            continue
        question = QUESTION.fullmatch(line)
        if question:
            if current is not None:
                if set(current["options"]) != set("ABCD"):
                    raise ValueError(f"Question {current['number']} needs options A-D")
                questions.append(current)
            current = {
                "number": int(question.group(1)),
                "left": float(question.group(2)),
                "operator": question.group(3),
                "right": float(question.group(4)),
                "options": {},
            }
            continue
        option = OPTION.fullmatch(line)
        if option and current is not None:
            letter = option.group(1)
            if letter in current["options"]:
                raise ValueError(f"Duplicate option {letter} on line {line_number}")
            current["options"][letter] = float(option.group(2))
            continue
        raise ValueError(f"Invalid exam format on line {line_number}: {line}")
    if current is not None:
        if set(current["options"]) != set("ABCD"):
            raise ValueError(f"Question {current['number']} needs options A-D")
        questions.append(current)
    if not questions:
        raise ValueError("No questions found")
    return questions

def main():
    calculator = importlib.import_module("calculator")
    questions = parse_exam(EXAM_FILE)
    print("Mathematics Examination - Answer Key")
    for question in questions:
        result = calculate(
            calculator, question["left"], question["operator"], question["right"]
        )
        matches = [
            letter for letter, answer in question["options"].items()
            if math.isclose(result, answer, rel_tol=1e-9, abs_tol=1e-9)
        ]
        answer = matches[0] if len(matches) == 1 else "INVALID"
        print(f"Question {question['number']}: {answer}")
    print(f"Total questions processed: {len(questions)}")

if __name__ == "__main__":
    main()
