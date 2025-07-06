#!/bin/bash
set -e

export PYTHONPATH=$PYTHONPATH:$(pwd)
python codegen/generate.py \
    --model codex-o4-mini \
    --bs 1 \
    --temperature 0.0 \
    --dataset EvoEval_difficult \
    --root ./codex/output/codex_o4_mini_1 \
    --n_samples 1 \
    --greedy

python codegen/generate.py \
    --model codex-o4-mini \
    --bs 1 \
    --temperature 0.0 \
    --dataset EvoEval_difficult \
    --root ./codex/output/codex_o4_mini_2 \
    --n_samples 1 \
    --greedy

python codegen/generate.py \
    --model codex-o4-mini \
    --bs 1 \
    --temperature 0.0 \
    --dataset EvoEval_difficult \
    --root ./codex/output/codex_o4_mini_3 \
    --n_samples 1 \
    --greedy

python codegen/generate.py \
    --model codex-o4-mini \
    --bs 1 \
    --temperature 0.0 \
    --dataset EvoEval_difficult \
    --root ./codex/output/codex_o4_mini_4 \
    --n_samples 1 \
    --greedy

python codegen/generate.py \
    --model codex-o4-mini \
    --bs 1 \
    --temperature 0.0 \
    --dataset EvoEval_difficult \
    --root ./codex/output/codex_o4_mini_5 \
    --n_samples 1 \
    --greedy