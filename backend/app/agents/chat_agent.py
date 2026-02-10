from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled, RunConfig, ModelSettings



# Disable tracing globally

set_tracing_disabled(True)

from agents.mcp import MCPServerStreamableHttp

from app.models.database import Session, engine

from app.models.chat import Conversation, Message

from uuid import UUID

from sqlmodel import select

from app.core.config import settings

from typing import Optional

import logging

import asyncio



logger = logging.getLogger(__name__)



# Create a custom AsyncOpenAI client

client = AsyncOpenAI(api_key=settings.GEMINI_API_KEY, base_url=settings.GEMINI_BASE_URL)





async def get_initialized_orchestrator_agent(mcp_http_server: MCPServerStreamableHttp) -> Agent:

    """

    Initializes and returns the OrchestratorAgent with all its tools and instructions.

    """

    # Define the Gemini model using OpenAIChatCompletionsModel

    gemini_model = OpenAIChatCompletionsModel(

        model=settings.MODEL_NAME,

        openai_client=client,

    )



    # The main orchestrator agent

    orchestrator_agent = Agent(

        name="OrchestratorAgent",

        instructions="""You are a concise and efficient Task Manager. Your primary goal is to help users manage their tasks using the available tools.



**Tool Usage Strategy:**

1.  **Analyze Intent:** Before using any tool, carefully analyze the user's intent. Do not use a tool if the intent is ambiguous.

2.  **One Tool at a Time:** Use one tool at a time. Do not chain multiple tool calls in a single turn.

3.  **Get Task ID:** If the user wants to update, delete, or complete a task but does not provide a task ID, you must first use the `list_tasks` tool to get the list of tasks and their IDs. Then, you can use the `task_id` from the list to call the appropriate tool.

4.  **Prefer Specific Tools:** If the user provides a task ID, prefer tools that use it (`update_task`, `delete_task`, `complete_task`).

5.  **Avoid Redundant `list_tasks`:** Do not use `list_tasks` after every operation. Only use it when the user explicitly asks for the task list or when you need to get a `task_id`.

6.  **Clarify Ambiguity:** If the user's request is unclear, ask for clarification instead of guessing which tool to use. For example, if the user says "update my task", ask "Which task would you like to update? Please provide the task ID.".



**Response Guidelines:**

- Keep your responses short and to the point.

- After a successful operation, provide a brief confirmation. Example: "Task added.", "Task updated.", "Task deleted."

- If an operation fails, provide a clear and concise error message.

- Do not add any extra information that is not relevant to the user's request.""",

        model=gemini_model,

        mcp_servers=[mcp_http_server],

    )

    return orchestrator_agent





async def get_agent_response(orchestrator_agent: Agent, user_input: str, user_id: str, conversation_id: UUID) -> str:

    # Validate conversation_id is not None

    if conversation_id is None:

        raise ValueError("conversation_id is required and cannot be None")

    

    with Session(engine) as session:

        conversation = session.exec(select(Conversation).where(Conversation.id == conversation_id)).first()

        if not conversation:

            # Handle new conversation

            conversation = Conversation(id=conversation_id, user_id=user_id)

            session.add(conversation)

            session.commit()

            session.refresh(conversation)



        # Retrieve last 5 messages for the current conversation

        messages = session.exec(

            select(Message)

            .where(Message.conversation_id == conversation_id)

            .order_by(Message.created_at.desc())  # Get newest first

            .limit(5)

        ).all()



        # Reverse to chronological order for the agent context

        messages.reverse()



        # Prepare messages for the agent

        formatted_messages = [{"role": m.role, "content": m.content} for m in messages]

        

        # Add the user input

        formatted_messages.append({"role": "user", "content": user_input})



        # Run the orchestrator agent with timeout and error handling

        try:

            run_config = RunConfig(

                model_settings=ModelSettings(temperature=0.2)

            )



            result = await asyncio.wait_for(

                Runner.run(

                    orchestrator_agent,

                    formatted_messages,

                    context={"user_id": user_id},

                    run_config=run_config,

                ),

                timeout=180.0  # 3 minute timeout for entire agent run

            )

            assistant_response = result.final_output

            logger.info(f"Agent response: {assistant_response}")



            # Log successful completion

            logger.info(f"Agent completed successfully for user {user_id[:8]}...")



        except asyncio.TimeoutError:

            logger.error(f"Agent timed out for user {user_id[:8]}...")

            assistant_response = "I'm sorry, the request took too long to process. Your task may have been created - please use 'list tasks' to check, or try again."



        except Exception as e:

            error_str = str(e)

            logger.error(f"Agent error for user {user_id[:8]}...: {error_str}")



            if "RateLimitError" in error_str:

                assistant_response = "I'm sorry, I'm a bit overwhelmed right now. Please try again in a few moments."

            elif "timeout" in error_str.lower() or "timed out" in error_str.lower():

                assistant_response = "The operation took longer than expected. Your task may have been processed - please check your task list."

            elif "connection" in error_str.lower():

                assistant_response = "I'm having trouble connecting to the task service. Please try again in a moment."

            elif "MCP" in error_str or "tool" in error_str.lower():

                assistant_response = f"There was an issue processing your request: {error_str}. Please try again."

            else:

                assistant_response = "I encountered an unexpected error. Please try again or rephrase your request."



        # We also need to save the assistant's response to the database.

        if assistant_response:

            # Ensure conversation_id is set before creating the message

            new_message = Message(

                conversation_id=conversation_id,  # Always use the validated conversation_id

                role="assistant",

                content=assistant_response,

            )

            session.add(new_message)

            session.commit()



        return assistant_response
