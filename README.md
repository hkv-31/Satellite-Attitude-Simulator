# Satellite Attitude Control Simulator

A small end-to-end reinforcement-learning project that simulates 1D satellite attitude control.

## Architecture

User -> Firebase Hosting -> Cloud Run/FastAPI -> Q-table -> Satellite simulation -> Firestore

The Q-learning model is trained locally. Cloud Run only loads the resulting Q-table and performs inference.

## Project structure

```text
satellite_attitude_control_simulator/
├── app/
│   ├── environment.py
│   ├── q_learning.py
│   ├── storage.py
│   ├── config.py
│   └── main.py
├── model/
│   └── q_table.json
├── tests/
│   ├── test_api.py
│   └── test_environment.py
├── frontend/
│   └── index.html
├── train.py
├── requirements.txt
├── Dockerfile
├── firebase.json
├── firestore.rules
└── README.md
```

## Local setup

Python 3.11+ recommended.

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Install:

```bash
pip install -r requirements.txt
```

Train the model:

```bash
python train.py
```

Run tests:

```bash
pytest
```

Run the API:

```bash
uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

## Example API request

```bash
curl -X POST http://127.0.0.1:8000/simulate ^
  -H "Content-Type: application/json" ^
  -d "{\"target_angle\":0,\"start_angle\":45,\"start_angular_velocity\":0,\"max_steps\":100}"
```

## Firestore

For local Firestore writes, authenticate using Google Application Default Credentials:

```bash
gcloud auth application-default login
```

In Cloud Run, attach a service account with Firestore access instead of putting a service-account JSON file in the repository.

## Docker

Build:

```bash
docker build -t satellite-api .
```

Run:

```bash
docker run -p 8080:8080 satellite-api
```

Test:

```text
http://localhost:8080/docs
```

## Google Cloud Run

Set your project:

```bash
gcloud config set project YOUR_PROJECT_ID
```

Deploy directly from the source directory:

```bash
gcloud run deploy satellite-api \
  --source . \
  --region asia-south1 \
  --allow-unauthenticated \
  --min 0 \
  --max 1 \
  --memory 256Mi \
  --cpu 1
```

Use the resulting `https://...run.app` URL as the API URL.

## Firebase Hosting

Install Firebase CLI:

```bash
npm install -g firebase-tools
```

Login:

```bash
firebase login
```

Initialize Hosting if needed:

```bash
firebase init hosting
```

Choose the existing Firebase project and `frontend` as the public directory.

Then deploy:

```bash
firebase deploy --only hosting
```

The frontend can also be configured to proxy `/api/**` to Cloud Run using the `firebase.json` rewrite.

## Cost-control checklist

- Train locally, never inside Cloud Run.
- Cloud Run min instances = 0.
- Cloud Run max instances = 1.
- Keep memory at 256Mi unless the app needs more.
- Use a Cloud Billing spend cap for Cloud Run.
- Use budget alerts as a second warning system.
- Use one Firestore database.
- Do not enable Firestore PITR, backups, TTL, or other paid features for this demo.
- Keep the API lightweight and avoid continuous/background workloads.

## Important

A billing budget by itself is only an alert. A Cloud Billing spend cap is the mechanism to pause eligible Cloud Run usage after the cap is reached. Always verify the current Google Cloud billing UI and eligible-service list before deployment.
