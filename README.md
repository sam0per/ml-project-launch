# ML Project Template & Launcher

This repository is the **"Golden Template"** for all new client projects. It is designed to be forked for each new engagement. Its primary function is to standardize the project kickoff process via an automated script (`project_init/cli.py`).

## Purpose
1.  **For Project Lead:** Ensure a consistent and best-practice start for every new project.
2.  **Capture Requirements:** Guide the lead through a structured questionnaire to capture all critical project information.
3.  **Generate Blueprint:** Produce a `project_manifest.json` and a first-draft AI-generated strategy document (`strategy.md`) to align everyone involved.

---

## For the Project Lead: Per-Project Workflow

This is the process you will follow for **each new client project**.

### Step 1: Create a New Project Repository by Forking
1.  Go to the main [Golden Template](https://github.com/sam0per/ml-project-launch.git) on GitHub.
2.  Click the **"Fork"** button in the top-right corner.
3.  Select your account or organization as the owner. This creates your new project repository under your namespace (e.g., `github.com/LeadUsername/ml-project-launch`).

### Step 2: Get the Code on Your Machine
1.  On your new fork's GitHub page, click the "Code" button and copy the URL.
2.  On your local machine, clone your fork:
    ```bash
    git clone https://github.com/LeadUsername/ml-project-launch.git
    cd ml-project-launch
    ```

### Step 3: Setup the Python Environment
1.  **Create a virtual environment:**
    ```bash
    python -m venv .venv
    ```
2.  **Activate it:**
    *   On macOS/Linux: `source .venv/bin/activate`
    *   On Windows: `.venv\Scripts\activate`
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Configure API Keys:**
    ```bash
    # Copy the example environment file
    cp .env.example .env
    # Now edit .env with your favorite text editor and add your API key
    # (e.g., OPENAI_API_KEY='sk-your-key-here')
    ```

### Step 4: Run the Project Initialization Script
Execute the script and follow the prompts. It will handle branch creation and file generation.
```bash
python project_init/cli.py
```

### Step 5: Review, Commit, and Push
1. Review the generated files in the `outputs/` directory.
2. Commit the new branch and all generated files to your fork:
```bash
git add outputs/
git commit -m "chore: initialize project with manifest and strategy"
git push origin project/awesome-client-analysis # Push the new branch the script created
```
3. Finally, give your collaborator access to this fork and branch.

## For the Technical Collaborator
Once the Project Lead has completed the steps above and granted you access:
1. Clone the Project Lead's fork (not the original template):
```bash
git clone https://github.com/LeadUsername/ml-project-launch.git
cd ml-project-launch
```
2. Check out the feature branch created for the project:
```bash
git fetch origin
git checkout project/awesome-client-analysis
```
3. The `outputs/` directory contains your blueprint (`manifest.json` and `strategy.md`) for execution.

## Local Development (For Modifying This Template)
If you want to improve this template itself (e.g., add new questions, change the script):
1. Clone the original "Golden Template" repository (this one).
2. Create a new feature branch, make your changes, and submit a Pull Request.
```bash
git clone https://github.com/sam0per/ml-project-launch.git
cd ml-project-launch
git checkout -b feat/add-new-question
# ... make your changes ...
git commit -m "feat: add new question about data privacy"
git push origin feat/add-new-question
# Then open a PR on GitHub from your branch to the main branch.
```

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
