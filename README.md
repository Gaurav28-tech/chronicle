# AuditVault 🛡️

[![CI](https://github.com/Gaurav28-tech/audit-vault/actions/workflows/ci.yml/badge.svg)](https://github.com/Gaurav28-tech/audit-vault)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python: 3.9+](https://img.shields.io/badge/Python-3.9+-brightgreen.svg)]()

**AuditVault** is a tamper-evident audit trail and immutable ledger engine designed for compliance (SOC2, HIPAA, GDPR) and zero-trust security architectures. It links log events into an unbroken cryptographic SHA-256 hash chain, allowing automated proof of integrity and instant detection of retroactive modifications.

---

## 🚀 Key Features

- **Cryptographic Hash Chaining**: Every log record contains the SHA-256 hash of the preceding block, creating an immutable timeline.
- **Tamper Detection Engine**: Detects inserted, altered, or deleted logs with exact pinpointing of corruption boundaries.
- **Deterministic Canonicalization**: Sorts and canonicalizes JSON payloads before hashing to guarantee cross-system repeatability.
- **Compliance Query Filter**: Query ledger events by actor ID, resource type, action, or Unix epoch time ranges.
- **Self-Contained**: Implemented purely with Python standard libraries.

---

## 🏗️ Architecture

```
Event 1: "User.Login"
[Data + PrevHash: "000000"]  ===> SHA-256 ===> Hash: "e3b0c442..."
                                                      |
                                                      v
Event 2: "Role.Update"                    [PrevHash: "e3b0c442..."]
[Data + PrevHash: "e3b0c442..."] ===> SHA-256 ===> Hash: "a89f31b1..."
                                                      |
                                                      v
Event 3: "Payment.Transfer"               [PrevHash: "a89f31b1..."]
[Data + PrevHash: "a89f31b1..."] ===> SHA-256 ===> Hash: "5f4dcc3b..."
```

---

## 📦 Quickstart

### Installation

```bash
git clone https://github.com/Gaurav28-tech/audit-vault.git
cd audit-vault
```

### Basic Usage

```python
from auditvault.ledger import AuditLedger
from auditvault.verifier import ChainVerifier

ledger = AuditLedger()

# Append immutable audit entries
ledger.append(actor="usr_admin", action="user.delete", resource="usr_target_44", metadata={"ip": "192.168.1.1"})
ledger.append(actor="usr_billing", action="subscription.upgrade", resource="org_stripe", metadata={"tier": "enterprise"})

# Verify chain integrity
is_valid, error = ChainVerifier.verify(ledger.get_chain())
print(f"Ledger Integrity Valid: {is_valid}") # True
```

### Running Tests

```bash
python -m unittest discover -s tests -p "test_*.py"
```

---

## 📄 License

Distributed under the [MIT License](LICENSE).
