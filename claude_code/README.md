# Claude Code Agent for EvoEval

This directory contains the Claude Code CLI integration for the EvoEval benchmarking framework.

## Overview

The Claude Code agent enables evaluation of Anthropic's Claude models through the Claude Code CLI interface within the EvoEval framework. This integration allows fair comparison with other coding models using identical prompt formats and evaluation criteria.

## Architecture

The implementation follows the standard EvoEval model pattern:

- **`claude_code_agent.py`**: Core agent extending `DecoderBase` class
- **`scripts/`**: Automated generation and evaluation scripts  
- **`claude-code-setup.sh`**: CLI installation script

## Requirements

1. **API Access**: Valid `ANTHROPIC_API_KEY` environment variable
2. **Runtime**: Node.js and npm for Claude Code CLI
3. **CLI Tool**: Claude Code CLI (auto-installed via setup script)

## Setup

```bash
# Set API credentials
export ANTHROPIC_API_KEY=your_api_key_here

# Install Claude Code CLI (if needed)
./claude_code/claude-code-setup.sh

# Verify installation
claude --version
```

## Supported Models

| Model Name | Description | Underlying Model |
|------------|-------------|------------------|
| `claude-code-4-opus` | Claude 4 Opus via CLI | `claude-4-opus-20250514` |
| `claude-code-4-sonnet` | Claude 4 Sonnet via CLI | `claude-4-sonnet-20250514` |

## Models

### Current Implementation

The Claude Code agent currently supports two model configurations:

- **`claude-code-4-opus`**: Uses the most capable Claude 4 Opus model for complex reasoning tasks
- **`claude-code-4-sonnet`**: Uses Claude 4 Sonnet for balanced performance and efficiency

### Adding New Models

To add support for additional Claude models, follow these steps:

1. **Update Model Factory** (`codegen/model.py`):
   ```python
   elif name == "claude-code-new-model":
       if ClaudeCodeAgent is None:
           raise ImportError("ClaudeCodeAgent not available. Please ensure claude_code module is installed.")
       return ClaudeCodeAgent(
           batch_size=batch_size,
           name="claude-code-new-model",
           temperature=temperature,
           model_name="claude-new-model-date",  # Actual Claude model ID
       )
   ```

2. **Create Generation Script** (`claude_code/scripts/run_generate_claude_code_new_model.sh`):
   ```bash
   #!/bin/bash
   set -e
   
   export PYTHONPATH=$PYTHONPATH:$(pwd)
   python codegen/generate.py \
       --model claude-code-new-model \
       --bs 1 \
       --temperature 0.0 \
       --dataset EvoEval_difficult \
       --root ./claude_code/claude_code_new_model \
       --n_samples 1 \
       --greedy
   ```

3. **Make Script Executable**:
   ```bash
   chmod +x claude_code/scripts/run_generate_claude_code_new_model.sh
   ```

### Model Configuration Notes

- **Model Names**: Use the pattern `claude-code-{model-variant}` for consistency
- **Underlying Models**: Refer to official Anthropic model identifiers (e.g., `claude-4-opus-20250514`)
- **CLI Compatibility**: Ensure the underlying model is supported by Claude Code CLI

## Usage

### Quick Start

```bash
# Generate solutions for EvoEval_difficult using Claude 4 Sonnet
./claude_code/scripts/run_generate_claude_code_4_sonnet.sh

# Evaluate the results
./claude_code/scripts/evaluate_claude_code.sh ./claude_code/claude_code_4_sonnet/EvoEval_difficult/claude-code-4-sonnet_temp_0.0
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
claude_code/
└── claude_code_4_sonnet/
    └── EvoEval_difficult/
        └── claude-code-4-sonnet_temp_0.0/
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
- Uses subprocess calls to Claude Code CLI with specified tool permissions
- Handles temporary file creation and cleanup automatically
- Supports multi-sample generation (though typically n_samples=1 and is set to default)
- Error handling with empty string fallbacks

### Tool Permissions
The agent grants Claude access to these tools:
- File operations: `Read`, `Write`, `Edit`, `LS`, `Glob`, `Grep`
- Execution: `Bash`
- Web access: `WebFetch`
- Notebooks: `NotebookRead`, `NotebookEdit`
- Task management: `TodoRead`, `TodoWrite`
- Sub-agents: `Agent`

### Prompt Format
The agent uses this instruction template to adapt terminal agents like Claude Code to write files in place, compared to chat models where we extract code snippets from responses:
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
| `claude command not found` | CLI not installed | Run `./claude_code/claude-code-setup.sh` |
| `ANTHROPIC_API_KEY not set` | Missing environment variable | Set `export ANTHROPIC_API_KEY=your_key` |
| Import errors | Wrong working directory | Run from evoeval-adapter root |
| Empty solutions | CLI execution failure | Check API key and network connectivity |


### Verification Steps

1. **CLI Check**: `claude --version` should return version info
2. **API Check**: `echo $ANTHROPIC_API_KEY` should show your key  
3. **Python Path**: `echo $PYTHONPATH` should include current directory
4. **File Generation**: Check if `0.py` files are created in output directories, and the python file has actual codes besides function signature (i.e., the prompt)