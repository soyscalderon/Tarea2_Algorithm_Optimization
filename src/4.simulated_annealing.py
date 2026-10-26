import argparse
import math
import random
import time

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

def tour_length(city_coordinates, tour):
    return sum(math.dist(city_coordinates[tour[i]], city_coordinates[tour[(i + 1) % len(tour)]])
               for i in range(len(tour)))

def two_opt_neighbor(tour):
    """2-opt move: reverse the segment between two random positions."""
    first, second = sorted(random.sample(range(len(tour)), 2))
    return tour[:first] + tour[first:second + 1][::-1] + tour[second + 1:]

def exponential_cooling_schedule(initial_temperature=100.0, cooling_rate=0.995,
                                 minimum_temperature=1e-3):
    def temperature_at(step):
        temperature = initial_temperature * cooling_rate ** step
        return temperature if temperature >= minimum_temperature else 0.0
    return temperature_at

def linear_cooling_schedule(initial_temperature=100.0, total_steps=20_000):
    def temperature_at(step):
        return max(initial_temperature * (1 - step / total_steps), 0.0)
    return temperature_at

def simulated_annealing(initial_tour, city_coordinates, cooling_schedule):
    current_tour = initial_tour[:]
    current_cost = tour_length(city_coordinates, current_tour)
    step = 1
    while True:
        temperature = cooling_schedule(step)
        if temperature == 0:
            return current_tour
        candidate_tour = two_opt_neighbor(current_tour)      # Diff 1: random pick (not best)
        candidate_cost = tour_length(city_coordinates, candidate_tour)
        cost_change = candidate_cost - current_cost          # -delta_E of the pseudocode
        if cost_change < 0 or random.random() < math.exp(-cost_change / temperature):
            current_tour, current_cost = candidate_tour, candidate_cost  # Diff 2: accept bad moves
        step += 1

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simulated annealing for the TSP.")
    parser.add_argument("--graph", action="store_true",
                        help="Also generate the matplotlib figures.")
    args = parser.parse_args()

    random.seed(7)
    city_coordinates = [(random.uniform(0, 10), random.uniform(0, 10)) for _ in range(9)]
    initial_tour = list(range(len(city_coordinates)))
    random.shuffle(initial_tour)                            # random initial solution
    initial_cost = tour_length(city_coordinates, initial_tour)

    print("Simulated Annealing Algorithm for the TSP (Travelling Salesman Problem) in 10 cities in a 10x10 grid.\n")
    run_count = 10
    for schedule_name, cooling_schedule in {"exponential": exponential_cooling_schedule(),
                                            "linear": linear_cooling_schedule()}.items():
        total_time, final_costs = 0.0, []
        for _ in range(run_count):
            start_time = time.perf_counter()
            final_tour = simulated_annealing(initial_tour, city_coordinates, cooling_schedule)
            total_time += time.perf_counter() - start_time
            final_costs.append(tour_length(city_coordinates, final_tour))
        print(f"{schedule_name:12s} cost = {initial_cost:.2f} -> "
              f"{sum(final_costs) / run_count:.2f}  mean time = {total_time / run_count:.4f} s")

# Graficas
if __name__ == "__main__" and args.graph:
    import time
    import matplotlib.pyplot as plt
    from pathlib import Path

    def simulated_annealing_with_history(initial_tour, city_coordinates, cooling_schedule):
        """Same algorithm as simulated_annealing, but records the cost after every step."""
        current_tour = initial_tour[:]
        current_cost = tour_length(city_coordinates, current_tour)
        cost_history = [current_cost]
        step = 1
        while True:
            temperature = cooling_schedule(step)
            if temperature == 0:
                return current_tour, cost_history
            candidate_tour = two_opt_neighbor(current_tour)
            candidate_cost = tour_length(city_coordinates, candidate_tour)
            cost_change = candidate_cost - current_cost
            if cost_change < 0 or random.random() < math.exp(-cost_change / temperature):
                current_tour, current_cost = candidate_tour, candidate_cost
            cost_history.append(current_cost)
            step += 1

    figure_directory = Path(__file__).resolve().parents[1] / "graphs"
    figure_directory.mkdir(parents=True, exist_ok=True)

    cooling_schedules = {"exponential": exponential_cooling_schedule(),
                         "linear": linear_cooling_schedule()}

    # 1) Convergence curves: cost vs iteration, same instance and same initial tour
    random.seed(7)
    convergence_coordinates = [(random.uniform(0, 10), random.uniform(0, 10)) for _ in range(9)]
    convergence_initial_tour = list(range(len(convergence_coordinates)))
    random.shuffle(convergence_initial_tour)

    convergence_figure, convergence_axis = plt.subplots(figsize=(8, 5))
    for schedule_name, cooling_schedule in cooling_schedules.items():
        _, cost_history = simulated_annealing_with_history(convergence_initial_tour,
                                                           convergence_coordinates,
                                                           cooling_schedule)
        convergence_axis.plot(range(len(cost_history)), cost_history, linewidth=2,
                              label=f"{schedule_name} ({len(cost_history)} steps)")
        print(f"{schedule_name:12s} convergence: {len(cost_history)} steps")
    convergence_axis.set_xlabel("Iteration (step)")
    convergence_axis.set_ylabel("Tour cost")
    convergence_axis.set_title("Simulated Annealing convergence by cooling schedule")
    convergence_axis.grid(alpha=0.3)
    convergence_axis.legend()
    convergence_figure.tight_layout()

    convergence_path = figure_directory / "4.sa_convergence.png"
    convergence_figure.savefig(convergence_path, dpi=150)
    print(f"Figure saved to {convergence_path}")

    # 2) Execution time vs quality of the final solution (several runs per schedule)
    run_count = 10
    time_samples = {schedule_name: [] for schedule_name in cooling_schedules}
    cost_samples = {schedule_name: [] for schedule_name in cooling_schedules}
    for run in range(run_count):
        random.seed(1000 + run)
        run_initial_tour = list(range(len(convergence_coordinates)))
        random.shuffle(run_initial_tour)
        for schedule_name, cooling_schedule in cooling_schedules.items():
            start_time = time.perf_counter()
            final_tour = simulated_annealing(run_initial_tour, convergence_coordinates,
                                             cooling_schedule)
            time_samples[schedule_name].append(time.perf_counter() - start_time)
            cost_samples[schedule_name].append(tour_length(convergence_coordinates, final_tour))

    quality_figure, quality_axis = plt.subplots(figsize=(8, 5))
    for schedule_name in cooling_schedules:
        quality_axis.scatter(time_samples[schedule_name], cost_samples[schedule_name],
                             s=70, label=schedule_name)
        print(f"{schedule_name:12s}: mean time = "
              f"{sum(time_samples[schedule_name]) / run_count:.4f} s, "
              f"mean final cost = "
              f"{sum(cost_samples[schedule_name]) / run_count:.2f}")
    quality_axis.set_xlabel("Execution time (s)")
    quality_axis.set_ylabel("Final tour cost")
    quality_axis.set_title(f"Execution time vs solution quality ({run_count} runs per schedule)")
    quality_axis.grid(alpha=0.3)
    quality_axis.legend()
    quality_figure.tight_layout()

    quality_path = figure_directory / "4.sa_time_vs_quality.png"
    quality_figure.savefig(quality_path, dpi=150)
    print(f"Figure saved to {quality_path}")
    
