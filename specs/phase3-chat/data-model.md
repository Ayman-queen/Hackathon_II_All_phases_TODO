# Data Model: Phase 3 Chat

## Conversation Table
```sql
CREATE TABLE conversations (
  id UUID PRIMARY KEY,
  user_id VARCHAR REFERENCES "user"(id) NOT NULL,
  title VARCHAR(255),
  context_summary TEXT,
  message_count INTEGER DEFAULT 0,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

## Message Table
```sql
CREATE TABLE messages (
  id UUID PRIMARY KEY,
  conversation_id UUID REFERENCES conversations(id) ON DELETE CASCADE,
  role VARCHAR(20) CHECK (role IN ('user', 'assistant')) NOT NULL,
  content TEXT NOT NULL,
  is_summary BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_messages_conversation ON messages(conversation_id);
CREATE INDEX idx_conversations_user ON conversations(user_id);
```

Relationships: Messages 1:N Conversation; Conversation 1:1 User.
Validation: content <= 2000 chars; message_count triggers summary.
