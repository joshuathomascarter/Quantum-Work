# ===============================================================================
# Qiskit Entanglement & Interference Playground
# Description: This script builds and simulates a quantum circuit demonstrating
#              entanglement and interference with 2 qubits.
#              It applies Hadamard and CNOT gates and measures the probabilistic
#              collapse.
# ===============================================================================

# Import necessary Qiskit components
from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer  # Updated import to reflect modular Qiskit structure
from qiskit.visualization import plot_histogram, circuit_drawer
import matplotlib.pyplot as plt

# --- 1. Define the Quantum Circuit ---
# Create a quantum circuit with 2 qubits and 2 classical bits
# qc = QuantumCircuit(num_qubits, num_classical_bits)
# We need classical bits to store the measurement results.
num_qubits = 2
qc = QuantumCircuit(num_qubits, num_qubits)

# --- 2. Apply Hadamard Gate to Qubit 0 ---
# The Hadamard gate puts a qubit into a superposition state.
# If qubit 0 starts in |0⟩, after Hadamard it will be in ( |0⟩ + |1⟩ ) / sqrt(2)
# This creates the necessary condition for interference later.
qc.h(0)  # Apply Hadamard to qubit 0

# --- 3. Apply CNOT Gate for Entanglement ---
# The CNOT (Controlled-NOT) gate entangles the two qubits.
# Qubit 0 is the control, Qubit 1 is the target.
# If control is |0⟩, target doesn't change.
# If control is |1⟩, target flips (NOT operation).
# With qubit 0 in superposition, this creates an entangled state where
# neither qubit's state can be described independently.
# The state becomes ( |00⟩ + |11⟩ ) / sqrt(2)
qc.cx(0, 1)  # Apply CNOT with qubit 0 as control and qubit 1 as target

# --- 4. Measure the Qubits ---
# Measure both qubits and map the quantum results to classical bits.
# This causes the "probabilistic collapse" of the entangled superposition.
# We expect to predominantly see '00' or '11' as outcomes due to entanglement.
qc.measure([0, 1], [0, 1])  # Measure qubit 0 to classical bit 0, and qubit 1 to classical bit 1

# --- 5. Choose a Simulator and Run the Circuit ---
# We'll use the Aer simulator, which is a high-performance simulator for Qiskit.
# The 'qasm_simulator' simulates the circuit execution and provides counts of outcomes.
simulator = Aer.get_backend('qasm_simulator')

# Transpile the circuit for the simulator (optimizes it)
transpiled_qc = transpile(qc, simulator)

# Run the circuit on the simulator
# shots: number of times to run the circuit to get statistical results.
# Higher shots give a more accurate representation of the probabilities.
num_shots = 1024
job = simulator.run(transpiled_qc, shots=num_shots)

# Get the results from the job
result = job.result()

# Get the measurement outcome counts
counts = result.get_counts(qc)

# --- 6. Visualize the Results ---

# Print the circuit drawing
print("--- Quantum Circuit Diagram ---")
print(qc.draw(output='text'))

# Plot the histogram of results
print(f"\n--- Measurement Outcomes (Simulated {num_shots} shots) ---")
print(counts)

# Display the histogram plot
# Using try-except for matplotlib to handle potential display issues in some environments
try:
    fig = plot_histogram(counts, title="Measurement Outcomes of Entangled Qubits")
    plt.tight_layout()  # Adjust layout to prevent labels overlapping
    plt.show()
    print("\nSuccessfully displayed histogram plot.")
    # To save the plot for Paper 5 later, you can uncomment the line below:
    # fig.savefig("entanglement_circuit_histogram.png")
except Exception as e:
    print(f"\nCould not display histogram plot. Error: {e}")
    print("This might happen in environments without a graphical backend.")
    print("You can still examine the 'counts' dictionary directly.")


print("\n--- Creating a 3-Qubit GHZ State Circuit ---")
qc_ghz = QuantumCircuit(3, 3)
qc_ghz.h(0) # Hadamard on qubit 0
qc_ghz.cx(0, 1) # CNOT(0,1)
qc_ghz.cx(0, 2) # CNOT(0,2) - entangles qubit 0 with qubit 2
qc_ghz.measure([0, 1, 2], [0, 1, 2])

transpiled_qc_ghz = transpile(qc_ghz, simulator)
job_ghz = simulator.run(transpiled_qc_ghz, shots=num_shots)
result_ghz = job_ghz.result()
counts_ghz = result_ghz.get_counts(qc_ghz)

print("\n--- 3-Qubit GHZ State Circuit Diagram ---")
print(qc_ghz.draw(output='text'))
print(f"\n--- 3-Qubit GHZ State Measurement Outcomes (Simulated {num_shots} shots) ---")
print(counts_ghz)

try:
    fig_ghz = plot_histogram(counts_ghz, title="Measurement Outcomes of 3-Qubit GHZ State")
    plt.tight_layout()
    plt.show()
    # To save this plot:
    # fig_ghz.savefig("ghz_state_histogram.png")
except Exception as e:
    print(f"\nCould not display GHZ histogram plot. Error: {e}")