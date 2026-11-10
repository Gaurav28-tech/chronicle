import os
import sys
import unittest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from auditvault.ledger import AuditLedger
from auditvault.verifier import ChainVerifier

class TestAuditVault(unittest.TestCase):
    def setUp(self):
        self.ledger = AuditLedger()

    def test_ledger_append_and_verify(self):
        b0 = self.ledger.append(actor="alice", action="create", resource="user:1")
        b1 = self.ledger.append(actor="bob", action="update", resource="user:1")
        
        self.assertEqual(len(self.ledger.get_chain()), 2)
        self.assertEqual(b1.prev_hash, b0.hash)

        is_valid, err = ChainVerifier.verify(self.ledger.get_chain())
        self.assertTrue(is_valid)
        self.assertIsNone(err)

    def test_tamper_detection(self):
        self.ledger.append(actor="alice", action="login", resource="app")
        self.ledger.append(actor="admin", action="grant_role", resource="user:10")

        chain = self.ledger.get_chain()
        # Tamper with an action in index 1
        chain[1].action = "revoke_role"

        is_valid, err = ChainVerifier.verify(chain)
        self.assertFalse(is_valid)
        self.assertIn("Tampered data detected", err)

    def test_query_filter(self):
        self.ledger.append(actor="user_1", action="read", resource="doc")
        self.ledger.append(actor="user_2", action="write", resource="doc")

        results = self.ledger.query(actor="user_1")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].action, "read")

if __name__ == "__main__":
    unittest.main()
