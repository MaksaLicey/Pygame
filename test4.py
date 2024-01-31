import os
import random

file_0 = open(os.path.join("AI", "AI_0"), mode="r+", encoding="utf-8")
AI_0_tactic = file_0.readlines()

file_1 = open(os.path.join("AI", "AI_1"), mode="r+", encoding="utf-8")
AI_1_tactic = file_1.readlines()

file_2 = open(os.path.join("AI", "AI_1"), mode="r+", encoding="utf-8")
AI_2_tactic = file_2.readlines()


class AI:
    def __init__(self, money, fabric, shops, enemy_money=[]):
        self.money = money
        self.fabric = fabric
        self.shops = shops
        self.enemy_money = enemy_money
        self.steps = {}


AI_0 = AI(10.0, 1, 0)
AI_1 = AI(10.0, 1, 0)
AI_2 = AI(10.0, 1, 0)

sls_AI = [AI_0, AI_1, AI_2]


def checker(command, bot_name, step):
    if command < 4:
        sls_AI[bot_name].fabric += 1
        sls_AI[bot_name].money -= 10
    elif command == 4:
        sls_AI[bot_name].shops += 1
        sls_AI[bot_name].money -= 10


def aio_0(step):
    sls_AI.remove(AI_0)
    [AI_0.enemy_money.append(i.money) for i in sls_AI]
    sls_AI.append(AI_0)
    if len(AI_0_tactic) >= 1:
        for str1 in AI_0_tactic:
            pass
    else:
        for i in range(10):
            if random.randrange(0, 8) < 4 and i > 0:
                i -= 1
            elif i < 6:
                i += 2
        if AI_0.money > 10:
            checker(random.randrange(0, 5), 1, step)


def aio_1(step):
    sls_AI.remove(AI_1)
    [AI_1.enemy_money.append(i.money) for i in sls_AI]
    sls_AI.append(AI_1)
    if len(AI_1_tactic) >= 1:
        for str1 in AI_1_tactic:
            pass
    else:
        for i in range(10):
            if random.randrange(0, 8) < 4 and i > 0:
                i -= 1
            elif i < 6:
                i += 2
        if AI_1.money > 10:
            checker(random.randrange(0, 5), 1, step)


def aio_2(step):
    sls_AI.remove(AI_2)
    [AI_2.enemy_money.append(i.money) for i in sls_AI]
    sls_AI.append(AI_2)
    if len(AI_2_tactic) >= 1:
        for str1 in AI_2_tactic:
            pass
    else:
        for i in range(10):
            if random.randrange(0, 8) < 4 and i > 0:
                i -= 1
            elif i < 6:
                i += 2
        if AI_0.money > 10:
            checker(random.randrange(0, 5), 1, step)


for humber in range(10):
    AI_0.steps[humber] = (AI_0.money, AI_0.fabric, AI_0.shops, AI_0.enemy_money)
    AI_1.steps[humber] = (AI_1.money, AI_1.fabric, AI_1.shops, AI_1.enemy_money)
    AI_2.steps[humber] = (AI_2.money, AI_2.fabric, AI_2.shops, AI_2.enemy_money)
    aio_0(humber)
    aio_1(humber)
    aio_2(humber)
    AI_0.money += float('%.2f' % (1 + AI_0.fabric * 3 + sum(AI_0.enemy_money) * 0.1))
    AI_1.money += float('%.2f' % (1 + AI_1.fabric * 3 + sum(AI_1.enemy_money) * 0.1))
    AI_2.money += float('%.2f' % (1 + AI_2.fabric * 3 + sum(AI_2.enemy_money) * 0.1))
    AI_0.enemy_money.clear()
    AI_1.enemy_money.clear()
    AI_2.enemy_money.clear()

winner = []
[winner.append(i.money) for i in sls_AI]
for m in sls_AI:
    # if m.money == winner[winner.index(max(winner))]:
    for p in m.steps:
        print(m.steps[p])
    print("==========")
