# the start of a packet is indicated by a sequence of four characters that are all different.
# your subroutine needs to identify the first position where the four most recently received characters were all different.
# Specifically, it needs to report the number of characters from the beginning of the buffer to the end of the first such four-character marker.
from collections import deque, Counter

def read_data() -> list[str]:
    with open("day6.txt", "r") as f:
        raw = [l.strip() for l in f.readlines()][0]
    return list(raw)

def get_first_marker(data: list[str], distinct_chars: int) -> int:
    tracker = deque()
    for i, c in enumerate(data):
        tracker.append(c)
        if len(tracker) == distinct_chars:
            if len(Counter(tracker)) == len(tracker):
                return i + 1
            else:
                tracker.popleft()

data = read_data()
print(get_first_marker(data, 4))
print(get_first_marker(data, 14))
