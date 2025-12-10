#!/usr/bin/env python3
"""Test script for custom_grep implementation."""

import subprocess
import os
import tempfile


def test_ripgrep_availability():
    """Test if ripgrep is available in the system."""
    try:
        result = subprocess.run(["rg", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"ripgrep is available: {result.stdout.strip()}")
            return True
        else:
            print("ripgrep (rg) command not found")
            return False
    except FileNotFoundError:
        print("ripgrep (rg) command not found")
        return False

def create_test_files(test_dir):
    """Create test files for testing."""
    # Create test Python file
    test_py = os.path.join(test_dir, "test.py")
    with open(test_py, 'w') as f:
        f.write("""def hello_world():
    print("Hello, World!")
    return True

def goodbye_world():
    print("Goodbye, World!")
    return False
""")
    
    # Create test JavaScript file
    test_js = os.path.join(test_dir, "test.js")
    with open(test_js, 'w') as f:
        f.write("""function helloWorld() {
    console.log("Hello, World!");
    return true;
}

function goodbyeWorld() {
    console.log("Goodbye, World!");
    return false;
}
""")
    
    # Create test text file
    test_txt = os.path.join(test_dir, "test.txt")
    with open(test_txt, 'w') as f:
        f.write("""This is a test file.
It contains some sample text.
Hello world appears here.
Goodbye world appears here too.
""")

def test_basic_functionality():
    """Test basic custom_grep functionality."""
    
    # Import the custom_grep function
    import sys
    sys.path.append('../..')
    from tools.grep.custom_grep_tool import custom_grep
    
    # Create temporary test directory
    with tempfile.TemporaryDirectory() as test_dir:
        create_test_files(test_dir)
        
        print("Testing custom_grep functionality...")
        
        # Test 1: Basic search
        print("\n1. Basic search for 'Hello':")
        result = custom_grep("Hello", path=test_dir, output_mode="content", n=True)
        print(result)
        
        # Test 2: Case insensitive search
        print("\n2. Case insensitive search for 'hello':")
        result = custom_grep("hello", path=test_dir, i=True, output_mode="files_with_matches")
        print(result)
        
        # Test 3: File type filtering
        print("\n3. Search in Python files only:")
        result = custom_grep("def", path=test_dir, type="py", output_mode="content", n=True)
        print(result)
        
        # Test 4: Count matches
        print("\n4. Count matches for 'return':")
        result = custom_grep("return", path=test_dir, output_mode="count")
        print(result)
        
        # Test 5: Search with context
        print("\n5. Search with context (2 lines before and after):")
        result = custom_grep("Hello", path=test_dir, C=1, output_mode="content", n=True)
        print(result)
        
        # Test 6: Head limit
        print("\n6. Limited results (max 2):")
        result = custom_grep("world", path=test_dir, i=True, output_mode="content", head_limit=2, n=True)
        print(result)

if __name__ == "__main__":
    print("Testing ripgrep availability...")
    if test_ripgrep_availability():
        test_basic_functionality()
    else:
        print("Cannot proceed without ripgrep. Please install ripgrep first.")
        print("Installation: ")
        print("  Ubuntu/Debian: sudo apt install ripgrep")
        print("  macOS: brew install ripgrep")
        print("  Windows: choco install ripgrep")