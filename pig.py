"""Play a game of Pig with two strategy functions."""

import random


def play_turn(banked_score, should_hold, verbose=True):
    """Play one turn and return the player's updated banked score.

    should_hold is a strategy function: it receives the current turn's points
    and returns True to hold or False to roll again.
    """
    turn_points = 0

    while True:
        roll = random.randint(1, 6)
        if verbose:
            print(f"Rolled a {roll}.")

        # A 1 loses only the points earned during this turn.
        if roll == 1:
            if verbose:
                print(f"Busted! Lost {turn_points} turn points.")
            return banked_score

        turn_points += roll
        if verbose:
            print(f"This turn: {turn_points} points.")

        # Bank a winning total immediately, regardless of the strategy.
        if banked_score + turn_points >= 100:
            if verbose:
                print("Reached 100! You win.")
            return banked_score + turn_points

        # The engine asks the strategy to decide; the rules stay the same.
        if should_hold(turn_points):
            if verbose:
                print(f"Holding: bank {turn_points} points.")
            return banked_score + turn_points


def hold_at_ten(turn_points):
    """Our baseline strategy: hold at 10 or more turn points."""
    return turn_points >= 10


def hold_at_twenty(turn_points):
    """Hold at 20 or more turn points."""
    return turn_points >= 20


def play_game(strategy_one, strategy_two, verbose=True):
    """Alternate turns until someone wins; return 1 or 2 for the winner."""
    scores = [0, 0]
    strategies = [strategy_one, strategy_two]
    current_player = 0  # List index 0 is Player 1; index 1 is Player 2.

    while True:
        if verbose:
            print(f"\nPlayer {current_player + 1}'s turn.")

        # Reuse the one-turn function, keeping each player's banked score.
        scores[current_player] = play_turn(
            scores[current_player], strategies[current_player], verbose=verbose
        )
        if verbose:
            print(f"Scores: Player 1 = {scores[0]}, Player 2 = {scores[1]}")

        if scores[current_player] >= 100:
            if verbose:
                print(f"\nPlayer {current_player + 1} wins!")
            return current_player + 1

        # Switch from 0 to 1, or from 1 back to 0.
        current_player = 1 - current_player


def run_tournament(strategy_one, strategy_two, games=100):
    """Count wins for each strategy, giving each an equal number of starts."""
    if games <= 0 or games % 2 != 0:
        raise ValueError("Use a positive, even number of games so starts are equal.")

    wins = [0, 0]  # These counts belong to strategies, not starting seats.

    for game_number in range(games):
        if game_number % 2 == 0:
            winner = play_game(strategy_one, strategy_two, verbose=False)
        else:
            winner = play_game(strategy_two, strategy_one, verbose=False)
            # Seats were swapped: translate the winner back to strategy 1 or 2.
            winner = 3 - winner

        wins[winner - 1] += 1

    print(f"Tournament: {games} games, each strategy starts {games // 2} times.")
    print(f"{strategy_one.__name__}: {wins[0]} wins ({wins[0] / games:.1%})")
    print(f"{strategy_two.__name__}: {wins[1]} wins ({wins[1] / games:.1%})")
    return wins


if __name__ == "__main__":
    run_tournament(hold_at_ten, hold_at_twenty, games=100)
