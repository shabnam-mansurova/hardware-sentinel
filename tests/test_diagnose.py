"""Tests for end-to-end deterministic diagnosis."""

import unittest
from unittest.mock import patch

from hardware_sentinel.diagnose import diagnose_current_state


class DiagnoseTests(unittest.TestCase):

    @patch("hardware_sentinel.diagnose.create_incidents")
    @patch("hardware_sentinel.diagnose.analyze_snapshot")
    @patch("hardware_sentinel.diagnose.collect_snapshot")
    def test_diagnosis_connects_snapshot_analysis_and_incidents(
        self,
        mock_snapshot,
        mock_analysis,
        mock_create_incidents,
    ):
        mock_snapshot.return_value = {
            "timestamp_utc": "2026-09-28T10:00:00+00:00",
            "system": {
                "hostname": "test-machine",
                "os": "Linux",
                "kernel": "test-kernel",
                "architecture": "x86_64",
                "cpu_logical_count": 8,
                "cpu_physical_count": 4,
            },
        }

        mock_analysis.return_value = {
            "status": "normal",
            "warnings": [],
            "thermal_warnings": [],
            "metrics": {},
        }

        mock_create_incidents.return_value = []

        result = diagnose_current_state()

        mock_analysis.assert_called_once_with(mock_snapshot.return_value)

        self.assertEqual(
            result["machine"]["hostname"],
            "test-machine",
        )
        self.assertEqual(
            result["snapshot_timestamp_utc"],
            "2026-09-28T10:00:00+00:00",
        )
        self.assertEqual(result["analysis"]["status"], "normal")
        self.assertEqual(result["incidents"], [])
        self.assertTrue(result["session"]["session_id"])

        call = mock_create_incidents.call_args

        self.assertEqual(
            call.args[0],
            mock_analysis.return_value,
        )
        self.assertEqual(
            call.kwargs["detected_at"],
            "2026-09-28T10:00:00+00:00",
        )
        self.assertEqual(
            call.kwargs["session_id"],
            result["session"]["session_id"],
        )


if __name__ == "__main__":
    unittest.main()
