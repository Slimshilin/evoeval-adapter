#!/bin/bash
set -e

export PYTHONPATH=$PYTHONPATH:$(pwd)
python codegen/generate.py \
    --model claude-code-4-opus \
    --bs 1 \
    --temperature 0.0 \
    --dataset EvoEval_difficult \
    --root ./claude_code/output/claude_code_4_opus_1 \
    --n_samples 1 \
    --greedy

python codegen/generate.py \
    --model claude-code-4-opus \
    --bs 1 \
    --temperature 0.0 \
    --dataset EvoEval_difficult \
    --root ./claude_code/output/claude_code_4_opus_2 \
    --n_samples 1 \
    --greedy

python codegen/generate.py \
    --model claude-code-4-opus \
    --bs 1 \
    --temperature 0.0 \
    --dataset EvoEval_difficult \
    --root ./claude_code/output/claude_code_4_opus_3 \
    --n_samples 1 \
    --greedy

python codegen/generate.py \
    --model claude-code-4-opus \
    --bs 1 \
    --temperature 0.0 \
    --dataset EvoEval_difficult \
    --root ./claude_code/output/claude_code_4_opus_4 \
    --n_samples 1 \
    --greedy

python codegen/generate.py \
    --model claude-code-4-opus \
    --bs 1 \
    --temperature 0.0 \
    --dataset EvoEval_difficult \
    --root ./claude_code/output/claude_code_4_opus_5 \
    --n_samples 1 \
    --greedy