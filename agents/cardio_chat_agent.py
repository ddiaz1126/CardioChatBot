# AI Server - agents/cardio_chat_agent.py
from openai import OpenAI
import json
import asyncio
from typing import Dict, List, Any
import inspect
import tiktoken

from core.agents.base import BaseAgent, AgentInput, AgentOutput
from config import get_settings

from tools.cardio_tools import (
    # Session Tools
    get_recent_cardio_sessions,
    get_cardio_by_date,
    get_cardio_history,
    get_cardio_session_details,
    get_cardio_frequency,
    
    # Performance Tools
    get_pace_progression,
    get_heart_rate_trends,
    get_speed_progression,
    get_cardio_personal_bests,
    get_cardio_intensity_zones,
    compare_cardio_sessions,
    
    # Distance & Duration Tools
    get_distance_trends,
    get_duration_trends,
    get_weekly_mileage,
    get_monthly_volume,
    get_longest_sessions,
    
    # Splits & Pacing Tools
    get_split_analysis,
    get_pacing_consistency,
    get_negative_splits,
    get_fastest_splits,
    
    # Elevation Tools
    get_elevation_gain_trends,
    get_altitude_performance,
    get_hill_workouts,
    
    # Cardio Type Tools
    get_cardio_type_distribution,
    get_cardio_type_frequency,
    compare_cardio_types
)

# ==========================================
# TOOL FUNCTION REGISTRY
# ==========================================
TOOL_FUNCTIONS = {
    # Session Tools
    'get_recent_cardio_sessions': get_recent_cardio_sessions,
    'get_cardio_by_date': get_cardio_by_date,
    'get_cardio_history': get_cardio_history,
    'get_cardio_session_details': get_cardio_session_details,
    'get_cardio_frequency': get_cardio_frequency,
    
    # Performance Tools
    'get_pace_progression': get_pace_progression,
    'get_heart_rate_trends': get_heart_rate_trends,
    'get_speed_progression': get_speed_progression,
    'get_cardio_personal_bests': get_cardio_personal_bests,
    'get_cardio_intensity_zones': get_cardio_intensity_zones,
    'compare_cardio_sessions': compare_cardio_sessions,
    
    # Distance & Duration Tools
    'get_distance_trends': get_distance_trends,
    'get_duration_trends': get_duration_trends,
    'get_weekly_mileage': get_weekly_mileage,
    'get_monthly_volume': get_monthly_volume,
    'get_longest_sessions': get_longest_sessions,
    
    # Splits & Pacing Tools
    'get_split_analysis': get_split_analysis,
    'get_pacing_consistency': get_pacing_consistency,
    'get_negative_splits': get_negative_splits,
    'get_fastest_splits': get_fastest_splits,
    
    # Elevation Tools
    'get_elevation_gain_trends': get_elevation_gain_trends,
    'get_altitude_performance': get_altitude_performance,
    'get_hill_workouts': get_hill_workouts,
    
    # Cardio Type Tools
    'get_cardio_type_distribution': get_cardio_type_distribution,
    'get_cardio_type_frequency': get_cardio_type_frequency,
    'compare_cardio_types': compare_cardio_types,
}

