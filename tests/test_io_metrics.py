"""Tests for disk and network I/O telemetry."""

import unittest

from hardware_sentinel.io_metrics import calculate_io_rates


class IOMetricsTests(unittest.TestCase):

    def _previous(self):
        return {
            "disk": {
                "available": True,
                "read_bytes": 1000,
                "write_bytes": 2000,
            },
            "network": {
                "available": True,
                "bytes_sent": 500,
                "bytes_received": 1000,
            },
        }

    def _current(self):
        return {
            "disk": {
                "available": True,
                "read_bytes": 3000,
                "write_bytes": 6000,
            },
            "network": {
                "available": True,
                "bytes_sent": 1500,
                "bytes_received": 5000,
            },
        }

    def test_calculates_rates(self):
        result = calculate_io_rates(
            self._previous(),
            self._current(),
            2.0,
        )

        self.assertEqual(
            result["disk"]["read_bytes_per_sec"],
            1000.0,
        )
        self.assertEqual(
            result["disk"]["write_bytes_per_sec"],
            2000.0,
        )
        self.assertEqual(
            result["network"]["sent_bytes_per_sec"],
            500.0,
        )
        self.assertEqual(
            result["network"]["received_bytes_per_sec"],
            2000.0,
        )

    def test_counter_reset_does_not_create_negative_rate(self):
        previous = self._previous()
        current = self._current()

        current["disk"]["read_bytes"] = 100
        current["network"]["bytes_received"] = 100

        result = calculate_io_rates(
            previous,
            current,
            2.0,
        )

        self.assertEqual(
            result["disk"]["read_bytes_per_sec"],
            0.0,
        )
        self.assertEqual(
            result["network"]["received_bytes_per_sec"],
            0.0,
        )

    def test_rejects_invalid_elapsed_time(self):
        with self.assertRaises(ValueError):
            calculate_io_rates(
                self._previous(),
                self._current(),
                0,
            )


if __name__ == "__main__":
    unittest.main()
