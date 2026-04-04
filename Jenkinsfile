pipeline {
    agent any

    environment {
        IMAGE_NAME = "aceest-fitness-gym"
    }

    stages {

        // ─────────────────────────────────────────────
        // STAGE 1: Install Python dependencies
        // ─────────────────────────────────────────────
        stage('Install Dependencies') {
            steps {
                echo '>>> Installing Python dependencies...'
                bat 'python -m pip install --upgrade pip'
                bat 'pip install -r requirements.txt'
            }
        }

        // ─────────────────────────────────────────────
        // STAGE 2: Build Validation (syntax check)
        // ─────────────────────────────────────────────
        stage('Build Validation') {
            steps {
                echo '>>> Validating Python syntax...'
                bat 'python -m py_compile app.py'
                echo '>>> app.py compiled successfully — no syntax errors.'
            }
        }

        // ─────────────────────────────────────────────
        // STAGE 3: Run Unit Tests
        // ─────────────────────────────────────────────
        stage('Run Tests') {
            steps {
                echo '>>> Running Pytest test suite...'
                bat 'pytest tests/ -v --tb=short'
            }
        }

        // ─────────────────────────────────────────────
        // STAGE 4: Build Docker Image
        // ─────────────────────────────────────────────
        stage('Docker Build') {
            steps {
                echo '>>> Building Docker image...'
                bat 'docker build -t %IMAGE_NAME%:latest .'
                echo '>>> Docker image built successfully.'
            }
        }

    }

    post {
        success {
            echo '=========================================='
            echo '  BUILD SUCCESSFUL — All stages passed!  '
            echo '=========================================='
        }
        failure {
            echo '=========================================='
            echo '   BUILD FAILED — Check console output.  '
            echo '=========================================='
        }
        always {
            echo '>>> Pipeline finished.'
        }
    }
}