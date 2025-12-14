# Memory Compression Module

Intelligent memory management for code agents with type-specific compression strategies.

## Quick Start

```python
from memory.memory_compression import compress_memory, search_compressed_memories

# Compress a memory
result = compress_memory("User: How do I fix this? Agent: Use data.get('key')", "conversation")

# Search memories
results = search_compressed_memories("flask", "code", limit=3)
```

## Core Functions

- `compress_memory(content, memory_type, context)` - Compress single memory
- `search_compressed_memories(query, memory_type, limit)` - Search with relevance ranking
- `get_memory_compression_stats()` - Get usage statistics
- `batch_compress_memories(memories)` - Batch compression
- `generate_memory_summary(summary_type)` - Generate summaries

## Compression Types

| Type | Strategy | Ratio | Preserves |
|------|----------|-------|-----------|
| conversation | Key dialogue extraction | 40-60% | Important exchanges |
| code | Structural patterns | 50-70% | Imports, functions, classes |
| error | Critical info extraction | 60-80% | File paths, error types |
| solution | Step-by-step extraction | 50-70% | Key steps, code examples |
| context | Smart truncation | 40-60% | Beginning/end sections |

## Testing

```bash
python3 tools/test_memory_compression.py              # Basic tests
python3 tools/examples/memory_compression_usage.py    # Usage examples
python3 tools/examples/compression_simple_demo.py     # Strategy demos
```

## Integration

Module is integrated into main agent - tools available automatically.

## Performance

- 30-70% space savings typical
- Fast indexed search
- Automatic memory cleanup
- Supports 1000+ memories