# Core Tools

**Space Black** provides these tools to **Ghost** (the agent). Ghost uses them autonomously to complete your requests.

### 🔐 Vault (Secure Storage)
Manage sensitive credentials securely. The Vault uses **AES encryption** (Fernet + PBKDF2) with a machine-local master key that auto-unlocks on each session — no passphrase needed.

*   `vault_act(action, key, value, category)`: Unified tool for all vault operations.
    *   `action="get"`: Retrieve a secret by key.
    *   `action="set"`: Store a secret with an optional category (`api_keys`, `passwords`, `tokens`, `oauth`, `general`).
    *   `action="delete"`: Remove a secret by key.
    *   `action="list"`: List all stored keys grouped by category (values hidden).
    *   `action="status"`: Show vault health — file size, secret count, categories.


### 🌐 Autonomous Web Browsing
Space Black gives Ghost a full headless browser to interact with the web.
*   `browser_go_to(url)`: Navigate to a URL.
*   `browser_click(selector)`: Click elements (buttons, links).
*   `browser_type(selector, text)`: Type into forms.
*   `browser_scroll(direction, amount)`: Scroll the page.
*   `browser_get_state()`: Get the Accessibility Tree (Ghost's "vision").
*   `browser_screenshot()`: Save a snapshot.

**See [BROWSING.md](./BROWSING.md) for the full guide on Browsing capabilities.**

### 🛠️ System Tools
Core capabilities for interacting with your machine.
### `execute_terminal_command`
Executes shell commands.
-   **Security**: Restricted to non-interactive commands.
-   **input**: `command` (string).

### `reflect_and_evolve`
Allows Ghost to update its own "Soul" (System Prompt).
-   **Usage**: Invoked when Ghost learns something new about how you want it to behave.
-   **Storage**: Updates `brain/SOUL.md`.

### `update_memory`
Writes to long-term memory.
-   **Usage**: Storing facts, events, or context.
-   **Storage**: `brain/memory/YYYY-MM-DD.md`.

### `update_user_profile`
Updates your user profile.
-   **Usage**: Learning about you (name, tech stack, preferences).
-   **Storage**: `brain/USER.md`.

### `exit_conversation`
Terminates the current conversational loop.
-   **Usage**: Used when interactions naturally conclude, or when the user explicitly requests to stop talking, preventing infinite or repetitive agent responses.

## Scheduler Tools (Cron Jobs)
Space Black runs a background daemon that constantly checks for due tasks.

### `schedule_task`
Adds a task to the execution queue (acts as a cron job or scheduled reminder).
-   **Usage**: Can define absolute times (`2026-10-10 14:00`) or relative recurrences (`daily`, `1h`, `30m`). When the task executes, the Daemon routes it to Ghost natively.
-   **Storage**: Updates `brain/SCHEDULE.json`.

### `cancel_task`
Removes a pending task from the queue.
-   **Usage**: Passing the exact task summary or ID to stop a recurring background job.

## Search Tools

### `web_search`
Quick search for information.
-   **Usage**: "Search for 'Python best practices'."
-   **Difference from Browsing**: `web_search` gets a list of results. `browser_go_to` actually visits the page to read/interact.

## File System (Native)

Ghost has safe, direct access to the local file system.

### `read_file`
-   **Description**: Reads text content.
-   **Usage**: "Read `brain/SOUL.md`."

### `write_file`
-   **Description**: Writes text content (overwrites).
-   **Usage**: "Create `notes.txt`."

### `list_directory`
-   **Description**: Lists files in a folder.

## Integration Tools

### 4. Jira Module
- `jira_act`: Central tool for Atlassian Jira interactions.
  - Actions: `get_issue`, `search_issues` (via JQL), `create_issue`, `add_comment`, `get_transitions`, `transition_issue`.
  - Usage examples: "What's the status of PROJ-42?", "Create a task in project TST for updating the database."

### 5. Google Workspace Module
When the Google skill is enabled via standard OAuth2, Ghost gains access to the following `@tool` endpoints:
*   `gmail_act(action, ...)`: Send, read, search, and manage emails.
*   `calendar_act(action, ...)`: Create, list, delete, and check calendar events.
*   `drive_act(action, ...)`: Upload, download, move, share, and list Drive files.
*   `docs_act(action, ...)`: Create, append, and read Google Docs.
*   `sheets_act(action, ...)`: Create, read, and write cell ranges to Google Sheets.
*   `wallet_act(action, ...)`: Create and manage Google Wallet passes (classes and objects).

### macOS Native Control
When running on macOS (with the skill enabled), Ghost can control local applications via AppleScript using a single endpoint:
*   `macos_act(action, ...)`: Controls Apple Mail, Calendar, Notes, Reminders, Finder, and System state. All operations are handled natively on your machine without relying on external web APIs. Only available on macOS (Darwin).

### Developer & Service APIs
*   `github_act(action, ...)`: Direct control over GitHub via API. Can read repos, manage issues, create branches, and directly manipulate code files.
*   `stripe_act(action, ...)`: Secure gateway to the Stripe API. Check accounts, list invoices, manage customers, and generate checkout sessions.
*   `paypal_act(action, ...)`: Access the PayPal Developer API to check balances, securely send payouts (with explicit console confirmation required), and draft invoices.
*   `discord_act(action, ...)`: Background Discord bot controller. Can send messages, list guild members, read channels, and manage DMs.
*   `slack_act(action, ...)`: Background Socket Mode Slack bot. Send DM/Channel messages, read histories, and react to threads.
*   `get_current_weather(location)`: Fetches real-time weather from OpenWeather.
*   `send_telegram_message(message)`: Broadcasts a message to the user via the Telegram Gateway.
