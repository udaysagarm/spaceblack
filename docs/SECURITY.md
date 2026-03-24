# Security & Privacy

Space Black is designed with a "Local-First" philosophy. Your data, keys, and memories stay on your machine.

## API Key Management
-   **Storage**: API keys (Google, OpenAI, Anthropic, Telegram) are stored in the `.env` file in the project root.
-   **Protection**: The `.env` file is included in `.gitignore` to prevent accidental commits to public repositories.
-   **Configuration**: Keys can be managed via the TUI (`/config` and `/skills`) or by manually editing the `.env` file.

## Vault Security (Credential Storage)
Space Black provides a zero-configuration encrypted vault for storing user passwords, API keys, and tokens.
1.  **Machine-Local Master Key**: A random 32-byte key is generated once and stored in the OS keyring (macOS Keychain, Windows Credential Manager, Linux Secret Service). A file fallback at `~/.spaceblack/.vault_key` is used if keyring is unavailable.
2.  **AES Encryption at Rest**: All secrets are encrypted using Fernet (AES-128-CBC + HMAC-SHA256) with a key derived via PBKDF2 (390,000 iterations). The encrypted vault lives at `brain/vault/secrets.enc`.
3.  **Auto-Unlock**: The vault automatically unlocks on the same machine without requiring a passphrase each session. Secrets cannot be decrypted on a different machine without the master key.
4.  **No Plaintext Storage**: All legacy plaintext secret files (`secrets.json`) have been removed. Secrets are only ever stored encrypted.
5.  **Category Organization**: Secrets are organized by category (`passwords`, `api_keys`, `tokens`, `oauth`, `general`) with modification timestamps for auditing.

## Telegram Gateway Security
The Telegram Bot skill is a public-facing interface. To secure it:
1.  **Allowed User ID**: The bot validates every incoming message against the `allowed_user_id` configured in `config.json`. Messages from unauthorized users are rejected immediately.
2.  **No Public Access**: The bot does not respond to group chats or unknown users by default.

## File System Access
The agent has the ability to execute terminal commands.
-   **Risk**: The agent runs with the same permissions as the user who started the script.
-   **Mitigation**: Do not run the agent as `root` or `Administrator`.
-   **Guardrails**: Critical system commands (like `rm -rf /`) are ideally blocked by the agent's internal safety prompts, but user discretion is advised when authorizing command logic.

## Memory Privacy
All conversation logs and user profiles are stored in plain text (Markdown) within the `brain/` directory.
-   **Encryption**: At rest, these files are not encrypted by Space Black. Rely on your operating system's disk encryption (e.g., FileVault, BitLocker).
-   **Sharing**: The `brain/` directory is ignored by Git to prevent uploading your personal conversation history.
