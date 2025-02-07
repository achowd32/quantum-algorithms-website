from qiskit import QuantumCircuit, transpile
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_bloch_multivector
from qiskit_aer import Aer
import matplotlib.pyplot as plt

def blochs(state: Statevector):
    plot_bloch_multivector(state)

def counts(qc: QuantumCircuit, n: int):
    """given a quantum circuit, returns the counts of that circuit
    simulated n times"""
    backend = Aer.get_backend("aer_simulator")
    tqc = transpile(qc, backend)
    counts = backend.run(tqc, shots = n).result().get_counts()
    return counts
    #plot_histogram(counts)

def sample(qc: QuantumCircuit):
    """samples once from a given quantum circuit and returns the sampled result"""
    backend = Aer.get_backend("aer_simulator")
    tqc = transpile(qc, backend)
    counts = backend.run(tqc, shots = 1).result().get_counts()
    val = list(counts.keys())[0]
    return val