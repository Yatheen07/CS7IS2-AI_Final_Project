# 3x3 TIME
import matplotlib.pyplot as plt

bfs = [None, 0.001,
       0.01,
       0.266,
       1,
       7,
       75,
       1937, None]

astar = [None, 0.008,
         0.01,
         0.0204,
         0.0197,
         0.023,
         0.03,
         1937, None]

qlearning = [None, 5.45,
             5.62,
             5.65,
             5.6,
             5.62,
             5.64,
             5.7, 5.83]

manual_baseline = [None, 1, 2, 10, 30, 180, 192, 210, 211]
scrabmle_length = [None, 1, 2, 3, 4, 5, 6, 7, 15]

plt.plot(scrabmle_length, bfs, label="BFS")
plt.plot(scrabmle_length, astar, label="A*")
plt.plot(scrabmle_length, qlearning, label="qLearning")
plt.plot(scrabmle_length, manual_baseline, label="Baseline")
plt.xlabel("Scramble Length")
plt.ylabel("Time (s) - logarithmic scale")
plt.yscale("log")
plt.title("Time Comparison for 3x3x3 Cube")
plt.legend()
plt.show()
