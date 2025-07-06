#!/bin/bash
set -e

if [ $# -ne 1 ]; then
    echo "Usage: $0 <results_directory>"
    exit 1
fi

RESULTS_DIR="$1"
DATASET="EvoEval_difficult"

export PYTHONPATH=$PYTHONPATH:$(pwd)
python evoeval/evaluate.py --dataset "$DATASET" --samples "$RESULTS_DIR"