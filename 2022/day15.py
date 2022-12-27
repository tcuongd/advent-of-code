import re


def read_data() -> list[tuple[complex, complex]]:
    pairs = []
    with open("day15.txt", "r") as f:
        for l in f.readlines():
            l = l.strip()
            sensor, beacon = (t.strip() for t in l.split(":"))
            sensor_x, sensor_y = (
                int(c) for c in re.search(".*x=(-?[0-9]+), y=(-?[0-9]+)", sensor).groups()
            )
            beacon_x, beacon_y = (
                int(c) for c in re.search(".*x=(-?[0-9]+), y=(-?[0-9]+)", beacon).groups()
            )
            pairs.append(
                (
                    complex(sensor_x, sensor_y),
                    complex(beacon_x, beacon_y),
                )
            )
    return pairs


def get_taxi_distance(c1: complex, c2: complex) -> int:
    return int(abs((c1 - c2).real) + abs((c1 - c2).imag))


def get_detected_in_row(data: list[tuple[complex, complex]], row: int) -> list[tuple[int, int]]:
    detected = []
    for sensor, beacon in data:
        distance = get_taxi_distance(sensor, beacon)
        total_dy = abs(int(row - sensor.imag))
        if distance < total_dy:
            continue
        total_dx = distance - total_dy
        low_x, high_x = int(sensor.real - total_dx), int(sensor.real + total_dx)
        detected.append((low_x, high_x))
    detected = sorted(detected)
    # Merge overlapping sections
    current_idx = 1
    while current_idx < len(detected):
        if (
            detected[current_idx][0] >= detected[current_idx - 1][0]
            and detected[current_idx][1] <= detected[current_idx - 1][1]
        ):
            del detected[current_idx]
        elif detected[current_idx - 1][1] >= detected[current_idx][0]:
            new_range = (detected[current_idx - 1][0], detected[current_idx][1])
            del detected[current_idx]
            del detected[current_idx - 1]
            detected.insert(current_idx - 1, new_range)
        else:
            current_idx += 1
    return detected


def count_detected_in_row(detected: list[list[int, int]]) -> int:
    total_detected = 0
    for low, high in detected:
        total_detected += high - low + 1
    return total_detected


def count_known_beacons(data: list[tuple[complex, complex]], row: int) -> int:
    to_remove = set()
    for _, beacon in data:
        if beacon.imag == row:
            to_remove.add(beacon.real)
    return len(to_remove)


def find_unknown_beacon(
    data: list[tuple[complex, complex]], min_xy: int, max_xy: int
) -> tuple[int, int]:
    x_value = None
    for row in range(max_xy + 1):
        detected = get_detected_in_row(data, row)
        if len(detected) == 1:
            if detected[0][0] == min_xy + 1 and detected[0][1] == max_xy:
                x_value = min_xy
                break
            elif detected[0][1] == max_xy - 1 and detected[0][0] == min_xy:
                x_value = max_xy
                break
        elif len(detected) == 2:
            if detected[0][1] + 1 > min_xy and detected[0][1] + 1 < max_xy:
                x_value = detected[0][1] + 1
                break
    return (x_value, row)


ROW = 2000000
data = read_data()
detected = get_detected_in_row(data, ROW)
coverage = count_detected_in_row(detected)
known_beacons = count_known_beacons(data, ROW)
print(coverage - known_beacons)

MIN_XY = 0
MAX_XY = 4000000
distress = find_unknown_beacon(data, MIN_XY, MAX_XY)
print(distress)
print(distress[0] * 4000000 + distress[1])
