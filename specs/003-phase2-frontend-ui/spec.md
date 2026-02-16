# Feature Specification: Phase II Frontend UI

**Feature Branch**: `003-phase2-frontend-ui`
**Created**: 2025-12-30
**Updated**: 2025-12-30 (Complete Frontend Specification)
**Status**: Ready for Planning
**Input**: Update speckit.specify for the complete Frontend. Define the 'What': * Auth Flow: Fully functional /login and /signup pages using Better Auth hooks. * Todo Dashboard: A protected /todo route that displays the user's task list. * Core Features: Add, Update, Delete, and Toggle Completion functionality for tasks. * Advanced UI: Implement Shadcn/UI components with support for Light/Dark mode and responsive layouts. * Security: A Higher Order Component (HOC) or middleware to redirect unauthenticated users to /login.

## User Scenarios & Testing *(mandatory)*

<!--
  IMPORTANT: User stories should be PRIORITIZED as user journeys ordered by importance.
  Each user story/journey must be INDEPENDENTLY TESTABLE - meaning if you implement just ONE of them,
  you should still have a viable MVP (Minimum Viable Product) that delivers value.
  
  Assign priorities (P1, P2, P3, etc.) to each story, where P1 is the most critical.
  Think of each story as a standalone slice of functionality that can be:
  - Developed independently
  - Tested independently
  - Deployed independently
  - Demonstrated to users independently
-->

### User Story 0 - Landing Page & Onboarding (Priority: P0)

An unauthenticated user arrives at the application homepage and needs a clear, compelling landing page that explains the product value and provides seamless navigation to signup or login. The page must be responsive, visually appealing, and mobile-friendly to maximize conversion from visitor to registered user.

**Why this priority**: The landing page is the first touchpoint for all users. It blocks access to all other features and must work correctly for users to begin their journey. A broken landing page (404 errors on auth links) breaks the entire user acquisition funnel.

**Independent Test**: Can be fully tested by visiting the root URL `/`, observing the landing page renders correctly on mobile/tablet/desktop, and verifying that the "Sign Up" and "Sign In" buttons redirect to the correct authentication pages without errors.

**Acceptance Scenarios**:

1. **Given** an unauthenticated user visits the app root URL `/`, **When** the page loads, **Then** a visually appealing landing page with hero section, value proposition, and feature highlights is displayed
2. **Given** a user viewing the landing page, **When** they click the "Get Started Free" button, **Then** they are redirected to the signup page (`/signup`) without 404 errors
3. **Given** a user viewing the landing page, **When** they click the "Sign In" button, **Then** they are redirected to the login page (`/login`) without 404 errors (CRITICAL BUG FIX: Previously linked to non-existent `/signin`)
4. **Given** a user on the landing page, **When** the page loads on a mobile device (320px width), **Then** all content is visible and properly laid out with no horizontal scrolling required
5. **Given** a user on the landing page, **When** they toggle dark mode, **Then** the landing page styling updates to dark theme and persists on subsequent visits
6. **Given** a user on the landing page, **When** it loads, **Then** the page completes rendering and is interactive in under 2 seconds
7. **Given** an authenticated user who navigates back to `/`, **When** they visit the page, **Then** they are optionally redirected to the protected todos page `/todos` (can show landing page as preview)

---

### User Story 1 - New User Registration (Priority: P1)

A new user arrives at the application and needs to create an account securely. The signup process should be intuitive, provide clear feedback, and integrate seamlessly with Better Auth to issue JWT tokens upon successful registration.

**Why this priority**: User registration is the critical path for onboarding. Without it, users cannot access the application. This is the foundation for all other features.

**Independent Test**: Can be fully tested by visiting the signup page, entering credentials, and verifying that a new user account is created and the user is authenticated with a JWT token stored in the browser.

**Acceptance Scenarios**:

