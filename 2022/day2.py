# A, X = rock
# B, Y = paper
# C, Z = scissors

Q1_OUTCOMES = {
    "AX": 3,
    "AY": 6,
    "AZ": 0,
    "BX": 0,
    "BY": 3,
    "BZ": 6,
    "CX": 6,
    "CY": 0,
    "CZ": 3,
}

Q1_CHOICES = {
    "X": 1,
    "Y": 2,
    "Z": 3,
}

Q2_REQUIRED = {
    "AX": "scissors",
    "AY": "rock",
    "AZ": "paper",
    "BX": "rock",
    "BY": "paper",
    "BZ": "scissors",
    "CX": "paper",
    "CY": "scissors",
    "CZ": "rock",
}

Q2_CHOICES = {
    "rock": 1,
    "paper": 2,
    "scissors": 3,
}

Q2_OUTCOMES = {
    "X": 0,
    "Y": 3,
    "Z": 6,
}


def read_data() -> list[list[str]]:
    with open("day2.txt") as f:
        plays = [l.strip().split(" ") for l in f.readlines()]
    return plays


def get_outcomes(plays: list[list[str]]) -> list[int]:
    pairs = ["".join(p) for p in plays]
    return [Q1_OUTCOMES[pair] for pair in pairs]


def get_scores(plays: list[list[str]]) -> list[int]:
    scores_outcomes = get_outcomes(plays)
    scores_choices = [Q1_CHOICES[s] for o, s in plays]
    return [o + c for o, c in zip(scores_outcomes, scores_choices)]


def get_required(plays: list[list[str]]) -> list[int]:
    return [Q2_REQUIRED["".join(p)] for p in plays]


def get_scores_q2(plays: list[list[str]]) -> list[int]:
    required = get_required(plays)
    scores_choices = [Q2_CHOICES[r] for r in required]
    scores_outcomes = [Q2_OUTCOMES[result] for o, result in plays]
    return [o + c for o, c in zip(scores_outcomes, scores_choices)]


plays = read_data()
scores = get_scores(plays)
print(sum(scores))
scores_q2 = get_scores_q2(plays)
print(sum(scores_q2))
