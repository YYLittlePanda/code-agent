#!/usr/bin/env python3
"""
Memory Compression Module for Code Agent

This module provides memory compression and management capabilities for code agents,
helping to maintain efficient context while preserving important information.
"""

import json
import hashlib
import time
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
import re
from collections import deque


@dataclass
class CompressedMemory:
    """Represents a compressed memory entry."""
    memory_id: str
    timestamp: str
    memory_type: str  # 'conversation', 'code', 'error', 'solution', 'context'
    original_content: str
    compressed_content: str
    key_entities: List[str]
    importance_score: float
    compression_ratio: float
    metadata: Dict[str, Any]


@dataclass
class MemorySummary:
    """Represents a summary of memory patterns."""
    summary_id: str
    timestamp: str
    summary_type: str  # 'session', 'task', 'project'
    key_points: List[str]
    entities: List[str]
    patterns: List[str]
    decisions: List[str]
    compressed_memories: List[str]  # memory_ids


class MemoryCompressor:
    """
    Advanced memory compression system for code agents.
    Provides intelligent compression while preserving critical information.
    """
    
    def __init__(self, 
                 max_memory_size: int = 1000,
                 compression_threshold: float = 0.7,
                 importance_threshold: float = 0.5):
        self.max_memory_size = max_memory_size
        self.compression_threshold = compression_threshold
        self.importance_threshold = importance_threshold
        
        # Storage
        self.compressed_memories: Dict[str, CompressedMemory] = {}
        self.memory_summaries: Dict[str, MemorySummary] = {}
        self.recent_memories = deque(maxlen=100)  # Keep recent memories for quick access
        
        # Statistics
        self.total_original_size = 0
        self.total_compressed_size = 0
        self.compression_count = 0
        
        # Compression patterns
        self.code_patterns = {
            'import': r'^(import|from)\s+\w+',
            'function_def': r'^def\s+\w+',
            'class_def': r'^class\s+\w+',
            'variable_assignment': r'^\w+\s*=\s*',
            'error_traceback': r'Traceback.*Error:|File ".*".*line \d+',
            'test_result': r'(PASSED|FAILED|ERROR|SKIPPED)',
        }
        
    def compress_memory(self, 
                       content: str,
                       memory_type: str,
                       context: Optional[Dict[str, Any]] = None) -> str:
        """
        Compress memory content based on type and importance.
        
        Args:
            content: Original memory content
            memory_type: Type of memory (conversation, code, error, etc.)
            context: Additional context for compression
            
        Returns:
            Compressed memory ID
        """
        # Generate memory ID
        memory_id = self._generate_memory_id(content)
        
        # Analyze content importance
        importance_score = self._calculate_importance(content, memory_type, context)
        
        # Compress based on type
        compressed_content = self._compress_by_type(content, memory_type)
        
        # Extract key entities
        key_entities = self._extract_entities(content, memory_type)
        
        # Calculate compression ratio
        compression_ratio = len(compressed_content) / len(content) if content else 1.0
        
        # Create compressed memory
        compressed_memory = CompressedMemory(
            memory_id=memory_id,
            timestamp=datetime.now().isoformat(),
            memory_type=memory_type,
            original_content=content,
            compressed_content=compressed_content,
            key_entities=key_entities,
            importance_score=importance_score,
            compression_ratio=compression_ratio,
            metadata=context or {}
        )
        
        # Store memory
        self.compressed_memories[memory_id] = compressed_memory
        self.recent_memories.append(memory_id)
        
        # Update statistics
        self.total_original_size += len(content)
        self.total_compressed_size += len(compressed_content)
        self.compression_count += 1
        
        # Check if cleanup is needed
        if len(self.compressed_memories) > self.max_memory_size:
            self._cleanup_old_memories()
        
        return memory_id
    
    def _generate_memory_id(self, content: str) -> str:
        """Generate unique memory ID based on content hash."""
        content_hash = hashlib.md5(content.encode()).hexdigest()
        timestamp = str(int(time.time() * 1000))
        return f"mem_{content_hash[:8]}_{timestamp}"
    
    def _calculate_importance(self, 
                            content: str, 
                            memory_type: str,
                            context: Optional[Dict[str, Any]] = None) -> float:
        """
        Calculate importance score for memory content.
        
        Factors considered:
        - Content length (longer = more important)
        - Error presence (errors = high importance)
        - Code complexity
        - Context relevance
        - Recency factor
        """
        importance_factors = []
        
        # Length factor
        length_score = min(len(content) / 1000, 1.0)  # Normalize to 0-1
        importance_factors.append(length_score * 0.2)
        
        # Error factor
        error_keywords = ['error', 'exception', 'failed', 'traceback', 'bug', 'fix']
        error_score = sum(1 for keyword in error_keywords if keyword.lower() in content.lower()) / len(error_keywords)
        importance_factors.append(min(error_score, 1.0) * 0.3)
        
        # Code complexity factor
        if memory_type == 'code':
            complexity_score = self._calculate_code_complexity(content)
            importance_factors.append(complexity_score * 0.2)
        
        # Context relevance factor
        if context and 'relevance' in context:
            importance_factors.append(context['relevance'] * 0.2)
        
        # Recency factor (will be updated when accessed)
        importance_factors.append(0.1)
        
        return sum(importance_factors)
    
    def _calculate_code_complexity(self, code: str) -> float:
        """Calculate code complexity score."""
        complexity_indicators = [
            (r'def\s+\w+', 0.1),  # Function definitions
            (r'class\s+\w+', 0.15),  # Class definitions
            (r'if\s+.*:', 0.05),  # Conditional statements
            (r'for\s+.*:', 0.05),  # Loops
            (r'while\s+.*:', 0.05),  # While loops
            (r'try:', 0.1),  # Exception handling
            (r'import\s+\w+', 0.02),  # Imports
            (r'#.*TODO|FIXME|NOTE', 0.1),  # Comments with intent
        ]
        
        total_score = 0.0
        for pattern, weight in complexity_indicators:
            matches = len(re.findall(pattern, code, re.MULTILINE))
            total_score += min(matches * weight, 0.5)  # Cap each factor
        
        return min(total_score, 1.0)
    
    def _compress_by_type(self, content: str, memory_type: str) -> str:
        """Compress content based on memory type."""
        if memory_type == 'conversation':
            return self._compress_conversation(content)
        elif memory_type == 'code':
            return self._compress_code(content)
        elif memory_type == 'error':
            return self._compress_error(content)
        elif memory_type == 'solution':
            return self._compress_solution(content)
        else:
            return self._compress_generic(content)
    
    def _compress_conversation(self, content: str) -> str:
        """Compress conversation content."""
        # Extract key sentences and entities
        sentences = content.split('.')
        key_sentences = []
        
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) > 10:  # Substantial sentences
                # Look for important keywords
                important_words = ['understand', 'need', 'should', 'must', 'important', 'key', 'solution', 'problem']
                if any(word in sentence.lower() for word in important_words):
                    key_sentences.append(sentence)
        
        # Keep first few and last few sentences for context
        if len(sentences) > 10:
            compressed = sentences[:3] + ['[...]'] + key_sentences + ['[...]'] + sentences[-3:]
        else:
            compressed = sentences
        
        return '. '.join(compressed)
    
    def _compress_code(self, code: str) -> str:
        """Compress code content."""
        lines = code.split('\n')
        compressed_lines = []
        
        # Keep important code elements
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):  # Skip empty lines and comments
                continue
                
            # Keep important patterns
            for pattern_name, pattern in self.code_patterns.items():
                if re.match(pattern, line):
                    compressed_lines.append(line)
                    break
        
        # Add structure indicators
        if len(lines) > len(compressed_lines) * 2:
            compressed_lines.insert(0, f"# Code compressed: {len(lines)} -> {len(compressed_lines)} lines")
        
        return '\n'.join(compressed_lines)
    
    def _compress_error(self, error_content: str) -> str:
        """Compress error content."""
        # Extract key error information
        lines = error_content.split('\n')
        key_lines = []
        
        for line in lines:
            line = line.strip()
            # Keep error messages and file references
            if any(keyword in line.lower() for keyword in ['error:', 'exception:', 'traceback', 'file "', 'line']):
                key_lines.append(line)
            # Keep unique error patterns
            elif re.search(r'[A-Z][a-z]+Error:', line):
                key_lines.append(line)
        
        # Limit to prevent excessive compression
        if len(key_lines) > 20:
            key_lines = key_lines[:10] + [f'[... {len(key_lines) - 20} more error lines ...]'] + key_lines[-10:]
        
        return '\n'.join(key_lines) if key_lines else error_content[:500] + '...'
    
    def _compress_solution(self, solution: str) -> str:
        """Compress solution content."""
        # Extract key solution steps
        lines = solution.split('\n')
        key_steps = []
        
        for i, line in enumerate(lines):
            line = line.strip()
            # Look for numbered steps or bullet points
            if re.match(r'^\d+\.|^[-*+]\s', line):
                key_steps.append(line)
            # Look for action words
            elif any(word in line.lower() for word in ['step', 'solution', 'fix', 'implement', 'change', 'add', 'remove']):
                key_steps.append(line)
        
        # Keep introduction and conclusion
        if len(lines) > len(key_steps) * 2:
            compressed = lines[:2] + key_steps + lines[-2:]
        else:
            compressed = key_steps
        
        return '\n'.join(compressed)
    
    def _compress_generic(self, content: str) -> str:
        """Generic compression for unknown types."""
        # Simple truncation with ellipsis for very long content
        if len(content) > 500:
            return content[:250] + '\n[... compressed ...]\n' + content[-250:]
        return content
    
    def _extract_entities(self, content: str, memory_type: str) -> List[str]:
        """Extract key entities from content."""
        entities = []
        
        if memory_type == 'code':
            # Extract function names, class names, variables
            patterns = [
                (r'def\s+(\w+)', 'function'),
                (r'class\s+(\w+)', 'class'),
                (r'^(\w+)\s*=', 'variable'),
                (r'import\s+(\w+)', 'module'),
            ]
            for pattern, entity_type in patterns:
                matches = re.findall(pattern, content, re.MULTILINE)
                entities.extend([f"{entity_type}:{match}" for match in matches])
        
        elif memory_type == 'error':
            # Extract error types and file names
            error_matches = re.findall(r'([A-Z][a-zA-Z]*Error)', content)
            file_matches = re.findall(r'File "([^"]+)"', content)
            entities.extend(error_matches)
            entities.extend([f"file:{f}" for f in file_matches])
        
        else:
            # Generic entity extraction
            # Look for quoted strings, code-like patterns, and technical terms
            quoted_matches = re.findall(r'"([^"]+)"', content)
            code_matches = re.findall(r'`([^`]+)`', content)
            technical_terms = re.findall(r'\b[A-Z][a-zA-Z]+\b', content)
            
            entities.extend(quoted_matches)
            entities.extend(code_matches)
            entities.extend(technical_terms[:10])  # Limit technical terms
        
        # Remove duplicates and limit total
        entities = list(set(entities))
        return entities[:20]  # Limit to prevent excessive entities
    
    def get_memory(self, memory_id: str) -> Optional[CompressedMemory]:
        """Retrieve compressed memory by ID."""
        return self.compressed_memories.get(memory_id)
    
    def search_memories(self, 
                       query: str,
                       memory_type: Optional[str] = None,
                       limit: int = 10) -> List[CompressedMemory]:
        """
        Search compressed memories by query.
        
        Args:
            query: Search query
            memory_type: Optional memory type filter
            limit: Maximum results to return
            
        Returns:
            List of matching compressed memories
        """
        results = []
        query_lower = query.lower()
        
        for memory in self.compressed_memories.values():
            # Type filter
            if memory_type and memory.memory_type != memory_type:
                continue
            
            # Search in content and entities
            search_score = 0
            
            # Content search
            if query_lower in memory.compressed_content.lower():
                search_score += 1.0
            
            # Entity search
            for entity in memory.key_entities:
                if query_lower in entity.lower():
                    search_score += 0.5
                    break
            
            # Importance boost
            search_score += memory.importance_score * 0.3
            
            if search_score > 0:
                results.append((search_score, memory))
        
        # Sort by score and return top results
        results.sort(key=lambda x: x[0], reverse=True)
        return [memory for _, memory in results[:limit]]
    
    def generate_summary(self, 
                        summary_type: str = 'session',
                        memory_ids: Optional[List[str]] = None) -> str:
        """
        Generate memory summary for a session or task.
        
        Args:
            summary_type: Type of summary ('session', 'task', 'project')
            memory_ids: Specific memory IDs to include, or None for recent memories
            
        Returns:
            Summary ID
        """
        if memory_ids is None:
            # Use recent memories
            memory_ids = list(self.recent_memories)
        
        # Collect memories
        memories = [self.compressed_memories[mid] for mid in memory_ids if mid in self.compressed_memories]
        
        if not memories:
            return ""
        
        # Extract key points
        key_points = []
        entities = set()
        patterns = []
        decisions = []
        
        for memory in memories:
            # Extract key points from compressed content
            content_lines = memory.compressed_content.split('\n')
            for line in content_lines:
                if len(line.strip()) > 20:  # Substantial content
                    key_points.append(line.strip())
            
            # Collect entities
            entities.update(memory.key_entities)
            
            # Look for decisions and patterns
            if memory.memory_type == 'solution':
                decisions.extend([f"{memory.memory_type}:{point}" for point in key_points[-3:]])
        
        # Generate summary ID
        summary_id = f"summary_{summary_type}_{int(time.time() * 1000)}"
        
        # Create memory summary
        memory_summary = MemorySummary(
            summary_id=summary_id,
            timestamp=datetime.now().isoformat(),
            summary_type=summary_type,
            key_points=key_points[:10],  # Limit key points
            entities=list(entities)[:15],  # Limit entities
            patterns=patterns,
            decisions=decisions,
            compressed_memories=memory_ids
        )
        
        # Store summary
        self.memory_summaries[summary_id] = memory_summary
        
        return summary_id
    
    def get_summary(self, summary_id: str) -> Optional[MemorySummary]:
        """Retrieve memory summary by ID."""
        return self.memory_summaries.get(summary_id)
    
    def get_compression_stats(self) -> Dict[str, Any]:
        """Get compression statistics."""
        if self.compression_count == 0:
            return {
                "total_memories": 0,
                "compression_ratio": 0.0,
                "space_saved": "0%",
                "avg_importance_score": 0.0
            }
        
        overall_compression_ratio = self.total_compressed_size / self.total_original_size if self.total_original_size > 0 else 0
        space_saved = (1 - overall_compression_ratio) * 100
        avg_importance = sum(m.importance_score for m in self.compressed_memories.values()) / len(self.compressed_memories)
        
        return {
            "total_memories": len(self.compressed_memories),
            "compression_ratio": overall_compression_ratio,
            "space_saved": f"{space_saved:.1f}%",
            "avg_importance_score": avg_importance,
            "total_original_size": self.total_original_size,
            "total_compressed_size": self.total_compressed_size,
            "memory_types": self._get_memory_type_distribution()
        }
    
    def _get_memory_type_distribution(self) -> Dict[str, int]:
        """Get distribution of memory types."""
        distribution = {}
        for memory in self.compressed_memories.values():
            distribution[memory.memory_type] = distribution.get(memory.memory_type, 0) + 1
        return distribution
    
    def _cleanup_old_memories(self):
        """Clean up old memories based on importance and recency."""
        if len(self.compressed_memories) <= self.max_memory_size:
            return
        
        # Sort memories by importance and recency
        memories_with_scores = []
        current_time = time.time()
        
        for memory_id, memory in self.compressed_memories.items():
            # Recency score (older = lower score)
            memory_time = datetime.fromisoformat(memory.timestamp).timestamp()
            recency_score = max(0, 1 - (current_time - memory_time) / (7 * 24 * 3600))  # 1 week decay
            
            # Combined score
            combined_score = memory.importance_score * 0.7 + recency_score * 0.3
            memories_with_scores.append((combined_score, memory_id))
        
        # Sort by score (ascending - lowest scores first)
        memories_with_scores.sort()
        
        # Remove lowest scoring memories
        to_remove = len(self.compressed_memories) - self.max_memory_size
        for _, memory_id in memories_with_scores[:to_remove]:
            if memory_id in self.compressed_memories:
                memory = self.compressed_memories[memory_id]
                self.total_original_size -= len(memory.original_content)
                self.total_compressed_size -= len(memory.compressed_content)
                del self.compressed_memories[memory_id]


