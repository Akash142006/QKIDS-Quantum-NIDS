"""
QKIDS: Quantum Kernel Module
Implements quantum feature maps and kernel computation using PennyLane
"""

import pennylane as qml
import numpy as np
from tqdm import tqdm

class QuantumKernel:
    """
    Quantum Kernel using PennyLane for kernel computation
    """
    
    def __init__(self, n_qubits, entanglement='linear'):
        """
        Initialize quantum kernel
        
        Args:
            n_qubits (int): Number of qubits (features)
            entanglement (str): Type of entanglement ('linear', 'full', 'none')
        """
        self.n_qubits = n_qubits
        self.entanglement = entanglement
        
        # Create quantum device
        self.dev = qml.device('default.qubit', wires=n_qubits)
        
        print(f"🔮 Quantum Kernel initialized:")
        print(f"   Qubits: {n_qubits}")
        print(f"   Entanglement: {entanglement}")
        print(f"   Device: {self.dev.name}")
    
    def feature_map(self, x):
        """
        Quantum feature map circuit
        
        Args:
            x (array): Input feature vector (length = n_qubits)
        """
        # Rotation layer: encode features as rotation angles
        for i in range(self.n_qubits):
            qml.RY(x[i], wires=i)
        
        # Entanglement layer
        if self.entanglement == 'linear':
            # Linear CNOT chain: qubit i -> i+1
            for i in range(self.n_qubits - 1):
                qml.CNOT(wires=[i, i + 1])
        
        elif self.entanglement == 'full':
            # All-to-all entanglement
            for i in range(self.n_qubits):
                for j in range(i + 1, self.n_qubits):
                    qml.CNOT(wires=[i, j])
        
        # If 'none', no entanglement is applied
    
    def kernel_circuit(self, x1, x2):
        """
        Quantum circuit for computing kernel between two samples
        
        Args:
            x1 (array): First sample
            x2 (array): Second sample
            
        Returns:
            float: Kernel value |<ψ(x1)|ψ(x2)>|²
        """
        @qml.qnode(self.dev)
        def circuit():
            # Apply feature map for x1
            self.feature_map(x1)
            
            # Apply adjoint (inverse) of feature map for x2
            qml.adjoint(self.feature_map)(x2)
            
            # Measure probability of all qubits being in |0⟩
            return qml.probs(wires=range(self.n_qubits))
        
        # Kernel value is the probability of measuring |00...0⟩
        probs = circuit()
        kernel_value = probs[0]  # Probability of |00...0⟩ state
        
        return kernel_value
    
    def compute_kernel_matrix(self, X1, X2=None):
        """
        Compute kernel matrix K[i,j] = k(x_i, x_j)
        
        Args:
            X1 (array): First set of samples (n_samples_1, n_features)
            X2 (array): Second set of samples (optional, defaults to X1)
            
        Returns:
            array: Kernel matrix (n_samples_1, n_samples_2)
        """
        if X2 is None:
            X2 = X1
            symmetric = True
        else:
            symmetric = False
        
        n1 = len(X1)
        n2 = len(X2)
        
        print(f"\n⚛️  Computing quantum kernel matrix ({n1}×{n2})...")
        
        K = np.zeros((n1, n2))
        
        # Progress bar
        total_computations = (n1 * (n1 + 1)) // 2 if symmetric else n1 * n2
        pbar = tqdm(total=total_computations, desc="   Kernel computation")
        
        for i in range(n1):
            start_j = i if symmetric else 0
            for j in range(start_j, n2):
                K[i, j] = self.kernel_circuit(X1[i], X2[j])
                
                # If symmetric, fill the other half
                if symmetric and i != j:
                    K[j, i] = K[i, j]
                
                pbar.update(1)
        
        pbar.close()
        
        print(f"   ✓ Kernel matrix computed: {K.shape}")
        print(f"   ✓ Min value: {K.min():.4f}, Max value: {K.max():.4f}")
        
        return K
    
    def compute_kernel_vector(self, x_new, X_train):
        """
        Compute kernel vector between new sample and training set
        Used for prediction
        
        Args:
            x_new (array): New sample (n_features,)
            X_train (array): Training samples (n_samples, n_features)
            
        Returns:
            array: Kernel vector (n_samples,)
        """
        n_train = len(X_train)
        k_vector = np.zeros(n_train)
        
        print(f"\n⚛️  Computing kernel vector for new sample...")
        
        for i in tqdm(range(n_train), desc="   Computing"):
            k_vector[i] = self.kernel_circuit(x_new, X_train[i])
        
        print(f"   ✓ Kernel vector computed: {k_vector.shape}")
        
        return k_vector
    
    def visualize_circuit(self, sample_input):
        """
        Visualize the quantum circuit
        
        Args:
            sample_input (array): Sample input for visualization
        """
        @qml.qnode(self.dev)
        def circuit():
            self.feature_map(sample_input)
            return qml.probs(wires=range(self.n_qubits))
        
        print("\n🔍 Quantum Circuit Visualization:")
        print(qml.draw(circuit)())
        
        return circuit


def create_quantum_kernel(n_qubits, entanglement='linear'):
    """
    Factory function to create quantum kernel
    
    Args:
        n_qubits (int): Number of qubits
        entanglement (str): Entanglement type
        
    Returns:
        QuantumKernel: Initialized quantum kernel
    """
    return QuantumKernel(n_qubits, entanglement)
