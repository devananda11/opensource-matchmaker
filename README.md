# First Issue - An Open Source Matchmaker

First Issue helps developers find beginner-friendly open source issues that match their skills.

It analyzes a GitHub profile or allows manual language selection to recommend relevant `good first issues`.

---

## Overview

The system connects a user’s skillset with suitable open source contributions by:

- Fetching repositories from GitHub
- Identifying most used programming languages
- Searching for beginner-friendly issues
- Ranking them based on relevance and repository quality

For users without public repositories, the system supports manual language selection to generate recommendations.

---

## Workflow

```
GitHub → Profile Analysis → Issue Search → Matching → Health Check → API
```

---

## Demo Video

[Watch the demo](./docs/demo.mp4)

<video src="./docs/demo.mp4" controls muted width="100%"></video>

---

## Features

- Personalized issue recommendations based on user skills
- Support for new users via manual language input
- Filtering using `good first issue` labels
- Issue summaries generated using Gemini 1.5 Flash
- Lightweight and fast response pipeline

---

## Tech Stack

**Frontend**

- React (with Vite)
- Tailwind CSS

**Backend**

- FastAPI
- GitHub REST API
- Gemini 1.5 Flash (AI descriptions)

---

## Modules

- **GitHub API (`github_api.py`)** – handles repository and issue fetching
- **Profile Analyzer (`profile_analyzer.py`)** – extracts language-based profile
- **Matcher (`matcher.py`)** – ranks issues using scoring logic
- **Repository checker ( `health_check.py`)** – filters out inactive repositories
- **Backend (`main.py`)** – integrates pipeline and exposes API
- **Frontend** – user interface for input and results

---

## Setup

### Backend

```bash
git clone <repo-url>
cd open-source-matchmaker
pip install -r requirements.txt
uvicorn backend.main:app --reload
```

---

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Open the local Vite server URL (shown in terminal) in your browser.

---

## Contribution Guidelines

- Work on feature branches: `feature/<module-name>`
- Pull latest changes before starting work
- Write clear commit messages
- Use Pull Requests for merging
- Avoid direct pushes to `main`

---

## License

MIT License
