from common.config import config
from common.logger import configure_logger
from common.paths import OUTPUTS_DIR

logger = configure_logger(__name__)


def greet(name: str) -> str:
    message = f"{config['greeting_prefix']} Hello, {name} 👋"
    if config.get("save_output", True):
        from datetime import datetime

        path = OUTPUTS_DIR / f"greeting_{datetime.now():%Y%m%d_%H%M%S}.txt"
        path.write_text(message)
        logger.info(f"Saved to {path}")
    else:
        logger.info("Output not saved (save_output=False)")
    return message
