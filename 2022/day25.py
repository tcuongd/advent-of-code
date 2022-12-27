def read_data() -> list[str]:
    with open("day25.txt", "r") as f:
        raw = [l.strip() for l in f.readlines()]
    return raw


def snafu_to_decimal(snafu: str) -> int:
    decimal = 0
    for i, char in enumerate(list(reversed(snafu))):
        if char == "-":
            num = -1
        elif char == "=":
            num = -2
        else:
            num = int(char)
        decimal += (5**i) * num
    return decimal


def parse_all(snafus: list[str]) -> list[int]:
    return [snafu_to_decimal(snafu) for snafu in snafus]


def decimal_to_snafu(decimal: int) -> str:
    snafu = []
    target = decimal
    while target > 0:
        target, mod = divmod(target, 5)
        if mod == 3:
            mod = -2
            target += 1
        elif mod == 4:
            mod = -1
            target += 1
        snafu.append(mod)
    snafu = [str(c).replace("-2", "=").replace("-1", "-") for c in reversed(snafu)]
    return "".join(snafu)


data = read_data()
decimals = parse_all(data)
print(sum(decimals))
print(decimal_to_snafu(sum(decimals)))