1. **Given** a new user on the signup page, **When** they enter valid email and password, **Then** an account is created and they are redirected to the todos dashboard with JWT token available
2. **Given** a user on signup page, **When** they enter an invalid email format, **Then** an error message displays and account is not created
3. **Given** a user on signup page, **When** they enter a weak password, **Then** password validation feedback is shown and account is not created
4. **Given** an existing user email on signup page, **When** they try to register, **Then** an error message states the email already exists

---

### User Story 2 - User Login & JWT Token Management (Priority: P1)

An existing user needs to securely log in to access their todos. The login process should authenticate via Better Auth, retrieve a JWT token, and automatically include that token in all subsequent API requests to the backend.

**Why this priority**: Login is equally critical as registration. Without proper authentication, users cannot access protected resources and the JWT-based security model cannot function.

**Independent Test**: Can be fully tested by logging in with valid credentials and verifying that subsequent API calls to `/api/todos` succeed with automatic JWT token inclusion in the Authorization header.

**Acceptance Scenarios**:

1. **Given** a registered user on the login page, **When** they enter correct credentials, **Then** they are authenticated and redirected to the todos dashboard
2. **Given** a user on login page, **When** they enter incorrect credentials, **Then** an "Invalid credentials" error displays and they remain on login page
3. **Given** a logged-in user, **When** they make an API request to the backend, **Then** the JWT token is automatically included in the Authorization: Bearer <token> header
4. **Given** a logged-in user, **When** their JWT expires, **Then** they are prompted to log in again and redirected to the login page

---

### User Story 3 - Todo List Display with Filtering (Priority: P1)

A logged-in user views their todo list and needs to filter tasks by status (All, Pending, Completed) to focus on what matters. The interface should load todos from the backend API and display them in a clean, organized manner with filter controls.

**Why this priority**: This is the core feature - the reason users open the app. Without the ability to view and filter todos, the application has no primary value.

**Independent Test**: Can be fully tested by logging in, viewing the todos page, using filter buttons, and verifying that the task list updates to show only tasks matching the selected filter status.

**Acceptance Scenarios**:

1. **Given** a logged-in user with existing todos, **When** they view the todos page, **Then** all their todos are displayed in a list format
2. **Given** a user with todos of mixed status, **When** they select the "Pending" filter, **Then** only incomplete todos are displayed
3. **Given** a user with todos of mixed status, **When** they select the "Completed" filter, **Then** only completed todos are displayed
4. **Given** a user with no todos, **When** they view the todos page, **Then** an empty state message is displayed with a call-to-action to create their first todo
5. **Given** a logged-in user, **When** they select the "All" filter, **Then** all their todos regardless of status are shown

---

### User Story 4 - Todo Sorting (Priority: P2)

A user with many todos needs to organize them by priority level, due date, or title to effectively manage their workload. The interface should provide sortable column headers or a dropdown menu to reorder the task list.

**Why this priority**: While important for usability with many todos, basic filtering (Story 3) delivers core functionality. Sorting enhances power-user workflows and task organization.

**Independent Test**: Can be fully tested by loading a todo list with multiple items having different priorities and due dates, clicking sort controls, and verifying the list reorders correctly by the selected criteria.

**Acceptance Scenarios**:

1. **Given** a user viewing todos, **When** they select "Sort by Priority", **Then** todos are reordered from High → Medium → Low priority
2. **Given** a user viewing todos, **When** they select "Sort by Due Date", **Then** todos are reordered chronologically (soonest first)
3. **Given** a user viewing todos, **When** they select "Sort by Title", **Then** todos are reordered alphabetically (A-Z)
4. **Given** a user with unsorted todos, **When** they apply a sort filter, **Then** the sorting persists until they select a different sort option

---

### User Story 5 - Priority Tagging (Priority: P2)

When creating or editing a todo, a user should be able to assign a priority level (High, Medium, Low) to help categorize task importance. The priority tag should be visually distinct in the todo list.

