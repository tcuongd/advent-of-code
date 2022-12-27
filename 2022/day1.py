def read_data() -> list[list[int]]:
    data = []
    with open("day1.txt") as f:
        current_elf = []
        for l in f.readlines():
            if l.strip() != '':
                current_elf.append(int(l.strip()))
            else:
                data.append(current_elf)
                current_elf = []
    return data

def get_totals(data: list[list[int]]) -> list[int]:
    return [sum(e) for e in data]

data = read_data()
totals = get_totals(data)
print(max(totals))
totals_sorted = sorted(totals, reverse=True)
print(sum(totals_sorted[:3]))
