import matplotlib.pyplot as plt
from basic_quantum_circuits import BasicQuantumCircuits
import numpy as np

def show_circuit(circuit_name, qc):
    print(f"{circuit_name}: ")
    qc.draw('mpl')
    plt.show()

def parse_angle(angle_str):
    """Safely evaluates an angle string that might contain 'pi'"""
    # create a safe mapping so the string 'pi' equals the actual numerical value
    safe_dict = {"pi": np.pi, "np": np}
    
    try:
        # Evaluate the math string securely
        return float(eval(angle_str, {"__builtins__": None}, safe_dict))
    except Exception:
        raise ValueError(f"Could not parse angle: '{angle_str}'. Please use decimals or 'pi' (e.g., pi/2).")

circuit = BasicQuantumCircuits()

inp = input("Which Circuit Do You Want To Configure & Display? (type the corresponding number):\n\n" \
            "Bell State Circuit - 1\n" \
            "GHZ State Circuit - 2\n" \
            "Grover Circuit - 3\n" \
            "Parameterized Circuit - 4\n" \
            "Variable Depth Circuit - 5\n" \
            "\n:")

match inp.strip().lower():
    case "1":
        print("You chose Bell State Circuit. Since you cannot configure this circuit, it will be displayed as is.")
        show_circuit("Bell State Circuit", circuit.bell_state_circuit())
    case "2":
        num_qubits = input("You chose GHZ State Circuit. Enter the number of qubits to configure this circuit with: ")
        show_circuit("GHZ State Circuit", circuit.ghz_state_circuit(int(num_qubits)))
    case "3":
        num_qubits = input("You chose Grover Circuit. Enter the number of qubits to configure this circuit with: ")
        target = input("Now, enter the target sequence of qubits that you want the circuit to be configured to find: ")
        show_circuit("Grover Circuit", circuit.grover_circuit(int(num_qubits), target.strip()))
    case "4":
        num_qubits = input("You chose Parameterized Circuit. Enter the number of qubits to configure this circuit with: ")
        parameters = [] # list to store the tuples of (axis, angle)

        for i in range(int(num_qubits)):
            axis_angle = input(f"Now, enter the axis and angle to rotate qubit q{i}. The format you enter must be (axis, angle) WITHOUT parentheses: ")
            axis_angle = [item.strip() for item in axis_angle.split(",")]

            # if the user forgot to include a comma
            if len(axis_angle) != 2:
                print("Invalid format. Please enter as 'axis, angle' (example: rx, pi/2). Defaulting to rx, 0.")
                parameters.append(('rx', 0.0))
                continue

            axis = axis_angle[0].lower()
            angle_str = axis_angle[1].lower()

            try:
                angle = parse_angle(angle_str)
            except ValueError as e:
                print(e)
                print("Defaulting angle to 0.0")
                angle = 0.0
            
            parameters.append((axis, angle))

        show_circuit("Parameterized Circuit", circuit.parameterized_circuit(int(num_qubits), parameters))
    case "5":
        num_qubits = input("You chose Variable Depth Circuit. Enter the number of qubits to configure this circuit with: ")
        depth = input("Now, enter the depth level (a number between 1 to 10) to configure this circuit with: ")
        show_circuit("Variable Depth Circuit", circuit.variable_depth_circuit(int(num_qubits), int(depth)))
    case _:
        raise ValueError("Not valid input. Please enter a number between 1 - 5, corresponding to which circuit you want to display.")