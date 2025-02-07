from qiskit_aer import Aer
from qiskit import QuantumCircuit, transpile
from qiskit.circuit import QuantumRegister
from qiskit.visualization import plot_histogram

from math import log2, ceil, floor
import matplotlib.pyplot as plt

def rngCircuit(numQb: int) -> int:
    """builds a quantum circuit of n Qubits and n Hadamard gates,
    which is measured to return a random integer between 0 and 2^(n-1) inclusive"""
    qr = QuantumRegister(numQb)
    qc = QuantumCircuit(qr)
    qc.h(qr)
    qc.measure_all()
    
    backend = Aer.get_backend("aer_simulator")
    tqc = transpile(qc, backend)
    job = backend.run(tqc, shots = 1)
    result = job.result()
    countDict = result.get_counts()
    val = list(countDict.keys())[0]
    return int(str(val), 2)

def randomNumber(low: int, high: int, p: int) -> int:
    """outputs a random integer in the range [low, high);
    higher values of p are more random but more costly"""
    zeroIvl = rngCircuit(p) / (2 ** p)
    range = high - low
    val = floor(zeroIvl * range) + low
    return val
