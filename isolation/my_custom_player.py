from collections import Counter

from sample_players import DataPlayer
from isolation import DebugState
import time
import random
import math


class CustomPlayer(DataPlayer):
    """ Implement your own agent to play knight's Isolation

    The get_action() method is the only required method for this project.
    You can modify the interface for get_action by adding named parameters
    with default values, but the function MUST remain compatible with the
    default interface.

    **********************************************************************
    NOTES:
    - The test cases will NOT be run on a machine with GPU access, nor be
      suitable for using any other machine learning techniques.

    - You can pass state forward to your agent on the next turn by assigning
      any pickleable object to the self.context attribute.
    **********************************************************************
    """
    def get_action(self, state):
        """ Employ an adversarial search technique to choose an action
        available in the current state calls self.queue.put(ACTION) at least

        This method must call self.queue.put(ACTION) at least once, and may
        call it as many times as you want; the caller will be responsible
        for cutting off the function after the search time limit has expired.

        See RandomPlayer and GreedyPlayer in sample_players for more examples.

        **********************************************************************
        NOTE: 
        - The caller is responsible for cutting off search, so calling
          get_action() from your own code will create an infinite loop!
          Refer to (and use!) the Isolation.play() function to run games.
        **********************************************************************
        """

        if state.ply_count == 0:
            minimax = 57
        else:
            if state.ply_count == 1:
                minimax = random.choice(state.actions())
            else:
                minimax = self.minimax(state, depth=3)
        self.queue.put(minimax)


    def minimax(self, state, depth):

        def min_value(state, depth):
            if state.terminal_test(): return state.utility(self.player_id)
            if depth <= 0:
                return self.score_old(state)
            value = float("inf")
            for action in state.actions():
                value = min(value, max_value(state.result(action), depth - 1))
            return value

        def max_value(state, depth):
            if state.terminal_test(): return state.utility(self.player_id)
            if depth <= 0:
                return self.score(state)
            value = float("-inf")
            for action in state.actions():
                value = max(value, min_value(state.result(action), depth - 1))
            return value

        return max(state.actions(), key=lambda x: min_value(state.result(x), depth - 1))

    def score(self, state):
        progress = state.ply_count / 80
        remainder = 1 - progress
        a = -5
        b = 1.5

        dist = self.distance(state)
        own_liberties = state.liberties(self.own_location(state))
        opp_liberties = state.liberties(self.opp_location(state))


    def opp_location(self, state):
        return state.locs[1 - self.player_id]

    def own_location(self, state):
        return state.locs[self.player_id]

    def distance(self, state):
        x1, y1 = DebugState.ind2xy(self.own_location(state))
        #xc, yc = DebugState.ind2xy(57)
        xc, yc = (5, 4)
        dx = x1 - xc
        dy = y1 - yc
        c = Counter()

        return math.sqrt(dx*dx + dy*dy)

    def score_old(self, state):
        own_liberties = state.liberties(self.own_location(state))
        opp_liberties = state.liberties(self.opp_location(state))
        return len(own_liberties) - len(opp_liberties)