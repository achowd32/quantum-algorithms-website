from qiskit import QuantumCircuit
from qiskit.circuit.library import QFT
from qiskit.quantum_info import Statevector
import matplotlib.pyplot as plt
from qiskit.visualization import plot_bloch_multivector

def applyQFT(bitstr: str):
    initial = Statevector.from_label(bitstr)
    num_qb = len(bitstr)
    qc = QuantumCircuit(num_qb)
    qc.prepare_state(initial, range(num_qb))
    qc.append(QFT(num_qb), range(num_qb))
    output = Statevector(qc)
    return output.data