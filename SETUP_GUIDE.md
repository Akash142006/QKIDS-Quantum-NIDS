# QKIDS Setup Guide
## Complete Installation Instructions

This guide will walk you through setting up QKIDS from scratch, even if you're new to Python and Jupyter notebooks.

---

## 📋 Prerequisites

Before starting, make sure you have:
- Windows, Mac, or Linux computer
- Internet connection
- At least 2GB free disk space

---

## 🛠️ Step-by-Step Setup

### Step 1: Install Anaconda

#### Windows:
1. Go to: https://www.anaconda.com/download
2. Click "Download" for Windows
3. Run the installer (Anaconda3-xxx-Windows-x86_64.exe)
4. Follow installation wizard:
   - Click "Next"
   - Accept license terms
   - Choose "Just Me" (recommended)
   - Use default installation path
   - **IMPORTANT**: Check "Add Anaconda to my PATH" (ignore warning)
   - Click "Install"
5. Wait for installation (5-10 minutes)
6. Click "Finish"

#### Mac:
1. Go to: https://www.anaconda.com/download
2. Click "Download" for macOS
3. Open the downloaded .pkg file
4. Follow installation wizard
5. Open Terminal and verify:
   ```bash
   conda --version
   ```

#### Linux:
1. Download installer:
   ```bash
   wget https://repo.anaconda.com/archive/Anaconda3-2023.09-0-Linux-x86_64.sh
   ```
2. Install:
   ```bash
   bash Anaconda3-2023.09-0-Linux-x86_64.sh
   ```
3. Follow prompts and accept defaults
4. Restart terminal

---

### Step 2: Verify Anaconda Installation

Open **Anaconda Prompt** (Windows) or **Terminal** (Mac/Linux):

**Windows:**
- Search for "Anaconda Prompt" in Start Menu
- Click to open

**Mac/Linux:**
- Open Terminal application

Then run:
```bash
conda --version
```

You should see something like: `conda 23.x.x`

If you get an error, restart your computer and try again.

---

### Step 3: Create Python Environment

In Anaconda Prompt/Terminal, run these commands one by one:

```bash
# Create a new environment called 'qkids' with Python 3.10
conda create -n qkids python=3.10

# Press 'y' and Enter when asked to proceed
```

Wait for the environment to be created (2-3 minutes).

---

### Step 4: Activate Environment

```bash
conda activate qkids
```

Your prompt should now show `(qkids)` at the beginning, like:
```
(qkids) C:\Users\YourName>
```

**IMPORTANT**: You need to activate this environment **every time** you open a new Anaconda Prompt/Terminal!

---

### Step 5: Install Required Packages

With the environment activated, run:

```bash
# Install basic scientific computing packages
conda install numpy pandas matplotlib seaborn scikit-learn jupyter

# Press 'y' and Enter when asked
```

Wait for installation (5-10 minutes).

Then install PennyLane:
```bash
pip install pennylane
```

---

### Step 6: Verify Installation

Check if everything is installed correctly:

```bash
python -c "import pennylane; import sklearn; import pandas; print('✅ All packages installed successfully!')"
```

If you see the success message, you're good to go!

---

### Step 7: Download NSL-KDD Dataset

1. Go to: https://www.kaggle.com/datasets/hassan06/nslkdd
2. If you don't have a Kaggle account:
   - Click "Register" and create a free account
   - Verify your email
3. Click "Download" button
4. Extract the downloaded ZIP file
5. You'll see many files - you only need:
   - `KDDTrain+.txt`
   - `KDDTest+.txt`

---

### Step 8: Set Up Project Folder

1. Create a folder called `QKIDS` on your Desktop or Documents
2. Copy all the project files into this folder:
   ```
   QKIDS/
   ├── data/
   ├── notebooks/
   ├── src/
   ├── requirements.txt
   └── README.md
   ```
3. Copy `KDDTrain+.txt` and `KDDTest+.txt` into the `data/` folder

Your `data/` folder should now contain:
```
data/
├── KDDTrain+.txt
└── KDDTest+.txt
```

---

### Step 9: Launch Jupyter Notebook

1. Open Anaconda Prompt/Terminal
2. Activate environment:
   ```bash
   conda activate qkids
   ```
