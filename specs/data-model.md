# Data Model: Chatbot Enhancements

## Entities

### User
- **Description**: Represents a user of the application.
- **Fields**:
    - `id`: integer (primary key)
    - `username`: string
    - `email`: string
    - `hashed_password`: string
- **Relationships**:
    - Has many Tasks

### Task
- **Description**: Represents a to-do item.
- **Fields**:
    - `id`: integer (primary key)
    - `title`: string
    - `description`: string (optional)
    - `status`: string (e.g., "pending", "completed")
    - `user_id`: integer (foreign key to User)
- **Relationships**:
    - Belongs to a User
- **Validation**:
    - `title` cannot be empty.
    - `status` must be one of the predefined values.

### Session
- **Description**: Represents an authenticated user session.
- **Fields**:
    - `id`: string (session token)
    - `user_id`: integer (foreign key to User)
    - `expires_at`: datetime
- **Relationships**:
    - Belongs to a User
