# ACEest Fitness & Gym — CI/CD Pipeline Implementation

> A production-grade Flask REST API for ACEest Fitness & Gym, deployed through a fully automated CI/CD pipeline using GitHub Actions and Jenkins.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Local Setup & Execution](#local-setup--execution)
- [API Endpoints](#api-endpoints)
- [Running Tests Manually](#running-tests-manually)
- [Docker — Build & Run](#docker--build--run)
- [GitHub Actions Pipeline](#github-actions-pipeline)
- [Jenkins BUILD Integration](#jenkins-build-integration)
- [Version History](#version-history)

---

## Project Overview

This project implements a complete DevOps lifecycle for **ACEest Fitness & Gym**, a rapidly scaling fitness startup. The application was migrated from a desktop Tkinter GUI (v1.0) through iterative versions into a fully containerised Flask REST API (v2.0.1), with automated testing and deployment pipelines enforcing code quality at every stage.

The pipeline ensures:
- **Code integrity** via automated Pytest on every push
- **Environmental consistency** via Docker containerisation
- **Rapid delivery** via GitHub Actions CI/CD and a Jenkins BUILD quality gate

---

## Architecture

```
Developer Machine
      │
      │  git push / pull_request
      ▼
┌─────────────────────────────────────┐
│         GitHub Repository           │
│     main branch ← feature branches  │
└────────────┬────────────────────────┘
             │  triggers
     ┌───────┴────────┐
     │                │
     ▼                ▼
GitHub Actions     Jenkins Server
(CI Pipeline)      (BUILD Quality Gate)
     │                │
     │  1. Lint       │  1. Declarative Checkout
     │  2. Docker     │  2. Install Dependencies
     │     Build      │  3. Build Validation
     │  3. Pytest     │  4. Run Tests
     │                │  5. Docker Build
     ▼                ▼
  ✅ Pass / ❌ Fail   ✅ BUILD SUCCESS
```

---

## Tech Stack

| Technology | Version | Purpose |
|---|---|---|
| Python | 3.10 | Application runtime |
| Flask | Latest | REST API framework |
| SQLite | Built-in | Lightweight persistent storage |
| Pytest | Latest | Unit testing framework |
| Docker | Latest | Containerisation |
| GitHub Actions | — | Automated CI/CD pipeline |
| Jenkins (LTS) | — | Build server / quality gate |

---

## Project Structure

```
aceest-fitness-gym/
│
├── .github/
│   └── workflows/
│       └── main.yml          # GitHub Actions CI/CD pipeline
│
├── tests/
│   └── test_app.py           # Pytest unit test suite
│
├── app.py                    # Flask REST API — core application
├── requirements.txt          # Python dependencies
├── Dockerfile                # Container build instructions
├── Jenkinsfile               # Jenkins Pipeline as Code (Windows-compatible)
└── README.md                 # This document
```

---

## Local Setup & Execution

### Prerequisites

- Python 3.10+
- pip
- Git
- Docker Desktop (for containerised runs)

### Step 1 — Clone the Repository

```bash
git clone https://github.com/2024tm93564-khushika/aceest-fitness-gym.git
cd aceest-fitness-gym
```

### Step 2 — Create a Virtual Environment

```bash
python -m venv venv

# Linux / macOS:
source venv/bin/activate

# Windows:
venv\Scripts\activate
```

### Step 3 — Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4 — Run the Application

```bash
python app.py
```

The API will be available at `http://localhost:5000`

### Step 5 — Verify

```bash
curl http://localhost:5000/
# Expected: {"message": "ACEest Fitness API v2.0.1"}
```

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Health check — returns API version |
| POST | `/add-client` | Register a new client |
| GET | `/client/<name>` | Retrieve a client record by name |
| POST | `/progress` | Log a client's weekly progress |
| POST | `/calculate-calories` | Calculate recommended daily calories |

### Supported Programs

| Key | Description | Calorie Multiplier |
|---|---|---|
| `fat_loss` | Fat Loss programme | 0.8× base |
| `muscle_gain` | Muscle Gain programme | 1.2× base |
| `beginner` | Beginner programme | 1.0× base |

### Example Requests

**Add a Client:**
```bash
curl -X POST http://localhost:5000/add-client \
  -H "Content-Type: application/json" \
  -d '{"name": "Priya", "program": "fat_loss", "calories": 2000}'
```

**Get a Client:**
```bash
curl http://localhost:5000/client/Priya
```

**Calculate Calories:**
```bash
curl -X POST http://localhost:5000/calculate-calories \
  -H "Content-Type: application/json" \
  -d '{"program": "muscle_gain", "base_calories": 2500}'
```

**Log Progress:**
```bash
curl -X POST http://localhost:5000/progress \
  -H "Content-Type: application/json" \
  -d '{"name": "Priya", "week": "Week-1", "adherence": 90}'
```

---

## Running Tests Manually

All tests are located in the `tests/` directory and use the Pytest framework.

### Run All Tests

```bash
# Standard
pytest tests/ -v

# Windows (if pytest.exe is blocked by system policy)
python -m pytest tests/ -v
```

### Run with Short Traceback

```bash
python -m pytest tests/ -v --tb=short
```

### Expected Output

```
tests/test_app.py::test_home_endpoint            PASSED
tests/test_app.py::test_add_client_valid         PASSED
tests/test_app.py::test_add_client_invalid       PASSED
tests/test_app.py::test_get_client               PASSED
tests/test_app.py::test_calculate_calories       PASSED
tests/test_app.py::test_save_progress            PASSED

6 passed in 0.XXs
```

---

## Docker — Build & Run

### Build the Image

```bash
docker build -t aceest-fitness-gym .
```

### Run the Container

```bash
docker run -p 5000:5000 aceest-fitness-gym
```

API available at `http://localhost:5000`

### Run Tests Inside the Container

```bash
docker run aceest-fitness-gym python -m pytest tests/ -v
```

### Dockerfile Explained

```dockerfile
FROM python:3.10-slim        # Minimal base image — smaller, more secure

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt  # No cache = lean image

COPY . .

EXPOSE 5000
CMD ["python", "app.py"]
```

**Design decisions:**
- `python:3.10-slim` keeps the image small vs the full Python image
- `--no-cache-dir` avoids storing pip's download cache in the image layer
- Dependencies are installed before copying source code so Docker layer caching avoids reinstalling on every code change

---

## GitHub Actions Pipeline

Defined in `.github/workflows/main.yml`. Triggers automatically on every `push` and `pull_request` to `main`.

### Pipeline Stages

```
Trigger: push / pull_request → main
│
├── Stage 1: Build & Lint
│     └── pip install dependencies
│         flake8 syntax check
│
├── Stage 2: Docker Image Assembly
│     └── docker build -t aceest-fitness-gym .
│
└── Stage 3: Automated Testing
      └── pytest tests/ -v  (run inside Docker container)
```

### How It Works

1. Every push to `main` spins up an `ubuntu-latest` GitHub-hosted runner
2. Stage 1 installs dependencies and lints the code with `flake8`
3. Stage 2 builds the Docker image — confirms containerisation works end-to-end
4. Stage 3 runs Pytest **inside the Docker container** — validates the app behaves correctly in the production-equivalent environment, not just on a developer's machine

A failure in any stage blocks the pipeline and marks the commit as failed on GitHub.

---

## Jenkins BUILD Integration

Jenkins serves as a secondary **BUILD quality gate** — validating that the codebase integrates cleanly in a controlled server-side build environment, separate from the developer's machine and GitHub Actions.

### Environment Note

This Jenkins setup runs on **Windows** with Python 3.14. All pipeline commands use `python -m <tool>` syntax instead of direct executable calls (e.g. `python -m pip`, `python -m pytest`) to comply with Windows Device Guard security policies that block unsigned `.exe` files in certain user directories.

### Jenkinsfile — Pipeline Stages

The `Jenkinsfile` in the repo root defines a 4-stage declarative pipeline:

```groovy
pipeline {
    agent any

    environment {
        IMAGE_NAME = "aceest-fitness-gym"
    }

    stages {

        stage('Install Dependencies') {
            steps {
                bat 'python -m pip install -r requirements.txt'
            }
        }

        stage('Build Validation') {
            steps {
                bat 'python -m py_compile app.py'
            }
        }

        stage('Run Tests') {
            steps {
                bat 'python -m pytest tests/ -v --tb=short'
            }
        }

        stage('Docker Build') {
            steps {
                bat 'docker build -t %IMAGE_NAME%:latest .'
            }
        }
    }
}
```

### Stage Breakdown

| Stage | Command | Purpose |
|---|---|---|
| Install Dependencies | `python -m pip install -r requirements.txt` | Installs Flask and Pytest in the Jenkins environment |
| Build Validation | `python -m py_compile app.py` | Compiles app.py — catches syntax errors before tests run |
| Run Tests | `python -m pytest tests/ -v --tb=short` | Executes the full Pytest suite as a quality gate |
| Docker Build | `docker build -t aceest-fitness-gym:latest .` | Builds the Docker image to confirm containerisation works |

### Jenkins Project Configuration

1. Open Jenkins → **New Item** → name it `aceest-fitness-gym` → select **Pipeline** → click **OK**
2. Under **General**: check **GitHub project** → paste repo URL
3. Under **Build Triggers**: check **Poll SCM** → schedule `H/5 * * * *`
4. Under **Pipeline**:
   - Definition: `Pipeline script from SCM`
   - SCM: `Git`
   - Repository URL: `https://github.com/2024tm93564-khushika/aceest-fitness-gym.git`
   - Branch: `*/main`
   - Script Path: `Jenkinsfile`
5. Click **Save** → **Build Now**

### Jenkins vs GitHub Actions — Role Comparison

| Aspect | GitHub Actions | Jenkins |
|---|---|---|
| Trigger | Every push / PR to main | Poll SCM every 5 min or manual |
| Runner environment | GitHub-hosted Ubuntu | Self-hosted Windows machine |
| Shell syntax | `sh` (bash) | `bat` (Windows CMD) |
| Primary role | CI — lint, containerise, test | BUILD gate — environment validation |
| Docker build | ✅ Yes | ✅ Yes |
| Test execution | ✅ Yes (in container) | ✅ Yes (on host) |

---

## Version History

This project evolved iteratively from a desktop GUI application into a containerised REST API, following a feature-branch Git workflow.

| Version | Type | Key Changes |
|---|---|---|
| v1.0 | Desktop GUI | Initial Tkinter UI — programme display only |
| v1.1 | Desktop GUI | Client selection and diet chart added |
| v1.1.2 | Desktop GUI | Improved layout, site metrics panel |
| v2.0.1 | Desktop + DB | SQLite database integration, client records |
| v2.1.2 | Desktop + DB | Progress tracking table added |
| v2.2.x | Desktop | Modularisation and code cleanup |
| v3.x | Desktop | Full-featured desktop application |
| **Flask v2.0.1** | **REST API** | **Migration to Flask — this repository** |

---

*Submitted as part of the DevOps Assignment — ACEest Fitness & Gym CI/CD Pipeline Implementation.*