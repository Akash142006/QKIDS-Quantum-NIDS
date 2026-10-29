# QKIDS: Quantum Kernel Learning for Network Intrusion Detection

![Python](https://img.shields.io/badge/Python-3.10-blue)
![PennyLane](https://img.shields.io/badge/PennyLane-0.35-green)
![scikit--learn](https://img.shields.io/badge/scikit--learn-1.3-orange)

A research project exploring quantum kernel methods for intrusion detection using the NSL-KDD dataset.

## 🎯 Project Overview

**QKIDS** compares quantum-computed kernels against classical kernels (RBF, linear, polynomial) for binary network intrusion detection. The quantum component uses PennyLane to create quantum feature maps with entanglement, computing similarity between network traffic samples via quantum state overlaps.

### Key Features
- ✅ **Qubit Ablation Study**: Tests 4-8 qubits to find optimal quantum feature space dimension
- ✅ **Quantum Kernel SVM**: Uses precomputed quantum kernels with classical SVM
- ✅ **Classical Baselines**: Linear, RBF (tuned), and Polynomial SVMs
- ✅ **Interactive Demo**: Test individual samples with trained model
- ✅ **Comprehensive Evaluation**: F1-score, accuracy, precision, recall, confusion matrices

### Research Question
*Can quantum kernels capture intrusion patterns better than classical kernels?*

---

## 📁 Project Structure

```
QKIDS/
├── data/                          # Dataset files (you add NSL-KDD here)
│   ├── KDDTrain+.txt             # Training data
│   ├── KDDTest+.txt              # Test data
│   └── preprocessed_*.pkl         # Generated preprocessed data
├── saved_models/                  # Trained models
│   ├── best_quantum_model.pkl
│   └── best_classical_model.pkl
├── results/                       # Experiment results
│   ├── figures/                   # Generated plots
│   └── metrics/                   # Performance metrics
├── notebooks/                     # Jupyter notebooks (run in order)
│   ├── 01_preprocessing.ipynb    # Data loading & preprocessing
│   ├── 02_train_evaluate.ipynb   # Training & evaluation
│   └── 03_interactive_demo.ipynb # Interactive testing
├── src/                           # Source code modules
│   ├── preprocessing.py          # Data preprocessing
│   ├── quantum_kernel.py         # Quantum kernel computation
│   ├── classical_baselines.py    # Classical SVM implementations
│   ├── evaluation.py             # Metrics & visualization
│   └── utils.py                  # Helper functions
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

---

## 🚀 Getting Started

### Prerequisites
- **Python 3.8+** (3.10 recommended)
- **Anaconda** or **Miniconda** (recommended for environment management)

### Step 1: Install Anaconda

If you don't have Anaconda:
1. Download from: https://www.anaconda.com/download
2. Install following the instructions
3. Verify installation:
   ```bash
   conda --version
   ```

### Step 2: Create Environment

Open **Anaconda Prompt** (Windows) or terminal (Mac/Linux):

```bash
# Create environment
conda create -n qkids python=3.10

# Activate environment
conda activate qkids
```

### Step 3: Install Dependencies

```bash
# Install conda packages
conda install numpy pandas matplotlib seaborn scikit-learn jupyter

# Install PennyLane via pip
pip install pennylane

# Or install all at once using requirements.txt
pip install -r requirements.txt
```

### Step 4: Download NSL-KDD Dataset

1. Download from: https://www.kaggle.com/datasets/hassan06/nslkdd
2. Extract and place these files in the `data/` folder:
   - `KDDTrain+.txt`
   - `KDDTest+.txt`

Your `data/` folder should look like:
```
data/
├── KDDTrain+.txt
└── KDDTest+.txt
```

### Step 5: Launch Jupyter Notebook

```bash
# Make sure you're in the QKIDS directory
cd QKIDS

# Launch Jupyter
jupyter notebook
```

This will open Jupyter in your browser.

---

## 📖 How to Run

### Run notebooks in order:

#### **Notebook 1: Preprocessing** (`01_preprocessing.ipynb`)
- Loads NSL-KDD dataset
- Creates binary labels (Normal vs Attack)
- Encodes features and normalizes to [0, π]
- Selects top features for each qubit count (4-8)
- Saves preprocessed data

**⏱️ Estimated Time:** 2-5 minutes

---

#### **Notebook 2: Training & Evaluation** (`02_train_evaluate.ipynb`)
- **Part 1:** Qubit ablation study (tests 4-8 qubits)
- **Part 2:** Trains classical baselines
- **Part 3:** Compares all models
- **Part 4:** Generates confusion matrices and reports
- **Part 5:** Visualizes quantum kernel
- **Part 6:** Saves best models

**⏱️ Estimated Time:** 20-40 minutes (depends on sample size)

**Key Outputs:**
- Qubit ablation plot
- Model comparison chart
- Confusion matrices
- Kernel heatmap
- Trained models

---

#### **Notebook 3: Interactive Demo** (`03_interactive_demo.ipynb`)
- Loads trained quantum model
- Shows available test samples
- **User selects sample number (1-20)**
- Displays prediction with confidence
- Compares with actual label
- Batch testing option

**⏱️ Estimated Time:** 2-5 minutes per sample

**Example Output:**
```
✨ PREDICTION RESULTS
========================================
   Sample ID: 7821
   Predicted Class: ATTACK
   Confidence: 92.7%
   Actual Class: ATTACK
   Status: ✅ CORRECT
========================================
```

---

## 🔧 Configuration

### Experimental Setup (as specified)
- **Dataset**: NSL-KDD
- **Classification**: Binary (Normal vs All Attacks)
- **Data Split**: Stratified 80/20 train/test
- **Sample Size**: 800-1,500 total (computational constraints)
- **Cross-validation**: Not used (computational constraints)
- **SVM Tuning**: C ∈ {0.1, 1, 10}, gamma ∈ {scale, auto} (RBF only)
- **Quantum Kernel Tuning**: None (fixed feature map)
- **Entanglement**: Linear CNOT chain (qubit i → i+1)
- **Reproducibility**: Fixed random seed (42)

### Customization

You can modify these in the notebooks:

**Sample Size** (affects computation time):
```python
SAMPLE_SIZE = 1000  # Increase/decrease as needed
```

**Qubit Range**:
```python
QUBIT_COUNTS = [4, 5, 6, 7, 8]  # Add/remove qubit counts
```

**Entanglement Type** (in `quantum_kernel.py`):
- `'linear'`: CNOT chain (default)
- `'full'`: All-to-all entanglement
- `'none'`: No entanglement

---

## 📊 Expected Results

### Outputs Generated

1. **Figures** (`results/figures/`):
   - `qubit_ablation.png` - Performance vs qubit count
   - `model_comparison.png` - Quantum vs classical comparison
   - `quantum_confusion_matrix.png` - Quantum model confusion matrix
   - `rbf_confusion_matrix.png` - RBF baseline confusion matrix
   - `quantum_kernel_heatmap.png` - Kernel matrix visualization

2. **Metrics** (`results/metrics/`):
   - `model_comparison.csv` - All model metrics
   - `experiment_summary.pkl` - Full experimental results

3. **Models** (`saved_models/`):
   - `best_quantum_model.pkl` - Optimal quantum kernel SVM
   - `best_classical_model.pkl` - Best classical baseline

---

## 🎓 For Your Research Paper

### Key Sections to Include

**1. Methods Section:**
- Quantum feature map architecture (RY rotations + linear CNOT)
- Kernel computation: K[i,j] = |⟨ψ(xi)|ψ(xj)⟩|²
- Feature selection using mutual information
- Hyperparameter settings (from this README)

**2. Results Section:**
- Table 1: Performance vs qubit count (from qubit ablation)
- Table 2: Quantum vs classical comparison
- Figure 1: Qubit ablation plot
- Figure 2: Model comparison chart
- Confusion matrices

**3. Discussion:**
- Optimal qubit count justification
- Quantum vs classical trade-offs
- Computational complexity analysis
- Feature space interpretation

---

## 🐛 Troubleshooting

### Common Issues

**Issue 1: "ModuleNotFoundError: No module named 'pennylane'"**
```bash
# Solution: Install PennyLane
conda activate qkids
pip install pennylane
```

**Issue 2: "FileNotFoundError: KDDTrain+.txt not found"**
- Make sure dataset files are in `data/` folder
- Update paths in notebook 01 if needed

**Issue 3: Kernel computation too slow**
- Reduce `SAMPLE_SIZE` in notebook 01
- Use fewer qubits (e.g., only test 4, 5, 6)

**Issue 4: Out of memory**
- Decrease sample size
- Close other applications
- Use fewer qubit counts

---

## 📚 Dependencies

- **PennyLane**: Quantum computing framework
- **scikit-learn**: Machine learning library
- **pandas**: Data manipulation
- **numpy**: Numerical computing
- **matplotlib/seaborn**: Visualization
- **jupyter**: Interactive notebooks
- **joblib**: Model serialization

---

## 🔬 Technical Details

### Quantum Feature Map

```python
def feature_map(x):
    # Rotation layer
    for i in range(n_qubits):
        RY(x[i], qubit=i)
    
    # Entanglement layer (linear CNOT chain)
    for i in range(n_qubits - 1):
        CNOT(control=i, target=i+1)
```

### Kernel Computation

```
K[i,j] = |⟨ψ(xi)|ψ(xj)⟩|²
       = P(|00...0⟩ | circuit with xi† xj)
```

---

## 📝 Citation

If you use this code for your research, please cite:

```bibtex
@misc{qkids2025,
  title={QKIDS: Quantum Kernel Learning for Network Intrusion Detection},
  author={Your Name},
  year={2025},
  note={GitHub repository}
}
```

---

## 📞 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review notebook comments and docstrings
3. Verify all installation steps completed

---

## ✨ Features Highlight

- 🔮 **Quantum Kernel**: PennyLane-based quantum kernel computation
- 📊 **Ablation Study**: Empirical qubit count selection
- 🎯 **Interactive Demo**: User-friendly prediction interface
- 📈 **Visualization**: Comprehensive plots and metrics
- 💾 **Reproducible**: Fixed random seeds, saved models
- 📚 **Well-documented**: Extensive comments and README

---

## 🏁 Quick Start Checklist

- [ ] Install Anaconda
- [ ] Create `qkids` environment
- [ ] Install dependencies
- [ ] Download NSL-KDD dataset
- [ ] Place dataset in `data/` folder
- [ ] Run notebook 01 (preprocessing)
- [ ] Run notebook 02 (training)
- [ ] Run notebook 03 (demo)
- [ ] Collect results for paper

---

**Good luck with your research! 🚀**

For questions about quantum machine learning or the methodology, refer to:
- Havlíček et al., "Supervised learning with quantum-enhanced feature spaces" (2019)
- Schuld & Killoran, "Quantum Machine Learning in Feature Hilbert Spaces" (2019)
