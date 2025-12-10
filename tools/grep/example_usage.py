#!/usr/bin/env python3
"""
Example usage of the custom_grep implementation.
"""
import shutil

from custom_grep_implementation import custom_grep
import os
import tempfile


def create_example_files():
    """Create example files for demonstration."""
    temp_dir = tempfile.mkdtemp()
    
    # Create Python file
    py_file = os.path.join(temp_dir, "example.py")
    with open(py_file, 'w') as f:
        f.write("""# Example Python file
import os
import sys

def main():
    print("Hello, World!")
    return 0

if __name__ == "__main__":
    main()
""")
    
    # Create JavaScript file
    js_file = os.path.join(temp_dir, "example.js")
    with open(js_file, 'w') as f:
        f.write("""// Example JavaScript file
function main() {
    console.log("Hello, World!");
    return 0;
}

main();
""")
    
    # Create text file
    txt_file = os.path.join(temp_dir, "example.txt")
    with open(txt_file, 'w') as f:
        f.write("""Example text file
This file contains various words and phrases.
Hello world is a common programming greeting.
The main function is where execution begins.
""")
    
    return temp_dir


def main():
    """Demonstrate custom_grep usage."""
    print("Custom Grep Tool - Example Usage")
    print("=" * 40)
    
    # Create example files
    temp_dir = create_example_files()
    
    try:
        # Example 1: Find files containing "Hello"
        print("\n1. Find files containing 'Hello':")
        result = custom_grep("Hello", path=temp_dir, output_mode="files_with_matches")
        print(result)
        
        # Example 2: Search for function definitions in Python files
        print("\n2. Function definitions in Python files:")
        result = custom_grep("def", path=temp_dir, type="py", output_mode="content", n=True)
        print(result)
        
        # Example 3: Count occurrences of "main"
        print("\n3. Count occurrences of 'main':")
        result = custom_grep("main", path=temp_dir, output_mode="count")
        print(result)
        
        # Example 4: Search with context
        print("\n4. Search for 'Hello' with context:")
        result = custom_grep("Hello", path=temp_dir, C=1, output_mode="content", n=True)
        print(result)
        
        # Example 5: Case-insensitive search
        print("\n5. Case-insensitive search for 'hello':")
        result = custom_grep("hello", path=temp_dir, i=True, output_mode="files_with_matches")
        print(result)
        
        # Example 6: Limited results
        print("\n6. Limited results (max 2):")
        result = custom_grep("file", path=temp_dir, head_limit=2, output_mode="content", n=True)
        print(result)
        
    finally:
        # Clean up
        shutil.rmtree(temp_dir)


if __name__ == "__main__":
    main()