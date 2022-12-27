from collections import deque
import copy
import math


def read_data() -> tuple[
    list[deque], list[callable], list[str], list[str], list[int], list[int], list[int]
]:
    all_items = []
    operations = []
    operation_types = []
    operation_values = []
    div_tests = []
    trues = []
    falses = []
    with open("day11.txt", "r") as f:
        raw = [l.strip() for l in f.readlines()]
    for l in raw:
        if l.startswith("Monkey "):
            continue
        elif l.startswith("Starting items:"):
            items = deque([int(i.strip()) for i in l.split(":")[1].strip().split(",")])
            all_items.append(items)
        elif l.startswith("Operation:"):
            op = l.split(":")[1].strip().split(" = ")[1]
            operations.append(eval(f"lambda old: {op}"))
            if "+" in op:
                operation_types.append("add")
                operation_values.append(op.split(" + ")[1])
            elif "*" in op:
                operation_types.append("mul")
                operation_values.append(op.split(" * ")[1])
        elif l.startswith("Test:"):
            div_int = int(l.replace("Test: divisible by ", ""))
            div_tests.append(div_int)
        elif l.startswith("If true"):
            m_true = int(l.replace("If true: throw to monkey ", ""))
            trues.append(m_true)
        elif l.startswith("If false"):
            m_false = int(l.replace("If false: throw to monkey ", ""))
            falses.append(m_false)
    return all_items, operations, operation_types, operation_values, div_tests, trues, falses


def do_rounds(
    all_items: list[deque],
    operations: list[callable],
    div_tests: list[int],
    trues: list[int],
    falses: list[int],
    n_rounds: int,
) -> tuple[list[deque], int]:
    all_items = copy.deepcopy(all_items)
    n_inspections = [0 for _ in range(len(operations))]
    for _ in range(n_rounds):
        for i in range(len(operations)):
            for _ in range(len(all_items[i])):
                n_inspections[i] += 1
                worry = all_items[i].popleft()
                worry = operations[i](worry)
                worry = worry // 3
                if worry % div_tests[i] == 0:
                    target_monkey = trues[i]
                else:
                    target_monkey = falses[i]
                all_items[target_monkey].append(worry)
    return all_items, n_inspections


all_items, operations, _, _, div_tests, trues, falses = read_data()
final_items, n_inspections = do_rounds(all_items, operations, div_tests, trues, falses, 20)
print(n_inspections)
print(math.prod(sorted(n_inspections)[-2:]))


def do_rounds_v2(
    all_items: list[deque],
    operation_types: list[str],
    operation_values: list[str],
    div_tests: list[int],
    trues: list[int],
    falses: list[int],
    n_rounds: int,
) -> tuple[list[deque], list[int]]:
    modulos = []
    for i, monkey in enumerate(all_items):
        modulos.append(deque())
        for orig_value in monkey:
            modulos[i].append([orig_value % divisor for divisor in div_tests])
    n_inspections = [0 for _ in range(len(operation_types))]
    for _ in range(n_rounds):
        for i in range(len(operation_types)):
            for _ in range(len(modulos[i])):
                n_inspections[i] += 1
                item = modulos[i].popleft()
                if operation_types[i] == "add":
                    updated_item = [
                        (m + (int(operation_values[i]) % divisor)) % divisor
                        for m, divisor in zip(item, div_tests)
                    ]
                elif operation_types[i] == "mul":
                    if operation_values[i] == "old":
                        updated_item = [(m**2) % divisor for m, divisor in zip(item, div_tests)]
                    else:
                        updated_item = [
                            (m * (int(operation_values[i]) % divisor)) % divisor
                            for m, divisor in zip(item, div_tests)
                        ]
                if updated_item[i] == 0:
                    target_monkey = trues[i]
                else:
                    target_monkey = falses[i]
                modulos[target_monkey].append(updated_item)
    return modulos, n_inspections


all_items, _, operation_types, operation_values, div_tests, trues, falses = read_data()
final_items, n_inspections = do_rounds_v2(
    all_items, operation_types, operation_values, div_tests, trues, falses, 10000
)
print(n_inspections)
print(math.prod(sorted(n_inspections)[-2:]))
