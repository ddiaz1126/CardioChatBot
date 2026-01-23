# test_cardio_agent.py
"""
Simple test script for CardioAgent with SQLite databases.

Tests if the agent can:
1. Connect to SQLite databases
2. Use tools to query data
3. Call GCP Vertex AI (Gemini)
4. Return a proper response
"""

import asyncio
import sys
from agents.cardio_chat_agent import CardioAgent
from core.agents.models import AgentInput

async def test_cardio_agent():
    """Test the CardioAgent with a simple question."""
    
    print("="*60)
    print("CARDIO AGENT TEST")
    print("="*60)
    
    # Initialize agent
    print("\n1. Initializing CardioAgent...")
    agent = CardioAgent()
    print("   ✓ Agent initialized")
    
    # Prepare test input
    print("\n2. Preparing test question...")
    test_question = "What are the recent cardio sessions for this client?"
    test_client_id = 1  # Using client 1's database
    
    agent_input = AgentInput(
        data={
            "question": test_question,
            "client_id": test_client_id,
            "conversation_history": "[]",
            "max_iterations": 5,
            "temperature": 0.3
        }
    )
    
    print(f"   Question: {test_question}")
    print(f"   Client ID: {test_client_id}")
    
    # Run agent
    print("\n3. Running agent...")
    print("-"*60)
    
    result = await agent.run(agent_input)
    
    print("-"*60)
    print("\n4. Results:")
    print(f"   Success: {result.success}")
    
    if result.success:
        print(f"   Iterations: {result.data['iterations']}")
        print(f"   Tools used: {', '.join(result.data['tools_used'])}")
        print(f"\n   Answer:\n   {result.data['answer']}")
    else:
        print(f"   Error: {result.error}")
    
    print("\n" + "="*60)
    print("TEST COMPLETE")
    print("="*60)

if __name__ == "__main__":
    # Run the async test
    asyncio.run(test_cardio_agent())