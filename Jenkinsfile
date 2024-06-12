pipeline {
    agent any
    
    environment {
        VENV_DIR = 'venv'
        REQUIREMENTS = 'requirements.txt'
    }

    stages {
        stage('Checkout') {
            steps {
                // Checkout the code from the repository
                git(
                    url: 'https://github.com/EvgeniyaP/test_playwright.git',
                    branch: 'main'
                ) 
            }
        }

        stage('Setup Python Environment') {
            steps {
                // Create a virtual environment
                sh 'python3 -m venv ${VENV_DIR}'
                
                // Activate the virtual environment and install dependencies
                sh '''
                    source ${VENV_DIR}/bin/activate
                    pip install -r ${REQUIREMENTS}
                '''
            }
        }

        stage('Install Playwright') {
            steps {
                // Install Playwright and its dependencies
                sh '''
                    source ${VENV_DIR}/bin/activate
                    python -m playwright install --with-deps
                '''
            }
        }

        stage('Run Tests') {
            steps {
                // Run pytest in the virtual environment
                sh '''
                    source ${VENV_DIR}/bin/activate
                    pytest
                '''
            }
        }
    }

    post {
        always {
            // Archive test results, logs, etc.
            archiveArtifacts artifacts: '**/test-results/*.xml', allowEmptyArchive: true
            junit 'test-results/*.xml'
            
            // Clean up virtual environment
            sh 'rm -rf ${VENV_DIR}'
        }
    }
}
