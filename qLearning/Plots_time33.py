# 3x3 TIME
import matplotlib.pyplot as plt

bfs = [None, 0.001,
       0.008,
       0.177,
       0.705,
       4.37,
       39.4,
       327, None]
astar = [None, 0.008,
         0.01,
         0.0204,
         0.0197,
         0.023,
         0.03,
         327, None]
qlearning = [None, 1.14,
             1.33,
             1.42,
             1.99,
             1.78,
             1.88,
             1.93, 2.04]

manual_baseline = [None, 1, 2, 10, 30, 180, 192, 210, 211]
scrabmle_length = [None, 1, 2, 3, 4, 5, 6, 7, 15]

plt.plot(scrabmle_length, bfs, label="BFS")
plt.plot(scrabmle_length, astar, label="A*")
plt.plot(scrabmle_length, qlearning, label="qLearning")
plt.plot(scrabmle_length, manual_baseline, label="Baseline")
plt.xlabel("Scramble Length")
plt.ylabel("Time (s) - logarithmic scale")
plt.yscale("log")
plt.title("Time Comparison")
plt.legend()
plt.show()
