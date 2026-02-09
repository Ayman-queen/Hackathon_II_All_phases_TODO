<!--

Sync Impact Report:

- Version change: 2.0.0 → 3.0.0 (major bump for Phase III new principles and constraints)

- Modified principles: None renamed

- Added principles:

  - VIII. Backend Statelessness

  - IX. Conversation Memory Window

  - X. Message Summarization

  - XI. Proactive User Greeting

  - XII. Tool User Isolation

  - XIII. UI Consistency

- Removed sections: None

- Templates requiring updates:

  - plan-template.md: ✅ Constitution Check aligns (no changes needed)

  - spec-template.md: ✅ No constitution references requiring update

  - tasks-template.md: ✅ Task structure compatible

- Follow-up TODOs: Update Git branching refs in PROJECT_SUMMARY.md if Phase III expands; monitor for new MCPs if memory features require external tools

-->



# Evo-TODO Constitution (Phase III)



## Core Principles



### I. Full-Stack Web Application with Separation of Concerns

- **Frontend**: Next.js 16+ (App Router) – modern React with server and client components

- **Backend**: FastAPI – high-performance async Python API

- **Database**: SQLModel + Neon Serverless PostgreSQL – type-safe ORM with scalable cloud database

- **Authentication**: Better Auth with JWT integration – secure, user-scoped data access

This stack enables rapid development, type safety across layers, and production-ready scalability.



### II. User-Scoped Data and JWT Authentication (Mandatory)

All API endpoints MUST accept a JWT token in the Authorization header. Every response MUST be filtered by `user_id` derived from the token. No endpoint returns unfiltered data. This enforces data isolation, security, and multi-tenant correctness. Token validation happens at the API boundary; internal functions assume valid, authenticated context.



### III. Clean Code Principles (Mandatory)

Code must follow clean code discipline: functions are small and focused (single responsibility), variable names are clear and self-documenting, nesting is minimal, and logic is testable in isolation. Complexity must be justified. Code reviews enforce clarity over brevity.



### IV. Task-Driven Implementation

All code MUST map to a Task ID. Every pull request, feature, and refactor starts with a task definition in tasks.md. Orphaned code (not traceable to a task) is not permitted. This ensures accountability, reviewability, and architectural coherence.



### V. Performance Over Brevity

Design and implementation prioritize measurable performance (latency, throughput, memory efficiency) over code brevity or cleverness. Profiling and optimization are expected for critical paths. Trade-offs must be documented with rationale.



### VI. No Manual Code Writing

Code generation, scaffolding, and templating are preferred. Manual coding is permitted only after generator/template approach is exhausted and justified. Reduces human error and ensures consistency across the codebase.



### VII. MCP Integration for Documentation and Authentication

- **Context7 MCP**: Use for accessing updated technical documentation and debugging context to avoid errors and ensure correctness.

- **Better Auth MCP**: Use for all Better Auth integration, configuration, and best practices to ensure secure and correct authentication implementation.

These MCPs provide authoritative, up-to-date guidance; all debugging and authentication work MUST reference these sources first.



### VIII. Backend Statelessness (Phase III)

The backend MUST hold zero state in RAM. All conversation history and persistent data MUST reside exclusively in Neon DB. No in-memory caches, sessions, or global variables for user data. Stateless design enables horizontal scaling and fault tolerance.



### IX. Conversation Memory Window (Phase III)

Implement a strict 5-message window for active context. Only the most recent 5 messages are loaded into agent context per conversation. Older messages are archived in DB and accessible only via explicit retrieval or summarization.



### X. Message Summarization Pattern (Phase III)

Every 5 messages, the agent MUST generate a concise summary and store it in the `conversations` table. Summaries maintain long-term context without bloating active memory. Summary generation uses structured format: key decisions, open tasks, unresolved issues.



### XI. Proactive User Greeting (Phase III)

Upon dashboard load, the agent MUST call `get_user_stats` and greet the user with personalized stats: current open task count, completed tasks, and total conversations. Greeting format: "Welcome back! You have X open tasks across Y conversations."



