# Experiment 9: MLOps Basics

## 1. Experiment Title
**MLOps Basics: Version Control, Containerization, and Continuous Integration**

---

## 2. Aim
To introduce the production machine learning lifecycle by applying:
1. **Version Control** with Git
2. **Containerization** with Docker
3. **Continuous Integration / Continuous Deployment (CI/CD)** with GitHub Actions

The experiment builds upon the deployed Flask-based deep learning model (MNIST digit-classification ANN) from Experiment 8.

---

## 3. Technologies Used
- **Git**: Distributed version control system
- **Docker**: Application containerization platform
- **GitHub Actions**: Automated CI/CD pipeline
- **Python 3.10+**: Core programming language
- **Flask**: Micro web framework for serving the ML REST API
- **TensorFlow / Keras**: Deep learning library for the ANN model
- **NumPy & Pillow**: Data manipulation and image preprocessing
- **Pytest**: Automated testing framework

---

## 4. Project Structure
```text
mlops-basics/
├── .github/
│   └── workflows/
│       └── ci.yml             # GitHub Actions CI workflow configuration
├── models/
│   └── baseline_ann.h5        # Trained MNIST ANN model
├── tests/
│   └── test_api.py            # Automated tests for API endpoints (/health, /predict)
├── app.py                     # Flask application entry point with /health and /predict
├── Dockerfile                 # Docker container specification
├── requirements.txt           # Project Python dependencies
├── README.md                  # Project documentation & lab guide
└── .gitignore                 # Files and patterns excluded from version control
```

---

## 5. How to Install Dependencies
To install the required Python packages in your local environment or virtual environment:

```bash
pip install -r requirements.txt
```

---

## 6. How to Run Flask Locally
To start the Flask development server on port 5000:

```bash
python app.py
```

The application will start and listen on `http://0.0.0.0:5000`.

---

## 7. How to Run Tests Locally
Run the automated test suite using `pytest`:

```bash
python -m pytest tests/
```

Expected output:
```text
tests/test_api.py ....                                                   [100%]
4 passed in 0.30s
```

---

## 8. How to Build Docker Image
To build the Docker container image from the `Dockerfile`:

```bash
docker build -t dl-lab-app:latest .
```

Expected output:
```text
Successfully built 7c3f9a2b1d4e
Successfully tagged dl-lab-app:latest
```

---

## 9. How to Run Docker Container
To run the containerized Flask API and map port 5000 on the host to port 5000 in the container:

```bash
docker run -p 5000:5000 dl-lab-app:latest
```

To list active running containers:
```bash
docker ps
```

---

## 10. How to Verify /health Endpoint
Verify container and API health using `curl` or a web browser:

```bash
curl http://localhost:5000/health
```

**Expected JSON Response:**
```json
{"status": "ok"}
```

---

## 11. GitHub Actions CI Workflow
The CI pipeline (`.github/workflows/ci.yml`) triggers on every `push` and `pull_request` to the `main` branch. It executes the following steps:
1. **Checkout code**: Pulls the repository using `actions/checkout@v4`.
2. **Set up Python 3.10**: Configures the Python runtime using `actions/setup-python@v5`.
3. **Install dependencies**: Runs `pip install -r requirements.txt`.
4. **Run tests**: Executes `python -m pytest tests/` to validate endpoints.
5. **Build Docker image**: Verifies container build with `docker build -t dl-lab-app:ci .`.

---

## 12. Results Summary

| Step | Tool | Status |
| :--- | :--- | :--- |
| Version Control | Git | Completed |
| Containerization | Docker | Configured (Dockerfile ready) |
| Automated Testing | Pytest / GitHub Actions | Passed & Configured |
| Container Health Check | Docker / curl | Configured (`/health` returns `{"status": "ok"}`) |
