# Phase 3 Chat Research Summary

**Date**: 2026-01-27

## MCP SDK (/modelcontextprotocol/python-sdk)
- Official Python SDK for Model Context Protocol.
- Enables MCP servers/clients for tools, resources, prompts.
- High reputation, 296 code snippets, score 89.2.
- Best for exposing task CRUD as tools in FastAPI backend.
- Integration: pip install modelcontextprotocol/python-sdk; define @tool decorators.

Alternatives rejected: Go/Ruby/C# SDKs (not Python).

## OpenAI Agents SDK (/openai/openai-agents-python)
- Python framework for multi-agent workflows.
- Supports agents, tools, handoffs, guardrails, Runner for execution.
- High reputation, 606 snippets, score 90.3.
- Key: Runner.run(agent, input) with tools; add message-count logic for summarization trigger.
- pip install openai-agents; define Agent with tools=[mcp_tools].

Alternatives rejected: JS SDK (frontend Python mismatch).

## Decisions
- Use MCP Python SDK for tool exposure.
- OpenAI Agents SDK for runner with custom summarization after 5 msgs.
- Stateless: Run per request via POST /api/{user_id}/chat.
