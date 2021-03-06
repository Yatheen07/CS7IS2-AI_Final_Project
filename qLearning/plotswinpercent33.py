# 3x3 Win percentage
import matplotlib.pyplot as plt

bfs = [None, 100, 100, 100, 100, 100, 100, 100, None]
astar = [None, 100,
         100,
         100,
         100,
         100,
         90,
         90, None]
qlearning = [None, 100,
             100,
             100,
             90,
             80,
             70,
             50, 5.83]

manual_baseline = [None, 100, 100, 100, 100, 100, 100, 100, 100]
scrabmle_length = [None, 1, 2, 3, 4, 5, 6, 7, 15]

plt.plot(scrabmle_length, bfs, label="BFS", lw=3)
plt.plot(scrabmle_length, astar, label="A*", alpha=0.3, lw=7)
plt.plot(scrabmle_length, qlearning, label="qLearning", lw=0.8)
plt.plot(scrabmle_length, manual_baseline, label="Baseline", lw=0.4)
plt.xlabel("Scramble Length")
plt.ylabel("Win percentage")
# plt.yscale("log")
plt.title("Winning Percentages for 3x3x3 Cube")
plt.legend()
plt.show()
