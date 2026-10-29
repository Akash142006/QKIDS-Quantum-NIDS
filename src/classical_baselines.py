"""
QKIDS: Classical Baselines Module
Implements classical SVM baselines with different kernels
"""

from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV
import numpy as np
import time

class ClassicalSVMBaseline:
    """
    Classical SVM with various kernels
    """
    
    def __init__(self, kernel='rbf', tune_hyperparameters=True, random_state=42):
        """
        Initialize classical SVM
        
        Args:
            kernel (str): Kernel type ('linear', 'rbf', 'poly')
            tune_hyperparameters (bool): Whether to tune C and gamma
            random_state (int): Random seed
        """
        self.kernel = kernel
        self.tune_hyperparameters = tune_hyperparameters
        self.random_state = random_state
        self.model = None
        self.best_params = None
        
        print(f"🔧 Classical SVM initialized:")
        print(f"   Kernel: {kernel}")
        print(f"   Hyperparameter tuning: {tune_hyperparameters}")
    
    def train(self, X_train, y_train):
        """
        Train SVM classifier
        
        Args:
            X_train (array): Training features
            y_train (array): Training labels
            
        Returns:
            dict: Training metrics (time, etc.)
        """
        print(f"\n🎯 Training {self.kernel.upper()} SVM...")
        
        start_time = time.time()
        
        if self.tune_hyperparameters and self.kernel in ['rbf', 'poly']:
            # Hyperparameter tuning
            print("   Tuning hyperparameters...")
            
            if self.kernel == 'rbf':
                param_grid = {
                    'C': [0.1, 1, 10],
                    'gamma': ['scale', 'auto']
                }
            else:  # polynomial
                param_grid = {
                    'C': [0.1, 1, 10],
                    'degree': [2, 3, 4]
                }
            
            grid_search = GridSearchCV(
                SVC(kernel=self.kernel, random_state=self.random_state),
                param_grid,
                cv=3,
                scoring='f1',
                n_jobs=-1
            )
            
            grid_search.fit(X_train, y_train)
            
            self.model = grid_search.best_estimator_
            self.best_params = grid_search.best_params_
            
            print(f"   ✓ Best parameters: {self.best_params}")
        
        else:
            # No tuning or linear kernel
            self.model = SVC(kernel=self.kernel, random_state=self.random_state)
            self.model.fit(X_train, y_train)
            self.best_params = {'C': 1.0}
        
        training_time = time.time() - start_time
        
        print(f"   ✓ Training complete in {training_time:.2f}s")
        
        return {
            'training_time': training_time,
            'best_params': self.best_params
        }
    
    def predict(self, X_test):
        """
        Make predictions
        
        Args:
            X_test (array): Test features
            
        Returns:
            array: Predictions
        """
        if self.model is None:
            raise ValueError("Model not trained yet!")
        
        return self.model.predict(X_test)
    
    def predict_proba(self, X_test):
        """
        Get prediction probabilities (requires probability=True in SVC)
        
        Args:
            X_test (array): Test features
            
        Returns:
            array: Prediction probabilities
        """
        if self.model is None:
            raise ValueError("Model not trained yet!")
        
        # Retrain with probability enabled if not already
        if not hasattr(self.model, 'predict_proba'):
            print("   ⚠️  Retraining with probability estimates enabled...")
            self.model.probability = True
            self.model.fit(self.model.support_vectors_, self.model.dual_coef_[0])
        
        return self.model.predict_proba(X_test)


class QuantumSVM:
    """
    SVM with precomputed quantum kernel
    """
    
    def __init__(self, random_state=42):
        """
        Initialize Quantum SVM
        
        Args:
            random_state (int): Random seed
        """
        self.random_state = random_state
        self.model = None
        self.K_train = None
        self.X_train = None
        
        print(f"🔮 Quantum Kernel SVM initialized")
    
    def train(self, K_train, y_train, X_train=None):
        """
        Train SVM with precomputed kernel
        
        Args:
            K_train (array): Precomputed kernel matrix (n_train, n_train)
            y_train (array): Training labels
            X_train (array): Training features (for later prediction)
            
        Returns:
            dict: Training metrics
        """
        print(f"\n🎯 Training Quantum Kernel SVM...")
        
        start_time = time.time()
        
        # Store training data for prediction
        self.K_train = K_train
        self.X_train = X_train
        
        # Train SVM with precomputed kernel
        self.model = SVC(kernel='precomputed', random_state=self.random_state)
        self.model.fit(K_train, y_train)
        
        training_time = time.time() - start_time
        
        print(f"   ✓ Training complete in {training_time:.2f}s")
        print(f"   ✓ Support vectors: {len(self.model.support_)}")
        
        return {
            'training_time': training_time,
            'n_support_vectors': len(self.model.support_)
        }
    
    def predict(self, K_test):
        """
        Make predictions with precomputed kernel
        
        Args:
            K_test (array): Kernel matrix between test and train (n_test, n_train)
            
        Returns:
            array: Predictions
        """
        if self.model is None:
            raise ValueError("Model not trained yet!")
        
        return self.model.predict(K_test)
    
    def decision_function(self, K_test):
        """
        Get decision function values (distance from hyperplane)
        
        Args:
            K_test (array): Kernel matrix between test and train
            
        Returns:
            array: Decision function values
        """
        if self.model is None:
            raise ValueError("Model not trained yet!")
        
        return self.model.decision_function(K_test)


def create_classical_baseline(kernel='rbf', tune=True, random_state=42):
    """
    Factory function for classical SVM
    
    Args:
        kernel (str): Kernel type
        tune (bool): Whether to tune hyperparameters
        random_state (int): Random seed
        
    Returns:
        ClassicalSVMBaseline: Initialized SVM
    """
    return ClassicalSVMBaseline(kernel, tune, random_state)


def create_quantum_svm(random_state=42):
    """
    Factory function for quantum kernel SVM
    
    Args:
        random_state (int): Random seed
        
    Returns:
        QuantumSVM: Initialized quantum SVM
    """
    return QuantumSVM(random_state)
