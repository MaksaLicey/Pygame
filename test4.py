import json
import sys

with open('scoring.json') as file:
    data = json.load(file)
answers = list(map(str.strip, sys.stdin))
result = 0
for a in range(len(answers)):
    score = 0
    for j in range(len(data["scoring"])):
        if a in data["scoring"][j]["required_tests"]:
            score = data["scoring"][j]["points"] / len(data["scoring"][j]["required_tests"])
    if answers[a] == 'ok':
        result += score
print(round(result))
