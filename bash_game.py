def memorize(f):
    seen = dict()

    def new(*args):
        return seen.get(tuple(args), f(*args))

    return new

class Tree:
    def __init__(self, label, branches=[]):
        for b in branches:
            assert isinstance(b, Tree)
        self.label = label
        self.branches = list(branches)

    def is_leaf(self):
        return not self.branches

    def map(self, fn):
        self.label = fn(self.label)
        for b in self.branches:
            b.map(fn)

@memorize
def partition_ways(left, most):
    if left < 0 or most == 0:
        return []
    if left == 0:
        return [[]]
    ways = []
    for decision in range(1,most+1):
        ways += [[decision] + w for w in partition_ways(left - decision, most)]
    return ways

@memorize
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
    if len(all_win_ways) == 0:
        return 1
    all_win_ways = way_to_tree(0, all_win_ways)
    return min(all_win_ways.branches, key=lambda x:ungranted_choices(x,most)).label


def ungranted_choices(t,most,depth=0):
    if t.is_leaf():
        return 0
    if depth % 2 == 1:
        return sum([ungranted_choices(b, most, depth + 1) for b in t.branches])
    else:
        if len(t.branches) == most:
            return sum([ungranted_choices(b, most, depth + 1) for b in t.branches])
        else:
            return 1 + sum([ungranted_choices(b, most, depth + 1) for b in t.branches])

def way_to_tree(root_label, ways):
    branches_labels = list(set(map(lambda x:x[0],ways)))
    branches = []
    for label in branches_labels:
        branches.append(way_to_tree(label,[way[1:] for way in ways if way[0] == label and len(way[1:]) > 0]))
    return Tree(root_label, branches)

def play(total, most, player_turn):
    while total > 0:
        if player_turn:
            player_decision = input("{} left. You can draw at most {}. Enter your decision: ".format(total, most))
            total -= int(player_decision)
            assert total >= 0, 'Fault by player'
            assert 1 <= int(player_decision) <= most
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



def start():
    print("Welcome to Nim Game!")
    total = input("Total Amount in the bag: ")
    most = input("Most amount you can draw: ")
    who = input("Who First? (0 = Computer, 1 = Player):")
    play(int(total), int(most), bool(int(who)))

if __name__ == "__main__":
    start()
