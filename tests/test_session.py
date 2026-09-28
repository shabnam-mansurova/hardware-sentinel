"""Tests for Hardware Sentinel session metadata."""

import json
import unittest

from hardware_sentinel.session import Session


class SessionTests(unittest.TestCase):

    def test_session_has_unique_identifier(self):
        first = Session()
        second = Session()

        self.assertTrue(first.session_id)
        self.assertTrue(second.session_id)
        self.assertNotEqual(first.session_id, second.session_id)

    def test_session_has_start_timestamp(self):
        session = Session()

        self.assertTrue(session.started_at)
        self.assertIn("+00:00", session.started_at)

    def test_session_serializes_to_json(self):
        session = Session()

        encoded = json.dumps(session.to_dict())
        decoded = json.loads(encoded)

        self.assertEqual(decoded["session_id"], session.session_id)
        self.assertEqual(decoded["started_at"], session.started_at)


if __name__ == "__main__":
    unittest.main()
