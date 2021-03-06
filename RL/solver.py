import time
from agent import Agent,Patterns
from model.cube import RubicsCube
from model.scrambler import Scrammbler
from model.scramble_configurations import scramble_configurations

def solveCube():

    #The game should be played for 10 times. 
    wins = 0
    game_summary = []
    
    start = time.time()
    print("[INFO] REGISTERING PATTERN DATABASE")
    qValues = Patterns().qValues
    print(f"[INFO] GENERATED PATTERN DATABASE IN {time.time() - start} seconds")

    cube = RubicsCube(size=3)
    #cubeSolver = CubeSolver()
    #print(cube)

    #Scramble the state based on the preset configurations
    scrammbler = Scrammbler()
    scramble_sequence,unscramble_sequence = scrammbler.scramble(scramble_configurations[5])

    #Scramble a fresh cube to get a initial state
    cube.scramble(action_sequence=scramble_sequence)
    #print(cube)

    agent = Agent(qValues=qValues,cube=cube)
    #print(f"[INFO] QValues: {agent.QV}")
    Epsilons = [i/ 50 for i in range(50)]
    Epsilons.reverse()
    for _ in range(2):
        for j, e in enumerate(Epsilons):
            #print("======= ROUND " + str(j) + "=========")
            agent.QLearn(epsilon=e)
    #print("there are " + str(len(agent.QV)) + " keys in Q Table")

    for i in range(7):
        game = {}
        start = time.time()
        cube = RubicsCube(size=3)
        #cubeSolver = CubeSolver()
        #print(cube)

        #Scramble the state based on the preset configurations
        scramble_sequence,unscramble_sequence = scrammbler.scramble(scramble_configurations[i])

        #Scramble a fresh cube to get a initial state
        cube.scramble(action_sequence=scramble_sequence)
        cube_solved = agent.Play(cube)
        if cube_solved:
            wins+=1
        
        game['name'] = f"Game {i+1}"
        game['result'] = "Won" if cube_solved else "Lost"
        game['elapsed_time'] = time.time() - start
        game['summary'] = agent.print_()
        game_summary.append(game)
        print("="*75)


    for game in game_summary:
        print(f"[INFO] {game['name']} completed in {game['elapsed_time']}, Result: {game['result']}")
    
    print(f"Win Percentage: {(wins/len(game_summary))*100}")
    print("="*75)

if __name__ == "__main__":
    solveCube()