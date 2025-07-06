# Codex Agent for EvoEval

This directory contains the Codex CLI integration for the EvoEval benchmarking framework.

## Overview

The Codex agent enables evaluation of OpenAI's GPT models through the Codex CLI interface within the EvoEval framework. This integration allows fair comparison with other coding models using identical prompt formats and evaluation criteria.

## Architecture

The implementation follows the standard EvoEval model pattern:

- **`codex_agent.py`**: Core agent extending `DecoderBase` class
- **`scripts/`**: Automated generation and evaluation scripts  
- **`codex-setup.sh`**: CLI installation script

## Requirements

1. **API Access**: Valid `OPENAI_API_KEY` environment variable
2. **Runtime**: Node.js and npm for Codex CLI
3. **CLI Tool**: Codex CLI (auto-installed via setup script)

## Setup

```bash
# Set API credentials
export OPENAI_API_KEY=your_api_key_here

# Install Codex CLI (if needed)
./codex/codex-setup.sh

# Verify installation
codex --version
```

## Supported Models

| Model Name | Description | Underlying Model |
|------------|-------------|------------------|
| `codex-gpt-4o` | GPT-4o via Codex CLI | `gpt-4o` |
| `codex-o4-mini` | o4-mini via Codex CLI | `o4-mini` |

## Models

### Current Implementation

The Codex agent currently supports two model configurations:

- **`codex-gpt-4o`**: Uses OpenAI's GPT-4o model for advanced reasoning and code generation
- **`codex-o4-mini`**: Uses the o4-mini model for efficient code generation tasks

### Adding New Models

To add support for additional OpenAI models, follow these steps:

1. **Update Model Factory** (`codegen/model.py`):
   ```python
   elif name == "codex-new-model":
       if CodexAgent is None:
           raise ImportError("CodexAgent not available. Please ensure codex module is installed.")
       return CodexAgent(
           batch_size=batch_size,
           name="codex-new-model",
           temperature=temperature,
           model_name="new-model-name",  # Actual OpenAI model ID
       )
   ```

2. **Create Generation Script** (`codex/scripts/run_generate_codex_new_model.sh`):
   ```bash
   #!/bin/bash
   set -e
   
   export PYTHONPATH=$PYTHONPATH:$(pwd)
   python codegen/generate.py \
       --model codex-new-model \
       --bs 1 \
       --temperature 0.0 \
       --dataset EvoEval_difficult \
       --root ./codex/codex_new_model \
       --n_samples 1 \
       --greedy
   ```

3. **Make Script Executable**:
   ```bash
   chmod +x codex/scripts/run_generate_codex_new_model.sh
   ```

### Model Configuration Notes

- **Model Names**: Use the pattern `codex-{model-variant}` for consistency
- **Underlying Models**: Refer to official OpenAI model identifiers (e.g., `gpt-4o`, `o4-mini`)
- **CLI Compatibility**: Ensure the underlying model is supported by Codex CLI

## Usage

### Quick Start

```bash
# Generate solutions for EvoEval_difficult using GPT-4o
./codex/scripts/run_generate_codex_gpt_4o.sh

# Evaluate the results
./codex/scripts/evaluate_codex.sh ./codex/codex_gpt_4o/EvoEval_difficult/codex-gpt-4o_temp_0.0
```

### Evaluation
You may also evaluate using the following commands, after obtaining the generated codes.

```bash
# Direct evaluation
python evoeval/evaluate.py \
    --dataset EvoEval_difficult \
    --samples path/to/generated/samples/directory

# Using Docker (if available)
docker run --rm -v $(pwd):/app evoeval/evoeval:latest \
    --dataset EvoEval_difficult \
    --samples samples_directory
```

## Output Structure

Generated solutions follow this hierarchy:
```
codex/
└── codex_gpt_4o/
    └── EvoEval_difficult/
        └── codex-gpt-4o_temp_0.0/
            ├── EvoEval_0/
            │   └── 0.py
            ├── EvoEval_1/
            │   └── 0.py
            ⋮
            ├── args.txt
            └── eval_results.json  # Generated after evaluation
```

## Implementation Details

### Agent Behavior
- Uses subprocess calls to Codex CLI with full automation approval mode
- Handles temporary file creation and cleanup automatically
- Supports multi-sample generation (though typically n_samples=1 and is set to default)
- Error handling with empty string fallbacks

### CLI Configuration
The agent configures Codex CLI with these parameters:
- Writable root: `/` (full filesystem access)
- Quiet mode: `-q` (reduced output)
- Approval mode: `full-auto` (automatic execution)
- Model specification: configurable via model name parameter

### Prompt Format
The agent uses this instruction template to adapt terminal agents like Codex to write files in place, compared to chat models where we extract code snippets from responses:
```
Solve this python programming problem by completing the function definition. 
Test your solution with a program called check_solution.py, and iterate until it's correct.

Save your solution as 0.py.

[Original EvoEval problem prompt]
```

## Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| `codex command not found` | CLI not installed | Run `./codex/codex-setup.sh` |
| `OPENAI_API_KEY not set` | Missing environment variable | Set `export OPENAI_API_KEY=your_key` |
| Import errors | Wrong working directory | Run from evoeval-adapter root |
| Empty solutions | CLI execution failure | Check API key and network connectivity |


### Verification Steps

1. **CLI Check**: `codex --version` should return version info
2. **API Check**: `echo $OPENAI_API_KEY` should show your key  
3. **Python Path**: `echo $PYTHONPATH` should include current directory
4. **File Generation**: Check if `0.py` files are created in output directories, and the python file has actual codes besides function signature (i.e., the prompt)

## Integration Notes

The agent integrates seamlessly with the existing EvoEval infrastructure:
- Extends `DecoderBase` for consistent interface
- Registered in `codegen/model.py` model factory
- Compatible with all EvoEval datasets and evaluation metrics
- Supports standard command-line arguments and resume functionality