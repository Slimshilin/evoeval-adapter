import os
import shlex
import subprocess
import tempfile
from typing import List

from codegen.model import DecoderBase


class CodexAgent(DecoderBase):
    """
    Codex agent for evoeval evaluation.
    Uses the same prompt format as other models in evoeval.
    """
    
    def __init__(self, name: str, model_name: str = "gpt-4o-mini", **kwargs):
        super().__init__(name, **kwargs)
        self.model_name = model_name
        self.conversational = True
        
        # Set up environment
        self.env = {
            "OPENAI_API_KEY": os.environ.get("OPENAI_API_KEY"),
        }
        
        # Check if codex command is available
        try:
            subprocess.run(["codex", "--version"], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            raise RuntimeError(
                "Codex CLI not found. Please ensure it's installed and available in PATH."
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
    
    def _run_codex_command(self, prompt: str, work_dir: str) -> str:
        """Run codex command with the prompt in a working directory."""
        escaped_prompt = shlex.quote(prompt)
        cmd = [
            "codex",
            "--writable-root", "/",
            "-q", 
            "--approval-mode", "full-auto",
            "--model", self.model_name,
            escaped_prompt
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
            raise RuntimeError(f"Codex command failed: {result.stderr}")
        
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
        """Generate code using Codex CLI."""
        work_dir = None
        
        try:
            # Create temporary working directory
            work_dir = tempfile.mkdtemp()
            
            # Create instruction with prompt
            instruction = ("Solve this python programming problem by completing " +
                          "the function definition. Test your solution with a program called " +
                          "check_solution.py, and iterate until it's correct.\n\n")
            
            # Add instruction for multiple solutions if needed
            if num_samples > 1:
                instruction += f"Generate {num_samples} different solutions and save them as " + \
                              f"0.py, 1.py, 2.py ...\n\n"
            else:
                instruction += "Save your solution as 0.py.\n\n"
            
            full_instruction = instruction + prompt.strip()
            
            # Run codex command in working directory
            self._run_codex_command(full_instruction, work_dir)
            
            # Extract all generated files
            outputs = self._extract_generated_files(work_dir, num_samples)
            
            # If we got fewer outputs than expected, pad with empty strings
            while len(outputs) < num_samples:
                outputs.append("")
            
            return outputs
            
        except Exception as e:
            print(f"Error generating code with Codex: {e}")
            # Return empty strings for all samples on error
            return [""] * num_samples
            
        finally:
            # Clean up temporary files and directories
            if work_dir:
                try:
                    import shutil
                    shutil.rmtree(work_dir)
                except OSError:
                    pass