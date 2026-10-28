# Rock, Paper, Scissors

A friendly, mobile-ready Rock, Paper, Scissors game built with Python and
Streamlit. Play against three computer strategies, track your score, and race
to a majority in a best-of-3, best-of-5, or best-of-7 match.

## Features

- Large emoji buttons for Rock, Paper, and Scissors.
- Easy (random), Medium (usually counters your last move), and Smart (uses your
  move counts and recent move-to-move patterns) computer strategies.
- Best-of-3, best-of-5, and best-of-7 matches. A match ends when a player
  reaches a majority; draws do not count toward either target.
- Wins, losses, draws, win rate, latest-round message, and full round history.
- Win rate is wins divided by all completed rounds, including draws.
- New match and full reset controls.
- Session-state persistence between Streamlit interactions.
- Automated game, AI, and UI tests plus Ruff checks in GitHub Actions.

## Screenshots

The app's main screen contains the match controls, score cards, three move
buttons, latest-round result, and round history. The sidebar contains the rules
and match settings, and the **How the AI thinks** expander describes each
strategy. To capture a screenshot, run the app locally and use your operating
system's screenshot shortcut.

## Run locally

Python 3.12 is recommended (and is the version used by CI and Streamlit Cloud).
From the project directory, create and activate a virtual environment, then
install the pinned dependencies:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Run the test suite and quality checks:

```powershell
python -m pytest
python -m ruff check .
python -m ruff format --check .
```

Start the app:

```powershell
python -m streamlit run app.py
```

Streamlit prints a local URL (usually `http://localhost:8501`) that you can
open in your browser. On Windows, if PowerShell blocks script activation, run
`.\.venv\Scripts\python.exe -m pip install -r requirements.txt` and
`.\.venv\Scripts\python.exe -m streamlit run app.py` instead.

## Push the project to GitHub

Create an empty repository on GitHub (do not initialize it with a README,
license, or `.gitignore`, because those are already in this project). In
PowerShell, from this project directory, replace `YOUR-USERNAME` and
`YOUR-REPOSITORY` with your GitHub details:

```powershell
git init
git add .
git commit -m "Build Rock Paper Scissors Streamlit game"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
git push -u origin main
```

Git may ask you to sign in through your browser. Do not put an access token or
password in the remote URL.

## Deploy on Streamlit Community Cloud

1. Push the project to GitHub using the steps above.
2. Visit [share.streamlit.io](https://share.streamlit.io/) and sign in with
   GitHub. Authorize Streamlit to access the repository if asked.
3. Choose **Create app** (or **Deploy an app**).
4. Select your **repository**, the **main** branch, and `app.py` as the **Main
   file path**.
5. Open **Advanced settings** and choose **Python 3.12**.
6. Select **Deploy**. Streamlit installs the packages from `requirements.txt`
   and gives you a public app URL when deployment finishes.
7. Open the URL and try a few moves to check that the app is running.

### Update the deployed app

Make and test your changes locally, then commit and push them to the same
GitHub branch selected by Streamlit Cloud:

```powershell
git add .
git commit -m "Update game interface"
git push
```

Streamlit Community Cloud detects the new commit and redeploys the app. Refresh
the app page after deployment completes.

### Check deployment logs

In Streamlit Community Cloud, open your app, use its app menu, and choose
**Settings** or **Manage app** to open the management page. Select **Logs** to
see dependency-installation and runtime output. Read the first error message,
check that the main file is `app.py`, confirm Python 3.12 is selected, and
verify that every imported third-party package is listed in `requirements.txt`.
After correcting the issue, push the fix to GitHub; the app will redeploy.

## Project files

- `app.py` contains only the Streamlit interface and session-state handling.
- `game.py` contains the move rules, round results, scoring, and match rules.
- `ai.py` contains the three computer strategies.
- `tests/` contains pytest coverage for rules, scoring, and AI behavior.
- `.github/workflows/ci.yml` runs Ruff and pytest on every push and pull request.

## License

This project is released under the MIT License. See [LICENSE](LICENSE).
