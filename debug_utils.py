import logging
from typing import Any

DEBUG_MODE = True

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG if DEBUG_MODE else logging.INFO)

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler = logging.StreamHandler()
handler.setFormatter(formatter)

# Avoid adding multiple handlers
if not logger.hasHandlers():
    logger.addHandler(handler)

def debug_message(msg: Any, lvl: int) -> None:
    logger.log(lvl, msg)
