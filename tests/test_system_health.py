"""Tests for deterministic system health collection."""

import subprocess
import unittest
from unittest.mock import patch

from hardware_sentinel.system_health import (
    _failed_units,
    collect_system_health,
)


class SystemHealthTests(unittest.TestCase):

    @patch("hardware_sentinel.system_health._run_systemctl")
    def test_no_failed_units(self, mock_run):
        mock_run.return_value = subprocess.CompletedProcess(
            args=["systemctl"],
            returncode=0,
            stdout="",
            stderr="",
        )

        result = _failed_units()

        self.assertTrue(result["available"])
        self.assertEqual(result["count"], 0)
        self.assertEqual(result["units"], [])

    @patch("hardware_sentinel.system_health._run_systemctl")
    def test_failed_units_are_parsed(self, mock_run):
        mock_run.return_value = subprocess.CompletedProcess(
            args=["systemctl"],
            returncode=0,
            stdout=(
                "example.service loaded failed failed Example Service\n"
                "demo.service loaded failed failed Demo Service\n"
            ),
            stderr="",
        )

        result = _failed_units()

        self.assertTrue(result["available"])
        self.assertEqual(result["count"], 2)
        self.assertEqual(
            result["units"],
            ["example.service", "demo.service"],
        )

    @patch("hardware_sentinel.system_health._run_systemctl")
    def test_system_state_running(self, mock_run):
        mock_run.return_value = subprocess.CompletedProcess(
            args=["systemctl"],
            returncode=0,
            stdout="running\n",
            stderr="",
        )

        result = collect_system_health()

        self.assertEqual(
            result["systemd"]["system_state"]["state"],
            "running",
        )


    @patch("hardware_sentinel.system_health._run_systemctl")
    def test_degraded_state_is_available_but_unhealthy(self, mock_run):
        mock_run.return_value = subprocess.CompletedProcess(
            args=["systemctl"],
            returncode=1,
            stdout="degraded\n",
            stderr="",
        )

        result = collect_system_health()
        state = result["systemd"]["system_state"]

        self.assertTrue(state["available"])
        self.assertEqual(state["state"], "degraded")
        self.assertFalse(state["healthy"])


if __name__ == "__main__":
    unittest.main()
