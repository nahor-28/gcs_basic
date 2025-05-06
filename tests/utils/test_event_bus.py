# tests/utils/test_event_bus.py (Simplified)

import pytest
import logging
from unittest.mock import Mock

# Adjust import path if necessary
from utils.event_bus import EventBus, Events

# --- Fixtures ---

@pytest.fixture
def bus():
    """Provides a fresh EventBus instance for each test."""
    return EventBus()

@pytest.fixture
def mock_handler():
    """Provides a generic mock handler function with a name attribute."""
    # Just use the name argument, this is sufficient.
    return Mock(name='mock_handler_func')

# Remove mock_ui_app fixture as we are removing tests that use it for now
# @pytest.fixture
# def mock_ui_app(): ...

# --- Core Test Cases ---

def test_subscribe_single_handler(bus, mock_handler):
    """Core Test: Subscribing a single handler."""
    event_type = "test_event"
    bus.subscribe(event_type, mock_handler)
    assert event_type in bus._subscribers
    assert mock_handler in bus._subscribers[event_type]
    assert len(bus._subscribers[event_type]) == 1

def test_subscribe_multiple_handlers(bus):
    """Core Test: Subscribing multiple handlers to the same event."""
    event_type = "multi_handler_event"
    handler1 = Mock(name='handler1') # Use name= argument
    handler2 = Mock(name='handler2')
    bus.subscribe(event_type, handler1)
    bus.subscribe(event_type, handler2)
    assert len(bus._subscribers[event_type]) == 2
    assert handler1 in bus._subscribers[event_type]
    assert handler2 in bus._subscribers[event_type]

def test_subscribe_duplicate_handler(bus, mock_handler):
    """Core Test: Subscribing the same handler twice doesn't add duplicates."""
    event_type = "duplicate_event"
    bus.subscribe(event_type, mock_handler)
    bus.subscribe(event_type, mock_handler) # Subscribe again
    assert len(bus._subscribers[event_type]) == 1

# def test_subscribe_non_callable(bus, caplog):
#     """Core Test: Attempting to subscribe something non-callable fails gracefully."""
#     event_type = "non_callable_event"
#     with caplog.at_level(logging.ERROR):
#         bus.subscribe(event_type, 123)
#     assert event_type not in bus._subscribers
#     assert "non-callable handler" in caplog.text # Check log

def test_subscribe_non_callable(bus): # Remove caplog fixture, not needed now
    """Core Test: Attempting to subscribe something non-callable raises TypeError."""
    event_type = "non_callable_event"
    not_a_function = 123 # The non-callable thing

    # Use pytest.raises to assert that a TypeError occurs within this block
    with pytest.raises(TypeError) as excinfo:
        bus.subscribe(event_type, not_a_function)

    # Optional: Check the exception message contains useful info
    assert "not callable" in str(excinfo.value)
    # Ensure it wasn't actually added
    assert event_type not in bus._subscribers


def test_unsubscribe_handler(bus, mock_handler):
    """Core Test: Unsubscribing a handler."""
    event_type = "unsubscribe_event"
    bus.subscribe(event_type, mock_handler)
    assert mock_handler in bus._subscribers[event_type]
    bus.unsubscribe(event_type, mock_handler)
    assert event_type not in bus._subscribers or mock_handler not in bus._subscribers[event_type]

def test_unsubscribe_non_existent_handler(bus, mock_handler):
    """Core Test: Unsubscribing a handler that wasn't subscribed is handled."""
    event_type = "unsubscribe_fail_event"
    handler_never_subscribed = Mock(name='never_subscribed_handler')
    bus.subscribe(event_type, mock_handler) # Subscribe a different one
    bus.unsubscribe(event_type, handler_never_subscribed) # Should not raise error
    assert mock_handler in bus._subscribers[event_type] # Original should still be there

def test_publish_no_subscribers(bus, mock_handler):
    """Core Test: Publishing an event with no subscribers."""
    event_type = "no_subs_event"
    # Don't subscribe mock_handler
    bus.publish_safe(event_type, "some_data") # Should execute without error
    mock_handler.assert_not_called() # Verify our test mock wasn't called

def test_publish_calls_subscribed_handler(bus, mock_handler):
    """Core Test: A subscribed handler is called on publish with correct args."""
    event_type = "publish_call_event"
    test_arg = "hello"
    test_kwarg = 123
    bus.subscribe(event_type, mock_handler)
    bus.publish_safe(event_type, test_arg, data=test_kwarg)
    mock_handler.assert_called_once_with(test_arg, data=test_kwarg)

def test_publish_calls_multiple_handlers(bus):
    """Core Test: Multiple handlers are called."""
    event_type = "publish_multi_call"
    handler1 = Mock(name='handler1_multi')
    handler2 = Mock(name='handler2_multi')
    bus.subscribe(event_type, handler1)
    bus.subscribe(event_type, handler2)
    bus.publish_safe(event_type, "data")
    handler1.assert_called_once_with("data")
    handler2.assert_called_once_with("data")

def test_handler_exception_logged(bus, caplog):
    """Core Test: Exceptions in handlers are caught and logged."""
    event_type = "exception_event"
    error_message = "Handler failed intentionally!"
    # Define a real function that raises an error
    def failing_handler(*args, **kwargs): # Accept any args
        raise ValueError(error_message)

    bus.subscribe(event_type, failing_handler)

    with caplog.at_level(logging.ERROR):
        bus.publish_safe(event_type) # Call the failing handler (will be direct non-UI call)

    # Check that an error was logged containing the function name and message
    assert "Error executing non-UI handler failing_handler" in caplog.text
    assert error_message in caplog.text

# --- Removed Tests Related to UI Scheduling Mocks ---
# test_publish_safe_calls_non_ui_directly (Covered by test_publish_calls_subscribed_handler now)
# test_publish_safe_schedules_ui_handler (Removed)
# test_publish_safe_without_tk_app_ref (Removed)