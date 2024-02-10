f = open("27-A.txt", encoding="utf8")
n = int(f.readline())
lefts = [0 for i in range(1000)]
count = 0
sumi = 0
for i in range(1, n + 1):
    num = int(f.readline())
    sumi += num
    if sumi % 999 == 0:
        count = count + 1
    count += lefts[sumi % 999]
    print(count)
    lefts[sumi % 999] += 1
print(count)
