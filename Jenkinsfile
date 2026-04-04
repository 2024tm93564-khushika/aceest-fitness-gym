pipeline {
    agent any

    environment {
        IMAGE_NAME = "aceest-fitness-gym"
    }

    stages {

        stage('Install Dependencies') {
            steps {
                echo '>>> Installing Python dependencies...'
                bat 'python -m pip install -r requirements.txt'
            }
        }

        stage('Build Validation') {
            steps {
                echo '>>> Validating Python syntax...'
                bat 'python -m py_compile app.py'
                echo '>>> app.py compiled successfully — no syntax errors.'
            }
        }

        stage('Run Tests') {
            steps {
                echo '>>> Running Pytest test suite...'
                bat 'python -m pytest tests/ -v --tb=short'
            }
        }

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