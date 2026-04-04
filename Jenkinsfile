pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                git 'https://github.com/2024tm93564-khushika/aceest-fitness-gym.git'
            }
        }

        stage('Setup Python Environment') {
            steps {
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                . venv/bin/activate
                pytest
                '''
            }
        }
    }
}