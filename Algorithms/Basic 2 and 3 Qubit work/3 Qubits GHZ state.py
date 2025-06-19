# ===============================================================================
# 3-Qubit GHZ State Circuit - Self-Contained Qiskit Example
# Description: This script builds, simulates, and visualizes a 3-qubit GHZ
#              (Greenberger–Horne–Zeilinger) state.
#              The GHZ state is a multi-qubit entangled state fundamental to
#              quantum computing, demonstrating stronger non-local correlations
#              than Bell states.
# ===============================================================================

# --- Import necessary Qiskit components ---
# QuantumCircuit: Used to build quantum circuits.
# transpile: Optimizes a quantum circuit for a specific backend (simulator or real hardware).
# Aer: Qiskit's high-performance simulator backend.
from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

# --- 1. Define Simulator ---
# We'll use the Aer simulator, specifically the 'qasm_simulator'.
# This simulator mimics the behavior of a quantum computer and provides
# measurement counts from multiple "shots" (runs).
simulator = Aer.get_backend('qasm_simulator')


# --- 2. Define Number of Shots for Simulation ---
# 'shots' refers to the number of times the quantum circuit will be executed
# to gather statistical results. A higher number provides more accurate
# probabilities of measurement outcomes.
num_shots = 1024

# --- 3. Create a 3-Qubit GHZ State Circuit ---
# A GHZ state requires at least 3 qubits.
# We create a quantum circuit with 3 qubits and 3 classical bits.
# Classical bits are necessary to store the measurement results of the qubits.
num_ghz_qubits = 3
qc_ghz = QuantumCircuit(num_ghz_qubits, num_ghz_qubits)

# --- 4. Apply Hadamard Gate to Qubit 0 ---
# The Hadamard gate (H) transforms qubit 0 from its initial |0⟩ state
# into a superposition of |0⟩ and |1⟩: ( |0⟩ + |1⟩ ) / sqrt(2).
# This is the first step in creating the entangled state.
qc_ghz.h(0) # Apply Hadamard to the first qubit (index 0)

# --- 5. Apply CNOT Gates for Entanglement ---
# CNOT (Controlled-NOT) gates are used to create entanglement.
# The CNOT gate flips the target qubit if the control qubit is |1⟩.
#
# First CNOT: Qubit 0 (control) and Qubit 1 (target).
# This entangles Qubit 0 with Qubit 1.
# The state becomes ( |00⟩ + |11⟩ ) / sqrt(2) for qubits 0 and 1.
qc_ghz.cx(0, 1) # Control: qubit 0, Target: qubit 1

# Second CNOT: Qubit 0 (control) and Qubit 2 (target).
# This extends the entanglement to Qubit 2.
# The final GHZ state becomes ( |000⟩ + |111⟩ ) / sqrt(2).
# In this state, measuring any one qubit collapses the state of all three.
qc_ghz.cx(0, 2) # Control: qubit 0, Target: qubit 2

# --- 6. Measure All Qubits ---
# Measure each quantum qubit and store its result in a corresponding classical bit.
# This causes the "probabilistic collapse" of the multi-qubit superposition.
# For an ideal GHZ state, we expect to predominantly see '000' or '111' as outcomes.
qc_ghz.measure([0, 1, 2], [0, 1, 2]) # Measure all qubits to their respective classical bits

# --- 7. Transpile and Run the Circuit on the Simulator ---
# Transpilation optimizes the circuit for the target backend (simulator in this case).
transpiled_qc_ghz = transpile(qc_ghz, simulator)

# Run the transpiled circuit on the simulator for the specified number of shots.
job_ghz = simulator.run(transpiled_qc_ghz, shots=num_shots)

# Retrieve the results from the simulation job.
result_ghz = job_ghz.result()

# Get the frequency counts of each measurement outcome.
# 'counts' will be a dictionary where keys are bitstrings (e.g., '000', '111')
# and values are the number of times that outcome was observed.
counts_ghz = result_ghz.get_counts(qc_ghz)

# --- 8. Visualize the Results ---

# Print a text-based diagram of the quantum circuit.
print("\n--- 3-Qubit GHZ State Circuit Diagram ---")
print(qc_ghz.draw(output='text'))

# Print the raw measurement outcome counts.
print(f"\n--- 3-Qubit GHZ State Measurement Outcomes (Simulated {num_shots} shots) ---")
print(counts_ghz)

# Attempt to display a histogram plot of the measurement outcomes.
# A try-except block is used to gracefully handle environments where
# a graphical display for matplotlib plots might not be available.
try:
    fig_ghz = plot_histogram(counts_ghz, title="Measurement Outcomes of 3-Qubit GHZ State")
    plt.tight_layout() # Adjusts plot parameters for a tight layout.
    plt.show()         # Displays the plot.
    print("\nSuccessfully displayed GHZ state histogram plot.")
    # To save this plot as an image file (e.g., for Paper 5 later),
    # uncomment the following line and specify a filename:
    # fig_ghz.savefig("ghz_state_histogram.png")
except Exception as e:
    print(f"\nCould not display GHZ histogram plot. Error: {e}")
    print("This might happen in environments without a graphical backend for matplotlib.")
    print("You can still examine the 'counts_ghz' dictionary directly in the console.")

