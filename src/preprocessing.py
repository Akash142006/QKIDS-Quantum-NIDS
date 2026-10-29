"""
QKIDS: Data Preprocessing Module
Handles NSL-KDD dataset loading, cleaning, encoding, and feature selection
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.feature_selection import mutual_info_classif
from sklearn.model_selection import train_test_split
import pickle
import os

# NSL-KDD column names
COLUMN_NAMES = [
    'duration', 'protocol_type', 'service', 'flag', 'src_bytes', 'dst_bytes',
    'land', 'wrong_fragment', 'urgent', 'hot', 'num_failed_logins', 'logged_in',
    'num_compromised', 'root_shell', 'su_attempted', 'num_root', 'num_file_creations',
    'num_shells', 'num_access_files', 'num_outbound_cmds', 'is_host_login',
    'is_guest_login', 'count', 'srv_count', 'serror_rate', 'srv_serror_rate',
    'rerror_rate', 'srv_rerror_rate', 'same_srv_rate', 'diff_srv_rate',
    'srv_diff_host_rate', 'dst_host_count', 'dst_host_srv_count',
    'dst_host_same_srv_rate', 'dst_host_diff_srv_rate', 'dst_host_same_src_port_rate',
    'dst_host_srv_diff_host_rate', 'dst_host_serror_rate', 'dst_host_srv_serror_rate',
    'dst_host_rerror_rate', 'dst_host_srv_rerror_rate', 'label', 'difficulty'
]

class NSLKDDPreprocessor:
    """
    Preprocessor for NSL-KDD dataset
    """
    
    def __init__(self, train_path, test_path, sample_size=1000, random_state=42):
        """
        Initialize preprocessor
        
        Args:
            train_path (str): Path to KDDTrain+.txt
            test_path (str): Path to KDDTest+.txt
            sample_size (int): Number of samples to use (for computational efficiency)
            random_state (int): Random seed
        """
        self.train_path = train_path
        self.test_path = test_path
        self.sample_size = sample_size
        self.random_state = random_state
        
        self.label_encoders = {}
        self.scaler = MinMaxScaler(feature_range=(0, np.pi))
        self.feature_importances = {}
        
    def load_data(self):
        """
        Load NSL-KDD train and test datasets
        
        Returns:
            tuple: (train_df, test_df)
        """
        print("📂 Loading NSL-KDD dataset...")
        
        # Load training data
        train_df = pd.read_csv(self.train_path, header=None, names=COLUMN_NAMES)
        
        # Load test data
        test_df = pd.read_csv(self.test_path, header=None, names=COLUMN_NAMES)
        
        # Remove difficulty column
        train_df = train_df.drop('difficulty', axis=1)
        test_df = test_df.drop('difficulty', axis=1)
        
        print(f"   Training samples: {len(train_df)}")
        print(f"   Testing samples: {len(test_df)}")
        print(f"   Features: {len(train_df.columns) - 1}")
        
        return train_df, test_df
    
    def create_binary_labels(self, train_df, test_df):
        """
        Convert multi-class labels to binary (Normal vs Attack)
        
        Args:
            train_df (DataFrame): Training data
            test_df (DataFrame): Testing data
            
        Returns:
            tuple: (train_df, test_df) with binary labels
        """
        print("\n🔄 Creating binary labels (Normal vs Attack)...")
        
        # Map all attack types to 'attack'
        train_df['label'] = train_df['label'].apply(lambda x: 'normal' if x == 'normal' else 'attack')
        test_df['label'] = test_df['label'].apply(lambda x: 'normal' if x == 'normal' else 'attack')
        
        print(f"   Normal samples (train): {(train_df['label'] == 'normal').sum()}")
        print(f"   Attack samples (train): {(train_df['label'] == 'attack').sum()}")
        print(f"   Normal samples (test): {(test_df['label'] == 'normal').sum()}")
        print(f"   Attack samples (test): {(test_df['label'] == 'attack').sum()}")
        
        return train_df, test_df
    
    def encode_categorical_features(self, train_df, test_df):
        """
        Encode categorical features using LabelEncoder
        
        Args:
            train_df (DataFrame): Training data
            test_df (DataFrame): Testing data
            
        Returns:
            tuple: (train_df, test_df) with encoded features
        """
        print("\n🔢 Encoding categorical features...")
        
        categorical_columns = ['protocol_type', 'service', 'flag']
        
        for col in categorical_columns:
            le = LabelEncoder()
            
            # Fit on combined data to handle unseen categories
            combined = pd.concat([train_df[col], test_df[col]])
            le.fit(combined)
            
            train_df[col] = le.transform(train_df[col])
            test_df[col] = le.transform(test_df[col])
            
            self.label_encoders[col] = le
            print(f"   ✓ Encoded {col}")
        
        return train_df, test_df
    
    def encode_labels(self, train_df, test_df):
        """
        Encode target labels to 0 (normal) and 1 (attack)
        
        Args:
            train_df (DataFrame): Training data
            test_df (DataFrame): Testing data
            
        Returns:
            tuple: (train_df, test_df) with encoded labels
        """
        print("\n🎯 Encoding target labels...")
        
        le = LabelEncoder()
        le.fit(['normal', 'attack'])
        
        train_df['label'] = le.transform(train_df['label'])
        test_df['label'] = le.transform(test_df['label'])
        
        self.label_encoders['label'] = le
        
        print(f"   normal → 0")
        print(f"   attack → 1")
        
        return train_df, test_df
    
    def sample_data(self, train_df, test_df):
        """
        Sample data for computational efficiency with stratification
        
        Args:
            train_df (DataFrame): Training data
            test_df (DataFrame): Testing data
            
        Returns:
            tuple: (train_df_sampled, test_df_sampled)
        """
        print(f"\n📊 Sampling {self.sample_size} total samples (stratified 80/20 split)...")
        
        # Calculate train and test sizes
        train_size = int(self.sample_size * 0.8)
        test_size = self.sample_size - train_size
        
        # Sample training data (stratified)
        train_df_sampled = train_df.groupby('label', group_keys=False).apply(
            lambda x: x.sample(n=min(len(x), train_size // 2), random_state=self.random_state)
        )
        
        # Sample test data (stratified)
        test_df_sampled = test_df.groupby('label', group_keys=False).apply(
            lambda x: x.sample(n=min(len(x), test_size // 2), random_state=self.random_state)
        )
        
        print(f"   Training samples: {len(train_df_sampled)}")
        print(f"   Testing samples: {len(test_df_sampled)}")
        print(f"   Train Normal/Attack: {(train_df_sampled['label']==0).sum()}/{(train_df_sampled['label']==1).sum()}")
        print(f"   Test Normal/Attack: {(test_df_sampled['label']==0).sum()}/{(test_df_sampled['label']==1).sum()}")
        
        return train_df_sampled, test_df_sampled
    
    def select_features(self, train_df, n_features):
        """
        Select top n features using mutual information
        
        Args:
            train_df (DataFrame): Training data
            n_features (int): Number of features to select
            
        Returns:
            list: Selected feature names
        """
        print(f"\n🔍 Selecting top {n_features} features using Mutual Information...")
        
        X = train_df.drop('label', axis=1)
        y = train_df['label']
        
        # Calculate mutual information
        mi_scores = mutual_info_classif(X, y, random_state=self.random_state)
        
        # Get feature names and scores
        feature_scores = pd.DataFrame({
            'feature': X.columns,
            'score': mi_scores
        }).sort_values('score', ascending=False)
        
        # Select top n features
        selected_features = feature_scores.head(n_features)['feature'].tolist()
        
        self.feature_importances[n_features] = feature_scores
        
        print(f"   Top {n_features} features selected:")
        for i, (feat, score) in enumerate(zip(selected_features[:5], feature_scores['score'][:5]), 1):
            print(f"      {i}. {feat}: {score:.4f}")
        if n_features > 5:
            print(f"      ... and {n_features - 5} more")
        
        return selected_features
    
    def normalize_features(self, train_df, test_df, selected_features):
        """
        Normalize features to [0, π] range for quantum encoding
        
        Args:
            train_df (DataFrame): Training data
            test_df (DataFrame): Testing data
            selected_features (list): Features to normalize
            
        Returns:
            tuple: (X_train, X_test, y_train, y_test)
        """
        print(f"\n📏 Normalizing features to [0, π] range...")
        
        X_train = train_df[selected_features].values
        X_test = test_df[selected_features].values
        y_train = train_df['label'].values
        y_test = test_df['label'].values
        
        # Fit scaler on training data
        self.scaler.fit(X_train)
        
        # Transform both train and test
        X_train_normalized = self.scaler.transform(X_train)
        X_test_normalized = self.scaler.transform(X_test)
        
        print(f"   ✓ Features normalized to range [0, {np.pi:.4f}]")
        
        return X_train_normalized, X_test_normalized, y_train, y_test
    
    def preprocess_for_qubit_count(self, n_qubits):
        """
        Complete preprocessing pipeline for a specific qubit count
        
        Args:
            n_qubits (int): Number of qubits (features to select)
            
        Returns:
            dict: Preprocessed data dictionary
        """
        print(f"\n{'='*60}")
        print(f"  PREPROCESSING FOR {n_qubits} QUBITS")
        print(f"{'='*60}")
        
        # Load data
        train_df, test_df = self.load_data()
        
        # Create binary labels
        train_df, test_df = self.create_binary_labels(train_df, test_df)
        
        # Encode categorical features
        train_df, test_df = self.encode_categorical_features(train_df, test_df)
        
        # Encode labels
        train_df, test_df = self.encode_labels(train_df, test_df)
        
        # Sample data
        train_df, test_df = self.sample_data(train_df, test_df)
        
        # Select features
        selected_features = self.select_features(train_df, n_qubits)
        
        # Normalize features
        X_train, X_test, y_train, y_test = self.normalize_features(
            train_df, test_df, selected_features
        )
        
        print(f"\n✅ Preprocessing complete for {n_qubits} qubits!")
        print(f"   X_train shape: {X_train.shape}")
        print(f"   X_test shape: {X_test.shape}")
        
        return {
            'X_train': X_train,
            'X_test': X_test,
            'y_train': y_train,
            'y_test': y_test,
            'selected_features': selected_features,
            'n_qubits': n_qubits
        }
    
    def save_preprocessed_data(self, data_dict, filename):
        """
        Save preprocessed data to file
        
        Args:
            data_dict (dict): Preprocessed data
            filename (str): Output filename
        """
        filepath = os.path.join('data', filename)
        with open(filepath, 'wb') as f:
            pickle.dump(data_dict, f)
        print(f"\n💾 Preprocessed data saved to {filepath}")
    
    def load_preprocessed_data(self, filename):
        """
        Load preprocessed data from file
        
        Args:
            filename (str): Input filename
            
        Returns:
            dict: Preprocessed data
        """
        filepath = os.path.join('data', filename)
        with open(filepath, 'rb') as f:
            data_dict = pickle.load(f)
        print(f"\n📂 Loaded preprocessed data from {filepath}")
        return data_dict
