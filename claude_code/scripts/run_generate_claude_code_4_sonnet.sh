#!/bin/bash
set -e

export PYTHONPATH=$PYTHONPATH:$(pwd)
python codegen/generate.py \
    --model claude-code-4-sonnet \
    --bs 1 \
    --temperature 0.0 \
    --dataset EvoEval_difficult \
    --root ./claude_code/claude_code_4_sonnet \
    --n_samples 1 \
    --greedy