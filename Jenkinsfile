pipeline {
    agent any

    environment {
        // Image name for Docker build — matches your project name
        IMAGE_NAME = "aceest-fitness-gym"
    }

    stages {

        // ─────────────────────────────────────────────
        // STAGE 1: Pull latest code from GitHub
        // ─────────────────────────────────────────────
        stage('Checkout') {
            steps {
                echo '>>> Checking out source code from GitHub...'
                checkout scm
            }
        }

        // ─────────────────────────────────────────────
        // STAGE 2: Install Python dependencies
        // ─────────────────────────────────────────────
        stage('Install Dependencies') {
            steps {
                echo '>>> Installing Python dependencies...'
                sh '''
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        // ─────────────────────────────────────────────
        // STAGE 3: Build Validation (syntax check)
        // Compiles app.py to catch any syntax errors
        // before running tests
        // ─────────────────────────────────────────────
        stage('Build Validation') {
            steps {
                echo '>>> Validating Python syntax (Build Check)...'
                sh 'python -m py_compile app.py'
                echo '>>> app.py compiled successfully — no syntax errors found.'
            }
        }

        // ─────────────────────────────────────────────
        // STAGE 4: Run Unit Tests with Pytest
        // Executes the test suite in tests/
        // ─────────────────────────────────────────────
        stage('Run Tests') {
            steps {
                echo '>>> Running Pytest test suite...'
                sh 'pytest tests/ -v --tb=short'
            }
        }

        // ─────────────────────────────────────────────
        // STAGE 5: Build Docker Image
        // Builds the container using your Dockerfile
        // ─────────────────────────────────────────────
        stage('Docker Build') {
            steps {
                echo '>>> Building Docker image...'
                sh 'docker build -t ${IMAGE_NAME}:latest .'
                echo '>>> Docker image built successfully.'
            }
        }

    }

    // ─────────────────────────────────────────────
    // POST-BUILD ACTIONS
    // Runs regardless of success or failure
    // ─────────────────────────────────────────────
    post {
        success {
            echo '=========================================='
            echo '  BUILD SUCCESSFUL — All stages passed!  '
            echo '  ACEest Fitness API is ready.           '
            echo '=========================================='
        }
        failure {
            echo '=========================================='
            echo '  BUILD FAILED — Check console output.  '
            echo '  Fix the issues and push again.         '
            echo '=========================================='
        }
        always {
            echo '>>> Build complete. Check the logs above for details.'
        }
    }
}