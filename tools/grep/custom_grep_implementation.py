#!/usr/bin/env python3
"""
Custom implementation of custom_grep tool based on the provided documentation.

This implementation provides a Python interface to ripgrep functionality
with all the features described in the original documentation.
"""

import subprocess
import os
import tempfile
import shutil
from typing import Optional, List


class CustomGrep:
    """A powerful search tool built on ripgrep for searching file contents with regex patterns."""
    
    def __init__(self):
        """Initialize the CustomGrep tool."""
        self._check_ripgrep()
    
    def _check_ripgrep(self):
        """Check if ripgrep is available in the system."""
        try:
            result = subprocess.run(["rg", "--version"], capture_output=True, text=True)
            if result.returncode != 0:
                raise RuntimeError("ripgrep (rg) command not available")
        except FileNotFoundError:
            raise RuntimeError("ripgrep (rg) command not found. Please install ripgrep.")
    
    def search(
        self,
        pattern: str,
        path: str = ".",
        glob: Optional[str] = None,
        output_mode: str = "files_with_matches",
        B: Optional[int] = None,
        A: Optional[int] = None,
        C: Optional[int] = None,
        n: bool = False,
        i: bool = False,
        type: Optional[str] = None,
        head_limit: Optional[int] = None,
        multiline: bool = False
    ) -> str:
        """
        Search for patterns in files using ripgrep.

        Args:
            pattern: The regular expression pattern to search for in file contents.
                    Uses ripgrep syntax - literal braces need escaping (e.g., `interface\{\}` for `interface{}`).
            path: File or directory to search in. Defaults to current working directory if not specified.
            glob: Glob pattern to filter files (e.g., "*.js", "*.{ts,tsx}").
            output_mode: Output mode - "content" shows matching lines with optional context,
                        "files_with_matches" shows only file paths (default),
                        "count" shows match counts per file.
            B: Number of lines to show before each match. Only works with output_mode="content".
            A: Number of lines to show after each match. Only works with output_mode="content".
            C: Number of lines to show before and after each match. Only works with output_mode="content".
            n: Show line numbers in output. Only works with output_mode="content".
            i: Enable case insensitive search.
            type: File type to search (e.g., "js", "py", "rust", "go", "java").
                 More efficient than glob for standard file types.
            head_limit: Limit output to first N lines/entries. Works across all output modes.
            multiline: Enable multiline mode where patterns can span lines and . matches newlines.
                      Default is False (single-line matching only).

        Returns:
            Search results as a string, formatted according to the output_mode.
        """
        
        # Validate output_mode
        if output_mode not in ["content", "files_with_matches", "count"]:
            raise ValueError(f"Invalid output_mode: {output_mode}. Must be one of: content, files_with_matches, count")
        
        # Build ripgrep command
        cmd = ["rg"]
        
        # Add output mode specific flags
        if output_mode == "files_with_matches":
            cmd.append("--files-with-matches")
        elif output_mode == "count":
            cmd.append("--count")
        # For "content" mode, we don't need special flags
        
        # Add pattern
        cmd.append(pattern)
        
        # Add path
        cmd.append(path)
        
        # Add file filtering options
        if glob:
            cmd.extend(["--glob", glob])
        
        if type:
            cmd.extend(["--type", type])
        
        # Add context options (only for content mode)
        if output_mode == "content":
            if B is not None:
                if not isinstance(B, int) or B < 0:
                    raise ValueError("B must be a non-negative integer")
                cmd.extend(["--before-context", str(B)])
            
            if A is not None:
                if not isinstance(A, int) or A < 0:
                    raise ValueError("A must be a non-negative integer")
                cmd.extend(["--after-context", str(A)])
            
            if C is not None:
                if not isinstance(C, int) or C < 0:
                    raise ValueError("C must be a non-negative integer")
                cmd.extend(["--context", str(C)])
            
            if n:
                cmd.append("--line-number")
        
        # Add case sensitivity option
        if i:
            cmd.append("--ignore-case")
        
        # Add multiline mode
        if multiline:
            cmd.append("--multiline")
        
        # Add head limit
        if head_limit is not None:
            if not isinstance(head_limit, int) or head_limit <= 0:
                raise ValueError("head_limit must be a positive integer")
            cmd.extend(["--max-count", str(head_limit)])
        
        try:
            # Execute ripgrep command
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                # Success - found matches
                output = result.stdout.strip()
                
                # Apply additional head limit processing if needed
                if head_limit is not None and output_mode in ["content", "files_with_matches"]:
                    lines = output.split('\n')
                    if len(lines) > head_limit:
                        output = '\n'.join(lines[:head_limit])
                
                return output
                
            elif result.returncode == 1:
                # No matches found (ripgrep returns 1 when no matches)
                return ""
                
            else:
                # Error occurred
                error_msg = result.stderr.strip()
                if not error_msg:
                    error_msg = f"ripgrep failed with return code {result.returncode}"
                return f"Error: {error_msg}"
                
        except subprocess.TimeoutExpired:
            return "Error: Search timeout exceeded (60 seconds)"
        except Exception as e:
            return f"Error: {str(e)}"


