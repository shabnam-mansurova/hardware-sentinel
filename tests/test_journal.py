"""Tests for bounded systemd journal evidence collection."""

import json
import subprocess
import unittest
from unittest.mock import patch

from hardware_sentinel.journal import (
    MAX_LINES,
    TRUST_CLASSIFICATION,
    _parse_entry,
    collect_journal_evidence,
)


class JournalTests(unittest.TestCase):

    def test_parse_valid_entry(self):
        raw = {
            "__REALTIME_TIMESTAMP": "1720000000000000",
            "_SYSTEMD_UNIT": "kernel.service",
            "SYSLOG_IDENTIFIER": "kernel",
            "PRIORITY": "4",
            "MESSAGE": "Example warning",
        }

        result = _parse_entry(json.dumps(raw))

        self.assertIsNotNone(result)
        self.assertEqual(result["source"], "systemd_journal")
        self.assertEqual(result["trust"], TRUST_CLASSIFICATION)
        self.assertEqual(result["message"], "Example warning")
        self.assertEqual(result["priority"], "4")

    def test_parse_malformed_json_returns_none(self):
        self.assertIsNone(_parse_entry("not valid json"))

    def test_non_string_message_is_normalized(self):
        result = _parse_entry(json.dumps({"MESSAGE": 123}))

        self.assertIsNotNone(result)
        self.assertEqual(result["message"], "123")

    @patch("hardware_sentinel.journal._run_journalctl")
    def test_successful_collection(self, mock_run):
        entries = [
            json.dumps({"MESSAGE": "warning one", "PRIORITY": "4"}),
            json.dumps({"MESSAGE": "warning two", "PRIORITY": "4"}),
        ]

        mock_run.return_value = subprocess.CompletedProcess(
            args=["journalctl"],
            returncode=0,
            stdout="\n".join(entries),
            stderr="",
        )

        result = collect_journal_evidence(lines=20)

        self.assertTrue(result["available"])
        self.assertEqual(result["trust"], TRUST_CLASSIFICATION)
        self.assertEqual(result["count"], 2)
        self.assertEqual(len(result["entries"]), 2)

        for entry in result["entries"]:
            self.assertEqual(entry["trust"], "untrusted")

    @patch("hardware_sentinel.journal._run_journalctl")
    def test_malformed_lines_are_skipped(self, mock_run):
        stdout = "\n".join(
            [
                json.dumps({"MESSAGE": "valid"}),
                "malformed-json",
                json.dumps({"MESSAGE": "also valid"}),
            ]
        )

        mock_run.return_value = subprocess.CompletedProcess(
            args=["journalctl"],
            returncode=0,
            stdout=stdout,
            stderr="",
        )

        result = collect_journal_evidence()

        self.assertTrue(result["available"])
        self.assertEqual(result["count"], 2)

    @patch("hardware_sentinel.journal._run_journalctl")
    def test_unavailable_journalctl_degrades_cleanly(self, mock_run):
        mock_run.return_value = None

        result = collect_journal_evidence()

        self.assertFalse(result["available"])
        self.assertEqual(result["trust"], TRUST_CLASSIFICATION)
        self.assertEqual(result["entries"], [])
        self.assertEqual(result["reason"], "journalctl_unavailable")

    @patch("hardware_sentinel.journal._run_journalctl")
    def test_failed_journalctl_degrades_cleanly(self, mock_run):
        mock_run.return_value = subprocess.CompletedProcess(
            args=["journalctl"],
            returncode=1,
            stdout="",
            stderr="failure",
        )

        result = collect_journal_evidence()

        self.assertFalse(result["available"])
        self.assertEqual(result["reason"], "journalctl_failed")
        self.assertEqual(result["entries"], [])

    @patch("hardware_sentinel.journal._run_journalctl")
    def test_line_count_is_capped(self, mock_run):
        mock_run.return_value = subprocess.CompletedProcess(
            args=["journalctl"],
            returncode=0,
            stdout="",
            stderr="",
        )

        collect_journal_evidence(lines=10000)

        args = mock_run.call_args.args[0]
        self.assertIn(f"--lines={MAX_LINES}", args)

    @patch("hardware_sentinel.journal._run_journalctl")
    def test_line_count_has_minimum_of_one(self, mock_run):
        mock_run.return_value = subprocess.CompletedProcess(
            args=["journalctl"],
            returncode=0,
            stdout="",
            stderr="",
        )

        collect_journal_evidence(lines=0)

        args = mock_run.call_args.args[0]
        self.assertIn("--lines=1", args)

    @patch("hardware_sentinel.journal.subprocess.run")
    def test_timeout_returns_unavailable(self, mock_run):
        mock_run.side_effect = subprocess.TimeoutExpired(
            cmd=["journalctl"],
            timeout=5,
        )

        result = collect_journal_evidence()

        self.assertFalse(result["available"])
        self.assertEqual(result["reason"], "journalctl_unavailable")


if __name__ == "__main__":
    unittest.main()
