"""
Module for parsing structured project notes from a Markdown template.
"""

from pathlib import Path
from loguru import logger


def parse_notes(file_path: Path) -> dict:
    """
    Parse a structured project notes Markdown file into a dictionary.

    This function reads a Markdown file following a specific template format,
    extracts content from predefined sections, and returns a structured dictionary.

    Args:
        file_path: Path to the Markdown file to parse.

    Returns:
        A dictionary containing the extracted content from the notes file.
        Keys correspond to section names (e.g., 'client_name', 'primary_goal').

    Raises:
        FileNotFoundError: If the specified file_path does not exist.
        ValueError: If the file cannot be parsed correctly.
    """
    logger.debug(f"Attempting to parse notes file: {file_path}")
    
    if not file_path.exists():
        error_msg = f"Notes file not found at {file_path}"
        logger.error(error_msg)
        raise FileNotFoundError(error_msg)
    
    # Map header text (lowercase) to the desired dictionary key
    header_to_key = {
        'client name': 'client_name',
        'project name': 'project_name',
        'primary goal': 'primary_goal',
        'success metrics': 'success_metrics',
        'data sources': 'data_sources',
        'known constraints': 'known_constraints',
        'additional context': 'additional_context'
    }
    
    sections = {key: [] for key in header_to_key.values()}
    current_key = None
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        
        for line in lines:
            stripped_line = line.strip()
            
            # Check if the line is a section header
            if stripped_line.startswith('## '):
                header_text = stripped_line[3:].lower()
                current_key = header_to_key.get(header_text)
            elif current_key and stripped_line and not stripped_line.startswith('[') and not stripped_line.startswith('#'):
                # Add content to the current section
                sections[current_key].append(stripped_line)
        
        # Join the content for each section
        parsed_content = {key: '\n'.join(content).strip() for key, content in sections.items()}
        
        if not any(parsed_content.values()):
            error_msg = "No valid content could be parsed from the notes file. Ensure it follows the template."
            logger.error(error_msg)
            raise ValueError(error_msg)
            
        logger.success(f"Successfully parsed notes file: {file_path}")
        return parsed_content
        
    except Exception as e:
        logger.error(f"Failed to parse notes file {file_path}: {e}")
        raise ValueError(f"Failed to parse notes file: {e}") from e