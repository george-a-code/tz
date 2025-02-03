import logging
import os
import pytest

from timezones.utils.logger import setup_logger, app_logger, get_log_level

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
EXPECTED_FILE_CONTENT = {
    logging.DEBUG: [
        "DEBUG [test_logger.py] This is a debug message",
        "INFO [test_logger.py] This is an info message",
        "WARNING [test_logger.py] This is a warning message",
        "ERROR [test_logger.py] This is an error message",
        "CRITICAL [test_logger.py] This is a critical message",
    ],
    logging.INFO: [
        "INFO [test_logger.py] This is an info message",
        "WARNING [test_logger.py] This is a warning message",
        "ERROR [test_logger.py] This is an error message",
        "CRITICAL [test_logger.py] This is a critical message",
    ],
    logging.WARNING: [
        "WARNING [test_logger.py] This is a warning message",
        "ERROR [test_logger.py] This is an error message",
        "CRITICAL [test_logger.py] This is a critical message",
    ],
    logging.ERROR: [
        "ERROR [test_logger.py] This is an error message",
        "CRITICAL [test_logger.py] This is a critical message",
    ],
    logging.CRITICAL: ["CRITICAL [test_logger.py] This is a critical message"],
}


@pytest.mark.parametrize(
    "desired_log_level", ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
)
def test_setup_logger(desired_log_level: str):
    # Setup environment
    os.environ["LOG_LEVEL"] = desired_log_level
    TEST_LOG_PATH = TEST_DIR + "/test.log"

    # Setup logger
    log_level = get_log_level()
    logger = setup_logger(
        "test_logger", TEST_LOG_PATH, level=getattr(logging, log_level)
    )

    # Log messages
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")

    # Check logger levels
    assert logger.level == getattr(logging, os.environ["LOG_LEVEL"])
    for handler in logger.handlers:
        assert handler.level == getattr(logging, os.environ["LOG_LEVEL"])

    # Check log file
    with open(TEST_LOG_PATH, "r") as log_file:
        log_contents = log_file.read()
        for message in EXPECTED_FILE_CONTENT[getattr(logging, log_level)]:
            assert message in log_contents

    # Cleanup
    os.remove(TEST_LOG_PATH)
    del os.environ["LOG_LEVEL"]