# ==========================================
# OPENAI TOOL SCHEMAS
# ==========================================
OPENAI_TOOLS = [
    # Session Tools
    {
        "name": "get_recent_cardio_sessions",
        "description": "Get client's recent cardio sessions with pace, distance, heart rate",
        "parameters": {
            "type": "object",
            "properties": {
                "client_id": {"type": "integer"},
                "limit": {"type": "integer", "description": "Number of sessions (default: 10)"}
            },
            "required": ["client_id"]
        }
    },
    {
        "name": "get_cardio_frequency",
        "description": "How often client does cardio per week",
        "parameters": {
            "type": "object",
            "properties": {
                "client_id": {"type": "integer"},
                "weeks": {"type": "integer", "description": "Weeks to analyze (default: 4)"}
            },
            "required": ["client_id"]
        }
    },
    {
        "name": "get_cardio_session_details",
        "description": "Get detailed info for specific cardio session including splits",
        "parameters": {
            "type": "object",
            "properties": {
                "cardio_id": {"type": "integer"}
            },
            "required": ["cardio_id"]
        }
    },
    
    # Performance Tools
    {
        "name": "get_pace_progression",
        "description": "Track pace improvement over time for specific cardio type",
        "parameters": {
            "type": "object",
            "properties": {
                "client_id": {"type": "integer"},
                "cardio_type": {"type": "string", "description": "e.g., 'running', 'cycling'"},
                "weeks_back": {"type": "integer", "description": "Weeks to analyze (default: 12)"}
            },
            "required": ["client_id"]
        }
    },
    {
        "name": "get_heart_rate_trends",
        "description": "Track heart rate trends and averages",
        "parameters": {
            "type": "object",
            "properties": {
                "client_id": {"type": "integer"},
                "cardio_type": {"type": "string"},
                "weeks_back": {"type": "integer"}
            },
            "required": ["client_id"]
        }
    },
    {
        "name": "get_cardio_personal_bests",
        "description": "Get PRs for distance, pace, duration, speed",
        "parameters": {
            "type": "object",
            "properties": {
                "client_id": {"type": "integer"},
                "cardio_type": {"type": "string"}
            },
            "required": ["client_id"]
        }
    },
    
    # Distance & Duration Tools
    {
        "name": "get_weekly_mileage",
        "description": "Get weekly distance totals",
        "parameters": {
            "type": "object",
            "properties": {
                "client_id": {"type": "integer"},
                "cardio_type": {"type": "string"},
                "weeks": {"type": "integer"}
            },
            "required": ["client_id"]
        }
    },
    {
        "name": "get_longest_sessions",
        "description": "Get longest cardio sessions by distance or duration",
        "parameters": {
            "type": "object",
            "properties": {
                "client_id": {"type": "integer"},
                "cardio_type": {"type": "string"},
                "limit": {"type": "integer"}
            },
            "required": ["client_id"]
        }
    },
    
    # Splits & Pacing Tools
    {
        "name": "get_split_analysis",
        "description": "Analyze splits for a specific session",
        "parameters": {
            "type": "object",
            "properties": {
                "cardio_id": {"type": "integer"}
            },
            "required": ["cardio_id"]
        }
    },
    {
        "name": "get_pacing_consistency",
        "description": "Measure pacing consistency across splits",
        "parameters": {
            "type": "object",
            "properties": {
                "cardio_id": {"type": "integer"}
            },
            "required": ["cardio_id"]
        }
    },
    {
        "name": "get_negative_splits",
        "description": "Find sessions with negative splits (faster second half)",
        "parameters": {
            "type": "object",
            "properties": {
                "client_id": {"type": "integer"},
                "cardio_type": {"type": "string"},
                "weeks": {"type": "integer"}
            },
            "required": ["client_id"]
        }
    },
    
    # Elevation Tools
    {
        "name": "get_elevation_gain_trends",
        "description": "Track elevation gain over time",
        "parameters": {
            "type": "object",
            "properties": {
                "client_id": {"type": "integer"},
                "cardio_type": {"type": "string"},
                "weeks_back": {"type": "integer"}
            },
            "required": ["client_id"]
        }
    },
    {
        "name": "get_hill_workouts",
        "description": "Get sessions with significant elevation gain",
        "parameters": {
            "type": "object",
            "properties": {
                "client_id": {"type": "integer"},
                "weeks": {"type": "integer"},
                "min_elevation": {"type": "integer", "description": "Minimum elevation in meters"}
            },
            "required": ["client_id"]
        }
    },
    
    # Cardio Type Tools
    {
        "name": "get_cardio_type_distribution",
        "description": "Breakdown of cardio types (running, cycling, etc.)",
        "parameters": {
            "type": "object",
            "properties": {
                "client_id": {"type": "integer"},
                "weeks": {"type": "integer"}
            },
            "required": ["client_id"]
        }
    },
    {
        "name": "compare_cardio_types",
        "description": "Compare performance between two cardio types",
        "parameters": {
            "type": "object",
            "properties": {
                "cardio_type_1": {"type": "string"},
                "cardio_type_2": {"type": "string"},
                "client_id": {"type": "integer"},
                "weeks": {"type": "integer"}
            },
            "required": ["cardio_type_1", "cardio_type_2", "client_id"]
        }
    },
]


