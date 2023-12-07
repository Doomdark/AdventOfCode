def part1(pw):
    pw = list(str(pw))
    if pw != sorted(pw) or len(set(pw)) == len(pw):
        return False
    return True


def part2(pw):
    return 2 in [str(pw).count(d) for d in str(pw)]


pws = [pw for pw in range(357253, 892942 + 1) if part1(pw)]
print(f"PART 1: {len(pws)}")

pws_2 = [pw for pw in pws if part2(pw)]
print(f"PART 2: {len(pws_2)}")
