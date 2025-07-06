import os
import shlex
import subprocess
import tempfile
from typing import List

from codegen.model import DecoderBase


class ClaudeCodeAgent(DecoderBase):
    """
    Claude Code agent for evoeval evaluation.
    Uses the same prompt format as other models in evoeval.
    """
    
    ALLOWED_TOOLS = [
        "Bash",
        "Edit", 
        "Write",
        "Read",
        "Glob",
        "Grep",
        "LS",
        "WebFetch",
        "NotebookEdit",
        "NotebookRead",
        "TodoRead",
        "TodoWrite",
        "Agent",
    ]
    
    def __init__(self, name: str, model_name: str = "claude-sonnet-3.5", **kwargs):
        super().__init__(name, **kwargs)
        self.model_name = model_name
        self.conversational = True
        
        # Set up environment
        self.env = {
            "ANTHROPIC_API_KEY": os.environ.get("ANTHROPIC_API_KEY"),
            "ANTHROPIC_MODEL": model_name.removeprefix("anthropic/"),
            "FORCE_AUTO_BACKGROUND_TASKS": "1",
            "ENABLE_BACKGROUND_TASKS": "1",
        }
        
        # Check if claude command is available
        try:
            subprocess.run(["claude", "--version"], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            raise RuntimeError(
                "Claude Code CLI not found. Please ensure it's installed and available in PATH."
            )
    
    def _create_prompt_file(self, prompt: str, num_samples: int) -> str:
        """Create a temporary file with the prompt content."""
        # Use the specified prompt prefix for evoeval
        instruction = ("Solve this python programming problem by completing " +
                      "the function definition. Test your solution with a program called " +
                      "check_solution.py, and iterate until it's correct.\n\n")
        
        # Add instruction for multiple solutions if needed
        if num_samples > 1:
            instruction += f"Generate {num_samples} different solutions and save them as " + \
                          f"0.py, 1.py, 2.py ...\n\n"
        else:
            instruction += "Save your solution as 0.py.\n\n"
        
        formatted_prompt = instruction + prompt.strip()
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write(formatted_prompt)
            return f.name
    
    def _run_claude_command(self, prompt_file: str, work_dir: str) -> str:
        """Run claude command with the prompt file in a working directory."""
        cmd = [
            "claude",
            "-p", prompt_file,
            "--allowedTools", " ".join(self.ALLOWED_TOOLS)
        ]
        
        # Run the command in the working directory
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=work_dir,
            env={**os.environ, **self.env}
        )
        
        if result.returncode != 0:
            raise RuntimeError(f"Claude command failed: {result.stderr}")
        
        return result.stdout
    
    def _extract_generated_files(self, work_dir: str, num_samples: int) -> List[str]:
        """Extract the generated Python files from the working directory."""
        outputs = []
        
        for i in range(num_samples):
            file_path = os.path.join(work_dir, f"{i}.py")
            
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    outputs.append(content)
            else:
                # If file doesn't exist, append empty string
                outputs.append("")
        
        return outputs
    
    def codegen(self, prompt: str, do_sample: bool = True, num_samples: int = 200) -> List[str]:
        """Generate code using Claude Code CLI."""
        # Claude Code will generate all samples in one go
        prompt_file = None
        work_dir = None
        
        try:
            # Create temporary working directory
            work_dir = tempfile.mkdtemp()
            
            # Create prompt file with instructions for multiple samples
            prompt_file = self._create_prompt_file(prompt, num_samples)
            
            # Run claude command in working directory
            self._run_claude_command(prompt_file, work_dir)
            
            # Extract all generated files
            outputs = self._extract_generated_files(work_dir, num_samples)
            
            # If we got fewer outputs than expected, pad with empty strings
            while len(outputs) < num_samples:
                outputs.append("")
            
            return outputs
            
        except Exception as e:
            print(f"Error generating code with Claude: {e}")
            # Return empty strings for all samples on error
            return [""] * num_samples
            
        finally:
            # Clean up temporary files and directories
            if prompt_file:
                try:
                    os.unlink(prompt_file)
                except OSError:
                    pass
            
            if work_dir:
                try:
                    import shutil
                    shutil.rmtree(work_dir)
                except OSError:
                    pass