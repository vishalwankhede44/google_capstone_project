"""
Single-process ADK entrypoint for the wellness orchestrator.
Exposes the Chief Wellness Officer (CWO) agent as the root agent and
configures session memory via InMemorySessionService so multi-turn
conversations retain context.

Run with:
    adk api_server --a2a --app app:app_config --port 8002
"""

import os
import time
import uuid
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from google.adk.apps.app import App, ResumabilityConfig
from google.adk.runners import Runner
from google.adk.sessions.in_memory_session_service import InMemorySessionService
from google.genai.types import Content, Part

from chief_wellness_officer.cwo_agent import chief_wellness_officer

APP_NAME = "wellness_orchestrator"

app_config = App(
    name=APP_NAME,
    root_agent=chief_wellness_officer,
    resumability_config=ResumabilityConfig(is_resumable=True),
)

session_service = InMemorySessionService()
runner = Runner(
    app=app_config,
    session_service=session_service,
)

if __name__ == "__main__":
    import sys
    import asyncio

    def get_or_create_user_id() -> str:
        """Return the user id for this run.

        Priority:
        1. If WELLNESS_USER_ID env var is set, use that (explicit user switch).
        2. Otherwise, use a stable, randomized id persisted on disk.
        """
        # 1) Explicit override for running as a different user
        env_user = os.getenv("WELLNESS_USER_ID")
        if env_user:
            return env_user.strip()

        # 2) Fallback: persisted randomized id
        user_id_file = os.path.join("data", "user_id.txt")

        # Reuse existing id if present
        if os.path.exists(user_id_file):
            try:
                with open(user_id_file, "r", encoding="utf-8") as f:
                    existing = f.read().strip()
                    if existing:
                        return existing
            except OSError:
                pass

        # Create a new randomized but human-readable id
        new_id = f"user_{uuid.uuid4().hex[:8]}"
        os.makedirs(os.path.dirname(user_id_file), exist_ok=True)
        try:
            with open(user_id_file, "w", encoding="utf-8") as f:
                f.write(new_id)
        except OSError:
            # If we can't write, still return the new id for this process
            pass

        return new_id
    
    async def main():
        # Interactive mode: run agent directly without API server
        print("=== Wellness Orchestrator (Direct Mode) ===")
        print("Type your wellness goals or questions. Press Ctrl+C to exit.\n")
        
        # Create a session for the conversation (persistent randomized user id)
        user_id = get_or_create_user_id()
        session_id = str(uuid.uuid4())
        session = await session_service.create_session(
            app_name=APP_NAME,
            user_id=user_id,
            session_id=session_id
        )
        
        while True:
            try:
                user_input = input("You > ").strip()
                if not user_input:
                    continue
                
                # Run the agent with proper parameters
                # Create a proper Content message object
                message = Content(
                    role="user",
                    parts=[Part(text=user_input)]
                )
                
                # Collect all events from the async generator
                response_text = ""
                start_time = time.time()
                last_event_time = start_time
                print("🔄 Processing...\n")
                
                async for event in runner.run_async(
                    user_id=user_id,
                    session_id=session_id,
                    new_message=message
                ):
                    # Log event type for debugging
                    event_type = type(event).__name__
                    
                    # Log agent activity
                    if hasattr(event, 'agent_name') and event.agent_name:
                        print(f"  🤖 Agent: {event.agent_name}", flush=True)
                    
                    # Log tool calls and responses
                    if hasattr(event, 'content') and event.content:
                        if hasattr(event.content, 'parts') and event.content.parts:
                            for part in event.content.parts:
                                # Check for function calls
                                if hasattr(part, 'function_call') and part.function_call:
                                    func_name = part.function_call.name if hasattr(part.function_call, 'name') else 'unknown'
                                    print(f"  🔧 Tool call: {func_name}", flush=True)
                                
                                # Check for function responses
                                if hasattr(part, 'function_response') and part.function_response:
                                    func_name = part.function_response.name if hasattr(part.function_response, 'name') else 'unknown'
                                    print(f"  ✅ Tool response: {func_name}", flush=True)
                                
                                # Collect text responses
                                if hasattr(part, 'text') and part.text:
                                    response_text += part.text
                    
                    # Show progress dot for any event
                    current_time = time.time()
                    if current_time - last_event_time > 5:
                        print(f" [waiting {current_time - last_event_time:.1f}s]", end="", flush=True)
                    last_event_time = current_time
                    print(".", end="", flush=True)
                
                elapsed_time = time.time() - start_time
                print(f"\n⏱️  Total time: {elapsed_time:.2f}s")
                
                # Display the response
                if response_text:
                    print(f"\n🤖 CWO: {response_text}\n")
                else:
                    print(f"\n🤖 CWO: (No text response received)\n")
                    
            except KeyboardInterrupt:
                print("\n\nExiting. Stay well!")
                sys.exit(0)
            except EOFError:
                # Handle end-of-input (e.g., terminal closed) gracefully
                print("\n\nExiting. Stay well!")
                sys.exit(0)
            except Exception as e:
                print(f"\n❌ Error: {e}\n")
                import traceback
                traceback.print_exc()
    
    asyncio.run(main())
