import unittest
import sys
import os

# Ensure imports work
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from core.automation import WindowScanner, BomberEngine

class TestCyberBomberCore(unittest.TestCase):
    def test_imports(self):
        """Test if core modules import correctly"""
        self.assertIsNotNone(WindowScanner)
        self.assertIsNotNone(BomberEngine)

    def test_scanner_instantiation(self):
        """Test WindowScanner instantiation"""
        scanner = WindowScanner()
        self.assertIsInstance(scanner, WindowScanner)
        # scan_windows 使用硬编码的进程白名单，无需传递 keywords
        windows = scanner.scan_windows()
        self.assertIsInstance(windows, list)

    def test_engine_instantiation(self):
        """Test BomberEngine instantiation"""
        engine = BomberEngine()
        self.assertIsInstance(engine, BomberEngine)
        self.assertFalse(engine._stop_event.is_set())

    def test_engine_stop(self):
        """Test emergency stop sets the event"""
        engine = BomberEngine()
        engine.emergency_stop()
        self.assertTrue(engine._stop_event.is_set())

def mock_log(msg):
    print(f"[TEST LOG] {msg}")

if __name__ == '__main__':
    print("Running Core Tests...")
    unittest.main()