class CardioAgent(BaseAgent):
    """
    Intelligent cardio coaching agent that analyzes running, cycling, and other cardio data.
    """
    MAX_HISTORY_MESSAGES = 20  # Hard cap on message count
    MAX_CONTEXT_TOKENS = 6000 
    
    agent_id = "cardio_agent"
    name = "Cardio Coaching Agent"
    description = (
        "AI cardio coach that analyzes pace progression, heart rate trends, splits, "
        "elevation performance, and provides data-driven cardio training insights."
    )
    version = "1.0.0"
    category = "cardio"
    tags = ["cardio", "running", "cycling", "endurance", "ai", "coaching"]

    input_schema: Dict[str, Any] = {
        "type": "object",
        "properties": {
            "question": {
                "type": "string",
                "description": "User's cardio training question"
            },
            "client_id": {
                "type": "integer",
                "description": "Client ID to analyze"
            },
            "conversation_history": {
                "type": "string",
                "description": "JSON string of previous conversation messages",
                "default": "[]"
            },
            "max_iterations": {
                "type": "integer",
                "default": 15,
                "minimum": 1,
                "maximum": 30,
                "description": "Max tool-calling iterations"
            },
            "temperature": {
                "type": "number",
                "default": 0.3,
                "minimum": 0.0,
                "maximum": 1.0,
                "description": "GPT temperature for reasoning"
            }
        },
        "required": ["question", "client_id"]
    }

    output_schema: Dict[str, Any] = {
        "type": "object",
        "properties": {
            "answer": {
                "type": "string",
                "description": "AI's cardio analysis and recommendations"
            },
            "iterations": {
                "type": "integer",
                "description": "Number of tool calls made"
            },
            "tools_used": {
                "type": "array",
                "items": {"type": "string"},
                "description": "List of tools called"
            }
        },
        "required": ["answer", "iterations", "tools_used"]
    }

    SYSTEM_PROMPT = """You are an expert cardio coaching AI that helps trainers analyze their clients' running, cycling, and endurance training data.

    **CRITICAL WORKFLOW:**
    1. **Determine query type:**
    - Pace/speed trends → get_pace_progression / get_speed_progression
    - Heart rate → get_heart_rate_trends
    - Recent activity → get_recent_cardio_sessions
    - PRs → get_cardio_personal_bests
    - Weekly volume → get_weekly_mileage
    - Specific session → get_cardio_session_details → get_split_analysis
    - Hills/elevation → get_hill_workouts / get_elevation_gain_trends
    - Pacing → get_negative_splits / get_pacing_consistency

    2. **Be analytical and actionable:**
    - Identify pace trends and improvements
    - Track heart rate efficiency
    - Analyze pacing strategies
    - Compare cardio types
    - Flag overtraining or undertraining

    3. **Units:**
    - Always use metric (km, min/km, meters) unless asked for imperial
    - Convert pace to readable format (e.g., "5:30 min/km")

    **RESPONSE STRATEGY:**

    1. **Classify query intent first:**
    - "Details/analysis/breakdown of [specific session]" → Comprehensive (4-6 tools)
    - "Recent/last/latest [activity]" → Brief overview (1-2 tools)  
    - "Trends/progression/improvement" → Time-series analysis (2-4 tools)
    - "How is [metric]" → Current status (1-2 tools)

    2. **For comprehensive queries ("details", "analysis", "breakdown"):**
    - Use multiple relevant tools to build complete picture
    - Include: session data, splits, pacing, comparisons
    - Response: 4-6 sentences with key insights
    
    3. **For status queries ("how is", "what's", "current"):**
    - Use minimal tools needed to answer
    - Response: 2-3 sentences max
    
    4. **For trend queries:**
    - Focus on progression tools
    - Show change over time with specific metrics
    - Response: 3-4 sentences

    **CRITICAL:** Match response depth to question type. "Details of last run" needs splits + pacing analysis. "How often does he run" needs just frequency data."""

    def __init__(self):
        super().__init__(name="Cardio Coaching Agent")
        settings = get_settings()
        self.client = OpenAI(api_key=settings.openai_api_key)
        print("[CardioAgent] Initialized with OpenAI client")

    async def validate_input(self, input_data: AgentInput) -> bool:
        """Validate required inputs"""
        data = input_data.data or {}
        
        if "question" not in data or not data["question"]:
            raise ValueError("Missing required input: question")
        
        if "client_id" not in data or not isinstance(data["client_id"], int):
            raise ValueError("Missing or invalid input: client_id")
        
        return True

    def _prepare_conversation_history(self, conversation_history, model="gpt-4-turbo-preview"):
        """
        Prepare conversation history with token limits.
        Uses hybrid approach: sliding window + token counting
        """
        
        # First, apply sliding window
        if len(conversation_history) > self.MAX_HISTORY_MESSAGES:
            conversation_history = conversation_history[-self.MAX_HISTORY_MESSAGES:]
            print(f"[CardioAgent] Trimmed to last {self.MAX_HISTORY_MESSAGES} messages")
        
        # Then check tokens
        try:
            encoding = tiktoken.encoding_for_model(model)
        except KeyError:
            # Fallback if model not found
            encoding = tiktoken.get_encoding("cl100k_base")
        
        system_tokens = len(encoding.encode(self.SYSTEM_PROMPT))
        available_tokens = self.MAX_CONTEXT_TOKENS - system_tokens - 2000  # Reserve 2k for response + tools
        
        # Add messages until we hit token limit (from most recent backwards)
        prepared_messages = []
        current_tokens = 0
        
        for msg in reversed(conversation_history):
            if isinstance(msg, dict) and 'role' in msg and 'content' in msg:
                msg_tokens = len(encoding.encode(msg['content'])) + 4  # +4 for message formatting
                
                if current_tokens + msg_tokens < available_tokens:
                    prepared_messages.insert(0, {
                        "role": msg["role"],
                        "content": msg["content"]
                    })
                    current_tokens += msg_tokens
                else:
                    print(f"[CardioAgent] Token limit reached at {len(prepared_messages)} messages ({current_tokens} tokens)")
                    break
        
        print(f"[CardioAgent] Using {len(prepared_messages)} messages (~{current_tokens} tokens)")
        return prepared_messages

    async def run(self, input_data: AgentInput) -> AgentOutput:
        """
        Main agent execution - GPT-4 intelligently routes to appropriate cardio tools
        
        Returns:
            AgentOutput with cardio analysis and recommendations
        """
        try:
            data = input_data.data or {}
            question = data["question"]
            
            # Handle type conversion
            def safe_int(val, default):
                try:
                    return int(val)
                except (TypeError, ValueError):
                    return default
            
            def safe_float(val, default):
                try:
                    return float(val)
                except (TypeError, ValueError):
                    return default
            
            client_id = safe_int(data["client_id"], None)
            if client_id is None:
                raise ValueError("Invalid client_id")
                
            max_iterations = safe_int(data.get("max_iterations"), 15)
            temperature = safe_float(data.get("temperature"), 0.3)
            
            # Parse conversation history
            conversation_history_str = data.get("conversation_history", "[]")
            try:
                conversation_history = json.loads(conversation_history_str)
            except (json.JSONDecodeError, TypeError):
                conversation_history = []

            print(f"\n[CardioAgent] Processing question for client {client_id}")
            print(f"[CardioAgent] Question: '{question[:80]}...'")
            print(f"[CardioAgent] Raw conversation history: {len(conversation_history)} messages")

            # Apply token limits to conversation history
            prepared_history = self._prepare_conversation_history(conversation_history)

            # Build messages with prepared conversation history
            messages = [{"role": "system", "content": self.SYSTEM_PROMPT}]
            messages.extend(prepared_history)
            
            # Add current question
            messages.append({
                "role": "user",
                "content": f"Client ID: {client_id}\n\nQuestion: {question}"
            })
            
            tools_used = []
            
            for iteration in range(max_iterations):
                print(f"\n{'='*60}")
                print(f"[CardioAgent] ITERATION {iteration + 1}")
                print(f"{'='*60}")
                
                # Call GPT-4 with function calling
                response = self.client.chat.completions.create(
                    model="gpt-4-turbo-preview",
                    messages=messages,
                    functions=OPENAI_TOOLS,
                    function_call="auto",
                    temperature=temperature
                )
                
                message = response.choices[0].message
                
                # GPT wants to call a function
                if message.function_call:
                    function_name = message.function_call.name
                    function_args = json.loads(message.function_call.arguments)
                    
                    # Get the tool function
                    tool_func = TOOL_FUNCTIONS.get(function_name)
                    if not tool_func:
                        raise ValueError(f"Tool {function_name} not found")
                    
                    # Auto-inject client_id if function accepts it
                    sig = inspect.signature(tool_func)
                    if 'client_id' in sig.parameters and 'client_id' not in function_args:
                        function_args['client_id'] = client_id
                    
                    print(f"\n[CardioAgent] 🔧 Tool: {function_name}")
                    print(f"[CardioAgent]    Args: {json.dumps(function_args, indent=2)}")
                    
                    tools_used.append(function_name)
                    
                    # Add function call to messages
                    messages.append({
                        "role": "assistant",
                        "content": None,
                        "function_call": {
                            "name": function_name,
                            "arguments": json.dumps(function_args)
                        }
                    })
                    
                    try:
                        # Execute tool
                        if asyncio.iscoroutinefunction(tool_func):
                            result = await tool_func(**function_args)
                        else:
                            result = tool_func(**function_args)
                        
                        result_preview = json.dumps(result, indent=2)[:200]
                        print(f"[CardioAgent]    ✓ Result: {result_preview}...")
                        
                    except Exception as e:
                        import traceback
                        traceback.print_exc()
                        print(f"[CardioAgent]    ✗ Error: {str(e)}")
                        result = {'error': str(e)}
                    
                    # Add result to messages
                    messages.append({
                        "role": "function",
                        "name": function_name,
                        "content": json.dumps(result)
                    })
                
                # GPT has final answer
                else:
                    final_answer = message.content
                    print(f"\n{'='*60}")
                    print(f"[CardioAgent] ✅ COMPLETED IN {iteration + 1} ITERATIONS")
                    print(f"[CardioAgent] Tools used: {', '.join(tools_used)}")
                    print(f"{'='*60}")
                    print(f"\n{final_answer[:200]}...")
                    
                    return AgentOutput(
                        success=True,
                        data={
                            "answer": final_answer,
                            "iterations": iteration + 1,
                            "tools_used": tools_used
                        }
                    )
            
            # Max iterations reached
            return AgentOutput(
                success=False,
                data={
                    "answer": "Analysis incomplete - max iterations reached",
                    "iterations": max_iterations,
                    "tools_used": tools_used
                },
                error="Max iterations reached"
            )

        except Exception as e:
            print(f"[CardioAgent] ❌ Exception: {e}")
            import traceback
            traceback.print_exc()
            
            return AgentOutput(
                success=False,
                data={
                    "answer": "",
                    "iterations": 0,
                    "tools_used": []
                },
                error=str(e)
            )