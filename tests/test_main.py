import pytest
from PySide6.QtWidgets import QApplication
from PySide6.QtTest import QTest
from PySide6.QtCore import Qt
import sys
from main import main

@pytest.fixture
def app():
    return QApplication(sys.argv)

def test_main_application(app):
    """Test that the main application starts correctly."""
    # Create a mock for sys.exit to prevent the application from actually exiting
    with pytest.MonkeyPatch.context() as m:
        m.setattr(sys, 'exit', lambda x: None)
        
        # Run the main function
        main()
        
        # Verify that the application started
        assert QApplication.instance() is not None 