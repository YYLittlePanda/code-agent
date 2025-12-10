#!/usr/bin/env python3
"""
Sequential Thinking Implementation
A detailed tool for dynamic and reflective problem-solving through thoughts.
"""

import json
import time
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class Thought:
    """Represents a single thought in the thinking process."""
    thought: str
    thought_number: int
    timestamp: str
    is_revision: bool = False
    revises_thought: Optional[int] = None
    branch_from_thought: Optional[int] = None
    branch_id: Optional[str] = None
    hypothesis: Optional[str] = None
    hypothesis_verified: Optional[bool] = None
    confidence: Optional[float] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class SequentialThinking:
    """
    A comprehensive sequential thinking system that allows for dynamic,
    reflective problem-solving through structured thought processes.
    """
    
    def __init__(self):
        self.thoughts: List[Thought] = []
        self.total_thoughts: int = 5  # Default minimum
        self.current_branch: Optional[str] = None
        self.branches: Dict[str, List[int]] = {}  # branch_id -> thought_numbers
        self.hypotheses: List[str] = []
        self.final_answer: Optional[str] = None
        self.confidence_level: float = 0.0
        
    def add_thought(self, 
                   thought: str,
                   thought_number: int,
                   total_thoughts: int,
                   is_revision: bool = False,
                   revises_thought: Optional[int] = None,
                   branch_from_thought: Optional[int] = None,
                   branch_id: Optional[str] = None,
                   needs_more_thoughts: bool = False) -> Dict[str, Any]:
        """
        Add a new thought to the thinking process.
        
        Args:
            thought: The current thinking step content
            thought_number: Current number in sequence
            total_thoughts: Current estimate of total thoughts needed
            is_revision: Whether this thought revises previous thinking
            revises_thought: Which thought number is being reconsidered
            branch_from_thought: Branching point if applicable
            branch_id: Identifier for the current branch
            needs_more_thoughts: Whether more thoughts are needed
            
        Returns:
            Dictionary containing the thought result and process status
        """
        # Update total thoughts estimate
        self.total_thoughts = max(total_thoughts, thought_number + 1)
        
        # Handle branching
        if branch_id:
            self.current_branch = branch_id
            if branch_id not in self.branches:
                self.branches[branch_id] = []
            self.branches[branch_id].append(thought_number)
        
        # Create thought object
        thought_obj = Thought(
            thought=thought,
            thought_number=thought_number,
            timestamp=datetime.now().isoformat(),
            is_revision=is_revision,
            revises_thought=revises_thought,
            branch_from_thought=branch_from_thought,
            branch_id=branch_id
        )
        
        # Extract hypothesis if present
        if "hypothesis" in thought.lower() or "solution" in thought.lower():
            thought_obj.hypothesis = self._extract_hypothesis(thought)
            if thought_obj.hypothesis:
                self.hypotheses.append(thought_obj.hypothesis)
        
        # Add to thoughts list
        self.thoughts.append(thought_obj)
        
        # Analyze the thinking process
        analysis = self._analyze_process()
        
        # Generate response
        response = {
            "status": "thinking",
            "thought_number": thought_number,
            "total_thoughts": self.total_thoughts,
            "thought_added": True,
            "analysis": analysis,
            "needs_more_thoughts": needs_more_thoughts,
            "current_thought": thought_obj.to_dict()
        }
        
        # Check if we should conclude
        if not needs_more_thoughts and thought_number >= self.total_thoughts - 1:
            response["status"] = "ready_to_conclude"
            response["final_analysis"] = self._generate_final_analysis()
        
        return response
    
    def _extract_hypothesis(self, thought_text: str) -> Optional[str]:
        """Extract hypothesis from thought text."""
        lines = thought_text.split('\n')
        for line in lines:
            if any(keyword in line.lower() for keyword in ['hypothesis:', 'solution:', 'conclusion:', 'answer:']):
                return line.split(':', 1)[1].strip()
        return None
    
    def _analyze_process(self) -> Dict[str, Any]:
        """Analyze the current thinking process."""
        if not self.thoughts:
            return {"status": "no_thoughts"}
        
        analysis = {
            "total_thoughts": len(self.thoughts),
            "revisions_made": sum(1 for t in self.thoughts if t.is_revision),
            "branches_active": len(self.branches),
            "hypotheses_generated": len(self.hypotheses),
            "thinking_patterns": self._identify_patterns(),
            "confidence_trend": self._calculate_confidence_trend()
        }
        
        return analysis
    
    def _identify_patterns(self) -> List[str]:
        """Identify thinking patterns in the thought process."""
        patterns = []
        
        # Check for revision patterns
        revisions = [t for t in self.thoughts if t.is_revision]
        if len(revisions) > len(self.thoughts) * 0.3:
            patterns.append("high_revision_rate")
        
        # Check for branching patterns
        if len(self.branches) > 2:
            patterns.append("extensive_branching")
        
        # Check for hypothesis evolution
        if len(self.hypotheses) > 1:
            patterns.append("hypothesis_evolution")
        
        # Check for systematic approach
        thought_numbers = [t.thought_number for t in self.thoughts]
        if thought_numbers == sorted(thought_numbers):
            patterns.append("systematic_progression")
        
        return patterns
    
    def _calculate_confidence_trend(self) -> Dict[str, Any]:
        """Calculate confidence trend based on thoughts."""
        confidences = []
        for thought in self.thoughts:
            if thought.confidence is not None:
                confidences.append(thought.confidence)
        
        if not confidences:
            return {"trend": "unknown", "average": None}
        
        return {
            "trend": "increasing" if confidences[-1] > confidences[0] else "stable" if confidences[-1] == confidences[0] else "decreasing",
            "average": sum(confidences) / len(confidences),
            "latest": confidences[-1]
        }
    
    def _generate_final_analysis(self) -> Dict[str, Any]:
        """Generate final analysis of the thinking process."""
        if not self.thoughts:
            return {"error": "no_thoughts_available"}
        
        # Find the most confident hypothesis
        best_hypothesis = None
        best_confidence = 0.0
        
        for thought in self.thoughts:
            if thought.hypothesis and thought.confidence and thought.confidence > best_confidence:
                best_hypothesis = thought.hypothesis
                best_confidence = thought.confidence
        
        # If no confidence-based hypothesis, use the last one
        if not best_hypothesis and self.hypotheses:
            best_hypothesis = self.hypotheses[-1]
        
        # Generate final answer
        self.final_answer = self._synthesize_final_answer()
        self.confidence_level = best_confidence if best_confidence > 0 else 0.7
        
        return {
            "final_hypothesis": best_hypothesis,
            "final_answer": self.final_answer,
            "confidence": self.confidence_level,
            "thinking_summary": self._generate_summary(),
            "key_insights": self._extract_key_insights()
        }
    
    def _synthesize_final_answer(self) -> str:
        """Synthesize the final answer from all thoughts."""
        if not self.thoughts:
            return "No thoughts provided to generate answer."
        
        # Extract key points from thoughts
        key_points = []
        for thought in self.thoughts[-3:]:  # Focus on recent thoughts
            if len(thought.thought) > 20:  # Substantial thoughts
                key_points.append(thought.thought[:200])  # First 200 chars
        
        # Generate synthesis
        synthesis = "Based on the sequential thinking process:\n\n"
        synthesis += "Key insights gathered:\n"
        for i, point in enumerate(key_points, 1):
            synthesis += f"{i}. {point}\n"
        
        if self.hypotheses:
            synthesis += f"\nFinal hypothesis: {self.hypotheses[-1]}"
        
        return synthesis
    
    def _generate_summary(self) -> str:
        """Generate a summary of the thinking process."""
        return f"Thought process completed with {len(self.thoughts)} thoughts, " \
               f"{len([t for t in self.thoughts if t.is_revision])} revisions, " \
               f"and {len(self.hypotheses)} hypotheses generated."
    
    def _extract_key_insights(self) -> List[str]:
        """Extract key insights from the thinking process."""
        insights = []
        
        # Look for insights in recent thoughts
        for thought in self.thoughts[-5:]:
            thought_text = thought.thought.lower()
            if any(word in thought_text for word in ['insight', 'realization', 'discovery', 'understand']):
                insights.append(thought.thought[:150])
        
        return insights[:3]  # Top 3 insights
    
    def get_thinking_history(self) -> Dict[str, Any]:
        """Get the complete thinking history."""
        return {
            "thoughts": [t.to_dict() for t in self.thoughts],
            "branches": self.branches,
            "hypotheses": self.hypotheses,
            "final_answer": self.final_answer,
            "confidence_level": self.confidence_level,
            "analysis": self._analyze_process()
        }
    
    def export_to_json(self) -> str:
        """Export the thinking process to JSON format."""
        return json.dumps(self.get_thinking_history(), indent=2, ensure_ascii=False)


