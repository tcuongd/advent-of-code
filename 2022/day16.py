from collections import defaultdict, deque, Counter
import re

import numpy as np


def read_data() -> tuple[dict[str, int], dict[str, list[str]]]:
    flows = {}
    adjs = defaultdict(list)
    with open("day16.txt", "r") as f:
        for l in f.readlines():
            l = l.strip()
            valve, flow, leads = re.search(
                "^Valve ([A-Z]+).*flow rate=([0-9]+);.*valves? ([A-Z, ]+)$", l
            ).groups()
            flows[valve] = int(flow)
            adjs[valve].extend([n.strip() for n in leads.split(",")])
    return flows, adjs


def bfs(adjs: dict[str, list[str]], start: str, end: str) -> list[str]:
    q = deque([start])
    visited = set()
    links = {}
    while q:
        parent = q.popleft()
        if parent == end:
            break
        for child in adjs[parent]:
            if child not in visited:
                q.append(child)
                links[child] = parent
                visited.add(child)
    if end in links:
        path = [end]
        while path[-1] != start:
            path.append(links[path[-1]])
        return list(reversed(path))[1:]
    else:
        return []


def get_future_value(current_mins: int, total_mins: int, n_moves: int, pressure: int) -> int:
    wasted = n_moves + 1  # plus 1 to open the valve
    mins_left = total_mins - current_mins + 1
    return max(mins_left - wasted, 0) * pressure


def simulate(flows: dict[str, int], adjs: dict[str, list[str]], start: str) -> tuple[int, list]:
    MINS = 30
    valves_open = set()
    non_zeros = set([v for v, f in flows.items() if f > 0])
    current = start
    pressure = 0
    rngs = np.random.uniform(size=MINS)
    path = []
    has_target = False
    logger = []
    for i in range(1, MINS + 1):
        info_start = f"Minute {i}; Valves Open: {valves_open}; Pressure: {sum([flows[v] for v in valves_open]):,.0f}; Current: {current}; "
        for valve in valves_open:
            pressure += flows[valve]
        # We've opened all the valves
        if not non_zeros.difference(valves_open):
            continue
        if not path and not has_target:
            # Generate candidates
            candidates = non_zeros.difference(valves_open)
            future_values = []
            for candidate in candidates:
                if current == candidate:
                    candidate_path = []
                else:
                    candidate_path = bfs(adjs, current, candidate)
                    # If candidate unreachable
                    if not candidate_path:
                        continue
                n_moves = len(candidate_path)
                future_values.append(
                    (
                        candidate,
                        get_future_value(i, MINS, n_moves, flows[candidate]),
                        candidate_path,
                    )
                )
            priority = sorted(future_values, key=lambda item: item[1], reverse=True)
            values = np.array([item[1] for item in priority])
            if np.sum(values) == 0:
                chosen = -1
            else:
                normalized_cdf = np.cumsum(values / np.sum(values))
                chosen = np.argwhere(rngs[i - 1] < normalized_cdf)
                if chosen.shape[0] == 0:
                    chosen = -1
                else:
                    chosen = chosen[0][0]
            path = priority[chosen][2]
        # Opening the current valve is the best choice
        if not path:
            valves_open.add(current)
            has_target = False
            info_action = f"Opened {current}"
        # Moving is the best choice
        else:
            has_target = True
            current = path[0]
            del path[0]
            info_action = f"Moved to {current}"
        logger.append(info_start + info_action)
    return pressure, logger


def get_distribution(
    flows: dict[str, int], adjs: dict[str, list[str]], start: str, num_draws: int = 100000
) -> Counter:
    distribution = Counter()
    for _ in range(num_draws):
        pressure, logger = simulate(flows, adjs, start)
        distribution[pressure] += 1
        if pressure == max(list(distribution.keys())):
            with open("day16_logger.txt", "w") as f:
                f.write("\n".join(logger))
    return distribution


flows, adjs = read_data()
START = 'AA'
distribution = get_distribution(flows, adjs, START, 500000)
print(distribution)
print(max(list(distribution.keys())))
