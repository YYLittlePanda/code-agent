#!/usr/bin/env python3
"""
Simple test script for memory compression module
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from memory.memory_compression import (
    compress_memory, search_compressed_memories, get_memory_compression_stats,
    generate_memory_summary, reset_memory_compression, batch_compress_memories,
    _memory_compressor
)


def test_basic_compression():
    """Test basic memory compression."""
    print("🧪 Testing Basic Memory Compression")
    print("=" * 50)
    
    # Test conversation compression
    conversation = "User: How do I fix this Python error? Agent: Let me help you analyze the error message and provide a solution. First, I need to see the complete error traceback."
    result1 = compress_memory(conversation, "conversation")
    print(f"Conversation compression: {result1}")
    
    # Test code compression
    code = "def hello_world(): print('Hello, World!')"
    result2 = compress_memory(code, "code")
    print(f"Code compression: {result2}")
    
    # Test error compression
    error = "ValueError: invalid literal for int() with base 10: 'abc'"
    result3 = compress_memory(error, "error")
    print(f"Error compression: {result3}")
    
    print()


def test_search():
    """Test memory search functionality."""
    print("🔍 Testing Memory Search")
    print("=" * 50)
    
    # Test search
    results = search_compressed_memories("Python", limit=5)
    print(f"Search results: {results}")
    print()


def test_statistics():
    """Test compression statistics."""
    print("📊 Testing Compression Statistics")
    print("=" * 50)
    
    stats = get_memory_compression_stats()
    print(stats)
    print()


def test_batch_compression():
    """Test batch compression."""
    print("📦 Testing Batch Compression")
    print("=" * 50)
    
    memories = [
        {"content": "Memory 1: Simple test content", "type": "conversation"},
        {"content": "Memory 2: Another test content", "type": "code"},
    ]
    
    result = batch_compress_memories(memories)
    print(f"Batch result: {result}")
    print()


def test_summary():
    """Test summary generation."""
    print("📝 Testing Summary Generation")
    print("=" * 50)
    
    summary_id = generate_memory_summary('session')
    print(f"Summary generated: {summary_id}")
    print()


def main():
    """Run all tests."""
    print("🚀 Testing Memory Compression Module - Simple Version")
    print("=" * 60)
    print()
    
    # Reset memory compression first
    reset_memory_compression()
    
    # Run tests
    test_basic_compression()
    test_search()
    test_statistics()
    test_batch_compression()
    test_summary()
    
    print("✅ All tests completed!")
    print(f"Total memories: {len(_memory_compressor.compressed_memories)}")


if __name__ == "__main__":
    main()