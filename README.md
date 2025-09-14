# 📧 Email Phishing Detector

A machine learning-based project to detect phishing emails using classification models.

## 🚀 Features
- Detects phishing emails using multiple ML models.
- Preprocessing pipeline for cleaning and vectorizing email text.
- Support for training and testing with custom datasets.
- Modular code structure for easy updates.

## 📂 Project Structure
data/                      # (ignored in repo) datasets like phishing & spam email CSVs
models/                    # (ignored in repo) trained ML models
detector/                  # main detection engine
├── engine.py
├── ml.py
├── rules.py
└── utils.py
main.py                    # entry point for running detection
train_model.py             # basic training script
train_model_improved.py    # improved training script
test_model.py              # testing script


## ⚙️ Installation

# Clone the repo
git clone https://github.com/NomeshBabu/Email_pishing_detector.git
cd Email_pishing_detector

# Install dependencies
pip install -r requirements.txt

▶️ USAGE 
# Train model
python train_model_improved.py

# Test model
python test_model.py

# Run detection
python main.py

