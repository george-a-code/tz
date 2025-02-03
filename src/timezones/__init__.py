from .utils.logger import app_logger
from .app import main

__version__ = "0.1.0"

if __name__ == "__main__":
    app_logger.debug("Running main")
    main()
    app_logger.debug("Finished running main")
