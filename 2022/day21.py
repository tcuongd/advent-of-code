from collections import defaultdict
import re


def read_data() -> tuple[dict, dict, dict]:
    numbers = {}
    links = defaultdict(list)
    operators = {}
    with open("day21.txt", "r") as f:
        for l in f.readlines():
            l = l.strip()
            if re.search(r"([a-z]{4}): ([0-9]+)$", l):
                monkey, num = re.search(r"([a-z]{4}): ([0-9]+)$", l).groups()
                numbers[monkey] = int(num)
            elif re.search(r"([a-z]{4}): ([a-z]{4}) ([\+\-\*\/]{1}) ([a-z]){4}$", l):
                monkey, linked_1, operator, linked_2 = re.search(
                    r"([a-z]{4}): ([a-z]{4}) ([\+\-\*\/]{1}) ([a-z]{4})$", l
                ).groups()
                links[monkey].extend([linked_1, linked_2])
                operators[monkey] = operator
    return numbers, links, operators


def parse(
    numbers: dict[str, int], links: dict[str, list[str]], operators: dict[str, str]
) -> dict[str, int]:
    final_numbers = {m: v for m, v in numbers.items()}
    while "root" not in final_numbers:
        for monkey, linked_monkeys in links.items():
            if monkey not in final_numbers:
                if final_numbers.get(linked_monkeys[0]) and final_numbers.get(linked_monkeys[1]):
                    to_calculate = f"{final_numbers[linked_monkeys[0]]} {operators[monkey]} {final_numbers[linked_monkeys[1]]}"
                    final_numbers[monkey] = eval(to_calculate)
    return final_numbers


def force_equality(
    numbers: dict[str, int], links: dict[str, list[str]], operators: dict[str, str]
) -> int:
    numbers = {m: v for m, v in numbers.items()}
    lhs, rhs = links["root"]
    equality = False
    # Magic number found manually by re-running the search and inspecting the results for about 10 mins.
    # (kept increasing or decreasing each digit to get the RHS and LHS closer).
    test_value = 3219579395000
    while not equality:
        test_value += 1
        numbers["humn"] = test_value
        parsed = parse(numbers, links, operators)
        equality = parsed[lhs] == parsed[rhs]
    return test_value


numbers, links, operators = read_data()
final_numbers = parse(numbers, links, operators)
print(final_numbers["root"])

required_humn = force_equality(numbers, links, operators)
print(required_humn)
