import pickle
import random
from isolation import Isolation, Agent
from collections import defaultdict, Counter
from isolation import DebugState
from run_match import Match, play
from multiprocessing.pool import ThreadPool as Pool
from sample_players import RandomPlayer, GreedyPlayer, MinimaxPlayer



if __name__ == "__main__":
    initial_depth = 2
    state = Isolation()
    my_data = defaultdict(Counter)  # opening book always chooses the middle square on an open board
    pool = Pool(8)

    def score(state):
        own_loc = state.locs[state.player()]
        opp_loc = state.locs[1 - state.player()]
        own_liberties = state.liberties(own_loc)
        opp_liberties = state.liberties(opp_loc)
        return len(own_liberties) - len(opp_liberties)

    def simulate(state):
        if state.terminal_test():
            return 1, 0 if state.utility(0) > 0 else 0, 1
        matches = createMatch(state)
        wins = matches.count(True)
        losses = matches.count(False)
        return wins, losses

    def build_tree(state, depth, book):
        sp = (initial_depth - depth) * '  '
        if depth <= 0 or state.terminal_test():
            return simulate(state)

        value = (0, 0)
        print(sp + "Checking state {}".format(state))
        for action in state.actions():
            a_value = build_tree(state.result(action), depth - 1, book)
            # book[state][action] += a_value
            # print("choosing max from {} {}".format(value, a_value))
            value = [sum(x) for x in zip(value, a_value)]
        print(sp + "Returning {} with a win ratio of {}".format(value, value[0] / sum(value)))
        return value

    def createMatch(state):
        matches = []
        results = []

        for _ in range(1):
            matches.append(Match(
                players=(Agent(MinimaxPlayer, "p1"), Agent(MinimaxPlayer, "p2")),
                initial_state=state,
                time_limit=150,
                match_id=state,
                debug_flag=False))

        for result in pool.imap_unordered(play, matches):
            won = result[0].name == "p1"
            results.append(won)
        return results

    print("0")
    build_tree(state.result(0).result(3), initial_depth, my_data)
    build_tree(state.result(0).result(6), initial_depth, my_data)
    build_tree(state.result(0).result(30), initial_depth, my_data)
    print("30")
    build_tree(state.result(30).result(0), initial_depth, my_data)
    build_tree(state.result(30).result(3), initial_depth, my_data)

    final_book = {k: max(v, key=v.get) for k, v in my_data.items()}
    #print(final_book[state])

    with open("data.pickle", 'wb') as f:
        pickle.dump(my_data, f)