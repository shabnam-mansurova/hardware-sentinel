"""Tests for optional GPU telemetry."""

import unittest
from unittest.mock import patch

from hardware_sentinel.gpu import (
    _detect_intel_gpu,
    _gpu_capability,
    collect_gpu,
)


class GPUTests(unittest.TestCase):

    def setUp(self):
        """Clear cached hardware state before every test."""
        _detect_intel_gpu.cache_clear()
        _gpu_capability.cache_clear()

    def tearDown(self):
        """Prevent cached test state from leaking into another test."""
        _detect_intel_gpu.cache_clear()
        _gpu_capability.cache_clear()

    @patch("hardware_sentinel.gpu._detect_intel_gpu", return_value=False)
    def test_no_supported_gpu(self, _mock_detect):
        result = collect_gpu()

        self.assertFalse(result["available"])
        self.assertFalse(result["metrics_available"])
        self.assertEqual(result["reason"], "no_supported_gpu")

    @patch("hardware_sentinel.gpu.shutil.which", return_value=None)
    @patch("hardware_sentinel.gpu._detect_intel_gpu", return_value=True)
    def test_missing_intel_gpu_top(self, _mock_detect, _mock_which):
        result = collect_gpu()

        self.assertTrue(result["available"])
        self.assertFalse(result["metrics_available"])
        self.assertEqual(
            result["reason"],
            "intel_gpu_top_not_installed",
        )


if __name__ == "__main__":
    unittest.main()
