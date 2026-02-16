# Agent Development Rules - Evo-TODO (Phase III)

## Success Criteria
- All outputs follow SDD workflow: spec → plan → tasks → implement
- PHR created for every prompt
- ADR suggestions for decisions
- Small, testable changes with code refs (path:line)
- Constitution compliance (stateless, 5-msg window, MCP tools, UI consistency)

## Core Guarantees
- Record user input verbatim in PHR
- Route: history/prompts/constitution/, history/prompts/{feature}/, history/prompts/general/
- ADR: Suggest `/sp.adr <title>` for cross-cutting decisions
- No auto-ADRs

## Phase III Updates (from Constitution v3.0.0)
- **Backend Stateless**: Zero RAM state; Neon DB only
- **Memory Window**: Load last 5 msgs only
- **Summarization**: Generate/store summary every 5 msgs in conversations table
- **Proactive Greeting**: Dashboard load calls get_user_stats; greet with task counts
- **Tool Isolation**: Inject user_id from JWT to all tools
- **UI Consistency**: Shadcn/UI, App Shell, Light/Dark mode

## Development Guidelines
1. **Authoritative Sources**: MCP (Context7, Better Auth); CLI scripts first
2. **Execution**: CLI > manual files
3. **PHR After Every Request**: Implementation/planning/debugging/spec/plan/tasks
   - Title (3-7 words) → slug
   - Route by stage
   - Fill .specify/templates/phr-template.prompt.md
   - Report ID/path/stage/title
4. **ADR Suggestions**: Impactful decisions → suggest, wait consent
5. **Human-in-Loop**: Clarify ambiguities, prioritize, approve plans

## Workflow
1. `/sp.specify`: User stories/FRs/SC
2. `/sp.clarify`: Resolve ambiguities
3. `/sp.plan`: Research/design artifacts
4. `/sp.tasks`: Actionable task list
5. `/sp.implement`: TDD execution
After final completion/update, push all code to `phase-3` branch.

## Defaults
- Clarify/plan first
- .env secrets only
- Minimal diffs
- Code refs: path:line
- Private reasoning

## Execution Contract
1. Confirm surface/criteria
2. List constraints/non-goals
3. Artifact with checks
4. Follow-ups/risks (≤3)
5. PHR
6. ADR if applicable

## Architect Guidelines (Plan)
Address: Scope/deps, decisions, interfaces, NFRs, data, ops, risks, eval, ADRs

**Updated Stack**: Next.js/FastAPI/SQLModel/Neon/Better Auth + MCP SDK/OpenAI Agents (Phase III)

See CLAUDE.md for Claude-specific; adapt for other agents.
