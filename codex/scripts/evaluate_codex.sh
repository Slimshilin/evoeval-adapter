#!/bin/bash
set -e

if [ $# -ne 1 ]; then
    echo "Usage: $0 <samples_directory>"
    exit 1
fi

SAMPLES_DIR="$1"
DATASET="EvoEval_difficult"

export PYTHONPATH=$PYTHONPATH:$(pwd)
python evoeval/evaluate.py --dataset "$DATASET" --samples "$SAMPLES_DIR"