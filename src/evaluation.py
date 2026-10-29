"""
QKIDS: Evaluation Module
Performance metrics and visualization functions
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report
)
import os

# Set style
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (10, 6)

def evaluate_model(y_true, y_pred, model_name):
    """
    Evaluate model performance
    
    Args:
        y_true (array): True labels
        y_pred (array): Predicted labels
        model_name (str): Name of the model
        
    Returns:
        dict: Metrics dictionary
    """
    print(f"\n📊 Evaluating {model_name}...")
    
    # Calculate metrics
    accuracy = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred)
    recall = recall_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred)
    
    metrics = {
        'model': model_name,
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1_score': f1
    }
    
    print(f"   Accuracy:  {accuracy:.4f}")
    print(f"   Precision: {precision:.4f}")
    print(f"   Recall:    {recall:.4f}")
    print(f"   F1-Score:  {f1:.4f}")
    
    return metrics


def print_classification_report(y_true, y_pred, model_name):
    """
    Print detailed classification report
    
    Args:
        y_true (array): True labels
        y_pred (array): Predicted labels
        model_name (str): Model name
    """
    print(f"\n📋 Classification Report - {model_name}")
    print("="*60)
    print(classification_report(y_true, y_pred, target_names=['Normal', 'Attack']))


def plot_confusion_matrix(y_true, y_pred, model_name, save_path=None):
    """
    Plot confusion matrix
    
    Args:
        y_true (array): True labels
        y_pred (array): Predicted labels
        model_name (str): Model name
        save_path (str): Path to save figure (optional)
    """
    cm = confusion_matrix(y_true, y_pred)
    
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=['Normal', 'Attack'],
                yticklabels=['Normal', 'Attack'])
    plt.title(f'Confusion Matrix - {model_name}')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"   💾 Confusion matrix saved to {save_path}")
    
    plt.show()


def compare_models(results_list):
    """
    Compare multiple models
    
    Args:
        results_list (list): List of metric dictionaries
        
    Returns:
        DataFrame: Comparison table
    """
    df = pd.DataFrame(results_list)
    
    print("\n📊 Model Comparison")
    print("="*80)
    print(df.to_string(index=False))
    
    return df


def plot_model_comparison(results_df, save_path=None):
    """
    Plot model comparison bar chart
    
    Args:
        results_df (DataFrame): Results dataframe
        save_path (str): Path to save figure
    """
    metrics = ['accuracy', 'precision', 'recall', 'f1_score']
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    axes = axes.flatten()
    
    for idx, metric in enumerate(metrics):
        ax = axes[idx]
        
        data = results_df.sort_values(metric, ascending=False)
        
        bars = ax.barh(data['model'], data[metric])
        
        # Color code: quantum in blue, classical in orange/green/red
        colors = ['#1f77b4' if 'Quantum' in model else '#ff7f0e' 
                  for model in data['model']]
        for bar, color in zip(bars, colors):
            bar.set_color(color)
        
        ax.set_xlabel(metric.replace('_', ' ').title())
        ax.set_xlim([0, 1.0])
        ax.grid(axis='x', alpha=0.3)
        
        # Add value labels
        for i, v in enumerate(data[metric]):
            ax.text(v + 0.01, i, f'{v:.3f}', va='center')
    
    plt.suptitle('Model Performance Comparison', fontsize=16, fontweight='bold')
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"   💾 Comparison plot saved to {save_path}")
    
    plt.show()


def plot_qubit_ablation(qubit_results, save_path=None):
    """
    Plot performance vs number of qubits
    
    Args:
        qubit_results (list): List of dicts with 'n_qubits' and metrics
        save_path (str): Path to save figure
    """
    df = pd.DataFrame(qubit_results)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Plot F1-score vs qubits
    ax.plot(df['n_qubits'], df['f1_score'], marker='o', linewidth=2, 
            markersize=10, color='#1f77b4', label='F1-Score')
    ax.plot(df['n_qubits'], df['accuracy'], marker='s', linewidth=2, 
            markersize=8, color='#ff7f0e', label='Accuracy', alpha=0.7)
    
    # Highlight best performing qubit count
    best_idx = df['f1_score'].idxmax()
    best_qubits = df.loc[best_idx, 'n_qubits']
    best_f1 = df.loc[best_idx, 'f1_score']
    
    ax.scatter([best_qubits], [best_f1], s=200, c='red', marker='*', 
               zorder=5, label=f'Best: {best_qubits} qubits')
    
    ax.set_xlabel('Number of Qubits', fontsize=12)
    ax.set_ylabel('Score', fontsize=12)
    ax.set_title('Quantum Kernel Performance vs Qubit Count', fontsize=14, fontweight='bold')
    ax.legend()
    ax.grid(alpha=0.3)
    ax.set_xticks(df['n_qubits'])
    ax.set_ylim([0.5, 1.0])
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"   💾 Qubit ablation plot saved to {save_path}")
    
    plt.show()
    
    return best_qubits, best_f1


def plot_kernel_heatmap(kernel_matrix, title, save_path=None):
    """
    Visualize kernel matrix as heatmap
    
    Args:
        kernel_matrix (array): Kernel matrix
        title (str): Plot title
        save_path (str): Path to save figure
    """
    plt.figure(figsize=(10, 8))
    
    # Subsample if too large
    if kernel_matrix.shape[0] > 100:
        indices = np.random.choice(kernel_matrix.shape[0], 100, replace=False)
        kernel_matrix = kernel_matrix[np.ix_(indices, indices)]
        title += " (100 samples shown)"
    
    sns.heatmap(kernel_matrix, cmap='viridis', cbar_kws={'label': 'Kernel Value'})
    plt.title(title, fontsize=14, fontweight='bold')
    plt.xlabel('Sample Index')
    plt.ylabel('Sample Index')
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"   💾 Kernel heatmap saved to {save_path}")
    
    plt.show()


def save_results_to_csv(results_df, filename):
    """
    Save results to CSV file
    
    Args:
        results_df (DataFrame): Results dataframe
        filename (str): Output filename
    """
    filepath = os.path.join('results', 'metrics', filename)
    results_df.to_csv(filepath, index=False)
    print(f"\n💾 Results saved to {filepath}")


def create_results_summary(qubit_results, comparison_results, best_qubits):
    """
    Create comprehensive results summary
    
    Args:
        qubit_results (list): Qubit ablation results
        comparison_results (DataFrame): Model comparison results
        best_qubits (int): Optimal number of qubits
        
    Returns:
        dict: Summary dictionary
    """
    summary = {
        'best_qubits': best_qubits,
        'best_quantum_f1': comparison_results[comparison_results['model'].str.contains('Quantum')]['f1_score'].max(),
        'best_classical_f1': comparison_results[~comparison_results['model'].str.contains('Quantum')]['f1_score'].max(),
        'qubit_ablation': qubit_results,
        'full_comparison': comparison_results.to_dict('records')
    }
    
    print("\n" + "="*60)
    print("  RESULTS SUMMARY")
    print("="*60)
    print(f"\n✨ Best Qubit Count: {best_qubits}")
    print(f"✨ Best Quantum F1-Score: {summary['best_quantum_f1']:.4f}")
    print(f"✨ Best Classical F1-Score: {summary['best_classical_f1']:.4f}")
    
    if summary['best_quantum_f1'] > summary['best_classical_f1']:
        print(f"\n🎯 Quantum kernel OUTPERFORMS classical kernels!")
        improvement = (summary['best_quantum_f1'] - summary['best_classical_f1']) / summary['best_classical_f1'] * 100
        print(f"   Improvement: {improvement:.2f}%")
    else:
        print(f"\n📊 Classical kernels perform better in this setup")
    
    return summary
