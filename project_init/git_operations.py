"""
Module for handling Git operations and checks for project initialization.
Contains functions to validate the Git state and create a new project branch.
"""

import subprocess
from pathlib import Path
from loguru import logger

# Custom Exceptions with specific error messages
class GitError(Exception):
    """Base exception for Git-related errors."""
    pass

class NotAGitRepositoryError(GitError):
    """Exception raised when the current directory is not a Git repository."""
    pass

class DirtyWorkingTreeError(GitError):
    """Exception raised when the working tree has uncommitted changes."""
    pass

class BranchExistsError(GitError):
    """Exception raised when the target branch already exists."""
    pass

def run_git_command(command: list) -> subprocess.CompletedProcess:
    """
    Run a Git command and return the completed process object.
    
    Args:
        command: List of Git command arguments (e.g., ['git', 'status'])
        
    Returns:
        CompletedProcess object from subprocess.run()
        
    Raises:
        GitError: If the Git command fails for any reason.
    """
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False  # We'll check the return code manually
        )
        if result.returncode != 0:
            error_msg = result.stderr.strip() or f"Git command failed: {' '.join(command)}"
            logger.error(f"Git command error: {error_msg}")
            raise GitError(error_msg)
        return result
    except FileNotFoundError:
        error_msg = "Git is not installed or not found in system PATH."
        logger.error(error_msg)
        raise GitError(error_msg)

def validate_git_repo() -> None:
    """
    Validate that the current directory is a Git repository.
    
    Raises:
        NotAGitRepositoryError: If not in a Git repo.
    """
    logger.debug("Checking if current directory is a Git repository...")
    try:
        run_git_command(['git', 'rev-parse', '--git-dir'])
    except GitError as e:
        error_msg = "Not a Git repository."
        logger.error(error_msg)
        raise NotAGitRepositoryError(error_msg) from e
    logger.success("Current directory is a Git repository.")

def is_working_tree_clean() -> bool:
    """
    Check if the working tree is clean (no uncommitted changes).
    
    Returns:
        bool: True if working tree is clean, False otherwise.
    """
    logger.debug("Checking if working tree is clean...")
    try:
        # Check for any changes in tracked files
        status_result = run_git_command(['git', 'status', '--porcelain'])
        return len(status_result.stdout.strip()) == 0
    except GitError as e:
        logger.warning(f"Error checking working tree status: {e}")
        return False

def validate_working_tree_clean() -> None:
    """
    Validate that the working tree has no uncommitted changes.
    
    Raises:
        DirtyWorkingTreeError: If working tree has uncommitted changes.
    """
    if not is_working_tree_clean():
        error_msg = "Working tree has uncommitted changes."
        logger.error(error_msg)
        raise DirtyWorkingTreeError(error_msg)
    logger.success("Working tree is clean.")

def branch_exists(branch_name: str) -> bool:
    """
    Check if a branch already exists locally.
    
    Args:
        branch_name: Name of the branch to check.
        
    Returns:
        bool: True if branch exists, False otherwise.
    """
    logger.debug(f"Checking if branch '{branch_name}' exists...")
    try:
        run_git_command(['git', 'show-ref', '--verify', '--quiet', f'refs/heads/{branch_name}'])
        return True
    except GitError:
        return False

def validate_branch_does_not_exist(branch_name: str) -> None:
    """
    Validate that the target branch doesn't already exist.
    
    Args:
        branch_name: Name of the branch to check.
        
    Raises:
        BranchExistsError: If branch already exists.
    """
    if branch_exists(branch_name):
        error_msg = f"Branch '{branch_name}' already exists."
        logger.error(error_msg)
        raise BranchExistsError(error_msg)
    logger.success(f"Branch '{branch_name}' does not exist.")

def create_and_switch_branch(branch_name: str) -> None:
    """
    Create a new branch and switch to it.
    
    Args:
        branch_name: Name of the new branch to create.
        
    Raises:
        GitError: If branch creation fails.
    """
    logger.debug(f"Creating and switching to branch '{branch_name}'...")
    try:
        run_git_command(['git', 'checkout', '-b', branch_name])
        logger.success(f"Successfully created and switched to branch '{branch_name}'.")
    except GitError as e:
        error_msg = f"Failed to create branch '{branch_name}'."
        logger.error(error_msg)
        raise GitError(error_msg) from e

def commit_files(file_paths: list, commit_message: str) -> None:
    """
    Add and commit specified files to the current branch.
    
    Args:
        file_paths: List of file paths to commit.
        commit_message: Commit message.
        
    Raises:
        GitError: If commit operation fails.
    """
    logger.debug(f"Committing files: {file_paths}")
    try:
        # Add specified files
        run_git_command(['git', 'add'] + file_paths)
        
        # Commit with message
        run_git_command(['git', 'commit', '-m', commit_message])
        
        logger.success(f"Committed files with message: '{commit_message}'")
    except GitError as e:
        error_msg = f"Failed to commit files: {file_paths}"
        logger.error(error_msg)
        raise GitError(error_msg) from e

def create_project_branch(branch_name: str) -> None:
    """
    Main function to prepare Git environment for a new project.
    Performs all validation and creates the new branch.
    
    Args:
        branch_name: Name of the new project branch to create.
        
    Raises:
        NotAGitRepositoryError: If not in a Git repo.
        DirtyWorkingTreeError: If working tree has uncommitted changes.
        BranchExistsError: If branch already exists.
        GitError: For any other Git-related errors.
    """
    logger.info(f"Starting Git preparation for branch: {branch_name}")
    
    # Perform all validations
    validate_git_repo()
    validate_working_tree_clean()
    validate_branch_does_not_exist(branch_name)
    
    # Create the new branch
    create_and_switch_branch(branch_name)