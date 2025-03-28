import matplotlib.pyplot as plt
import numpy as np
from scipy import integrate

# Define parameters
iterations = 40
start_value = 1
bit_size = 32  # For a standard 32-bit integer

# Maximum positive value for a signed integer (2^(bit_size-1) - 1)
max_int = (1 << (bit_size - 1)) - 1

# Minimum value for a signed integer (-2^(bit_size-1))
min_int = -(1 << (bit_size - 1))


# Function that doubles the value, accounting for overflow
def double_with_overflow(x):
    doubled = (x * 2) & ((1 << bit_size) - 1)  # Apply bit mask for overflow
    # Convert to signed integer if needed
    if doubled > max_int:
        doubled = doubled - (1 << bit_size)
    return doubled


# Function for continuous exponential growth (before overflow)
def exponential_growth(x):
    return start_value * (2 ** x)


# Simulate the doubling process with overflow
dollars = [start_value]
for i in range(1, iterations):
    dollars.append(double_with_overflow(dollars[-1]))

# Create the plot
plt.figure(figsize=(14, 10))

# Plot 1: Actual Values with Overflow
plt.subplot(2, 1, 1)
x = list(range(iterations))
plt.plot(x, dollars, 'b-', marker='o', label='Actual values with overflow')

# Find where the overflow occurs
overflow_point = next((i for i, d in enumerate(dollars) if d < 0), None)

# Plot the theoretical exponential without overflow
x_continuous = np.linspace(0, overflow_point if overflow_point else iterations, 1000)
y_continuous = [exponential_growth(i) for i in x_continuous]
plt.plot(x_continuous, y_continuous, 'g--', label='Theoretical exponential growth (2ⁿ)')

# Mark overflow point if it exists
if overflow_point is not None:
    plt.axvline(x=overflow_point, color='r', linestyle='--',
                label=f'Overflow at iteration {overflow_point}')
    plt.text(overflow_point + 0.5, 0,
             f'Overflow occurs after {overflow_point} iterations\nValue becomes: {dollars[overflow_point]}',
             verticalalignment='bottom')

# Add horizontal lines at important boundaries
plt.axhline(y=0, color='k', linestyle='-', alpha=0.3)
plt.axhline(y=max_int, color='orange', linestyle='-.', alpha=0.7,
            label=f'Max int: {max_int} (2^{bit_size - 1}-1)')
plt.axhline(y=min_int, color='purple', linestyle='-.', alpha=0.7,
            label=f'Min int: {min_int} (-2^{bit_size - 1})')

plt.title('Integer Overflow in Doubling Process')
plt.xlabel('Iteration')
plt.ylabel('Value')
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()

# Plot 2: Mathematical Model - Periodic Function After Wrapping
plt.subplot(2, 1, 2)


# Create a continuous piecewise function that models the overflow behavior
def modular_exponential(x):
    # The raw exponential value
    raw_value = start_value * (2 ** x)
    # Model the overflow using modular arithmetic
    modulo_value = raw_value % (1 << bit_size)
    # Convert to signed representation
    if modulo_value > max_int:
        modulo_value -= (1 << bit_size)
    return modulo_value


# Plot the mathematical model
x_model = np.linspace(0, iterations - 1, 1000)
y_model = [modular_exponential(i) for i in x_model]
plt.plot(x_model, y_model, 'r-', label='Mathematical model of overflow')

# Plot the actual data points for comparison
plt.plot(x, dollars, 'bo', label='Actual values')

# Mark the period of the overflow cycle
if overflow_point is not None:
    # The period of the cycle after overflow is bit_size
    cycle_length = bit_size - overflow_point if overflow_point + bit_size < iterations else iterations - overflow_point
    if overflow_point + cycle_length <= iterations:
        plt.axvspan(overflow_point, overflow_point + cycle_length,
                    alpha=0.2, color='yellow', label=f'Overflow cycle (period={bit_size})')

plt.title('Mathematical Model of Integer Overflow')
plt.xlabel('Iteration')
plt.ylabel('Value')
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()

plt.tight_layout()

# Add text annotation for the formula beneath the plots
formula_text = (
    "General Formula:\n"
    "f(n) = 2^n                                  for n < 31\n"
    "f(n) = (2^n mod 2^32) - 2^32               for n ≥ 31 and (2^n mod 2^32) ≥ 2^31\n"
    "f(n) = 2^n mod 2^32                        for n ≥ 31 and (2^n mod 2^32) < 2^31"
)
plt.figtext(0.1, 0.01, formula_text, wrap=True, fontsize=9)

plt.subplots_adjust(bottom=0.15)  # Make room for the text

plt.show()

# Calculate the area under the curve before overflow (integration)
if overflow_point:
    # Define integration function
    def exp_func(x):
        return start_value * (2 ** x)


    # Integrate exponential growth until overflow
    area, error = integrate.quad(exp_func, 0, overflow_point)
    print(f"Area under the exponential curve before overflow: {area:.2f}")
    print(f"This represents the total theoretical sum if each value were accumulated")

    # Calculate actual sum before overflow
    actual_sum = sum(dollars[:overflow_point + 1])
    print(f"Actual sum of discrete values before overflow: {actual_sum}")

# Print the mathematical formula explanation
print("\nGeneral Formula for Integer Overflow in Doubling Process:")
print("For a starting value of 1 that doubles each iteration in a 32-bit signed integer:")
print("f(n) = 2^n                                  for n < 31")
print("f(n) = (2^n mod 2^32) - 2^32               for n ≥ 31 and (2^n mod 2^32) ≥ 2^31")
print("f(n) = 2^n mod 2^32                        for n ≥ 31 and (2^n mod 2^32) < 2^31")
print("\nIn simpler terms:")
print("1. Initial exponential growth: f(n) = 2^n")
print("2. After overflow, the function follows a cycle with period equal to the bit size (32)")
print("3. The overflow pattern creates a wave-like behavior with alternating positive and negative values")