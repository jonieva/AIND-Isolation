"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
INF = float("inf")

class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Similar to custom_score_2, but the weights for the parameters have been
    estimated empirically using a bayesian method for parameters optimization called Spearmint.

    Note that some weights have a negative value. These values kind of contradict their
    original thought, but they have been kept to respect the Spearmint output.

    See https://github.com/HIPS/Spearmint and the heurisic analysis document for additional info.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    own_moves = game.get_legal_moves()
    if len(own_moves) == 0:
        # terminal state. We don't use the Isolation.Board builtin functions for the sake of
        # efficiency (no need to recalculate the list of legal moves)
        if player == game.active_player:
            # player looses
            return -INF
        else:
            # player wins
            return INF
    else:
        opponent = game.get_opponent(player)
        opp_moves = game.get_legal_moves(opponent)
        # Distance to the center of the board
        w, h = game.width / 2., game.height / 2.
        my_y, my_x = game.get_player_location(player)
        center_distance = abs(h - my_y) + abs(w - my_x)
        # Opponent distance to the center
        opp_y, opp_x = game.get_player_location(opponent)
        opp_center_distance = abs(h - opp_y) + abs(w - opp_x)

        # Distance to the opponent (from a purely geometric point of view, other types of distances could be tested)
        my_pos = game.get_player_location(player)
        opp_pos = game.get_player_location(opponent)
        opp_distance = abs(my_pos[0] - opp_pos[0]) + abs(my_pos[1] - opp_pos[1])

        # Weights for the different parameters of the heuristic.
        # They have been calculated using Spearmint (see function help for more info)
        w_my_moves = -8.82446  # Weight for my moves
        w_opponent_moves = 1.6687 # Weight for opponent moves
        w_center_distance = 7.99194  # Weight for distance to the center of the board
        w_opponent_center_distance = 8.82935  # Weight for opponent's distance to the center of the board
        w_opponent_distance = -9.96948     # Weight for the distance to the opponent
        w_chase_opponent_factor = -3.33862 # Extra boost used when the distance to the opponent is 3

        d = len(own_moves) * w_my_moves \
            - len(opp_moves) * w_opponent_moves \
            - center_distance * w_center_distance \
            + opp_center_distance * w_opponent_center_distance \
            - opp_distance * w_opponent_distance

        opp_distance = abs(my_y - opp_y) + abs(my_x - opp_x)
        if opp_distance == 3:
            # This would have been one of the legal options of the opponent. Extra boost
            d += w_chase_opponent_factor

        return d