# Global instance for the function
_memory_compressor = MemoryCompressor()


def compress_memory(content: str,
                   memory_type: str = 'generic',
                   context: Optional[Dict[str, Any]] = None) -> str:
    """
    Compress memory content for the code agent.
    
    Args:
        content: Memory content to compress
        memory_type: Type of memory ('conversation', 'code', 'error', 'solution', 'context', 'generic')
        context: Optional context information for compression
        
    Returns:
        Memory ID of the compressed memory
        
    Example:
        >>> memory_id = compress_memory("Some long conversation...", "conversation")
        >>> print(f"Memory compressed with ID: {memory_id}")
    """
    global _memory_compressor
    
    try:
        memory_id = _memory_compressor.compress_memory(content, memory_type, context)
        return f"Memory compressed successfully. ID: {memory_id}"
    except Exception as e:
        return f"Error compressing memory: {str(e)}"


def search_compressed_memories(query: str,
                              memory_type: Optional[str] = None,
                              limit: int = 5) -> str:
    """
    Search through compressed memories.
    
    Args:
        query: Search query
        memory_type: Optional memory type filter
        limit: Maximum number of results
        
    Returns:
        Formatted search results
        
    Example:
        >>> results = search_compressed_memories("error handling", "error")
        >>> print(results)
    """
    global _memory_compressor
    
    try:
        memories = _memory_compressor.search_memories(query, memory_type, limit)
        
        if not memories:
            return "No matching memories found."
        
        results = []
        results.append(f"🔍 Found {len(memories)} matching memories:")
        results.append("=" * 50)
        
        for i, memory in enumerate(memories, 1):
            results.append(f"\n{i}. Memory ID: {memory.memory_id}")
            results.append(f"   Type: {memory.memory_type}")
            results.append(f"   Importance: {memory.importance_score:.2f}")
            results.append(f"   Compression: {memory.compression_ratio:.1%}")
            results.append(f"   Content: {memory.compressed_content[:100]}{'...' if len(memory.compressed_content) > 100 else ''}")
            
            if memory.key_entities:
                results.append(f"   Entities: {', '.join(memory.key_entities[:5])}")
        
        return "\n".join(results)
        
    except Exception as e:
        return f"Error searching memories: {str(e)}"


