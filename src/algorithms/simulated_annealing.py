import math
import random

# Pseaudo code for SA
# function SIMULATED-ANNEALING(problem, schedule) returns a state
#   current = problem.INITIAL_STATE
#   for t = 1 to infinity do
#     T = schedule(t)
#     if T = 0 then return current
#     next = RANDOM_SUCCESSOR(current)       # Diff 1: Random pick (not best)
#     delta_E = next.VALUE - current.VALUE
#     if delta_E > 0 then
#       current = next
#     else
#       current = next with probability e^(delta_E / T) # Diff 2: Accept bad moves

def simulated_annealing(current, value, successor, schedule):
    t = 1
    while True:
        T = schedule(t)
        if T == 0:
            return current
        nxt = successor(current)                      # Diff 1: random pick, not best
        delta_E = value(nxt) - value(current)
        if delta_E > 0 or random.random() < math.exp(delta_E / T):
            current = nxt                             # Diff 2: accept bad moves too
        t += 1

def exponential_schedule(T0=100.0, alpha=0.995, t_min=1e-3):
    def schedule(t):
        T = T0 * alpha ** t
        return T if T >= t_min else 0.0
    return schedule

def linear_schedule(T0=100.0, t_max=20_000):
    def schedule(t):
        return max(T0 * (1 - t / t_max), 0.0)
    return schedule

def tour_length(points, tour):
    return sum(math.dist(points[tour[i]], points[tour[(i + 1) % len(tour)]])
               for i in range(len(tour)))

def random_tour(n):
    tour = list(range(n))
    random.shuffle(tour)
    return tour

def two_opt_successor(tour):
    i, k = sorted(random.sample(range(len(tour)), 2))
    return tour[:i] + tour[i:k + 1][::-1] + tour[k + 1:]

if __name__ == "__main__":
    random.seed(7)
    points = [(random.uniform(0, 10), random.uniform(0, 10)) for _ in range(9)]
    value = lambda tour: -tour_length(points, tour)    # SA maximizes: value = -cost
    initial = random_tour(len(points))

    for name, schedule in {"exponential": exponential_schedule(),
                           "linear": linear_schedule()}.items():
        best = simulated_annealing(initial, value, two_opt_successor, schedule)
        print(f"{name:12s} cost = {tour_length(points, initial):.2f} -> "
              f"{tour_length(points, best):.2f}")
