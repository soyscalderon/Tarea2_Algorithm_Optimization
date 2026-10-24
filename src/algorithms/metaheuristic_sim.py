import random

# Each operator improves the solution with an unknown probability.
success_rate = {"swap": 0.10, "insert": 0.20, "2-opt": 0.35}
reward_sum = {op: 0.0 for op in success_rate}
uses = {op: 0 for op in success_rate}
epsilon = 0.1  # 10% exploration, 90% exploitation

for step in range(2_000):
    if random.random() < epsilon or step < len(success_rate):
        op = random.choice(list(success_rate))                               # explore
    else:
        op = max(success_rate, key=lambda o: reward_sum[o] / max(uses[o], 1))  # exploit
    improved = random.random() < success_rate[op]  # apply operator to the solution
    uses[op] += 1
    reward_sum[op] += improved

for op in success_rate:
    print(f"{op:7s} used {uses[op]:5d} times, learned success = {reward_sum[op] / max(uses[op], 1):.2f}")