# Convenience function that matches the original interface
def custom_grep(
    pattern: str,
    path: str = ".",
    glob: Optional[str] = None,
    output_mode: str = "files_with_matches",
    B: Optional[int] = None,
    A: Optional[int] = None,
    C: Optional[int] = None,
    n: bool = False,
    i: bool = False,
    type: Optional[str] = None,
    head_limit: Optional[int] = None,
    multiline: bool = False
) -> str:
    """
    A powerful search tool built on ripgrep for searching file contents with regex patterns.

    This function provides the same interface as described in the original documentation.
    """
    tool = CustomGrep()
    return tool.search(
        pattern=pattern,
        path=path,
        glob=glob,
        output_mode=output_mode,
        B=B,
        A=A,
        C=C,
        n=n,
        i=i,
        type=type,
        head_limit=head_limit,
        multiline=multiline
    )


def demonstrate_usage():
    """Demonstrate the usage of custom_grep with various examples."""
    
    print("Custom Grep Tool Demonstration")
    print("=" * 40)
    
    # Create sample files for demonstration
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create sample Python file
        py_file = os.path.join(temp_dir, "sample.py")
        with open(py_file, 'w') as f:
            f.write("""# Sample Python file
def greet(name):
    print(f"Hello, {name}!")
    return True

def farewell(name):
    print(f"Goodbye, {name}!")
    return False
""")
        
        # Create sample JavaScript file
        js_file = os.path.join(temp_dir, "sample.js")
        with open(js_file, 'w') as f:
            f.write("""// Sample JavaScript file
function greetUser(name) {
    console.log(`Hello, ${name}!`);
    return true;
}

function farewellUser(name) {
    console.log(`Goodbye, ${name}!`);
    return false;
}
""")
        
        # Create sample text file
        txt_file = os.path.join(temp_dir, "sample.txt")
        with open(txt_file, 'w') as f:
            f.write("""This is a sample text file.
It contains various words and phrases.
Hello world is a common greeting.
Goodbye is a common farewell.
""")
        
        # Demonstrate various search options
        examples = [
            {
                "description": "Find files containing 'Hello' (case insensitive)",
                "params": {"pattern": "hello", "path": temp_dir, "i": True, "output_mode": "files_with_matches"}
            },
            {
                "description": "Search for function definitions in Python files",
                "params": {"pattern": "def", "path": temp_dir, "type": "py", "output_mode": "content", "n": True}
            },
            {
                "description": "Count occurrences of 'return' in all files",
                "params": {"pattern": "return", "path": temp_dir, "output_mode": "count"}
            },
            {
                "description": "Search for 'greet' with context lines",
                "params": {"pattern": "greet", "path": temp_dir, "C": 1, "output_mode": "content", "n": True}
            },
            {
                "description": "Limited search results (max 2)",
                "params": {"pattern": "Hello", "path": temp_dir, "head_limit": 2, "output_mode": "content", "n": True}
            }
        ]
        
        for i, example in enumerate(examples, 1):
            print(f"\n{i}. {example['description']}")
            print("-" * 50)
            result = custom_grep(**example['params'])
            print(result if result else "No matches found")


if __name__ == "__main__":
    # Run demonstration
    demonstrate_usage()