def get_memory_compression_stats() -> str:
    """
    Get memory compression statistics.
    
    Returns:
        Formatted statistics report
        
    Example:
        >>> stats = get_memory_compression_stats()
        >>> print(stats)
    """
    global _memory_compressor
    
    try:
        stats = _memory_compressor.get_compression_stats()
        
        report = []
        report.append("📊 Memory Compression Statistics")
        report.append("=" * 40)
        report.append(f"Total memories: {stats['total_memories']}")
        report.append(f"Compression ratio: {stats['compression_ratio']:.1%}")
        report.append(f"Space saved: {stats['space_saved']}")
        report.append(f"Average importance: {stats['avg_importance_score']:.2f}")
        report.append(f"Original size: {stats['total_original_size']:,} bytes")
        report.append(f"Compressed size: {stats['total_compressed_size']:,} bytes")
        
        if stats['memory_types']:
            report.append("\nMemory type distribution:")
            for mem_type, count in stats['memory_types'].items():
                report.append(f"  {mem_type}: {count}")
        
        return "\n".join(report)
        
    except Exception as e:
        return f"Error getting compression stats: {str(e)}"


def generate_memory_summary(summary_type: str = 'session') -> str:
    """
    Generate a summary of compressed memories.
    
    Args:
        summary_type: Type of summary ('session', 'task', 'project')
        
    Returns:
        Summary ID and summary content
        
    Example:
        >>> summary_id = generate_memory_summary('session')
        >>> print(f"Summary generated: {summary_id}")
    """
    global _memory_compressor
    
    try:
        summary_id = _memory_compressor.generate_summary(summary_type)
        summary = _memory_compressor.get_summary(summary_id)
        
        if not summary:
            return "Error generating summary."
        
        report = []
        report.append(f"📝 Memory Summary Generated")
        report.append(f"Summary ID: {summary_id}")
        report.append(f"Type: {summary.summary_type}")
        report.append(f"Timestamp: {summary.timestamp}")
        report.append(f"Memories included: {len(summary.compressed_memories)}")
        
        if summary.key_points:
            report.append(f"\nKey points ({len(summary.key_points)}):")
            for i, point in enumerate(summary.key_points[:5], 1):
                report.append(f"  {i}. {point}")
        
        if summary.entities:
            report.append(f"\nKey entities: {', '.join(summary.entities[:10])}")
        
        if summary.decisions:
            report.append(f"\nDecisions made: {len(summary.decisions)}")
        
        return "\n".join(report)
        
    except Exception as e:
        return f"Error generating summary: {str(e)}"


