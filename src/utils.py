"""
QKIDS: Utility Functions
Helper functions for the project
"""

import numpy as np
import random
import os

def set_seed(seed=42):
    """
    Set random seed for reproducibility
    
    Args:
        seed (int): Random seed value
    """
    np.random.seed(seed)
    random.seed(seed)
    print(f"✅ Random seed set to {seed}")

def create_directories():
    """
    Create necessary directories if they don't exist
    """
    directories = [
        'data',
        'saved_models',
        'results/figures',
        'results/metrics'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    
    print("✅ All directories created/verified")

def print_section(title):
    """
    Print a formatted section header
    
    Args:
        title (str): Section title
    """
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60 + "\n")

def print_subsection(title):
    """
    Print a formatted subsection header
    
    Args:
        title (str): Subsection title
    """
    print(f"\n{'─'*60}")
    print(f"  {title}")
    print('─'*60)