**Why this priority**: Priority tagging enables todo categorization and pairs with sorting (Story 4) to provide powerful task management. Delivered after core CRUD ensures the MVP is solid.

**Independent Test**: Can be fully tested by creating a new todo with a priority level, viewing it in the list with a visible priority indicator, and editing an existing todo to change its priority.

**Acceptance Scenarios**:

1. **Given** the create todo form, **When** a user selects a priority level and creates a todo, **Then** the todo displays with the selected priority indicator
2. **Given** a todo in the list, **When** a user clicks to edit it, **Then** they can change the priority and the update is reflected immediately
3. **Given** todos with different priorities, **When** they are displayed, **Then** high-priority todos have a visually distinct appearance (e.g., red tag)
4. **Given** a new todo without an explicit priority set, **When** the user saves it, **Then** a default priority (Medium) is assigned

---

### User Story 6 - Dark Mode & Light Mode Toggle (Priority: P2)

Users should be able to toggle between light and dark themes based on their preference. The theme choice should be persistent across sessions and apply consistently to all UI elements.

**Why this priority**: Theme switching improves user experience and accessibility but is not core to task management. It enhances usability without blocking MVP functionality.

**Independent Test**: Can be fully tested by clicking the theme toggle button, verifying the entire UI switches to the selected theme, and confirming the preference persists after page refresh.

**Acceptance Scenarios**:

1. **Given** a user in light mode, **When** they click the dark mode toggle, **Then** the entire interface switches to dark theme immediately
2. **Given** a user who has selected dark mode, **When** they refresh the page, **Then** the dark mode preference is restored
3. **Given** a user in any theme, **When** they navigate to different pages, **Then** the selected theme applies consistently throughout the application
4. **Given** a new user on first visit, **When** no theme preference is saved, **Then** the system respects the user's OS-level theme preference (light or dark)

---

### User Story 7 - User Profile & Logout (Priority: P2)

A logged-in user should be able to view their profile information and securely log out. The logout action should clear the JWT token and redirect to the login page.

**Why this priority**: Profile viewing and logout are essential for security and user account management. Implement after core CRUD to ensure the authentication flow is solid.

**Independent Test**: Can be fully tested by accessing the profile page, viewing user details, clicking logout, and verifying the user is redirected to login with JWT token cleared.

**Acceptance Scenarios**:

1. **Given** a logged-in user, **When** they click on their profile menu, **Then** they can view their email and account details
2. **Given** a logged-in user, **When** they click the logout button, **Then** they are logged out and redirected to the login page
3. **Given** a logged-out user, **When** they try to access a protected page directly (e.g., `/todos`), **Then** they are redirected to the login page
4. **Given** a user who just logged out, **When** they navigate back in their browser history, **Then** they cannot access protected pages without re-logging in

---

### User Story 8 - Create & Edit Todo (Priority: P1)

A user needs to create new todos and edit existing ones. The form should include fields for title, description, priority, and optionally due date. Changes should be persisted to the backend via JWT-authenticated API calls.

**Why this priority**: Creating and editing todos is fundamental to the todo app's core function. Without this, users cannot add or modify tasks.

**Independent Test**: Can be fully tested by creating a new todo with a title, verifying it appears in the list, then editing it to change the title and confirming the change persists.

**Acceptance Scenarios**:

1. **Given** the create todo form, **When** a user enters a title and clicks save, **Then** the todo is created and appears in the list
2. **Given** a user creating a todo, **When** they submit with an empty title, **Then** a validation error is shown
3. **Given** an existing todo in the list, **When** a user clicks edit, **Then** the todo form is populated with current data
4. **Given** a user editing a todo, **When** they change the title and save, **Then** the updated title appears in the list immediately

---

### User Story 9 - Delete Todo & User Isolation (Priority: P1)

A user should be able to delete their own todos. Critically, users should never see todos belonging to other users - each user's todo list must be strictly isolated based on their JWT identity.

