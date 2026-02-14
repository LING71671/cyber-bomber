import unittest
import sys
import os
import threading
import time

# Ensure imports work
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from core.automation import WindowScanner, BomberEngine

class TestCyberBomberCore(unittes
t.TestCase):
    def test_imports(self):
        """Test if core modules import correctly"""
        self.assertIsNotNone(WindowScanner)
        self.assertIsNotNone(BomberEngine)

    def test_scanner_instantiation(self):
        """Test WindowScanner instantiation"""
        scanner = WindowScanner()
        self.assertIsInstance(scanner, WindowScanner)
        # Note: We can't easily test scan_windows without a GUI env, 
        # but we can try to scan and see if it returns a list (even empty)
        windows = scanner.scan_windows(keywords=["NonExistentWindow12345"])
        self.assertIsInstance(windows, list)
        self.assertEqual(len(windows), 0)

    def test_engine_instantiation(self):
        """Test BomberEngine instantiation"""
        engine = BomberEngine()
        self.assertIsInstance(engine, BomberEngine)
        self.assertFalse(engine._stop_event.is_set())

def mock_log(msg):
    print(f"[TEST LOG] {msg}")

if __name__ == '__main__':
    print("Running Core Tests...")
    unittest.main()
