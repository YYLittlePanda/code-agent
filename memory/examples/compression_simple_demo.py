#!/usr/bin/env python3
"""
Simple Compression Strategy Demonstration
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from memory.memory_compression import compress_memory, get_memory_compression_stats, reset_memory_compression


def show_compression_example(content, content_type, description):
    """Show a compression example."""
    print(f"\n{description}")
    print("=" * 60)
    
    original_length = len(content)
    print(f"📄 ORIGINAL ({content_type}):")
    print(f"Length: {original_length} characters")
    print(content[:200] + "..." if len(content) > 200 else content)
    print()
    
    # Compress
    result = compress_memory(content, content_type)
    print(f"🗜️  COMPRESSION RESULT:")
    print(result)
    
    # Show stats
    stats = get_memory_compression_stats()
    if "Total memories: 0" not in stats:
        print(f"\n📊 COMPRESSION STATISTICS:")
        lines = stats.split('\n')
        for line in lines[:8]:  # Show first 8 lines
            print(line)


def main():
    print("🎯 Memory Compression Strategy Demonstrations")
    print("=" * 70)
    
    # Reset for clean demo
    reset_memory_compression()
    
    # Example 1: Conversation
    conversation = """User: Hi, I need help with a Python issue I'm facing.
Agent: Hello! I'd be happy to help you with your Python issue. 
User: I'm getting an AttributeError when trying to access a dictionary key.
Agent: I see the issue. You're using get_value() instead of get() or [] syntax.
User: That fixed it! Thanks for your help."""
    
    show_compression_example(
        conversation, 
        "conversation", 
        "🗣️  Conversation Compression"
    )
    
    # Example 2: Code
    code = '''import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

def load_and_prepare_data(file_path):
    """Load and prepare data for machine learning."""
    # Load data
    df = pd.read_csv(file_path)
    
    # Data preprocessing
    df = df.dropna()  # Remove missing values
    df = df.drop_duplicates()  # Remove duplicates
    
    # Handle categorical variables
    df = pd.get_dummies(df, columns=categorical_columns, drop_first=True)
    
    return df'''
    
    show_compression_example(
        code, 
        "code", 
        "💻 Code Compression"
    )
    
    # Example 3: Error
    error = '''Traceback (most recent call last):
  File "/Users/user/project/main.py", line 45, in <module>
    result = process_data(input_file)
  File "/Users/user/project/utils.py", line 23, in process_data
    data = json.load(f)
  File "/usr/local/lib/python3.9/json/__init__.py", line 293, in load
    return loads(fp.read(),
  File "/usr/local/lib/python3.9/json/__init__.py", line 346, in loads
    return _default_decoder.decode(s)
  File "/usr/local/lib/python3.9/json/decoder.py", line 355, in raw_decode
    raise JSONDecodeError("Expecting value", s, err.value) from None
json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)'''
    
    show_compression_example(
        error, 
        "error", 
        "❌ Error Compression"
    )
    
    # Example 4: Solution
    solution = '''To fix the JSON parsing error, follow these steps:

Step 1: Validate the file exists
Check if the file path is correct and the file exists.

Step 2: Add proper error handling
```python
try:
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data
except FileNotFoundError:
    print(f"File not found: {file_path}")
    return None
except json.JSONDecodeError as e:
    print(f"Invalid JSON: {e}")
    return None
```

Step 3: Test the solution
Test with various JSON files to ensure robustness.'''
    
    show_compression_example(
        solution, 
        "solution", 
        "✅ Solution Compression"
    )
    
    print("\n" + "="*70)
    print("✅ All compression demonstrations completed!")
    print("\nKey Compression Strategies:")
    print("• Conversation: Extract key dialogue points, remove pleasantries")
    print("• Code: Preserve structural elements (imports, functions, classes)")
    print("• Error: Keep file references and error messages")
    print("• Solution: Maintain step-by-step structure and code examples")


if __name__ == "__main__":
    main()