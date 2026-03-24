"""
Space Black Vault — Integration Test
=====================================
Tests the unified vault_act tool: set, get, list, delete, status.
"""
from tools.vault import vault_act

PASS = "✅ PASS"
FAIL = "❌ FAIL"

def check(label: str, condition: bool):
    print(f"  {PASS if condition else FAIL}  {label}")
    return condition

def main():
    print("━" * 50)
    print("  🔐 Space Black Vault Test Suite")
    print("━" * 50)
    results = []

    # 1. SET a secret
    print("\n[1] Setting secrets...")
    r = vault_act.invoke({"action": "set", "key": "test_api_key", "value": "sk-12345", "category": "api_keys"})
    results.append(check("set api_key", "saved" in r.lower() or "✅" in r))

    r = vault_act.invoke({"action": "set", "key": "test_password", "value": "hunter2", "category": "passwords"})
    results.append(check("set password", "saved" in r.lower() or "✅" in r))

    # 2. GET a secret
    print("\n[2] Retrieving secrets...")
    r = vault_act.invoke({"action": "get", "key": "test_api_key"})
    results.append(check("get api_key == sk-12345", r == "sk-12345"))

    r = vault_act.invoke({"action": "get", "key": "test_password"})
    results.append(check("get password == hunter2", r == "hunter2"))

    # 3. GET non-existent
    r = vault_act.invoke({"action": "get", "key": "does_not_exist"})
    results.append(check("get missing key returns 'not found'", "not found" in r.lower()))

    # 4. LIST
    print("\n[3] Listing secrets...")
    r = vault_act.invoke({"action": "list"})
    results.append(check("list contains test_api_key", "test_api_key" in r))
    results.append(check("list contains test_password", "test_password" in r))
    results.append(check("list shows categories", "api_keys" in r and "passwords" in r))
    print(f"    → Output:\n{r}\n")

    # 5. STATUS
    print("[4] Vault status...")
    r = vault_act.invoke({"action": "status"})
    results.append(check("status shows file info", "secrets.enc" in r or "Secrets:" in r))
    print(f"    → Output:\n{r}\n")

    # 6. DELETE
    print("[5] Deleting secrets...")
    r = vault_act.invoke({"action": "delete", "key": "test_api_key"})
    results.append(check("delete api_key", "deleted" in r.lower() or "🗑️" in r))

    r = vault_act.invoke({"action": "get", "key": "test_api_key"})
    results.append(check("get after delete returns 'not found'", "not found" in r.lower()))

    # Clean up test password too
    vault_act.invoke({"action": "delete", "key": "test_password"})

    # 7. Invalid action
    print("\n[6] Edge cases...")
    r = vault_act.invoke({"action": "bogus"})
    results.append(check("unknown action returns error", "unknown" in r.lower()))

    r = vault_act.invoke({"action": "set", "key": "", "value": "x"})
    results.append(check("set without key returns error", "error" in r.lower()))

    # Summary
    passed = sum(results)
    total = len(results)
    print("\n" + "━" * 50)
    print(f"  Results: {passed}/{total} passed")
    if passed == total:
        print("  🎉 All tests passed!")
    else:
        print(f"  ⚠️  {total - passed} test(s) failed")
    print("━" * 50)

if __name__ == "__main__":
    main()
