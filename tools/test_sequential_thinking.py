#!/usr/bin/env python3
"""
Test script for sequential thinking implementation
"""

from sequential_thinking import sequential_thinking, reset_sequential_thinking, get_thinking_history

def test_sequential_thinking():
    """Test the sequential thinking implementation"""
    print("🧪 Testing Sequential Thinking Implementation")
    print("=" * 50)
    
    # Reset for clean test
    print(reset_sequential_thinking())
    print()
    
    # Test 1: Basic thought
    print("Test 1: Basic thought")
    result1 = sequential_thinking(
        thought="I need to analyze this problem step by step. First, let me understand what we're trying to solve.",
        thought_number=1,
        total_thoughts=5
    )
    print(result1)
    print()
    
    # Test 2: Thought with hypothesis
    print("Test 2: Thought with hypothesis")
    result2 = sequential_thinking(
        thought="Based on my analysis, I hypothesize that the solution involves breaking down the problem into smaller components. Hypothesis: We can solve this by modular approach.",
        thought_number=2,
        total_thoughts=5
    )
    print(result2)
    print()
    
    # Test 3: Revision thought
    print("Test 3: Revision thought")
    result3 = sequential_thinking(
        thought="Actually, let me revise my previous approach. I think we need to consider the edge cases first before breaking down the problem.",
        thought_number=3,
        total_thoughts=5,
        is_revision=True,
        revises_thought=2
    )
    print(result3)
    print()
    
    # Test 4: Branching thought
    print("Test 4: Branching thought")
    result4 = sequential_thinking(
        thought="Let me explore an alternative approach. What if we consider this from a different angle? Branch analysis: Maybe we should look at the performance implications first.",
        thought_number=4,
        total_thoughts=5,
        branch_from_thought=3,
        branch_id="performance_analysis"
    )
    print(result4)
    print()
    
    # Test 5: Final thought
    print("Test 5: Final thought")
    result5 = sequential_thinking(
        thought="After considering all approaches, I believe the best solution is to implement a hybrid approach that combines modular design with performance optimization. Final answer: Implement sequential thinking with comprehensive analysis capabilities.",
        thought_number=5,
        total_thoughts=5,
        needs_more_thoughts=False
    )
    print(result5)
    print()
    
    # Get complete history
    print("📊 Complete Thinking History:")
    print(get_thinking_history())

if __name__ == "__main__":
    test_sequential_thinking()