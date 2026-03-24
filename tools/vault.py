"""
Space Black Vault — Unified Encrypted Secret Manager
=====================================================
Provides a single `vault_act` LangChain tool for all secret operations.

Architecture:
  - Encryption: AES-128 via Fernet (PBKDF2-derived key, 390 000 iterations)
  - Master key: Random 32-byte token stored in the OS keyring (keyring lib).
    Falls back to a file at ~/.spaceblack/.vault_key if keyring is unavailable.
  - The encrypted vault lives at  brain/vault/secrets.enc
  - No manual passphrase needed — the vault auto-unlocks on the same machine.
"""

import os
import json
import time
import base64
import keyring
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from langchain_core.tools import tool

# ── Paths ────────────────────────────────────────────────────────────────────
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
VAULT_DIR = os.path.join(ROOT_DIR, "brain", "vault")
VAULT_FILE = os.path.join(VAULT_DIR, "secrets.enc")

KEYRING_SERVICE = "spaceblack_vault"
KEYRING_KEY     = "master_key"
FALLBACK_KEY_DIR  = os.path.expanduser("~/.spaceblack")
FALLBACK_KEY_FILE = os.path.join(FALLBACK_KEY_DIR, ".vault_key")

# Fixed salt — the master key itself is random, so per-file salts aren't needed
_SALT = b"SpaceBlack_Vault_"  # 17 bytes, padded/truncated to 16 below
_SALT = _SALT[:16]

# ── Internal helpers ─────────────────────────────────────────────────────────

def _get_or_create_master_key() -> str:
    """
    Retrieves the master key from OS keyring.
    If not found, generates one and stores it.
    Falls back to a hidden file if keyring is unavailable.
    """
    # 1. Try OS keyring
    try:
        stored = keyring.get_password(KEYRING_SERVICE, KEYRING_KEY)
        if stored:
            return stored
    except Exception:
        pass

    # 2. Try fallback file
    if os.path.exists(FALLBACK_KEY_FILE):
        try:
            with open(FALLBACK_KEY_FILE, "r") as f:
                return f.read().strip()
        except Exception:
            pass

    # 3. Generate new key
    new_key = base64.urlsafe_b64encode(os.urandom(32)).decode("utf-8")

    # Store in keyring
    try:
        keyring.set_password(KEYRING_SERVICE, KEYRING_KEY, new_key)
    except Exception:
        pass

    # Also store in fallback file
    try:
        os.makedirs(FALLBACK_KEY_DIR, mode=0o700, exist_ok=True)
        with open(FALLBACK_KEY_FILE, "w") as f:
            f.write(new_key)
        if os.name != "nt":
            os.chmod(FALLBACK_KEY_FILE, 0o600)
    except Exception:
        pass

    return new_key


