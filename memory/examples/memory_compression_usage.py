#!/usr/bin/env python3
"""
Example usage of memory compression in code agent workflows

This script demonstrates how to use the memory compression module
in realistic code agent scenarios.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from memory.memory_compression import (
    compress_memory, search_compressed_memories, get_memory_compression_stats,
    generate_memory_summary, batch_compress_memories
)


def scenario_1_debugging_session():
    """Scenario 1: Compressing a debugging session."""
    print("🔧 Scenario 1: Debugging Session Memory Compression")
    print("=" * 60)
    
    # Simulate a debugging conversation
    debug_conversation = """
    User: I'm getting an AttributeError when trying to access a dictionary key.
    Agent: Let me see the error message and your code.
    User: Here's the error: AttributeError: 'dict' object has no attribute 'get_value'
    Agent: I see the issue. You're using get_value() instead of get() or [] syntax.
    User: Oh, I see. How should I fix it?
    Agent: Use data.get('key') or data['key'] instead of data.get_value('key')
    User: That fixed it! Thanks for the help.
    """
    
    # Compress the debugging session
    memory_id = compress_memory(debug_conversation, "conversation", 
                               context={"topic": "debugging", "error_type": "AttributeError"})
    print(f"Debug session compressed: {memory_id}")
    
    # Later, search for similar debugging issues
    search_results = search_compressed_memories("AttributeError", "conversation")
    print(f"Found {len(search_results)} similar debugging sessions")
    
    return memory_id


def scenario_2_code_review():
    """Scenario 2: Compressing code review feedback."""
    print("👀 Scenario 2: Code Review Memory Compression")
    print("=" * 60)
    
    # Code review feedback
    code_review = """
    Code Review for user_auth.py:
    
    Issues found:
    1. Missing input validation for email addresses
    2. Password hashing not implemented (storing plain text passwords)
    3. No rate limiting on login attempts
    4. SQL injection vulnerability in user lookup query
    
    Recommendations:
    1. Add email validation using regex pattern
    2. Implement bcrypt for password hashing
    3. Add rate limiting with Flask-Limiter
    4. Use parameterized queries to prevent SQL injection
    
    Example fixes:
    - Use re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email)
    - Implement bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    - Add @limiter.limit("5 per minute") decorator
    - Use cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    """
    
    # Compress the code review
    memory_id = compress_memory(code_review, "solution",
                               context={"topic": "security", "file": "user_auth.py"})
    print(f"Code review compressed: {memory_id}")
    
    # Search for security-related reviews
    security_reviews = search_compressed_memories("security", "solution")
    print(f"Found {len(security_reviews)} security-related reviews")
    
    return memory_id


def scenario_3_error_analysis():
    """Scenario 3: Compressing error analysis and resolution."""
    print("🐛 Scenario 3: Error Analysis Memory Compression")
    print("=" * 60)
    
    # Error analysis session
    error_analysis = """
    Error: ImportError: cannot import name 'DataFrame' from 'pandas'
    
    Root Cause Analysis:
    1. Pandas installation is corrupted or incomplete
    2. Version conflict with other packages
    3. Circular import issue
    4. Virtual environment issues
    
    Resolution Steps:
    1. Check pandas installation: pip show pandas
    2. Reinstall pandas: pip uninstall pandas && pip install pandas
    3. Check for version conflicts: pip list | grep pandas
    4. Verify virtual environment is activated
    5. Check Python path: import sys; print(sys.path)
    6. Try importing in clean environment
    
    Prevention:
    - Use requirements.txt for dependency management
    - Pin package versions to avoid conflicts
    - Test imports in isolated environments
    - Use virtual environments for each project
    """
    
    # Compress the error analysis
    memory_id = compress_memory(error_analysis, "error",
                               context={"error_type": "ImportError", "package": "pandas"})
    print(f"Error analysis compressed: {memory_id}")
    
    # Search for similar errors
    pandas_errors = search_compressed_memories("pandas", "error")
    print(f"Found {len(pandas_errors)} pandas-related errors")
    
    return memory_id


def scenario_4_project_context():
    """Scenario 4: Maintaining project context across sessions."""
    print("📁 Scenario 4: Project Context Memory Compression")
    print("=" * 60)
    
    # Project setup information
    project_context = """
    Project: E-commerce Recommendation System
    
    Tech Stack:
    - Backend: Python Flask, PostgreSQL, Redis
    - Frontend: React, TypeScript, Tailwind CSS
    - ML: scikit-learn, TensorFlow, Pandas
    - Infrastructure: Docker, AWS, GitHub Actions
    
    Project Structure:
    /src
      /backend
        /api          # REST API endpoints
        /models       # Database models
        /services     # Business logic
        /ml           # Machine learning models
      /frontend
        /components   # React components
        /pages        # Page components
        /services     # API service layers
      /shared
        /types        # TypeScript type definitions
        /utils        # Shared utilities
    
    Key Features:
    1. User authentication and authorization
    2. Product catalog with search and filtering
    3. Recommendation engine using collaborative filtering
    4. Shopping cart and checkout process
    5. Order tracking and history
    6. Admin dashboard for product management
    
    Current Status:
    - Authentication system: Complete
    - Product catalog: 80% complete
    - Recommendation engine: In development
    - Frontend: 60% complete
    """
    
    # Compress project context
    memory_id = compress_memory(project_context, "context",
                               context={"project": "ecommerce", "type": "recommendation_system"})
    print(f"Project context compressed: {memory_id}")
    
    return memory_id


def scenario_5_batch_compression():
    """Scenario 5: Batch compression of related memories."""
    print("📦 Scenario 5: Batch Memory Compression")
    print("=" * 60)
    
    # Multiple related memories from a coding session
    session_memories = [
        {
            "content": "User: I need help implementing a REST API with Flask. Agent: I'll help you create a Flask REST API. Let's start with the basic setup.",
            "type": "conversation",
            "context": {"topic": "flask", "subtopic": "rest_api"}
        },
        {
            "content": "from flask import Flask, jsonify, request\n\napp = Flask(__name__)\n\n@app.route('/api/users', methods=['GET'])\ndef get_users():\n    users = [{'id': 1, 'name': 'John'}, {'id': 2, 'name': 'Jane'}]\n    return jsonify(users)",
            "type": "code",
            "context": {"topic": "flask", "subtopic": "rest_api", "file": "app.py"}
        },
        {
            "content": "Error: 404 Not Found when accessing /api/users. Solution: Make sure the Flask app is running and the route is properly defined. Check the URL and HTTP method.",
            "type": "error",
            "context": {"topic": "flask", "subtopic": "rest_api", "error_type": "404"}
        },
        {
            "content": "To test the Flask API: 1) Start the server: flask run 2) Test with curl: curl http://localhost:5000/api/users 3) Or use a tool like Postman for testing",
            "type": "solution",
            "context": {"topic": "flask", "subtopic": "rest_api", "type": "testing"}
        }
    ]
    
    # Batch compress all memories
    result = batch_compress_memories(session_memories)
    print(f"Batch compression result: {result}")
    
    # Search for Flask-related memories
    flask_memories = search_compressed_memories("flask")
    print(f"Found {len(flask_memories)} Flask-related memories")
    
    return flask_memories


def demonstrate_advanced_features():
    """Demonstrate advanced memory compression features."""
    print("🚀 Advanced Memory Compression Features")
    print("=" * 60)
    
    # Generate a comprehensive summary
    summary_id = generate_memory_summary('session')
    print(f"Generated session summary: {summary_id}")
    
    # Get compression statistics (this returns a formatted string)
    stats_text = get_memory_compression_stats()
    print(f"\nCompression Statistics:")
    print(stats_text)
    
    # Search across all memory types
    python_memories = search_compressed_memories("Python", limit=10)
    print(f"\nFound {len(python_memories)} memories mentioning Python")
    
    # Search by memory type
    code_memories = search_compressed_memories("def", "code")
    print(f"Found {len(code_memories)} code memories containing 'def'")


def main():
    """Run all scenarios."""
    print("🎯 Memory Compression Usage Examples")
    print("=" * 70)
    print()
    
    # Run scenarios
    scenario_1_debugging_session()
    print()
    
    scenario_2_code_review()
    print()
    
    scenario_3_error_analysis()
    print()
    
    scenario_4_project_context()
    print()
    
    scenario_5_batch_compression()
    print()
    
    demonstrate_advanced_features()
    print()
    
    print("✅ All scenarios completed!")
    print("The memory compression system helps maintain context across")
    print("long coding sessions while optimizing storage efficiency.")


if __name__ == "__main__":
    main()