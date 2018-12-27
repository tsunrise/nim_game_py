def partition_ways(left, most):
    if left < 0 or most == 0:
        return []
    if left == 0:
        return [[]]
    ways = []
    for decision in range(1,most+1):
        ways += [[decision] + w for w in partition_ways(left - decision, most)]
    return ways

def make_decision(left,most):

    def is_smart(way):
        total = sum(way)
        remain = total - sum(way[:-3])
        last_three = way[-3:]
        if len(last_three) < 3:
            return True
        else:
            return remain - last_three[0] > most
    all_win_ways = [w for w in partition_ways(left, most) if len(w) % 2 == 1 and is_smart(w)]
    # return all_win_ways[-1][0]
    return all_win_ways
# make_decision(7,4)

def play(total, most):
    player_turn = True
    while total > 0:
        if player_turn:
            player_decision = input("{} left. You can draw at most {}. Enter your decision: ".format(total, most))
            total -= int(player_decision)
            assert total >= 0, 'Fault by player'
        else:
            python_decision = make_decision(total, most)
            total -= int(python_decision)
            print("Computer draws {}.".format(python_decision))
            assert total >= 0, 'Fault by python'
        player_turn = not player_turn

    if not player_turn:
        print('Player wins.')
    else:
        print('Player loses.')