def reset_memory_compression() -> str:
    """
    Reset the memory compression system.
    
    Returns:
        Reset confirmation message
        
    Example:
        >>> result = reset_memory_compression()
        >>> print(result)
    """
    global _memory_compressor
    
    try:
        _memory_compressor = MemoryCompressor()
        return "Memory compression system reset successfully."
    except Exception as e:
        return f"Error resetting memory compression: {str(e)}"


# Convenience function for batch memory compression
def batch_compress_memories(memories: List[Dict[str, Any]]) -> str:
    """
    Compress multiple memories at once.
    
    Args:
        memories: List of memory dicts with 'content', 'type', and optional 'context'
        
    Returns:
        Batch compression results
        
    Example:
        >>> memories = [
        ...     {"content": "Long conversation...", "type": "conversation"},
        ...     {"content": "Error traceback...", "type": "error"}
        ... ]
        >>> results = batch_compress_memories(memories)
        >>> print(results)
    """
    global _memory_compressor
    
    try:
        memory_ids = []
        
        for memory in memories:
            content = memory.get('content', '')
            memory_type = memory.get('type', 'generic')
            context = memory.get('context', {})
            
            if content:
                memory_id = _memory_compressor.compress_memory(content, memory_type, context)
                memory_ids.append(memory_id)
        
        return f"Batch compression completed. {len(memory_ids)} memories compressed."
        
    except Exception as e:
        return f"Error in batch compression: {str(e)}"


