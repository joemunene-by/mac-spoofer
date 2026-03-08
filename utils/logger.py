import logging
import sys
from typing import Optional
from rich.console import Console
from rich.logging import RichHandler

# Global console instance for rich output
console = Console()

def setup_logger(name: str, log_file: Optional[str] = "spoofer.log") -> logging.Logger:
    """
    Sets up a logger with both console (Rich) and file handlers.
    
    Args:
        name: The name of the logger.
        log_file: Path to the log file. If None, no file logging is performed.
        
    Returns:
        A configured logging.Logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Remove existing handlers to avoid duplicates
    if logger.hasHandlers():
        logger.handlers.clear()

    # Rich console handler
    console_handler = RichHandler(
        console=console,
        show_path=False,
        omit_repeated_times=False,
        markup=True
    )
    console_handler.setLevel(logging.INFO)
    logger.addHandler(console_handler)

    # File handler
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_format = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(file_format)
        logger.addHandler(file_handler)

    return logger

def print_success(message: str) -> None:
    """Prints a success message."""
    console.print(f"[green]ok[/green] {message}")

def print_error(message: str) -> None:
    """Prints an error message."""
    console.print(f"[red]error[/red] {message}")

def print_warning(message: str) -> None:
    """Prints a warning message."""
    console.print(f"[yellow]warn[/yellow] {message}")

def print_info(message: str) -> None:
    """Prints an info message."""
    console.print(f"[blue]info[/blue] {message}")