3. Navigate to QKIDS folder:
   ```bash
   # Windows example:
   cd C:\Users\YourName\Desktop\QKIDS
   
   # Mac/Linux example:
   cd ~/Desktop/QKIDS
   ```
4. Launch Jupyter:
   ```bash
   jupyter notebook
   ```

This will open Jupyter in your web browser automatically!

---

### Step 10: Update Dataset Paths

1. In Jupyter, open `notebooks/01_preprocessing.ipynb`
2. Find the cell with:
   ```python
   TRAIN_PATH = '../data/KDDTrain+.txt'
   TEST_PATH = '../data/KDDTest+.txt'
   ```
3. Make sure these paths match where you placed your data files
4. If your data is elsewhere, update these paths

---

## ▶️ Running the Notebooks

### Start with Notebook 01:

1. Click on `01_preprocessing.ipynb` in Jupyter
2. Click on the first cell
3. Press **Shift + Enter** to run the cell
4. Continue pressing **Shift + Enter** for each cell
5. Wait for each cell to finish (you'll see `[*]` while running, then `[1]`, `[2]`, etc. when done)

### Then Notebook 02:

1. Open `02_train_evaluate.ipynb`
2. Run cells one by one with **Shift + Enter**
3. This will take 20-40 minutes depending on your computer

### Finally Notebook 03:

1. Open `03_interactive_demo.ipynb`
2. Run cells and interact with the demo!

---

## 🔄 Daily Workflow

Every time you want to work on QKIDS:

1. Open Anaconda Prompt/Terminal
2. Activate environment:
   ```bash
   conda activate qkids
   ```
3. Navigate to QKIDS folder:
   ```bash
   cd path/to/QKIDS
   ```
4. Launch Jupyter:
   ```bash
   jupyter notebook
   ```

---

## 🐛 Common Issues & Solutions

### Issue 1: "conda: command not found"

**Solution (Windows):**
1. Restart computer
2. Search for "Anaconda Prompt" and use that instead of regular Command Prompt

**Solution (Mac/Linux):**
```bash
export PATH="$HOME/anaconda3/bin:$PATH"
source ~/.bashrc
```

---

### Issue 2: "No module named 'pennylane'"

**Solution:**
```bash
conda activate qkids
pip install pennylane
```

---

### Issue 3: Jupyter doesn't open in browser

**Solution:**
1. Copy the URL from terminal (looks like: `http://localhost:8888/?token=...`)
2. Paste it manually in your browser

---

### Issue 4: "FileNotFoundError: KDDTrain+.txt"

**Solution:**
- Check that files are in the correct folder
- Update paths in notebook 01:
  ```python
  TRAIN_PATH = 'C:/full/path/to/KDDTrain+.txt'
  TEST_PATH = 'C:/full/path/to/KDDTest+.txt'
  ```

---

### Issue 5: Code runs very slowly

**Solution:**
In notebook 01, reduce sample size:
```python
SAMPLE_SIZE = 500  # Instead of 1000
```

---

### Issue 6: Out of memory error

**Solutions:**
1. Close other applications
2. Reduce sample size to 500
3. Test fewer qubit counts:
   ```python
   QUBIT_COUNTS = [4, 5, 6]  # Instead of [4,5,6,7,8]
   ```

---

## 📞 Getting Help

If you encounter other issues:

1. **Read error messages carefully** - they often tell you what's wrong
2. **Check the Troubleshooting section** in main README
3. **Verify all steps** in this guide were completed
4. **Google the error message** - many common issues have solutions online

---

## ✅ Installation Checklist

Use this to verify your setup:

- [ ] Anaconda installed
- [ ] `conda --version` works
- [ ] Created `qkids` environment
- [ ] Activated environment (see `(qkids)` in prompt)
- [ ] Installed packages (numpy, pandas, sklearn, etc.)
- [ ] Installed PennyLane
- [ ] Downloaded NSL-KDD dataset
- [ ] Copied dataset to `data/` folder
- [ ] Can launch Jupyter Notebook
- [ ] Can open and run notebook 01

If all boxes are checked, you're ready to start! 🎉

---

## 🎓 Next Steps

Once setup is complete:

1. Read the main README.md for project overview
2. Run notebook 01 to preprocess data
3. Run notebook 02 to train models
4. Run notebook 03 for interactive demo
5. Use results for your research paper!

**Good luck with your project! 🚀**
