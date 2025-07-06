#!/bin/bash
set -e

export PYTHONPATH=$PYTHONPATH:$(pwd)
python codegen/generate.py \
    --model codex-gpt-4o \
    --bs 1 \
    --temperature 0.0 \
    --dataset EvoEval_difficult \
    --root ./codex/codex_gpt_4o \
    --n_samples 1 \
    --greedy