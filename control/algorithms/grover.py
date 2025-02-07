from qiskit import QuantumCircuit, transpile
from qiskit.circuit import QuantumRegister
from qiskit.circuit.library import MCMT
from qiskit.visualization import plot_bloch_multivector, plot_histogram
from qiskit_aer import Aer

from math import sqrt, asin, floor, pi
import matplotlib.pyplot as plt

def partialSumOracle():
    """Defines an quantum circuit which identifies when two sums of three digits,
    either 0 or 1, are equivalent."""
    #establish circuit
    processing_register = QuantumRegister(6, name='p')
    sum_1 = QuantumRegister(2, name = 's1')
    sum_2 = QuantumRegister(2, name = 's2')
    aux_register = QuantumRegister(2, name = 'a')
    qc = QuantumCircuit(processing_register, sum_1, sum_2, aux_register)

    #assign variables
    q0, q1, q2 = processing_register[0], processing_register[1], processing_register[2]
    q3, q4, q5 = processing_register[3], processing_register[4], processing_register[5]
    s0, s1 = sum_1[0], sum_1[1]
    s2, s3 = sum_2[0], sum_2[1]
    a0, a1 = aux_register[0], aux_register[1]

    #add gates, construct circuit
    qc.cx(q0, s0)
    qc.cx(q1, s0)
    qc.cx(q2, s0)
    qc.ccx(q0, q1, s1)
    qc.ccx(q1, q2, s1)
    qc.ccx(q0, q2, s1)
    qc.cx(q3, s2)
    qc.cx(q4, s2)
    qc.cx(q5, s2)
    qc.ccx(q3, q4, s3)
    qc.ccx(q4, q5, s3)
    qc.ccx(q3, q5, s3)
    qc.cx(s0, aux_register[0])
    qc.cx(s1, aux_register[1])
    qc.cx(s2, aux_register[0])
    qc.cx(s3, aux_register[1])
    qc.x(aux_register)
    return qc

def sumOracle():
    """converts the partial sum oracle into a complete oracle"""
    part_oracle_circ = partialSumOracle()
    inv_oracle_circ = part_oracle_circ.inverse()
    part_oracle_gate = part_oracle_circ.to_gate(label='oracle')
    inv_oracle_gate = inv_oracle_circ.to_gate(label='inv_oracle')
    qc = QuantumCircuit(13)
    qc.x(12)
    qc.h(12)
    qc.append(part_oracle_gate, list(range(12)))
    qc.ccx(10, 11, 12)
    qc.append(inv_oracle_gate, list(range(12)))
    return qc

def diffuser(n: int):
    """defines a diffuser for use in Grover's algorithm"""
    qr = QuantumRegister(n)
    qc = QuantumCircuit(qr)
    #h-gates
    qc.h(qr)
    #x-gates
    qc.x(qr)
    #multi-controlled z gate
    qc.h(n-1)
    qc.mcx(list(range(n-1)), n-1)
    qc.h(n-1)
    #x-gates
    qc.x(qr)
    #h-gates
    qc.h(qr)
    return qc

def numIter(num_sol: int, total: int):
    """returns the optimal number of Grover iterations based on
    the number of solutions and total number of valid strings"""
    theta = asin(sqrt(num_sol / total))
    t = floor(pi / (4 * theta))
    return t

def groverCirc():
    """constructs a Grover circuit for identifying two sums of three digits
    (either 0 or 1) that are equivalent"""
    oracle_gate = sumOracle().to_gate(label='U_f')
    diffuser_gate = diffuser(6).to_gate(label='U_s')
    qc = QuantumCircuit(13, 6)
    qc.h(list(range(6)))
    qc.x(12)
    qc.h(12)
    for _ in range(numIter(20, 64)):
        qc.append(oracle_gate, list(range(13)))
        qc.append(diffuser_gate, list(range(6)))
    qc.measure(range(6), range(6))
    return qc