### XII. Tool User Isolation (Phase III)

Every tool call MUST inject the `user_id` extracted from the verified Better Auth JWT. Tools receive user-scoped parameters by default. No tool executes without explicit user context, preventing data leakage across tenants.



### XIII. UI Consistency (Phase III)

Maintain the professional App Shell, Shadcn/UI components, and existing Light/Dark mode. No deviations from Shadcn design system. Theme persistence via `next-themes`. Responsive design across all breakpoints mandatory.



## Technology Stack (Phase III)



- **Frontend**: Next.js 16+ (App Router)

- **Backend**: FastAPI (async Python)

- **ORM**: SQLModel (type-safe, Pydantic-integrated)

- **Database**: Neon Serverless PostgreSQL

- **Authentication**: Better Auth with JWT

- **Code Quality**: Clean code principles, single responsibility, testable functions

- **Task Tracking**: All code linked to Task IDs in tasks.md

- **State Management**: Fully stateless backend; DB-only persistence



## Development Workflow



1. **Task-First**: Every feature, fix, or refactor begins with a task definition in tasks.md.

2. **MCP-Driven Documentation**: Consult **Context7 MCP** for debugging and technical guidance; consult **Better Auth MCP** for all authentication work.

3. **Approval Before Code**: Tasks are reviewed and approved before implementation starts.

4. **Mapping Enforcement**: Every commit MUST reference its Task ID. Code without traceability is rejected.

5. **JWT Validation**: All API requests require valid JWT tokens; all responses filtered by user_id.

6. **Stateless Enforcement**: No RAM state; all data via DB queries.

7. **Testing**: Code must be testable in isolation; integration tests validate end-to-end behavior.

8. **Code Review**: All PRs reviewed for clean code adherence, task mapping, authentication/authorization, MCP compliance, performance considerations, and Phase III statelessness.



## Git Branching Strategy (Phase III)



- **Main Release Branch**: `phase-3` (final merged branch for Phase III)

- **Feature Branches**: `phase3-XXY-feature-name` (e.g., `phase3-001-memory`, `phase3-002-stats`)

- **Rules**: All PRs target `phase-3`. Feature branches are short-lived and deleted after merge. After final completion/update, push all code to `phase-3` branch.



## Non-Negotiable Constraints



- All API endpoints MUST require JWT tokens in Authorization header.

- All responses MUST be filtered by user_id from JWT claims.

- No unfiltered data access; data isolation is enforced at API boundary.

- Backend holds zero state in RAM; all history in Neon DB.

- Strict 5-message active context window.

- Summaries stored in `conversations` table every 5 messages.

- Proactive greeting on dashboard load via `get_user_stats`.

- Every tool call injects `user_id` from JWT.

- UI uses App Shell, Shadcn/UI, Light/Dark mode exclusively.

- All code MUST reference a Task ID (in commit messages and PR descriptions).

- SQLModel + PostgreSQL for all persistent data (no in-memory-only storage).

- No manual code generation if automated approach is feasible.

- No brevity at the expense of clarity and performance.

- **MCP Usage (Mandatory)**:

  - All debugging and technical documentation queries MUST use **Context7 MCP** for current, authoritative guidance.

  - All Better Auth integration, configuration, and security implementation MUST use **Better Auth MCP** as source of truth.

  - MCPs are consulted FIRST before manual implementation or external documentation.



## Governance



This constitution supersedes all other development practices and guidelines. Amendments require:

1. Documentation of the change and rationale.

2. Explicit approval (tracked in commit/PR).

3. Migration plan for existing code (if backward incompatible).



All PRs and reviews MUST verify compliance with these principles. Use `CLAUDE.md` for agent-specific guidance on development workflows. Violations are non-negotiable and must be remediated before merge.



**Version**: 3.0.0 (Phase III) | **Ratified**: 2025-12-27 | **Last Amended**: 2026-01-27
