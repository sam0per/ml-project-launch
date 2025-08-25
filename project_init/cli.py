#!/usr/bin/env python3
"""
Main CLI script for initializing a new ML project.
Handles questionnaire, manifest generation, and setup.
"""

# Standard library imports
import json
from pathlib import Path
from datetime import datetime

# Third-party imports
from loguru import logger
from rich.console import Console
from rich.prompt import Prompt
import rich.traceback

# Local imports
from project_init.questions import PROJECT_QUESTIONS

# Initialize Rich console for pretty printing
console = Console()
rich.traceback.install(console=console)

# Define paths
OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)  # Ensure the output directory exists

def configure_logger(project_name: str) -> Path:
    """
    Configures and returns the path to the log file.
    The log will be saved in the outputs/ directory with a timestamp.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    # Create a safe filename for the log
    safe_project_name = "".join(c for c in project_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
    safe_project_name = safe_project_name.replace(' ', '_')
    log_file_name = f"{timestamp}_{safe_project_name}.log"
    log_file_path = OUTPUT_DIR / log_file_name

    # Remove default logger sink and add a new one with our log file
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

def main():
    """Main function to run the project initialization script."""
    console.print("[bold green]🎯 ML Project Initialization Script[/bold green]")
    console.print("This script will guide you through creating a new project branch and manifest.\n")
    
    # Start by getting a project name for logging purposes.
    # We'll ask it officially again in the questionnaire loop.
    initial_project_name = Prompt.ask("[bold]Enter a short project name (for log files)[/bold]")
    
    # Configure the logger with the initial project name
    log_path = configure_logger(initial_project_name)
    logger.info("Script started.")
    logger.debug("Logger configured and output directory ensured.")

    # TODO: Phase 2 - Check if we're in a Git repo first
    logger.debug("Phase 2: Git check will be implemented here.")
    # TODO: Phase 2 - Confirm this is a forked repo
    logger.debug("Phase 2: Fork confirmation will be implemented here.")

    answers = {}
    console.print("\n[bold cyan]Please answer the following project questions:[/bold cyan]")
    logger.info("Starting questionnaire.")

    # Iterate through questions and collect answers
    for q in PROJECT_QUESTIONS:
        answer = Prompt.ask(f"[bold]{q['question']}[/bold]")
        answers[q['key']] = answer
        logger.debug(f"Q: {q['key']}, A: {answer}")

    logger.info("Questionnaire completed.")

    # Generate a manifest filename based on project name
    project_name_slug = answers.get('project_name', 'new_project').replace(' ', '-').lower()
    manifest_path = OUTPUT_DIR / f"{project_name_slug}_manifest.json"
    logger.debug(f"Manifest path determined: {manifest_path}")

    # Write the answers to the JSON manifest file
    try:
        with open(manifest_path, 'w') as f:
            json.dump(answers, f, indent=4)
        logger.success(f"Project manifest saved to: {manifest_path}")
        console.print(f"[bold green]✓ Project manifest saved to:[/bold green] {manifest_path}")
    except Exception as e:
        logger.error(f"Failed to write manifest file: {e}")
        console.print(f"[bold red]✗ Error saving manifest file: {e}[/bold red]")
        raise

    # TODO: Phase 2 - Create a new Git branch
    proposed_branch_name = f"project/{project_name_slug}"
    logger.info(f"Phase 2: Proposed Git branch name is '{proposed_branch_name}'")
    console.print(f"[bold yellow]Phase 2 will create Git branch:[/bold yellow] {proposed_branch_name}")

    # TODO: Phase 3 - LLM Call and strategy generation
    logger.info("Phase 3: LLM strategy generation will be implemented here.")
    console.print("[bold yellow]Phase 3 will generate the strategy document using an LLM.[/bold yellow]")

    console.print(f"\n[bold green]✅ Phase 1 complete![/bold green]")
    console.print(f"   - Review the manifest file: [bold]{manifest_path}[/bold]")
    console.print(f"   - Log file: [dim]{log_path}[/dim]")
    logger.success("Phase 1 execution completed successfully.")

if __name__ == "__main__":
    main()