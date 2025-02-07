from qiskit import QuantumCircuit, transpile
from qiskit.circuit import QuantumRegister
from qiskit.circuit.library import QAOAAnsatz
from qiskit.visualization import plot_bloch_multivector, plot_histogram
from qiskit.quantum_info import SparsePauliOp
from qiskit_ibm_runtime import EstimatorV2 as Estimator
from qiskit_aer import Aer

import matplotlib.pyplot as plt
from math import pi
from scipy.optimize import minimize

def qzz_paulis(edges: list[tuple[int, int, float]], graph_size: int) -> list[tuple[str, float]]:
    """Constructs a Pauli list corresponding to the QZZ term of a Hamiltonian
    for a QAOA algorithm that solves maxcut."""
    pauli_list = []
    for edge in edge_list:
        cur_pauli = ["I"] * graph_size
        node_one, node_two, weight = edge[0], edge[1], edge[2]
        cur_pauli[node_one] = "Z"
        cur_pauli[node_two] = "Z"
        pauli_str = "".join(cur_pauli)
        pauli_list.append((pauli_str, weight))
    return pauli_list

def bz_paulis(edges: list[tuple[int, int, float]], graph_size: int) -> list[tuple[str, float]]:
    """Constructs a Pauli list corresponding to the bZ term of a Hamiltonian
    for a QAOA algorithm that solves maxcut."""
    #find the sum of terms in each row Q_i; equivalently the sum of terms in column Q_j
    row_sum = [0] * graph_size
    for edge in edge_list:
        node_one, node_two, weight = edge[0], edge[1], edge[2]
        row_sum[node_one] += weight
        row_sum[node_two] += weight
    
    #add a tensor product for each node
    pauli_list = []
    for node in range(graph_size):
        cur_pauli = ["I"] * graph_size
        cur_pauli[node] = "Z"
        weight = row_sum[node]
        pauli_str = "".join(cur_pauli)
        pauli_list.append((pauli_str, weight))
    return pauli_list

def cost_function_estimator(params, ansatz, hamiltonian, estimator):
    """Runs an estimator circuit on given parameters, ansatz, and hamiltonian"""
    isa_hamiltonian = hamiltonian.apply_layout(ansatz.layout)
    pub = (ansatz, isa_hamiltonian, params)
    job = estimator.run([pub])
    results = job.result()[0]
    cost = results.data.evs
    return cost

def max_cut(edges: list[tuple[int, int, float]], graph_size: int):
    """performs QAOA on a maxcut problem described by the given list of edges
    and graph size. Returns the max_cut value"""
    #construct circuit
    cost_hamiltonian = SparsePauliOp.from_list(qzz_paulis(edges, 5))
    circuit = QAOAAnsatz(cost_operator=cost_hamiltonian, reps=2)
    circuit.measure_all()

    #initialize backend (simulator)
    backend = Aer.get_backend("aer_simulator")
    tqc = transpile(circuit, backend)

    #initialize parameters
    initial_gamma = pi
    initial_beta = pi/2
    init_params = [initial_gamma, initial_beta, initial_gamma, initial_beta]

    estimator = Estimator(backend)
    estimator.options.default_shots = 1000

    #properly setup estimator for the hardware, incl error mitigation stuff
    #optimize with SciPy
    result = minimize(
            cost_function_estimator,
            init_params,
            args=(tqc, cost_hamiltonian, estimator),
            method="COBYLA",
            tol=1e-2)
    #sample from optimized circuit
    optimized_circuit = tqc.assign_parameters(result.x)
    counts = backend.run(optimized_circuit, shots = 1).result().get_counts()
    val = list(counts.keys())[0]
    return val