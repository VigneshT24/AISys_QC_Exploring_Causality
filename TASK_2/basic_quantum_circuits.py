from qiskit import QuantumCircuit

class BasicQuantumCircuits():
    """
    A class containing 5 methods that return a configurable circuit that has a known output. 
    This can then be used to complete a benchmark suite to verify the quality of the output.

    Methods:
        1) bell_state_circuit()
        2) ghz_state_circuit() 
        3) parameterized_circuit()
        4) grover_circuit()
        5) variable_depth_circuit()
    """
    def bell_state_circuit(self) -> QuantumCircuit:
        """
        Returns a basic, 2-qubit bell-state quantum circuit, where q0 is in superposition, and q0 and q1 are entangled.

        Args:
            None

        Returns:
            'qc': a basic, 2-qubit bell-state quantum circuit

        Raises:
            None
        """
        qc = QuantumCircuit(2)
        qc.h(0) # superposition the first qubit
        qc.cx(0, 1) # entangle q0 (control qubit) with q1 (target qubit)
        
        return qc

    def ghz_state_circuit(self, n_qubits=3) -> QuantumCircuit:
        """
        Returns an n-qubit GHZ quantum circuit, where q0 is in superposition, and the remaining qubits is entangled with the prior

        Args:
            'n_qubits': the number of qubits to initialize the quantum circuit with

        Returns:
            'qc': a n-qubit GHZ state quantum circuit

        Raises:
            ValueError: if the entered parameter 'n_qubits' is not an integer and/or is negative
        """
        if not isinstance(self, n_qubits, int):
            raise ValueError("The parameter 'n_qubits' to the method \"ghz_state()\" must be an INTEGER, not a decimal or string.")
        if n_qubits < 1:
            raise ValueError(f"The parameter 'n_qubits' to the method \"ghz_state()\" must be a POSITIVE INTEGER. Instead, I got '{n_qubits}'")
        
        qc = QuantumCircuit(n_qubits)
        qc.h(0) 

        for i in range(n_qubits - 1):
            qc.cx(i, i+1) # entangle every next target qubit with the previous control qubit

        return qc

    def parameterized_circuit(self, n_qubits=1, axis_angles_list=None) -> QuantumCircuit:
        """
        Returns a n-qubit parameterized quantum circuit, where it takes a list of angles given and rotates each qubit to that angle

        Args:
            'n_qubits': the number of qubits to initialize the quantum circuit with
            'axis_angles_list': a list of tuples, where each element is in the form "(axis, angle)"

        Returns:
            'qc': a n-qubit GHZ state quantum circuit

        Raises:
            ValueError: if the entered parameter 'n_qubits' is not an integer and/or is negative
        """
        qc = QuantumCircuit(n_qubits)


        if axis_angles_list is None:
            raise ValueError(f"The parameter 'axis_angles_list' must not be empty, and it must be a valid entry (look at the docustring for an example).")
        
        if len(axis_angles_list) != n_qubits:
            raise ValueError(f"For the \"parameterized_circuit\" method, I expected {n_qubits} axis and angle pair(s), instead I got {len(axis_angles_list)}. \
                            Make sure that the length of your \"axis_angle_list\" is the same size as the number of qubits you passed into this method.")
        
        for i in range(n_qubits):
            match axis_angles_list[i][0].lower():
                case 'rx':
                    qc.rx(axis_angles_list[i][1], i)
                case 'ry':
                    qc.ry(axis_angles_list[i][1], i)
                case 'rz':
                    qc.rz(axis_angles_list[i][1], i)
                case _:
                    raise ValueError(f"Axis must be 'rx', 'ry', or 'rz'. Instead, I got '{axis_angles_list[i][0]}'")
        
        for j in range(n_qubits - 1):
            qc.cx(j, j+1)

        return qc

    def grover_circuit(self, n_qubits=2, target='11') -> QuantumCircuit:
        """
        Returns a n-qubit quantum circuit with the grover algorithm applied to search for a target in O(sqrt(N)) time

        Args:
            'n_qubits': the number of qubits to initialize the quantum circuit with
            'target': the target to search for using the Grover's quantum search algorithm

        Returns:
            'qc': a n-qubit Grover QSA applied circuit
        
        Raises:
            ValueError: if the entered 'n_qubits' or 'target' are not the same size or 
            if the value entered for 'n_qubits' or 'target' is not valid
        """
        
        if len(target) != n_qubits:
            raise ValueError(f"I expected the 'target' length to be {n_qubits}. \
                            Instead, I got the 'target' size to be {len(target)}.")
        if not all(qubit in '01' for qubit in target):
            raise ValueError(f"The 'target' must only contain '0' and '1'. Instead, I got \"{target}\".")
        if n_qubits > 5:
            raise ValueError("Keep the 'n_qubits' <= 5 to ensure the simulation performance is not too slow.")
        
        qc = QuantumCircuit(n_qubits)

        # initialize all bits to be in superposition
        for i in range(n_qubits):
            qc.h(i)

        qc.barrier()

        # oracle step: marks the target by flipping its phase
        for i, qubit in enumerate(reversed(target)):
            if qubit == "0":
                qc.x(i)

        if n_qubits == 2:
            qc.cz(0, 1)
        else:
            qc.h(n_qubits - 1)
            qc.mcx(list(range(n_qubits - 1)), (n_qubits - 1))
            qc.h(n_qubits - 1)

        for i, qubit in enumerate(reversed(target)):
            if qubit == "0":
                qc.x(i)

        qc.barrier()

        # diffuser step: amplifies the marked target 
        for i in range(n_qubits):
            qc.h(i)
        for i in range(n_qubits):
            qc.x(i)

        if n_qubits == 2:
            qc.cz(0, 1)
        else:
            qc.h(n_qubits - 1)
            qc.mcx(list(range(n_qubits - 1)), (n_qubits - 1))
            qc.h(n_qubits - 1)
        
        for i in range(n_qubits):
            qc.x(i)
        for i in range(n_qubits):
            qc.h(i)
        
        qc.barrier()

        return qc

    def variable_depth_circuit(self, n_qubits=2, depth=1) -> QuantumCircuit:
        """
        Returns a n-qubit quantum circuit with customizable depth, where depth=1 is shallow and depth=10 is deep

        Args:
            'n_qubits': the number of qubits to initialize the quantum circuit with
            'depth': the number of layers the circuit should have (following a H-X-H pattern for simplicity)

        Returns:
            'qc': a n-qubit quantum circuit with layers as specified

        Raises:
            ValueError: if the value entered for 'n_qubits' or 'depth' is not valid
        """
        if not isinstance(n_qubits, int):
            raise ValueError(f"The parameter 'n_qubits' must be an INTEGER. Instead, I got: \"{n_qubits}\".")
        if n_qubits < 1:
            raise ValueError(f"The parameter 'n_qubits' must be a POSITIVE integer. Instead, I got a negative or zero value: \"{n_qubits}\".")
        if not isinstance(depth, int):
            raise ValueError(f"The parameter 'depth' must be an INTEGER. Instead, I got: \"{depth}\".")
        if depth < 1:
            raise ValueError(f"The parameter 'depth' must be a POSTIVE integer. Instead, I got a negative or zero value: \"{depth}\".")
        
        qc = QuantumCircuit(n_qubits)

        # method that adds depth to a single qubit
        def sqdi(qubit, depth, switch_order):
            for iter in range(depth):
                if not switch_order:
                    if (iter % 2) == 0:
                        qc.h(qubit)
                    else:
                        qc.x(qubit)
                else:
                    if (iter % 2) != 0:
                        qc.x(qubit)
                    else:
                        qc.h(qubit)

        switch_order = False
        for i in range(n_qubits):
            sqdi(i, depth, switch_order)
            switch_order = not(switch_order)

        return qc