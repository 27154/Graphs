
import matplotlib.pyplot as plt
import numpy as np

iterations = 100
max_64bit = 0xFFFFFFFFFFFFFFFF  # Maximum value for 64-bit unsigned integer

# Track both the unlimited precision value and the overflowing value
dollars_unlimited = []
dollars_overflow = []

current_unlimited = 1
current_overflow = 1

for i in range(iterations):
    dollars_unlimited.append(current_unlimited)
    dollars_overflow.append(current_overflow)

    current_unlimited *= 2
    current_overflow = (current_overflow * 2) & max_64bit

# Find the iteration where overflow first occurs
overflow_point = None
for i in range(1, len(dollars_unlimited)):
    if dollars_unlimited[i] != dollars_overflow[i]:
        overflow_point = i
        break

# Create a plot
plt.figure(figsize=(12, 8))

# Plot the values on a logarithmic scale to handle the exponential growth
plt.subplot(2, 1, 1)
plt.plot(range(iterations), dollars_unlimited, label="Unlimited Precision", marker='o', markersize=3)
plt.plot(range(iterations), dollars_overflow, label="64-bit Overflow", marker='x', markersize=3)
plt.axvline(x=overflow_point, color='r', linestyle='--', label=f"Overflow at iteration {overflow_point}")
plt.yscale('log')
plt.xlabel('Iteration')
plt.ylabel('Value (log scale)')
plt.legend()
plt.title('Detecting Long Long Overflow Point (Log Scale)')
plt.grid(True)

# Plot the values after overflow on a linear scale to see the pattern
plt.subplot(2, 1, 2)
start_idx = max(0, overflow_point - 5)
end_idx = min(iterations, overflow_point + 15)
plt.plot(range(start_idx, end_idx), dollars_unlimited[start_idx:end_idx], label="Unlimited Precision", marker='o')
plt.plot(range(start_idx, end_idx), dollars_overflow[start_idx:end_idx], label="64-bit Overflow", marker='x')
plt.axvline(x=overflow_point, color='r', linestyle='--', label=f"Overflow at iteration {overflow_point}")
plt.xlabel('Iteration')
plt.ylabel('Value')
plt.legend()
plt.title('Overflow Behavior Close-up')
plt.grid(True)

plt.tight_layout()

# Print information about the overflow point
if overflow_point is not None:
    print(f"Overflow first detected at iteration {overflow_point}")
    print(f"Value before overflow: {dollars_unlimited[overflow_point - 1]}")
    print(
        f"Value at overflow: Unlimited={dollars_unlimited[overflow_point]}, 64-bit={dollars_overflow[overflow_point]}")
    print(f"Binary representation before overflow: {bin(dollars_unlimited[overflow_point - 1])}")
    print(f"Binary representation at overflow point (64-bit): {bin(dollars_overflow[overflow_point])}")
else:
    print("No overflow detected in the given range of iterations")

plt.show()