# Global instance for the function
_thinking_instance = SequentialThinking()


def sequential_thinking(thought: str,
                       thought_number: int,
                       total_thoughts: int,
                       is_revision: bool = False,
                       revises_thought: Optional[int] = None,
                       branch_from_thought: Optional[int] = None,
                       branch_id: Optional[str] = None,
                       needs_more_thoughts: bool = False) -> str:
    """
    A detailed tool for dynamic and reflective problem-solving through thoughts.
    This tool helps analyze problems through a flexible thinking process that can adapt and evolve.
    Each thought can build on, question, or revise previous insights as understanding deepens.

    When to use this tool:
    - Breaking down complex problems into steps
    - Planning and design with room for revision
    - Analysis that might need course correction
    - Problems where the full scope might not be clear initially
    - Problems that require a multi-step solution
    - Tasks that need to maintain context over multiple steps
    - Situations where irrelevant information needs to be filtered out

    Key features:
    - You can adjust total_thoughts up or down as you progress
    - You can question or revise previous thoughts
    - You can add more thoughts even after reaching what seemed like the end
    - You can express uncertainty and explore alternative approaches
    - Not every thought needs to build linearly - you can branch or backtrack
    - Generates a solution hypothesis
    - Verifies the hypothesis based on the Chain of Thought steps
    - Repeats the process until satisfied
    - Provides a correct answer

    Args:
        thought: Your current thinking step, which can include:
            * Regular analytical steps
            * Revisions of previous thoughts
            * Questions about previous decisions
            * Realizations about needing more analysis
            * Changes in approach
            * Hypothesis generation
            * Hypothesis verification
        thought_number: Current number in sequence (can go beyond initial total if needed)
        total_thoughts: Current estimate of thoughts needed (can be adjusted up/down)
        is_revision: A boolean indicating if this thought revises previous thinking
        revises_thought: If is_revision is true, which thought number is being reconsidered
        branch_from_thought: If branching, which thought number is the branching point
        branch_id: Identifier for the current branch (if any)
        needs_more_thoughts: If reaching end but realizing more thoughts needed

    Returns:
        String containing the thinking process result and recommendations
    """
    global _thinking_instance
    
    try:
        # Process the thought
        result = _thinking_instance.add_thought(
            thought=thought,
            thought_number=thought_number,
            total_thoughts=total_thoughts,
            is_revision=is_revision,
            revises_thought=revises_thought,
            branch_from_thought=branch_from_thought,
            branch_id=branch_id,
            needs_more_thoughts=needs_more_thoughts
        )
        
        # Format the response
        response_parts = []
        
        # Status header
        if result["status"] == "ready_to_conclude":
            response_parts.append("🎯 THINKING PROCESS COMPLETE")
            response_parts.append("=" * 50)
        else:
            response_parts.append(f"💭 Thought {thought_number + 1}/{result['total_thoughts']}")
            response_parts.append("-" * 30)
        
        # Current thought summary
        response_parts.append(f"Thought added: {thought[:100]}{'...' if len(thought) > 100 else ''}")
        
        # Analysis
        if "analysis" in result:
            analysis = result["analysis"]
            response_parts.append(f"\n📊 Process Analysis:")
            response_parts.append(f"  • Total thoughts: {analysis['total_thoughts']}")
            response_parts.append(f"  • Revisions made: {analysis['revisions_made']}")
            response_parts.append(f"  • Active branches: {analysis['branches_active']}")
            response_parts.append(f"  • Hypotheses generated: {analysis['hypotheses_generated']}")
            
            if analysis['thinking_patterns']:
                response_parts.append(f"  • Patterns: {', '.join(analysis['thinking_patterns'])}")
        
        # Final analysis if ready
        if "final_analysis" in result:
            final = result["final_analysis"]
            response_parts.append(f"\n🎯 Final Analysis:")
            response_parts.append(f"  • Confidence: {final['confidence']:.1%}")
            response_parts.append(f"  • Summary: {final['thinking_summary']}")
            
            if final['key_insights']:
                response_parts.append(f"  • Key insights: {len(final['key_insights'])} found")
            
            if final['final_hypothesis']:
                response_parts.append(f"  • Final hypothesis: {final['final_hypothesis']}")
        
        # Recommendations
        if result["needs_more_thoughts"]:
            response_parts.append(f"\n💡 Recommendation: Continue thinking - more analysis needed")
        elif result["status"] == "ready_to_conclude":
            response_parts.append(f"\n✅ Ready to conclude - sufficient analysis completed")
        else:
            response_parts.append(f"\n➡️  Continue with next thought when ready")
        
        return "\n".join(response_parts)
        
    except Exception as e:
        return f"Error in sequential thinking process: {str(e)}\nPlease check your input parameters and try again."