if __name__ == "__main__":
    # Test the memory compression implementation
    print("Testing memory compression implementation...")
    
    # Test conversation compression
    conversation = """
    User: I need help with a Python function that's not working properly.
    Agent: I'd be happy to help you with your Python function. Could you please share the code that's causing the issue?
    User: Here's the function I'm having trouble with:
    def calculate_average(numbers):
        total = sum(numbers)
        average = total / len(numbers)
        return average
    
    Agent: I see your function. It looks generally correct, but we should add some error handling for edge cases like empty lists.
    User: That's a good point. How would you handle that?
    Agent: You can add a check at the beginning of the function to handle empty lists and avoid division by zero errors.
    """
    
    result1 = compress_memory(conversation, "conversation")
    print(result1)
    
    # Test code compression
    code = """
    import json
    import os
    from typing import List, Dict
    
    def process_data(file_path: str) -> List[Dict]:
        '''Process data from JSON file.'''
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            processed_data = []
            for item in data:
                if 'name' in item and 'value' in item:
                    processed_item = {
                        'name': item['name'].strip(),
                        'value': float(item['value']),
                        'processed': True
                    }
                    processed_data.append(processed_item)
            
            return processed_data
        except FileNotFoundError:
            print(f"File not found: {file_path}")
            return []
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            return []
    """
    
    result2 = compress_memory(code, "code")
    print(result2)
    
    # Test error compression
    error = """
    Traceback (most recent call last):
      File "example.py", line 25, in <module>
        result = divide_numbers(10, 0)
      File "example.py", line 15, in divide_numbers
        return a / b
    ZeroDivisionError: division by zero
    
    During handling of the above exception, another exception occurred:
    
    Traceback (most recent call last):
      File "example.py", line 27, in <module>
        handle_error()
      File "example.py", line 20, in handle_error
        raise ValueError("Cannot divide by zero")
    ValueError: Cannot divide by zero
    """
    
    result3 = compress_memory(error, "error")
    print(result3)
    
    # Test search
    search_results = search_compressed_memories("function", "code")
    print(search_results)
    
    # Test statistics
    stats = get_memory_compression_stats()
    print(stats)
    
    # Test summary generation
    summary = generate_memory_summary('test')
    print(summary)