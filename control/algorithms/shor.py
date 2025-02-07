from qiskit import QuantumCircuit, transpile
from qiskit.circuit import QuantumRegister, ClassicalRegister
from qiskit.circuit.library import QFT
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_bloch_multivector, plot_histogram
from qiskit_aer import Aer

import matplotlib.pyplot as plt
from random import randint
from math import gcd
from typing import Optional
from fractions import Fraction

#reference: https://github.com/Qiskit/textbook/blob/main/notebooks/ch-algorithms/shor.ipynb
#next steps: https://arxiv.org/pdf/quant-ph/0205095

def c_amod15(a, p):
    """ Hard-coded controlled multiplication by a mod 15.
    Taken from IBM Quantum Learning."""
    if a not in [2, 4, 7, 8, 11, 13]:
        raise ValueError("'a' must not have common factors with 15")
    U = QuantumCircuit(4)
    for _ in range(p):
        if a in [2, 13]:
            U.swap(2, 3)
            U.swap(1, 2)
            U.swap(0, 1)
        if a in [7, 8]:
            U.swap(0, 1)
            U.swap(1, 2)
            U.swap(2, 3)
        if a in [4, 11]:
            U.swap(1, 3)
            U.swap(0, 2)
        if a in [7, 11, 13]:
            for q in range(4):
                U.x(q)
    U = U.to_gate()
    U.name = f"{a}^{p} mod 15"
    c_U = U.control()
    return c_U

def shorQPE(a_val: int, precision: int):
    """Performs the quantum phase estimation required for Shor's algorithm
    Hard-coded for factoring 15"""
    work_num = 4
    estimation_register = QuantumRegister(precision)
    work_register = QuantumRegister(work_num)
    classical_register = ClassicalRegister(precision)
    qc = QuantumCircuit(estimation_register, work_register, classical_register)

    qc.h(estimation_register)
    qc.x(work_register[0])
    for i in range(precision):
        qc.append(c_amod15(a_val, 2**i), [i] + [*range(precision, precision + work_num)])
    invQFT = QFT(precision, inverse = True)
    qc.append(invQFT, [*range(precision)])
    qc.measure(estimation_register, classical_register)

    backend = Aer.get_backend("aer_simulator")
    tqc = transpile(qc, backend)
    counts = backend.run(tqc, shots = 1).result().get_counts()
    val = list(counts.keys())[0]
    phase = int(val, 2)/(2**precision)
    return phase

def shor15(a_val: Optional[int] = None) -> tuple[Optional[int], list[int], bool]:
    """Runs Shor's algorithm for factoring 15 with the given a value.
    Randomises a if not given. Returns a tuple of the generated r-value,
    a list of generated factors, and whether the QPE was needed."""
    if not a_val:
        a_val = randint(2, 14)
    if not int(a_val):
        raise ValueError("Given a_val is not an integer")
    if a_val > 13 or a_val < 2:
        raise ValueError("Given a_val is out of bounds")
    if gcd(15, a_val) == 1:
        sr_val = shorQPE(a_val, 6) #s/r
        frac = Fraction(sr_val).limit_denominator(15)
        r = int(frac.denominator)
        if r % 2 == 0:
            factors = [gcd(a_val**(r//2)-1, 15), gcd(a_val**(r//2)+1, 15)]
            return (r, factors, True)
        else:
            return (r, [], True)
    else:
        p = gcd(15, a_val)
        q = int(15/p)
        factors = [p, q]
        return (None, factors, False)