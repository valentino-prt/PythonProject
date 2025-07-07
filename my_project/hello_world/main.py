import argparse
from datetime import datetime

from common.logger import configure_logger
from common.paths import OUTPUTS_DIR

logger = configure_logger(__name__)


def greet(name: str) -> str:
    message = f"Hello, {name} 👋"
    filename = OUTPUTS_DIR / f"greeting_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    filename.write_text(message)
    logger.info(f"Greeting saved to {filename}")
    return message


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", "-n", default="World", help="Name to greet")
    args = parser.parse_args()
    print(greet(args.name))


if __name__ == "__main__":
    main()