**Why this priority**: User isolation is a security/data integrity requirement. Users must only access their own data. Delete functionality completes CRUD operations.

**Independent Test**: Can be fully tested by creating two user accounts, having each create todos, verifying User A cannot see User B's todos, and confirming a user can delete their own todo.

**Acceptance Scenarios**:

1. **Given** a user with existing todos, **When** they click delete on a todo, **Then** the todo is removed from the list and backend
2. **Given** User A who has created todos, **When** User B logs in, **Then** User B sees only their own todos (empty if they haven't created any)
3. **Given** User A and User B with separate todos, **When** User A logs in, **Then** they cannot access User B's todos through any means (direct API call with User B's todo ID)
4. **Given** a user viewing a todo, **When** they delete it, **Then** the deletion is confirmed and the UI updates without requiring a page refresh

---

### Edge Cases

- What happens when the backend is temporarily unavailable? (Error message should display, user should be able to retry)
- How does the system handle a JWT token expiring mid-session? (User is prompted to log in again)
- What if a user tries to access another user's todo via direct API call with their token? (401 Unauthorized response from backend)
- How should the UI handle slow network connections during todo list loading? (Loading skeleton or spinner should display)
- What happens if a user's browser closes unexpectedly? (JWT persists in browser storage, user remains logged in on next visit)
- What if filter/sort selection is made but todos are loading? (UI should show loading state and apply filters once data arrives)

## Requirements *(mandatory)*

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right functional requirements.
-->

### Functional Requirements

#### Authentication & Security
- **FR-001**: System MUST provide a `/signup` page using Better Auth hooks for new user registration with email and password
- **FR-002**: System MUST provide a `/login` page using Better Auth hooks for user authentication with email and password
- **FR-003**: System MUST automatically include the JWT token in the `Authorization: Bearer <token>` header for all API requests to protected endpoints
- **FR-004**: System MUST implement a Higher Order Component (HOC) or middleware that redirects unauthenticated users attempting to access protected pages to `/login`
- **FR-005**: System MUST provide a logout button that clears the JWT token and redirects authenticated users to `/login`
- **FR-006**: System MUST provide a user profile page showing logged-in user's email and account information
- **FR-007**: System MUST prevent JWT token leakage in logs, error messages, or local storage (store in httpOnly cookies via Better Auth)
- **FR-008**: System MUST handle JWT expiration gracefully and prompt users to re-authenticate

#### Todo List Management & Display
- **FR-009**: System MUST display the user's todo list fetched from the backend API at the protected `/todo` route
- **FR-010**: System MUST display all task details including title, description, priority level, completion status, and optional due date
- **FR-011**: System MUST allow users to filter todos by status: All, Pending (incomplete), Completed
- **FR-012**: System MUST allow users to sort todos by: Priority (High → Medium → Low), Due Date (soonest first), Title (alphabetical)
- **FR-013**: System MUST display an empty state message when user has no todos, with CTA to create first task
- **FR-014**: System MUST implement loading skeleton or spinner while todos are being fetched from backend

#### Todo CRUD Operations
- **FR-015**: System MUST allow users to create new todos with required title field and optional description, priority (High/Medium/Low), and due date
- **FR-016**: System MUST allow users to edit existing todos and update any field (title, description, priority, due date, status)
- **FR-017**: System MUST allow users to delete their own todos with optional confirmation dialog
- **FR-018**: System MUST allow users to toggle todo completion status by clicking a checkbox or status indicator
- **FR-019**: System MUST display success/error feedback after create, update, or delete operations
- **FR-020**: System MUST prevent duplicate API calls when user rapidly clicks create/update/delete buttons

