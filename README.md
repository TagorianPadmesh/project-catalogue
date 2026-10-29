# Product Catalogue Final Project (Python)

Reference scaffold for the Coursera Product Catalogue assignment using Flask, SQLAlchemy, factory_boy, pytest, Behave, and Selenium.

**Important:** This is a starter/reference project, not a copy of the Coursera lab repository. Check your lab's exact enum members, selectors, fixtures, and setup before using it. Peer-graded URLs must point to files in your own GitHub repository.

## Setup
```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
flask --app service.app run
```

## Run API/model tests
```bash
pytest -q
```

BDD needs a running app, an actual UI, and a configured browser driver. Configure `features/environment.py` for your lab.

## Publish for peer grading
1. Create a repository in your GitHub account.
2. Extract this ZIP and copy its contents into the repository.
3. Compare with your actual lab and run tests.
4. Commit and push the files.
5. URLs will look like `https://github.com/YOUR_USERNAME/YOUR_REPO/blob/main/tests/factories.py`.
