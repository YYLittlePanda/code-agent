# Memory Compression Module Documentation

## Overview

The Memory Compression Module provides intelligent memory management and compression capabilities for code agents. It helps maintain context across long coding sessions while optimizing storage efficiency by compressing conversations, code snippets, error messages, and solutions.

## Architecture

```
code-agent/
├── tools/
│   ├── memory_compression.py          # Main module
│   ├── test_memory_compression.py     # Test suite
│   └── examples/                      # Usage examples
│       ├── memory_compression_usage.py
│       └── compression_simple_demo.py
└── docs/
    └── memory_compression_comprehensive.md  # This file
```

## Core Features

### Intelligent Compression Engine
- **Type-specific compression strategies** for different content types
- **Importance scoring system** based on multi-factor analysis
- **Entity extraction** for improved searchability
- **Real-time compression statistics** tracking

### Content Types Supported
- `conversation`: User-agent dialogues
- `code`: Code snippets and implementations  
- `error`: Error messages and stack traces
- `solution`: Step-by-step solutions
- `context`: Project and architectural information
- `generic`: Default for unknown types

## API Reference

### Core Functions

#### `compress_memory(content, memory_type='generic', context=None)`
Compress a single memory with specified type and context.

**Parameters:**
- `content` (str): The memory content to compress
- `memory_type` (str): Type of memory (conversation, code, error, etc.)
- `context` (dict): Optional context information for better compression

**Returns:** Success message with memory ID

**Example:**

```python
from memory.memory_compression import compress_memory

result = compress_memory("User: How do I fix this error? Agent: Let me help...",
                         "conversation",
                         context={"topic": "debugging", "error_type": "AttributeError"})
print(result)  # Memory compressed successfully. ID: mem_abc123...
```

#### `search_compressed_memories(query, memory_type=None, limit=5)`
Search through compressed memories with relevance ranking.

**Parameters:**
- `query` (str): Search query
- `memory_type` (str): Optional memory type filter
- `limit` (int): Maximum number of results (default: 5)

**Returns:** Formatted search results

**Example:**

```python
from memory.memory_compression import search_compressed_memories

results = search_compressed_memories("flask", "code", limit=3)
print(results)
```

#### `get_memory_compression_stats()`
Get compression statistics and memory usage information.

**Returns:** Formatted statistics report

**Example:**

```python
from memory.memory_compression import get_memory_compression_stats

stats = get_memory_compression_stats()
print(stats)
```

#### `batch_compress_memories(memories)`
Compress multiple memories efficiently in batch.

**Parameters:**
- `memories` (list): List of memory dictionaries with 'content', 'type', and optional 'context'

**Returns:** Batch compression results

**Example:**

```python
from memory.memory_compression import batch_compress_memories

memories = [
    {"content": "Memory 1...", "type": "conversation"},
    {"content": "Memory 2...", "type": "code", "context": {"file": "app.py"}}
]
result = batch_compress_memories(memories)
print(result)
```

## Compression Strategies

### 1. Conversation Compression
**Strategy**: Key Dialogue Extraction
- Detects important keywords ('understand', 'need', 'should', 'must', 'important', 'key', 'solution', 'problem')
- Retains substantial sentences (>10 characters)
- Preserves first and last sentences for context
- Uses ellipsis for removed content

**Compression Ratio**: 40-60%

### 2. Code Compression  
**Strategy**: Structural Pattern Preservation
- Preserves imports, function/class definitions, key assignments
- Removes non-essential comments and empty lines
- Maintains code structure and signatures

**Compression Ratio**: 50-70%

### 3. Error Compression
**Strategy**: Critical Error Information Extraction  
- Keeps file paths, line numbers, error types
- Truncates redundant stack trace frames
- Preserves error origin and final messages

**Compression Ratio**: 60-80%

### 4. Solution Compression
**Strategy**: Step-by-Step Solution Extraction
- Identifies numbered steps and bullet points
- Preserves code examples within solutions
- Maintains introduction, key steps, and conclusion

**Compression Ratio**: 50-70%

### 5. Context Compression
**Strategy**: Smart Truncation
- Preserves beginning and end sections
- Uses ellipsis for removed middle content
- Retains critical details and key information

**Compression Ratio**: 40-60%

## Importance Scoring System

The module uses a multi-factor importance scoring system:

- **Content Length** (20%): Longer content gets higher scores
- **Error Presence** (30%): Error-related content is prioritized
- **Code Complexity** (20%): Complex code gets higher scores
- **Context Relevance** (20%): Context-provided relevance boosts scores
- **Recency** (10%): Recent content gets slight boost

## Testing

Run the test suite to verify functionality:

```bash
# Basic functionality test
python3 tools/test_memory_compression.py

# Comprehensive usage examples
python3 tools/examples/memory_compression_usage.py

# Simple compression demonstrations  
python3 tools/examples/compression_simple_demo.py
```

## Integration with Code Agent

The memory compression module is integrated into the main code agent. The agent can use memory compression tools alongside other tools:

```python
# The agent automatically has access to memory compression tools
# compress_memory, search_compressed_memories, get_memory_compression_stats, etc.

# Example agent usage:
question = """
I need help with a Python Flask API. 
First, let me search for any previous Flask-related conversations we had.
Then help me implement a simple REST API.
"""

# The agent can:
# 1. Search for previous Flask discussions
# 2. Compress the current conversation  
# 3. Generate session summaries
# 4. Track compression statistics
```

## Performance Metrics

- **Compression Efficiency**: 30-70% space savings typical
- **Search Speed**: Fast indexed search with relevance ranking
- **Memory Management**: Automatic cleanup of low-importance memories
- **Scalability**: Supports up to 1000 memories by default

## Configuration Options

The memory compressor can be configured with:

- `max_memory_size`: Maximum memories to keep (default: 1000)
- `compression_threshold`: Minimum compression ratio (default: 0.7)  
- `importance_threshold`: Minimum importance score (default: 0.5)

## Error Handling

The module includes comprehensive error handling:

```python
try:
    result = compress_memory(content, "conversation")
    print(result)
except Exception as e:
    print(f"Compression failed: {e}")
```

## Best Practices

1. **Choose Appropriate Memory Types**: Use correct types for better compression
2. **Provide Context**: Include relevant context for better searchability  
3. **Batch Related Memories**: Use batch compression for efficiency
4. **Regular Summaries**: Generate summaries for long sessions
5. **Search Before Solving**: Check existing memories for similar problems
6. **Monitor Statistics**: Keep eye on compression efficiency

## Future Enhancements

- **Semantic Search**: Implement semantic similarity search
- **Memory Clustering**: Group related memories automatically  
- **Export/Import**: Backup and restore memory collections
- **Advanced Analytics**: Detailed memory usage analytics
- **Custom Compressors**: User-defined compression strategies