# Convenience function for resetting the thinking process
def reset_sequential_thinking():
    """Reset the sequential thinking instance for a new problem."""
    global _thinking_instance
    _thinking_instance = SequentialThinking()
    return "Sequential thinking process reset for new problem."


# Convenience function for getting the complete thinking history
def get_thinking_history() -> str:
    """Get the complete thinking history as a formatted string."""
    global _thinking_instance
    history = _thinking_instance.get_thinking_history()
    
    output = []
    output.append("🧠 COMPLETE THINKING HISTORY")
    output.append("=" * 50)
    
    # Thoughts
    output.append(f"\n📋 Thoughts ({len(history['thoughts'])} total):")
    for thought in history['thoughts']:
        output.append(f"\nThought #{thought['thought_number']}:")
        output.append(f"  Content: {thought['thought'][:100]}{'...' if len(thought['thought']) > 100 else ''}")
        output.append(f"  Time: {thought['timestamp']}")
        if thought['is_revision']:
            output.append(f"  Revision of thought #{thought['revises_thought']}")
        if thought['branch_id']:
            output.append(f"  Branch: {thought['branch_id']}")
    
    # Branches
    if history['branches']:
        output.append(f"\n🌿 Branches ({len(history['branches'])} total):")
        for branch_id, thought_nums in history['branches'].items():
            output.append(f"  {branch_id}: thoughts {thought_nums}")
    
    # Hypotheses
    if history['hypotheses']:
        output.append(f"\n🎯 Hypotheses ({len(history['hypotheses'])} total):")
        for i, hypothesis in enumerate(history['hypotheses'], 1):
            output.append(f"  {i}. {hypothesis}")
    
    # Final result
    if history['final_answer']:
        output.append(f"\n🏁 Final Answer:")
        output.append(f"  {history['final_answer']}")
        output.append(f"  Confidence: {history['confidence_level']:.1%}")
    
    return "\n".join(output)


if __name__ == "__main__":
    # Test the sequential thinking function
    print("Testing sequential thinking implementation...")
    
    # Example usage
    result1 = sequential_thinking(
        thought="I need to analyze this problem step by step. First, let me understand what we're trying to solve.",
        thought_number=1,
        total_thoughts=5
    )
    print(result1)
    
    result2 = sequential_thinking(
        thought="Based on my analysis, I hypothesize that the solution involves breaking down the problem into smaller components.",
        thought_number=2,
        total_thoughts=5
    )
    print(result2)
    
    # Get final history
    print("\n" + get_thinking_history())