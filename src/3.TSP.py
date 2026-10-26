import argparse
import math
import random

def tour_length(city_coordinates, tour):
    return sum(math.dist(city_coordinates[tour[i]], city_coordinates[tour[(i + 1) % len(tour)]])
               for i in range(len(tour)))

def reverse_segment(tour, first, second):
    """2-opt move: swap the order of the cities between first and second."""
    return tour[:first] + tour[first:second + 1][::-1] + tour[second + 1:]

def two_opt_local_search(initial_tour, city_coordinates):
    """Apply 2-opt moves until no improvement is left; returns the tour and the move count."""
    tour = initial_tour[:]
    improvement_count = 0
    improved = True
    while improved:
        improved = False
        for first in range(len(tour) - 1):
            for second in range(first + 1, len(tour)):
                candidate_tour = reverse_segment(tour, first, second)
                if tour_length(city_coordinates, candidate_tour) < tour_length(city_coordinates, tour):
                    tour = candidate_tour
                    improvement_count += 1
                    improved = True
    return tour, improvement_count

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TSP with 2-opt local search.")
    parser.add_argument("--graph", action="store_true",
                        help="Also generate the matplotlib figures.")
    args = parser.parse_args()

    random.seed(7)
    city_count = 10

    # Random coordinates in a 10x10 grid (same generation as 5.MST.py)
    city_coordinates = [(random.uniform(0, 10), random.uniform(0, 10))
                        for _ in range(city_count)]
    initial_tour = list(range(city_count))
    random.shuffle(initial_tour)                        # random initial solution

    final_tour, improvement_count = two_opt_local_search(initial_tour, city_coordinates)
    initial_cost = tour_length(city_coordinates, initial_tour)
    final_cost = tour_length(city_coordinates, final_tour)

    print("Travelling Salesman Problem with 2-opt (10 random cities in a 10x10 grid)\n")
    for index, (x, y) in enumerate(city_coordinates):
        print(f"City{index:2d}: (x={x:4.2f}, y={y:4.2f})")
    print(f"\nInitial tour (random):    {initial_tour}  cost = {initial_cost:.2f}")
    print(f"Final tour (using 2-opt): {final_tour}  cost = {final_cost:.2f}")
    print(f"Improvements to reach the local optimum: {improvement_count}")

# Graficas
if __name__ == "__main__" and args.graph:
    import matplotlib.pyplot as plt
    from pathlib import Path

    def nearest_neighbour_tour(city_coordinates, start_city):
        """Build a tour greedily by always jumping to the closest unvisited city."""
        unvisited = set(range(len(city_coordinates))) - {start_city}
        tour = [start_city]
        while unvisited:
            last_city = tour[-1]
            closest_city = min(unvisited,
                               key=lambda city: math.dist(city_coordinates[last_city],
                                                          city_coordinates[city]))
            tour.append(closest_city)
            unvisited.remove(closest_city)
        return tour

    trial_count = 50
    trial_city_count = 10
    random.seed(11)

    improvements_from_random, improvements_from_nn = [], []
    costs_from_random, costs_from_nn = [], []
    for _ in range(trial_count):
        trial_coordinates = [(random.uniform(0, 10), random.uniform(0, 10))
                             for _ in range(trial_city_count)]
        shuffled_tour = list(range(trial_city_count))
        random.shuffle(shuffled_tour)                       # scenario 1: random tour
        nn_tour = nearest_neighbour_tour(trial_coordinates,
                                         random.randrange(trial_city_count))  # scenario 2: NN tour

        random_final_tour, random_moves = two_opt_local_search(shuffled_tour, trial_coordinates)
        nn_final_tour, nn_moves = two_opt_local_search(nn_tour, trial_coordinates)

        improvements_from_random.append(random_moves)
        improvements_from_nn.append(nn_moves)
        costs_from_random.append(tour_length(trial_coordinates, random_final_tour))
        costs_from_nn.append(tour_length(trial_coordinates, nn_final_tour))

    print(f"\nMean improvements: random start = "
          f"{sum(improvements_from_random) / trial_count:.1f}, "
          f"nearest neighbour start = {sum(improvements_from_nn) / trial_count:.1f}")
    print(f"Mean local optimum cost: random start = {sum(costs_from_random) / trial_count:.2f}, "
          f"nearest neighbour start = {sum(costs_from_nn) / trial_count:.2f}")

    figure_directory = Path(__file__).resolve().parents[1] / "graphs"
    figure_directory.mkdir(parents=True, exist_ok=True)

    start_labels = ["Random tour", "Nearest Neighbour"]
    comparison_figure, (improvements_axis, costs_axis) = plt.subplots(1, 2, figsize=(12, 5))

    improvements_axis.boxplot([improvements_from_random, improvements_from_nn],
                              tick_labels=start_labels)
    improvements_axis.set_ylabel("Improvements to reach the local optimum")
    improvements_axis.set_title(f"Number of 2-opt improvements ({trial_count} trials)")
    improvements_axis.grid(alpha=0.3, axis="y")

    costs_axis.boxplot([costs_from_random, costs_from_nn], tick_labels=start_labels)
    costs_axis.set_ylabel("Local optimum tour cost")
    costs_axis.set_title("Quality of the local optimum reached")
    costs_axis.grid(alpha=0.3, axis="y")

    comparison_figure.suptitle("2-opt local search: random vs nearest-neighbour initial tour"
                               f" ({trial_city_count} cities)")
    comparison_figure.tight_layout()

    comparison_path = figure_directory / "3.tsp_2opt_initialization.png"
    comparison_figure.savefig(comparison_path, dpi=150)
    print(f"\nFigure saved to {comparison_path}")
    