def _derive_fernet(master_key: str) -> Fernet:
    """Derives a Fernet cipher from the master key using PBKDF2."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=_SALT,
        iterations=390_000,
    )
    derived = base64.urlsafe_b64encode(kdf.derive(master_key.encode("utf-8")))
    return Fernet(derived)


def _load_vault() -> dict:
    """Loads and decrypts the vault. Returns empty dict if missing or corrupt."""
    if not os.path.exists(VAULT_FILE):
        return {}
    try:
        fernet = _derive_fernet(_get_or_create_master_key())
        with open(VAULT_FILE, "rb") as f:
            ciphertext = f.read()
        plaintext = fernet.decrypt(ciphertext)
        return json.loads(plaintext.decode("utf-8"))
    except (InvalidToken, Exception) as e:
        # If decryption fails (different machine / corrupted), return empty
        return {}


def _save_vault(data: dict) -> bool:
    """Encrypts and writes the vault to disk."""
    try:
        os.makedirs(VAULT_DIR, exist_ok=True)
        fernet = _derive_fernet(_get_or_create_master_key())
        plaintext = json.dumps(data, indent=2).encode("utf-8")
        ciphertext = fernet.encrypt(plaintext)
        with open(VAULT_FILE, "wb") as f:
            f.write(ciphertext)
        if os.name != "nt":
            os.chmod(VAULT_FILE, 0o600)
        return True
    except Exception as e:
        print(f"[Vault] Write error: {e}")
        return False


def _timestamp() -> str:
    return time.strftime("%Y-%m-%d %H:%M:%S")


# ── Public LangChain Tool ───────────────────────────────────────────────────

@tool
def vault_act(action: str, key: str = "", value: str = "", category: str = "general") -> str:
    """
    Unified vault tool for secure secret management.
    All secrets are encrypted at rest using AES (Fernet) with a machine-local master key.

    Actions:
      • get     — Retrieve a secret.        Args: key (required)
      • set     — Store or update a secret.  Args: key (required), value (required), category (optional, default "general")
      • delete  — Remove a secret.           Args: key (required)
      • list    — List all stored secret keys and their categories (values are hidden).
      • status  — Show vault health info (file exists, number of secrets, categories).

    Categories help organize secrets: "passwords", "api_keys", "tokens", "oauth", "general", etc.
    """
    action = action.strip().lower()

    # ── GET ──────────────────────────────────────────────────────────────
    if action == "get":
        if not key:
            return "Error: 'key' is required for the 'get' action."
        vault = _load_vault()
        entry = vault.get(key)
        if entry is None:
            return f"Secret '{key}' not found in the vault."
        # entry is {"value": ..., "category": ..., "updated": ...}
        if isinstance(entry, dict):
            return entry.get("value", str(entry))
        return str(entry)  # legacy plain-value fallback

    # ── SET ──────────────────────────────────────────────────────────────
    elif action == "set":
        if not key:
            return "Error: 'key' is required for the 'set' action."
        if not value:
            return "Error: 'value' is required for the 'set' action."
        vault = _load_vault()
        vault[key] = {
            "value": value,
            "category": category or "general",
            "updated": _timestamp(),
        }
        if _save_vault(vault):
            return f"✅ Secret '{key}' saved to vault (category: {category})."
        return f"❌ Failed to save secret '{key}'."

    # ── DELETE ───────────────────────────────────────────────────────────
    elif action == "delete":
        if not key:
            return "Error: 'key' is required for the 'delete' action."
        vault = _load_vault()
        if key not in vault:
            return f"Secret '{key}' not found in the vault."
        del vault[key]
        if _save_vault(vault):
            return f"🗑️ Secret '{key}' deleted from vault."
        return f"❌ Failed to delete secret '{key}'."

    # ── LIST ─────────────────────────────────────────────────────────────
    elif action == "list":
        vault = _load_vault()
        if not vault:
            return "Vault is empty — no secrets stored."
        lines = ["🔐 **Vault Contents** (values hidden):\n"]
        # Group by category
        by_cat: dict[str, list[str]] = {}
        for k, v in vault.items():
            cat = v.get("category", "general") if isinstance(v, dict) else "general"
            by_cat.setdefault(cat, []).append(k)
        for cat in sorted(by_cat.keys()):
            lines.append(f"  **{cat}**")
            for k in sorted(by_cat[cat]):
                entry = vault[k]
                ts = entry.get("updated", "—") if isinstance(entry, dict) else "—"
                lines.append(f"    • {k}  (updated: {ts})")
        lines.append(f"\nTotal: {len(vault)} secret(s)")
        return "\n".join(lines)

    # ── STATUS ───────────────────────────────────────────────────────────
    elif action == "status":
        exists = os.path.exists(VAULT_FILE)
        if not exists:
            return "Vault file does not exist yet. Store a secret to create it."
        vault = _load_vault()
        categories = set()
        for v in vault.values():
            if isinstance(v, dict):
                categories.add(v.get("category", "general"))
        size_kb = os.path.getsize(VAULT_FILE) / 1024
        return (
            f"🔐 **Vault Status**\n"
            f"  File: brain/vault/secrets.enc ({size_kb:.1f} KB)\n"
            f"  Secrets: {len(vault)}\n"
            f"  Categories: {', '.join(sorted(categories)) if categories else '—'}\n"
            f"  Encryption: AES-128 (Fernet + PBKDF2)\n"
            f"  Auto-unlock: ✅ (machine-local key)"
        )

    else:
        return (
            f"Unknown action '{action}'. "
            f"Available actions: get, set, delete, list, status"
        )
