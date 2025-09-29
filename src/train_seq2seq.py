# src/train_seq2seq.py

import os
import pickle
import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split

# ----- Reproducibility
SEED = 42
tf.random.set_seed(SEED)
np.random.seed(SEED)

# ----- Special tokens (match your tokenizer setup)
PAD_ID = 0
BOS_ID = 1
EOS_ID = 2

# ----- Paths
DATA_PATH   = "data/processed/tokenized.pkl"   # train on this
CKPT_DIR    = "checkpoints"
os.makedirs(CKPT_DIR, exist_ok=True)

# ----- Model/data hyperparameters (you can tune later)
VOCAB_SIZE  = 8000          # your SentencePiece vocab size
MAX_LEN_SRC = 128
MAX_LEN_TGT = 128
BATCH_SIZE  = 128
EMBED_DIM   = 256
LSTM_UNITS  = 256
DROPOUT     = 0.2
LR          = 2e-3
EPOCHS      = 8

print("Config loaded. Ready to load data.")
