import time
from agent import Agent


def unscramble_cube():
    # The game should be played for 10 times.
    wins = 0
    game_summary = []

    agent = Agent()
    start = time.time()
    print("[INFO] REGISTERING PATTERN DATABASE")
    agent.register_patterns()
    # qValues = agent.qValues
    print(f"[INFO] GENERATED PATTERN DATABASE IN {time.time() - start} seconds")

    print("=" * 50)
    start = time.time()
    print("[INFO] STARTING LEARNING PHASE")
    Epsilons = [i / 50 for i in range(50)]
    Epsilons.reverse()
    max_states = -1
    for _ in range(2):
        for j, e in enumerate(Epsilons):
            # print("======= ROUND " + str(j) + "=========")
            states = agent.do_q_learning(epsilon=e)
            max_states = max(max_states, states)
    qValues = agent.qValues
    print(f"[INFO] COMPLETED LEARNING PHASE IN {time.time() - start} seconds")
    print(f"[INFO] Number of states explored: {len(qValues)}")
    print("=" * 50)

    # print(len(qValues))
    for i in range(10):
        game = {}
        agent = Agent(q_values=qValues)
        start = time.time()
        # print("there are " + str(len(agent.QV)) + " keys in Q Table")
        cube_solved = agent.play()
        if cube_solved:
            wins += 1

        game['name'] = f"Game {i + 1}"
        game['result'] = "Won" if cube_solved else "Lost"
        game['elapsed_time'] = time.time() - start
        game['summary'] = agent.print_()
        game_summary.append(game)
        print("=" * 75)
    for game in game_summary:
        print(f"[INFO] {game['name']} completed in {game['elapsed_time']}, Result: {game['result']}")

    print(f"Win Percentage: {(wins / len(game_summary)) * 100}")
    print("=" * 75)


if __name__ == "__main__":
    unscramble_cube()
