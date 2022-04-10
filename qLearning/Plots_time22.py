# 2x2 TIME
import matplotlib.pyplot as plt

bfs = [None, 0.001,
       0.008,
       0.177,
       0.705,
       4.37,
       39.4,
       327]
astar = [None, 0.008,
         0.01,
         0.0204,
         0.0197,
         0.023,
         0.03,
         327]
qlearning = [None, 1.14,
             1.33,
             1.42,
             1.99,
             1.78,
             1.88,
             1.93]

manual_baseline = [None, 1, 2, 10, 30, 180, 192, 210]
# scrabmle_length = [1, 2, 3, 4, 5, 6, 7]

plt.plot(bfs, label="BFS")
plt.plot(astar, label="A*")
plt.plot(qlearning, label="qLearning")
plt.plot(manual_baseline, label="Baseline")
plt.xlabel("Scramble Length")
plt.ylabel("Time (s) - logarithmic scale")
plt.yscale("log")
plt.title("Time Comparison")
plt.legend()
plt.show()
