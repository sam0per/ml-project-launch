# ML Project Template & Launcher

This repository is the template for all new client projects. It is designed to be forked for each new engagement.

Its primary function is to standardize the project kickoff process via an automated script (`project_init/cli.py`).

## Purpose
1.  Ensure best practices for GitHub setup (forking, branching).
2.  Capture all critical project information via a structured questionnaire.
3.  Generate a `project_manifest.json` and a first-draft strategy document using an LLM.

## Usage (For Project Lead)
1.  **Fork this repository** to the client's or your organization's GitHub account.
2.  Clone your new fork locally.
3.  Run the setup script:
    ```bash
    pip install -r requirements.txt
    python project_init/cli.py
    ```
4.  Follow the interactive prompts.
5.  The script will create a new branch and generate the project definition files in the `outputs/` directory.

## Structure
```bash
ml-project-launch/
│
├── .github/
│   └── workflows/                 # For GitHub Actions CI/CD (future use)
│       └── ...                    # You can add this later
│
├── project_init/                 # Main directory for the initialization script
│   ├── __init__.py               # Makes this a Python package
│   ├── cli.py                    # The main script to run (Command-Line Interface)
│   ├── questions.py              # Contains the list of questions and structure
│   └── templates/                # Directory for any file templates
│       └── STRATEGY_TEMPLATE.md  # A base template to guide the LLM's output
│
├── docs/                         # For general documentation about *using* this workflow
│   └── WORKFLOW_GUIDE.md
│
├── outputs/                      # Empty directory. For script output (gitignored later)
│   └── .gitkeep                  # Empty file to preserve the directory in git
│
├── .env.example                  # Example file for environment variables (e.g., API keys)
├── .gitignore
├── LICENSE
├── README.md                     # Explains the purpose of this template repo
├── requirements.txt              # Python dependencies for the script
└── runtime.txt                   # Optional: Specifies Python version if deploying
```
