# Research: Chatbot Enhancements

## Performance Goals

**Decision**: 
- p95 latency for chatbot responses should be < 500ms.
- Welcome message with stats should load in < 1s.

**Rationale**: These are standard performance targets for a responsive web application and provide a good user experience.

**Alternatives considered**: Stricter targets (e.g., < 200ms) were considered but deemed unnecessary for the initial implementation, as they would require more complex caching strategies.

## Constraints

**Decision**: The system should support up to 100 concurrent users.

**Rationale**: This is a reasonable starting point for a new feature and can be scaled up in the future if needed.

**Alternatives considered**: A higher number of concurrent users was considered, but it would require more significant infrastructure investment.

## Scale/Scope

**Decision**: The system should be able to handle up to 10,000 users in total.

**Rationale**: This number allows for significant user growth while keeping the initial database and infrastructure costs manageable.

**Alternatives considered**: A larger scale was considered, but it would require a more complex sharding strategy for the database.
