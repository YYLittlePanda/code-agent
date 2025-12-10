# Custom Grep Tool Implementation

This is a complete implementation of the `custom_grep` tool based on the provided documentation. The tool provides a Python interface to ripgrep functionality with various search and filtering options.

## Features

- **Pattern Matching**: Support for regular expressions using ripgrep syntax
- **File Filtering**: Filter by glob patterns or file types
- **Multiple Output Modes**: 
  - `content`: Show matching lines with optional context
  - `files_with_matches`: Show only file paths containing matches
  - `count`: Show match counts per file
- **Context Display**: Show lines before/after matches (B, A, C parameters)
- **Line Numbers**: Option to display line numbers (n parameter)
- **Case Sensitivity**: Case-sensitive or case-insensitive search (i parameter)
- **Multiline Mode**: Support for patterns spanning multiple lines
- **Result Limiting**: Limit number of results returned

## Usage

### Basic Usage

```python
from tools.grep.custom_grep_implementation import custom_grep

# Search for files containing "hello"
result = custom_grep("hello", output_mode="files_with_matches", i=True)
print(result)

# Search with content and line numbers
result = custom_grep("def", type="py", output_mode="content", n=True)
print(result)

# Count matches
result = custom_grep("import", output_mode="count")
print(result)
```

### Advanced Usage

```python
# Search with context
result = custom_grep("function", C=2, output_mode="content", n=True)

# Case-insensitive search with head limit
result = custom_grep("error", i=True, head_limit=10, output_mode="content")

# Search specific file types
result = custom_grep("class", type="py", output_mode="files_with_matches")
```

## Parameters

- `pattern` (str): Regular expression pattern to search for
- `path` (str): Directory or file to search in (default: current directory)
- `glob` (str, optional): Glob pattern for file filtering
- `output_mode` (str): Output format - "content", "files_with_matches", or "count"
- `B` (int, optional): Lines to show before each match (content mode only)
- `A` (int, optional): Lines to show after each match (content mode only)
- `C` (int, optional): Lines to show before and after each match (content mode only)
- `n` (bool): Show line numbers (content mode only)
- `i` (bool): Case-insensitive search
- `type` (str, optional): File type to search (e.g., "py", "js", "txt")
- `head_limit` (int, optional): Maximum number of results to return
- `multiline` (bool): Enable multiline pattern matching

## Requirements

- Python 3.6+
- ripgrep (`rg` command) installed on the system

## Installation

1. Install ripgrep:
   ```bash
   # Ubuntu/Debian
   sudo apt install ripgrep
   
   # macOS
   brew install ripgrep
   
   # Windows
   choco install ripgrep
   ```

2. Use the implementation:
   ```python
   from tools.grep.custom_grep_implementation import custom_grep
   ```

## Error Handling

The implementation includes comprehensive error handling for:
- Missing ripgrep installation
- Invalid parameters
- Search timeouts
- File access issues

## Testing

Run the demonstration to see all features in action:

```python
from tools.grep.custom_grep_implementation import demonstrate_usage

demonstrate_usage()
```

This will create sample files and demonstrate various search scenarios.