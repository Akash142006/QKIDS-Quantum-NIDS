# QKIDS Quick Start Guide

## 🚀 Get Running in 5 Steps

### 1. Setup Environment (One-time)
```bash
conda create -n qkids python=3.10
conda activate qkids
conda install numpy pandas matplotlib seaborn scikit-learn jupyter
pip install pennylane
```

### 2. Download Dataset
- Get NSL-KDD from: https://www.kaggle.com/datasets/hassan06/nslkdd
- Extract `KDDTrain+.txt` and `KDDTest+.txt`
- Place in `QKIDS/data/` folder

### 3. Launch Jupyter
```bash
cd QKIDS
conda activate qkids
jupyter notebook
```

### 4. Run Notebooks in Order
1. **01_preprocessing.ipynb** - Load & prepare data (5 min)
2. **02_train_evaluate.ipynb** - Train models (30 min)
3. **03_interactive_demo.ipynb** - Test predictions (5 min)

### 5. Collect Results
- Figures → `results/figures/`
- Metrics → `results/metrics/`
- Models → `saved_models/`

---

## 📊 What You'll Get

### Key Outputs:
- ✅ Qubit ablation plot (4-8 qubits comparison)
- ✅ Quantum vs classical performance chart
- ✅ Confusion matrices
- ✅ F1-scores, accuracy, precision, recall
- ✅ Trained quantum kernel model
- ✅ Interactive demo

### For Your Paper:
- Performance comparison table
- Optimal qubit count justification
- Kernel visualization
- Classification metrics

---

## ⚙️ Configuration Summary

```python
# Sample Size (adjust for speed)
SAMPLE_SIZE = 1000  # 800 train + 200 test

# Qubit Counts to Test
QUBIT_COUNTS = [4, 5, 6, 7, 8]

# Entanglement
ENTANGLEMENT = 'linear'  # CNOT chain

# Random Seed
RANDOM_SEED = 42

# SVM Hyperparameters (RBF only)
C_VALUES = [0.1, 1, 10]
GAMMA_VALUES = ['scale', 'auto']
```

---

## 🔧 Troubleshooting Quick Fixes

| Problem | Solution |
|---------|----------|
| Too slow | Reduce `SAMPLE_SIZE` to 500 |
| Out of memory | Use fewer qubits: `[4, 5, 6]` |
| Module not found | `pip install <module>` |
| Dataset not found | Update paths in notebook 01 |

---

## 📝 Daily Workflow

```bash
# 1. Open terminal/Anaconda Prompt
conda activate qkids

# 2. Navigate to project
cd path/to/QKIDS

# 3. Launch Jupyter
jupyter notebook

# 4. Run cells with Shift+Enter
```

---

## 🎯 Quick Tips

- **First time?** Follow SETUP_GUIDE.md
- **Need details?** Check README.md
- **Got errors?** See Troubleshooting in README
- **Want faster runs?** Reduce sample size
- **Need better results?** Increase sample size

---

## 📈 Expected Runtime

| Notebook | Time | What it does |
|----------|------|--------------|
| 01 | 5 min | Preprocessing |
| 02 | 30 min | Training & evaluation |
| 03 | 5 min | Interactive demo |

**Total: ~40 minutes**

---

## ✨ Core Concept

```
Network Traffic → Quantum Feature Map → Quantum State
                          ↓
    |⟨ψ(x₁)|ψ(x₂)⟩|² → Kernel Matrix → SVM → Prediction
```

---

**Ready? Start with notebook 01! 🚀**
