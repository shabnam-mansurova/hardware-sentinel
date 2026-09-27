"""Tests for deterministic hardware analysis."""

import unittest

from hardware_sentinel.analyzer import analyze_snapshot


class AnalyzerTests(unittest.TestCase):

    def _snapshot(self):
        return {
            "cpu": {"total_percent": 20.0},
            "memory": {"percent": 40.0},
            "swap": {"percent": 1.0},
            "disk": {"percent": 30.0},
            "temperatures": {
                "coretemp": [
                    {
                        "label": "Package id 0",
                        "current_c": 45.0,
                        "high_c": 100.0,
                        "critical_c": 100.0,
                    }
                ]
            },
        }

    def test_normal_snapshot(self):
        result = analyze_snapshot(self._snapshot())

        self.assertEqual(result["status"], "normal")
        self.assertEqual(result["warnings"], [])
        self.assertEqual(result["thermal_warnings"], [])

    def test_high_cpu_warning(self):
        snapshot = self._snapshot()
        snapshot["cpu"]["total_percent"] = 95.0

        result = analyze_snapshot(snapshot)

        self.assertEqual(result["status"], "warning")
        self.assertIn("high_cpu_usage", result["warnings"])

    def test_critical_temperature_uses_sensor_threshold(self):
        snapshot = self._snapshot()
        snapshot["temperatures"]["coretemp"][0]["current_c"] = 100.0

        result = analyze_snapshot(snapshot)

        self.assertIn("thermal_warning", result["warnings"])
        self.assertEqual(
            result["thermal_warnings"][0]["state"],
            "critical",
        )
        self.assertEqual(
            result["thermal_warnings"][0]["threshold_c"],
            100.0,
        )


if __name__ == "__main__":
    unittest.main()
