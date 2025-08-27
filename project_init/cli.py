#!/usr/bin/env python3
"""
Main CLI script for initializing a new ML project from meeting notes.
Handles notes parsing, manifest generation, and project setup.
"""

# Standard library imports
import json
import argparse
from pathlib import Path
from datetime import datetime

# Third-party imports
from loguru import logger
from rich.console import Console
import rich.traceback

# Local imports
from project_init.notes_parser import parse_notes

# Initialize Rich console for pretty printing
console = Console()
rich.traceback.install(console=console)

# Define paths
OUTPUT_DIR = Path("outputs")
INPUT_DIR = Path("inputs")
INPUT_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)


def slugify(text: str) -> str:
    """
    Convert a string into a file-safe slug.
    
    Args:
        text: The string to convert.
        
    Returns:
        A URL-friendly, file-safe slug.
    """
    return "".join(c for c in text if c.isalnum() or c in (' ', '-', '_')).rstrip().replace(' ', '-').lower()


def configure_logger() -> Path:
    """
    Configure logging with both file and console outputs.
        
    Returns:
        Path to the log file that was created.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file_name = f"{timestamp}_project_init.log"
    log_file_path = OUTPUT_DIR / log_file_name

    logger.remove()
    logger.add(
        sink=log_file_path,
        level="DEBUG",
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    )
    logger.add(
        sink=console.print,
        level="INFO",
        format="[dim]{time:HH:mm:ss}[/dim] | {level} | {message}",
        colorize=True,
    )
    return log_file_path


def find_latest_notes_file() -> Path:
    """
    Find the most recent Markdown file in the inputs directory.
    
    Returns:
        Path to the most recently modified Markdown file.
        
    Raises:
        FileNotFoundError: If no Markdown files are found in the inputs directory.
    """
    try:
        md_files = list(INPUT_DIR.glob("*.md"))
        if not md_files:
            error_msg = "No .md files found in inputs/ directory."
            logger.error(error_msg)
            console.print(f"[bold red]Error:[/bold red] {error_msg}")
            console.print("Please create a notes file from the template.")
            console.print("\n[bold yellow]Hint:[/bold yellow] You can copy the template to get started:")
            today_str = datetime.now().strftime("%Y-%m-%d")
            console.print(f"  [cyan]cp templates/PROJECT_NOTES_TEMPLATE.md inputs/{today_str}-my-project-notes.md[/cyan]")
            raise FileNotFoundError(error_msg)
        
        # Get the most recently modified file
        latest_file = max(md_files, key=lambda x: x.stat().st_mtime)
        logger.info(f"Found notes file: {latest_file}")
        return latest_file
        
    except Exception as e:
        # This block will now only handle unexpected errors, as the FileNotFoundError is handled above.
        logger.error(f"Error finding notes file: {e}")
        console.print(f"[bold red]An unexpected error occurred:[/bold red] {e}")
        raise


def parse_arguments():
    """
    Parse command line arguments for the script.
    
    Returns:
        Namespace object containing the parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description='Initialize a new ML project from structured meeting notes.'
    )
    parser.add_argument(
        '--input', '-i',
        type=Path,
        help='Path to the meeting notes file. If not provided, uses the most recent .md file in inputs/ directory.'
    )
    return parser.parse_args()


def get_notes_file_path(args) -> Path:
    """
    Determine which notes file to use based on command line arguments.
    
    Args:
        args: Parsed command line arguments.
        
    Returns:
        Path to the notes file to be parsed.
        
    Raises:
        FileNotFoundError: If the specified file doesn't exist.
    """
    if args.input:
        # Use the specified file
        notes_file = Path(args.input)
        if not notes_file.exists():
            raise FileNotFoundError(f"Specified file not found: {notes_file}")
        logger.info(f"Using specified notes file: {notes_file}")
        return notes_file
    else:
        # Find the most recent file automatically
        return find_latest_notes_file()


def main():
    """Main function to run the project initialization script."""
    # Configure logger at the very beginning
    log_path = configure_logger()
    logger.info("Script started.")

    # Parse command line arguments
    args = parse_arguments()
    
    console.print("[bold green]🎯 ML Project Initialization Script[/bold green]")
    console.print("This script will parse your meeting notes and create a project manifest.\n")
    
    # TODO: Phase 2 - Check if we're in a Git repo first
    logger.debug("Phase 2: Git check will be implemented here.")
    
    try:
        # Determine which notes file to use
        notes_file = get_notes_file_path(args)
        
        # Parse the notes file
        answers = parse_notes(notes_file)
        
        # Get project name for logging and filenames
        project_name = answers.get('project_name', 'new-project')
        logger.info(f"Project name from notes: '{project_name}'")
        
        # Generate a manifest filename based on project name
        project_name_slug = slugify(project_name)
        manifest_path = OUTPUT_DIR / f"{project_name_slug}_manifest.json"
        logger.debug(f"Manifest path determined: {manifest_path}")

        # Write the answers to the JSON manifest file
        with open(manifest_path, 'w') as file:
            json.dump(answers, file, indent=4)
        logger.success(f"Project manifest saved to: {manifest_path}")
        console.print(f"[bold green]✅ Project manifest saved to:[/bold green] {manifest_path}")

        # TODO: Phase 2 - Create a new Git branch
        proposed_branch_name = f"project/{project_name_slug}"
        logger.info(f"Phase 2: Proposed Git branch name is '{proposed_branch_name}'")
        console.print(f"[bold yellow]Phase 2 will create Git branch:[/bold yellow] {proposed_branch_name}")

        # TODO: Phase 3 - LLM Call and strategy generation
        logger.info("Phase 3: LLM strategy generation will be implemented here.")
        console.print("[bold yellow]Phase 3 will generate the strategy document using an LLM.[/bold yellow]")

        console.print(f"\n[bold green]✅ Phase 1 complete![/bold green]")
        console.print(f"   - Manifest: [bold]{manifest_path}[/bold]")
        console.print(f"   - Log file: [dim]{log_path}[/dim]")
        console.print(f"   - Source: [dim]{notes_file}[/dim]")
        logger.success("Phase 1 execution completed successfully.")

    except Exception as e:
        logger.critical(f"Script failed: {e}")
        console.print(f"[bold red]Script failed:[/bold red] {e}")
        raise


if __name__ == "__main__":
    main()