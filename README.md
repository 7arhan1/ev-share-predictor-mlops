# EV Share Predictor – MLOps Pipeline

A machine learning web application that predicts the global Electric Vehicle (EV) market share for a given year. Built with a full MLOps pipeline: automated CI/CD via GitHub Actions, containerised with Docker, and deployed to a Kubernetes cluster (Minikube) on a GCP VM.

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Run Locally](#run-locally)
  - [Run with Docker](#run-with-docker)
- [MLOps Pipeline](#mlops-pipeline)
  - [CI – Continuous Integration](#ci--continuous-integration)
  - [CD – Continuous Deployment](#cd--continuous-deployment)
- [Kubernetes Deployment](#kubernetes-deployment)
- [Testing](#testing)
- [Required Secrets](#required-secrets)

---

## Overview

This project trains a **Linear Regression** model on historical EV stock share data (2010–2022) and exposes it via a **Flask** web application. A user enters a year and receives the model's predicted EV market share percentage for that year.

The entire workflow — from training to deployment — is automated through a two-stage GitHub Actions pipeline targeting `Dev` and `Prod` branches.

---

## Architecture

```
User Browser
     │
     ▼
Flask App (flaskapp.py)
     │  POST /predict
     ▼
Linear Regression Model (model.pkl)
     │
     ▼
Prediction Response

─────────────────────────────────────────

GitHub Push (Prod branch)
     │
     ├── CI Job: install → train → test
     │
     └── CD Job: build & push Docker image
                     │
                     ▼
              GCP VM (SSH via gcloud)
                     │
                     ▼
          Minikube Kubernetes Cluster
          (Deployment + LoadBalancer Service)
```

---

## Project Structure

```
ev-share-predictor-mlops/
├── .github/
│   └── workflows/
│       ├── ci.yml              # CI: runs on Dev and Prod branches
│       └── cd.yml              # CD: deploys to Minikube on GCP (Prod only)
├── minikube_services/
│   ├── deployment.yml          # Kubernetes Deployment manifest
│   └── service.yml             # Kubernetes LoadBalancer Service manifest
├── templates/
│   ├── index.html              # Input form
│   └── result.html             # Prediction result page
├── tests/
│   ├── test_model.py           # Unit tests for the trained model
│   └── test_int.py             # Integration tests for the Flask routes
├── ev_data.csv                 # Historical EV share dataset (2010–2022)
├── model.py                    # Model training script – outputs model.pkl
├── flaskapp.py                 # Flask web application
├── Dockerfile                  # Container image definition
└── requirements.txt            # Python dependencies
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| ML Framework | scikit-learn (Linear Regression) |
| Web Framework | Flask + Gunicorn |
| Containerisation | Docker |
| Orchestration | Kubernetes (Minikube) |
| CI/CD | GitHub Actions |
| Cloud | Google Cloud Platform (Compute Engine) |
| Image Registry | Docker Hub |
| Language | Python 3.8 |

---

## Getting Started

### Prerequisites

- Python 3.8+
- Docker
- (For full deployment) A GCP VM with Minikube installed and a Docker Hub account

### Run Locally

```bash
# 1. Clone the repository
git clone -b Prod https://github.com/<your-username>/ev-share-predictor-mlops.git
cd ev-share-predictor-mlops

# 2. Install dependencies
pip install -r requirements.txt

# 3. Train the model (generates model.pkl)
python3 model.py

# 4. Start the Flask app
python3 flaskapp.py
```

The app will be available at `http://localhost:5000`.

### Run with Docker

```bash
# Build the image
docker build -t ev-share-predictor .

# Run the container
docker run -p 5000:5000 ev-share-predictor
```

The app will be available at `http://localhost:5000`.

---

## MLOps Pipeline

### CI – Continuous Integration

**Trigger:** Push to `Dev` or `Prod` branch.

**Steps:**
1. Check out code
2. Set up Python 3.8
3. Install dependencies from `requirements.txt`
4. Train the model (`python3 model.py`) to generate `model.pkl`
5. Run all unit and integration tests

### CD – Continuous Deployment

**Trigger:** Push to `Prod` branch only (runs after CI passes).

**Steps:**
1. Re-run CI steps (install, train, test)
2. Authenticate with GCP using a service account key
3. Log in to Docker Hub
4. Build and push three Docker image tags:
   - `latest`
   - `Prod`
   - `Prod-<short-sha>` (immutable, commit-specific tag)
5. SSH into the GCP VM via `gcloud compute ssh`
6. Clone the `Prod` branch fresh onto the VM
7. Apply the Kubernetes `deployment.yml` to the Minikube cluster (delete old deployment first, then re-apply)

---

## Kubernetes Deployment

The `minikube_services/` directory contains two manifests:

**`deployment.yml`** – deploys 1 replica of the app container (port 5000) using the `latest` image from Docker Hub.

**`service.yml`** – exposes the deployment as a `LoadBalancer` service on `nodePort: 30007`, forwarding traffic to container port 5000.

To apply manually on a Minikube cluster:

```bash
minikube kubectl -- apply -f minikube_services/deployment.yml
minikube kubectl -- apply -f minikube_services/service.yml
```

---

## Testing

Tests are located in the `tests/` directory and are auto-discovered by `unittest`.

```bash
# Generate model.pkl first
python3 model.py

# Run all tests
python3 -m unittest discover tests
```

**`test_model.py`** (Unit tests):
- Verifies the loaded model is a `LinearRegression` instance
- Verifies a prediction returns a single float value

**`test_int.py`** (Integration tests):
- Verifies the home page (`GET /`) returns HTTP 200
- Verifies the prediction endpoint (`POST /predict`) returns a result containing the expected output text

---

## Required Secrets

The CD pipeline requires the following secrets to be set in your GitHub repository (`Settings → Secrets and variables → Actions`):

| Secret | Description |
|---|---|
| `GCP_SA_KEY_JSON` | GCP service account key (JSON) with Compute Engine SSH access |
| `DOCKER_HUB_USERNAME` | Your Docker Hub username |
| `DOCKER_HUB_ACCESS_TOKEN` | Docker Hub access token (not your password) |
