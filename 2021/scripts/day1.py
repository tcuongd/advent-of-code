from typing import Iterable

def count_increases_sliding(readings: Iterable[float], window_size: int):
    last_window_reads = []
    increases = 0
    for i, reading in enumerate(readings):
        reading = float(reading)
        last_window_reads.append(reading)
        if i < window_size:
            continue
        if len(last_window_reads) > window_size + 1:
            del last_window_reads[0]
        if last_window_reads[-1] > last_window_reads[0]:
            increases += 1
    return increases

def main():
    with open("data/day1_input.txt", "r") as f:
        increases_lag1 = count_increases_sliding(f, window_size=1)
    print(f"A: {increases_lag1}")
    with open("data/day1_input.txt", "r") as f:
        increases_lag3 = count_increases_sliding(f, window_size=3)
    print(f"B: {increases_lag3}")

if __name__ == "__main__":
    main()