def custom_score_2(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This heuristic is based on a weighted sum of several components.
    Positive components:
        - Number of legal movements available for the given player
        - Distance to the center of the board for the given player
        - Extra boost when the distance of the given player to its opponent is exactly 3.
          In this condition is matched, the opponent legal movements are reduced by one, and
          the given player is in a good place to "harass" the opponent.
    Negative components:
        - Number of legal movements available for the opponent player
        - Distance to the center of the board for the opponent player

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    own_moves = game.get_legal_moves()
    if len(own_moves) == 0:
        # terminal state. We don't use the Isolation.Board builtin functions for the sake of
        # efficiency (no need to recalculate the list of legal moves)
        if player == game.active_player:
            # player looses
            return -INF
        else:
            # player wins
            return INF
    else:
        opponent = game.get_opponent(player)
        opp_moves = game.get_legal_moves(opponent)
        w, h = game.width / 2., game.height / 2.
        my_y, my_x = game.get_player_location(player)
        my_center_distance = abs(h - my_y) + abs(w - my_x)
        opp_y, opp_x = game.get_player_location(opponent)
        opp_center_distance = abs(h - opp_y) + abs(w - opp_x)

        # Weight for the different parameters (see function help for a full explanation)
        w_my_moves = 1.5             # Weight for my moves
        w_opponent_moves = 1.0       # Weight for opponent moves
        w_center = 0.2               # Weight for distance to the center
        w_chase_opponent_factor = 1.5   # Extra boost.

        # Metric value
        d = len(own_moves) * w_my_moves \
            - len(opp_moves) * w_opponent_moves \
            - my_center_distance * w_center \
            + opp_center_distance * w_center

        # Calculate the distance of the player to the opponent.
        opp_distance = abs(my_y - opp_y) + abs(my_x - opp_x)
        if opp_distance == 3:
            # Extra boost (see function help for a full explanation)
            d += w_chase_opponent_factor
        return d

def custom_score_3(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This heuristic is only based only in the number of moves remaining for the active player
    and its opponent, and it's the simplest one of the three proposed.
    Both numbers are weighted differently

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    own_moves = game.get_legal_moves()
    if len(own_moves) == 0:
        # terminal state. We don't use the Isolation.Board builtin functions for the sake of
        # efficiency (no need to recalculate the list of legal moves)
        if player == game.active_player:
            # player looses
            return -INF
        else:
            # player wins
            return INF
    else:
        opp_moves = game.get_legal_moves(game.get_opponent(player))
        w_my_moves = 1.5
        w_opponent_moves = 1.0

        return len(own_moves) * w_my_moves - len(opp_moves) * w_opponent_moves

class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=25.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            return self.minimax(game, self.search_depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def minimax(self, game, depth):
        """Implement depth-limited minimax search algorithm as described in
        the lectures.

        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        legal_moves = game.get_legal_moves()

        best_score = -INF
        best_move = (-1, -1) if len(legal_moves) == 0 else legal_moves[0]
        for move in legal_moves:
            score = self.min_value(game.forecast_move(move), depth-1)
            if score > best_score:
                best_move = move
                best_score = score
        return best_move


    def min_value(self, game, depth):
        """
        Return the minimum value that we can calculate in this node.
        If the node is terminal, return -INF
        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        float
            Minimum value obtained
        """

        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        if depth == 0:
            # Stop here. Evaluate the state of the board
            return self.score(game, self)

        legal_moves = game.get_legal_moves()
        num_moves = len(legal_moves)
        if num_moves == 0:
            # Terminal state. Should evaluate to -INF
            return game.utility(self)

        v = INF
        for move in legal_moves:
            new_game = game.forecast_move(move)
            v = min(v, self.max_value(new_game, depth-1))
        return v


    def max_value(self, game, depth):
        """
        Return the maximum value that we can calculate in this node.
        If the node is terminal, return -INF
        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        float
            Maximum value obtained
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        if depth == 0:
            # Stop here. Evaluate the state of the board
            return self.score(game, self)

        legal_moves = game.get_legal_moves()
        if len(legal_moves) == 0:
            #  Terminal state
            return game.utility(self)

        v = -INF
        for move in legal_moves:
            new_game = game.forecast_move(move)
            v = max(v, self.min_value(new_game, depth-1))
        return v

class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)
        legal_moves = game.get_legal_moves(self)
        if len(legal_moves) > 0:
            best_move = legal_moves[0]
        try:
            depth = 1
            while True:
                best_move = self.alphabeta(game, depth)
                depth += 1
        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move


    def alphabeta(self, game, depth, alpha=-INF, beta=INF):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # We assume that there is not going to be timeout while obtaining the legal moves (there will be a maximum
        # of four moves anytime)
        legal_moves = game.get_legal_moves()
        best_score = -INF
        # Pick a best move != (-1, -1) to avoid forfeit
        best_move = (-1, -1) if len(legal_moves) == 0 else legal_moves[0]
        for move in legal_moves:
            score = self.min_value(game.forecast_move(move), depth-1, alpha, beta)
            if score > best_score:
                best_move = move
                best_score = score
            alpha = max(alpha, best_score)
        return best_move


    def min_value(self, game, depth, alpha, beta):
        """
        Return the minimum value that we can calculate in this node.
        If the node is terminal, return -INF
        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        float
            Minimum value obtained
        """

        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        if depth == 0:
            # Stop here
            return self.score(game, self)

        legal_moves = game.get_legal_moves()
        if len(legal_moves) == 0:
            # Terminal state. Should evaluate to -INF
            return game.utility(self)

        v = INF
        # try:
        for move in legal_moves:
            v = min(v, self.max_value(game.forecast_move(move), depth - 1, alpha, beta))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    def max_value(self, game, depth, alpha, beta):
        """
        Return the maximum value that we can calculate in this node.
        If the node is terminal, return -INF
        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        float
            Maximum value obtained
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        if depth == 0:
            # Stop here
            return self.score(game, self)

        legal_moves = game.get_legal_moves()
        # legal_moves = [(3,5), (4,4)]
        if len(legal_moves) == 0:
            # Terminal state. Should evaluate to INF
            return game.utility(self)

        v = -INF
        # try:
        for move in legal_moves:
            v = max(v, self.min_value(game.forecast_move(move), depth - 1, alpha, beta))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v
