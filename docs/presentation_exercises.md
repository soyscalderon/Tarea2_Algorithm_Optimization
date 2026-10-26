# Presentation Exercises

## Exercise 1: Parallel Speedup

- Run `estimate_pi` with **1, 2, 4, and 8 processes**.
- Plot the speedup for each process count.
- Explain why the speedup is not linear.

## Exercise 2: Algorithmic Analysis

- Modify the greedy knapsack algorithm to prioritize items with the **lowest weight first**.
- Provide a small example where this approach performs worse than the method based on the **value-to-weight ratio**.

## Exercise 3: Local Search

- Implement **2-opt** for the Traveling Salesperson Problem (TSP).
- Count the number of improvements made before reaching a local optimum.
- Compare starting from a **Nearest Neighbour** tour with starting from a **random tour**.
- Does the Nearest Neighbour starting tour require fewer improvements? Explain your findings.

## Exercise 4: Parameter Tuning

- Implement **Simulated Annealing** based on the provided pseudocode.
- Experiment with different cooling schedules.
- Explain how the cooling schedule affects final solution quality and execution time.

## Exercise 5: Approximation Ratio

- Run the MST-based approximation algorithm on **100 random instances of 9 cities**.
- Calculate and plot the approximation ratio by comparing the obtained tour cost with the optimal tour cost.
- How close does the observed ratio get to **2**?
- What happens when you apply **2-opt** to the MST-based result?

## Exercise 6: Las Vegas vs. Monte Carlo

- Solve the **8-Queens problem** by placing queens randomly and restarting whenever a conflict occurs.
- Measure and plot the distribution of the number of restarts.
- Convert the algorithm into a **Monte Carlo algorithm** by imposing a restart limit.
- Explain the effect of the restart limit on the algorithm's behavior and probability of success.

## Exercise 7: Space vs. Time

- Rewrite the knapsack dynamic programming algorithm to use a **single row**, achieving **O(W) space complexity**.
- Solve the problem using a top-down approach with `@functools.cache`.
- Count how many subproblems are actually computed.
- Compare the memory usage and computation performed by the approaches.
