from typing import Dict, List, Set, Tuple
from collections import defaultdict

def read_data(input_path: str) -> Dict[str, List[str]]:
    graph = defaultdict(list)
    with open(input_path, "r") as f:
        connections = [tuple(p.split("-")) for p in [l.strip() for l in f.readlines()]]
    for c in connections:
        graph[c[0]].append(c[1])
        graph[c[1]].append(c[0])
    return graph

def get_small_caves(graph: Dict[str, List[str]]) -> Set[str]:
    return {cave for cave in graph.keys() if cave.lower() == cave and cave not in ['start', 'end']}

def _find_paths(
    graph: Dict[str, List[str]],
    current: str,
    destination: str,
    visited: Set[str],
    path: List[str],
    paths_container: Set[Tuple[str]],
    small_caves: Set[str],
    special_cave: str = None,
    special_cave_counter: int = None,
) -> None:
    """Updates paths_container in place."""
    # https://www.geeksforgeeks.org/find-paths-given-source-destination/
    if current in small_caves or current in ['start', 'end']:
        visited.add(current)
    if current == special_cave and special_cave_counter is not None:
        special_cave_counter += 1
        if special_cave_counter == 2:
            visited.add(current)
    path.append(current)

    if current == destination:
        paths_container.add(tuple(path.copy()))
    else:
        for next_step in graph[current]:
            if not next_step in visited:
                _find_paths(graph, next_step, destination, visited, path, paths_container, small_caves, special_cave, special_cave_counter)
    # Backtrack mutated objects for the next function call at the same stack level.
    del path[-1]
    visited.discard(current)

def find_paths(graph: Dict[str, List[str]]) -> Set[Tuple[str]]:
    all_paths = set()
    small_caves = get_small_caves(graph)
    visited = set()
    path = []
    _find_paths(graph, 'start', 'end', visited, path, all_paths, small_caves)
    return all_paths

def find_paths_with_special_cave(graph: Dict[str, List[str]]) -> Set[Tuple[str]]:
    all_paths = set()
    small_caves = get_small_caves(graph)
    for special_cave in small_caves:
        sc_paths = set()
        sc_small_caves = small_caves.copy()
        sc_small_caves.remove(special_cave)
        visited = set()
        path = []
        _find_paths(graph, 'start', 'end', visited, path, sc_paths, sc_small_caves, special_cave, 0)
        all_paths.update(sc_paths)
    return all_paths

def main():
    graph = read_data("data/day12_input.txt")
    all_paths = find_paths(graph)
    print(len(all_paths))
    sc_all_paths = find_paths_with_special_cave(graph)
    print(len(sc_all_paths))

if __name__ == "__main__":
    main()