#### User Interface & Theming
- **FR-021**: System MUST use Shadcn/UI components for all UI elements to ensure consistency and accessibility
- **FR-022**: System MUST use Tailwind CSS for responsive styling that works on desktop, tablet, and mobile screens (320px minimum width)
- **FR-023**: System MUST support light and dark theme modes with toggle control accessible from navigation or header
- **FR-024**: System MUST persist the user's theme preference across sessions using browser localStorage or server-side storage
- **FR-025**: System MUST automatically respect the user's OS-level theme preference on first visit if no saved preference exists
- **FR-026**: System MUST apply theme consistently across all pages (landing, login, signup, todo dashboard, profile)
- **FR-027**: System MUST provide a landing page at `/` with hero section, value proposition, and feature highlights for unauthenticated users
- **FR-028**: Landing page MUST include clear CTAs: "Get Started Free" redirecting to `/signup` and "Sign In" redirecting to `/login`
- **FR-029**: Landing page MUST be fully responsive and functional on screens 320px and larger with no horizontal scrolling

#### Error Handling & Feedback
- **FR-030**: System MUST display appropriate error messages when API calls fail (e.g., "Failed to load todos, please try again")
- **FR-031**: System MUST display error messages for validation failures (e.g., empty title, invalid email format, weak password)
- **FR-032**: System MUST implement retry mechanism for failed API requests with user-friendly prompts
- **FR-033**: System MUST handle backend unavailability gracefully with clear messaging and retry options

#### Data & User Isolation
- **FR-034**: System MUST display only the current user's todos based on their JWT identity (enforce on frontend and backend)
- **FR-035**: System MUST prevent users from accessing other users' todos even if they know the todo ID
- **FR-036**: System MUST redirect logged-out or unauthorized users accessing protected pages to `/login`

### Key Entities

- **User**: Represents a registered account with email, password managed by Better Auth, and a unique JWT token issued upon authentication
- **Todo**: Represents a task with title, description, priority (High/Medium/Low), status (Pending/Completed), optional due date, and ownership by a specific user
- **Theme**: Represents the UI theme preference (Light/Dark) stored per user in browser storage

## Success Criteria *(mandatory)*

<!--
  ACTION REQUIRED: Define measurable success criteria.
  These must be technology-agnostic and measurable.
-->

### Measurable Outcomes

- **SC-001**: Landing page loads and renders correctly without 404 errors on auth CTAs
- **SC-002**: Users can complete signup/login workflow in under 1 minute
- **SC-003**: Todo list loads and displays within 2 seconds on a standard broadband connection
- **SC-004**: Filtering and sorting operations update the displayed list instantly (under 500ms) without requiring a page reload
- **SC-005**: 95% of API requests include the JWT token in the Authorization header
- **SC-006**: User isolation is 100% enforced - no user can view, edit, or delete another user's todos
- **SC-007**: All pages are fully responsive and functional on screens 320px and larger (mobile-first design)
- **SC-008**: Theme toggle switches the entire UI between light and dark mode in under 1 second
- **SC-009**: Theme preference persists across browser sessions with 99% consistency
- **SC-010**: All interactive elements are keyboard navigable and screen reader compatible (WCAG 2.1 Level A)
- **SC-011**: Users can create a todo with title and priority in fewer than 10 keyboard/mouse interactions

## Assumptions

- Better Auth is already deployed and accessible at the configured `BETTER_AUTH_URL`
- Backend API at `NEXT_PUBLIC_API_URL` supports all CRUD operations for todos with JWT validation
- Users have modern browsers supporting ES2020+ and CSS custom properties (for theme switching)
- Network bandwidth is sufficient for real-time updates (no offline-first requirement)
- Theme preference is stored in browser localStorage (no server-side theme persistence required)
- JWT tokens are stored in secure browser storage (httpOnly cookies preferred by Better Auth)
- Landing page is served at root path `/` with correct route linking (no more `/signin` 404 errors)

## Out of Scope (Phase II)

- Real-time collaboration on shared todos
- Recurring/recurring task patterns
- File attachments to todos
- Task categories/projects beyond priority levels
- Email notifications or reminders
- Team/shared workspace functionality
- Offline mode or service workers

