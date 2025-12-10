#!/usr/bin/env python3
"""
A powerful search tool built on ripgrep for searching file contents with regex patterns.

This tool provides a Python interface to ripgrep functionality with various options
for file searching, filtering, and output formatting.
"""

import subprocess
import json
import os
import re
from typing import List, Optional, Dict, Any


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
    
    # Build ripgrep command
    cmd = ["rg", pattern]
    
    # Add basic options
    if output_mode == "files_with_matches":
        cmd.append("--files-with-matches")
    elif output_mode == "count":
        cmd.append("--count")
    elif output_mode == "content":
        # Default content output, no special flag needed
        pass
    
    # Add search path
    cmd.append(path)
    
    # Add file filtering options
    if glob:
        cmd.extend(["--glob", glob])
    
    if type:
        cmd.extend(["--type", type])
    
    # Add context options (only for content mode)
    if output_mode == "content":
        if B is not None:
            cmd.extend(["--before-context", str(B)])
        
        if A is not None:
            cmd.extend(["--after-context", str(A)])
        
        if C is not None:
            cmd.extend(["--context", str(C)])
        
        if n:
            cmd.append("--line-number")
    
    # Add case sensitivity
    if i:
        cmd.append("--ignore-case")
    
    # Add multiline mode
    if multiline:
        cmd.append("--multiline")
    
    # Add head limit
    if head_limit is not None:
        cmd.extend(["--max-count", str(head_limit)])
    
    try:
        # Execute ripgrep command
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            # Success - found matches
            output = result.stdout.strip()
            
            # Apply head limit to output if not already done by ripgrep
            if head_limit is not None and output_mode in ["content", "files_with_matches"]:
                lines = output.split('\n')
                if len(lines) > head_limit:
                    output = '\n'.join(lines[:head_limit])
            
            return output
        elif result.returncode == 1:
            # No matches found
            return ""
        else:
            # Error occurred
            error_msg = result.stderr.strip()
            if not error_msg:
                error_msg = f"ripgrep failed with return code {result.returncode}"
            return f"Error: {error_msg}"
            
    except subprocess.TimeoutExpired:
        return "Error: Search timeout exceeded (30 seconds)"
    except FileNotFoundError:
        return "Error: ripgrep (rg) command not found. Please install ripgrep."
    except Exception as e:
        return f"Error: {str(e)}"


def test_custom_grep():
    """Test function to verify custom_grep works correctly."""
    
    # Create test files
    test_dir = "test_files"
    os.makedirs(test_dir, exist_ok=True)
    
    # Create test Python file
    test_py = os.path.join(test_dir, "test.py")
    with open(test_py, 'w') as f:
        f.write("""
def hello_world():
    print("Hello, World!")
    return True

def goodbye_world():
    print("Goodbye, World!")
    return False
""")
    
    # Create test JavaScript file
    test_js = os.path.join(test_dir, "test.js")
    with open(test_js, 'w') as f:
        f.write("""
function helloWorld() {
    console.log("Hello, World!");
    return true;
}

function goodbyeWorld() {
    console.log("Goodbye, World!");
    return false;
}
""")
    
    print("Testing custom_grep tool...")
    
    # Test 1: Search for "hello" in all files
    print("\n1. Search for 'hello' (case insensitive):")
    result = custom_grep("hello", path=test_dir, i=True)
    print(result)
    
    # Test 2: Search for "world" in Python files only
    print("\n2. Search for 'world' in Python files:")
    result = custom_grep("world", path=test_dir, type="py", i=True, output_mode="content", n=True)
    print(result)
    
    # Test 3: Count matches
    print("\n3. Count matches for 'def':")
    result = custom_grep("def", path=test_dir, output_mode="count")
    print(result)
    
    # Test 4: Search with context
    print("\n4. Search for 'return' with context:")
    result = custom_grep("return", path=test_dir, output_mode="content", C=1, n=True)
    print(result)
    
    # Clean up
    import shutil
    shutil.rmtree(test_dir)
    
    print("\nTests completed!")


if __name__ == "__main__":
    # Run tests if executed directly
    test_custom_grep()