## Exploring quantum error correction


One may consider a quantum circuit as a mapping, which takes a qubit system from an initial state to a resulting output state. When a quantum circuit undergoes an error or noise, the resulting output state may be a physically distinguishable output state when compared to the originally desired output state.
<!-- 
A *logical state* refers to logical information which is encoded by an equivalence class of physical states: while a quantum circuit undergoing noise may result in a physically distinct output state, it is possible that logical information is retained either by the fact that the resulting output state lies in the same equivalence class, or may be adjusted to lie in the same equivalence class.  -->

Morally speaking, one can consider an quantum error correction code as a procedure for maintaining a desired output state, even in the presence of possible noise.



 <!-- By defining appropriate logical states, this desired output state may vary up to a state contained in the same logical equivalence class.  -->


#### Syndrome measurement 

As the goal of a quantum error correction code is to maintain a specific quantum state, one needs to understand how to operate on a given qubit system appropriately after it has gone through possible noise, without collapsing the state of the system. In particular, we cannot simply measure the state of the qubit system and operate according to the result of the measurement. Instead, the qubit system is coupled or entangled with another auxillary system of qubits, referred to as *syndrome qubits*. One can measure the syndrome qubits without collapsing the state of our original qubit system (the qubits in the original qubit system are sometimes referred to as *data qubits*). If this is done appropriately, in principle we can measure the state of the syndrome qubit system and then operate on the data qubit system accordingly. 

Of course, in the process of entangling the data qubit system with the syndrome qubit system, measuring the syndrome qubits may also have an effect on our data qubit system. Therefore, care must be taken in designing a quantum error correcting code, so that measuring the syndrome qubit system does not result in potential undesired effects on the data qubits. 

Furthermore, by the *no-cloning theorem*, the syndrome qubit system cannot simply be a perfect replica of the data qubit system. Therefore, the best that one can hope for in general, is that measuring the syndrome system will "inform us", or provide some *hint* about the state of the data qubits; and in hopes of maintaining a desired output state, one can operate on the data qubit system according to syndrome measurements in an appropriate way. 



### Repository details

We showcase qiskit implementations of some basic tools and concepts from the subject of quantum error correction. In particular, the module [exploringqec.py](exploringqec.py) provides a function ```noise_model(a,b,circuit)```, which takes a quantum circuit ```circuit```, and introduces a random Pauli X with probability ```a``` to each physical qubit of ```circuit``` and introduces a random Pauli Z with probability ```b``` to each physical qubit of ```circuit```. 


As mentioned, the module [exploringqec.py](exploringqec.py) consists of the function ```noise_model``` (the simple noise model), and implementations of the quantum repetition code, Shor's code, and Steane's code.
The [Jupyer notebook](exploringqec.ipynb) demonstrates the basic functionality behind these codes, and how to use the simple noise model. 

