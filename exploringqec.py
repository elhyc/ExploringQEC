
from qiskit.circuit import QuantumCircuit, QuantumRegister, AncillaRegister,ClassicalRegister
import itertools
import numpy as np
from qiskit_aer import AerSimulator


def noise_model(a,b,circuit, print_option=False):
    
    ## A simple noise model.  
    # Introduce a random Pauli (X with “a” probability,Z with “b” probability) into any circuit.
    # Returns a quantum circuit which is the result of noise added to input circuit

    circuit_with_noise = circuit 
    qubits = circuit_with_noise.qubits 
    
    for qubit in qubits:
        
        error_choice = np.random.choice([0,1,2],p=[1 - (a+b), a,b])
        
        if error_choice == 1:
            circuit_with_noise.x(qubit)
            if print_option:
                print('X applied to ' + str(qubit) )
            
        elif error_choice == 2:
            circuit_with_noise.z(qubit)
            if print_option:
                print('Z applied to ' + str(qubit) )

    return circuit_with_noise 


def quantum_rep_code(n, state=0, mode='X'):
    # Returns a quantum circuit that initializes a quantum repetition code of size n. 

    # Optional state parameter is set to 0 by default. If state is set to 0, then the quantum repetition 
    # code will initialize to logical 0, if state is set to 1 then the code will initialize to logical 1.

    # Optional parameter 'mode' is set to 'X' by default. If mode is set to 'X', then logical qubits
    # are encoded by | 00.. 0 > and | 1 1 .. 1 > (i.e. an eigenvector for Z operator acting on any qubit)
    # if mode is set to 'Z' then logical qubits are encoded as  | + + + .. + > and | - - ... - > respectively 
    # (i.e. eigenvectors for X operator acting on any qubit)
    
    repcode_circuit = QuantumCircuit(n)
    
    if mode == 'Z':
        for qubit in repcode_circuit.qubits:
            repcode_circuit.h(qubit)        
        
    if state == 1:
        for qubit in repcode_circuit.qubits:
            if mode == 'X':
                repcode_circuit.x(qubit)
            elif mode == 'Z':
                repcode_circuit.z(qubit)
            
    return repcode_circuit 
            
    
def shor_code(state=0):
    #Returns a circuit that initializes Shor's 9 qubit code.
    
    # Optional parameter 'state' is set to 0 by default. If state == 1, then 
    # Shor's code will be initialized to logical state 1 
    
    shor_circuit = QuantumCircuit(9)
    
    shor_circuit.cx(0,3)
    shor_circuit.cx(0,6) 
    
    for idx in range(len(shor_circuit.qubits)):
        if idx%3 == 0:
            lead_qubit = shor_circuit.qubits[idx]
            shor_circuit.h( lead_qubit )
            shor_circuit.cx(lead_qubit, shor_circuit.qubits[idx+1])
            shor_circuit.cx(lead_qubit,  shor_circuit.qubits[idx+2])
            
    if state == 1:
        for qubit in shor_circuit.qubits:
            shor_circuit.x(qubit) 

    return shor_circuit
            
def steane_code(state=0):
    # Returns a circuit that initializes Steane's code 
    # (i.e. the quantum CSS code defined by using Hamming code matrices as the parity check matrices ).
    
    # Optional parameter 'state' is set to 0 by default. If state == 1, then 
    # Steane's code will be initialized to logical state 1     
    
    
    steane_circuit = QuantumCircuit(7)
    steane_leaders = [0,1,3]
    for idx in steane_leaders:
        steane_circuit.h(  steane_circuit.qubits[idx] )
        if idx == 0:
            steane_circuit.cx(steane_circuit.qubits[0], steane_circuit.qubits[2] )
            steane_circuit.cx(steane_circuit.qubits[0], steane_circuit.qubits[4] )
            steane_circuit.cx(steane_circuit.qubits[0], steane_circuit.qubits[6] )
        elif idx == 1:
            steane_circuit.cx(steane_circuit.qubits[1], steane_circuit.qubits[2] )
            steane_circuit.cx(steane_circuit.qubits[1], steane_circuit.qubits[5] )
            steane_circuit.cx(steane_circuit.qubits[1], steane_circuit.qubits[6] )
        elif idx == 3:
            steane_circuit.cx(steane_circuit.qubits[3], steane_circuit.qubits[4] )
            steane_circuit.cx(steane_circuit.qubits[3], steane_circuit.qubits[5] )
            steane_circuit.cx(steane_circuit.qubits[3], steane_circuit.qubits[6] )
            
    if state == 1:
        for qubit in steane_circuit.qubits:
            steane_circuit.x(qubit)
            
    return steane_circuit     
            
def syndrome_measure(code_circuit, table, pauli_type):
    
    code_ancillas = AncillaRegister(len(table))
    code_classical_bits = ClassicalRegister(len(table))
    
    code_circuit.add_register(code_ancillas)
    code_circuit.add_register(code_classical_bits)
    
    for key in table:
        code_circuit.h(code_ancillas[key])
        for idx in table[key]:
            if pauli_type == 'X':
                code_circuit.cx(code_ancillas[key], code_circuit.qubits[idx])
            elif pauli_type == 'Z':
                code_circuit.cz( code_ancillas[key], code_circuit.qubits[idx])
                
        code_circuit.h(code_ancillas[key])
        code_circuit.measure(code_ancillas[key], code_classical_bits[key])



def measure_data( code_circuit, qubits ):
    classical_reg = ClassicalRegister(len(qubits))
    code_circuit.add_register(classical_reg)
    
    for idx in range(len(qubits)):
        code_circuit.measure(qubits[idx], classical_reg[idx])
        
    job = AerSimulator().run(code_circuit, shots=1, memory=True)   
    result = job.result()
    memory = result.get_memory(code_circuit)
    return memory[0][:len(qubits)]
    

    
