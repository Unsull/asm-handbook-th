import unittest
from authorization import read_order


class AuthorizationTests(unittest.TestCase):
    def test_cross_user_denied(self):
        with self.assertRaises(PermissionError):
            read_order("alice", "order-2")

    def test_owner_allowed(self):
        self.assertEqual(read_order("bob", "order-2")["total"], 950)

    def test_missing_order(self):
        with self.assertRaises(KeyError):
            read_order("bob", "does-not-exist")
