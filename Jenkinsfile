pipeline {
    agent any
    
    environment {
        VENV_DIR = 'venv'
        REQUIREMENTS = 'requirements.txt'
        ALLURE_RESULTS_DIR = "${env.WORKSPACE}/allure-results"
        ALLURE_REPORT_DIR = "${env.WORKSPACE}/allure-report"
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
                // Ensure the allure-results directory is clean before running tests
                sh "rm -rf ${ALLURE_RESULTS_DIR}"
                sh "mkdir -p ${ALLURE_RESULTS_DIR}"
                // Run pytest in the virtual environment
                sh '''
                    source ${VENV_DIR}/bin/activate
                    pytest
                '''
            }
        }
        stage('Generate Allure Report') {
            steps {
                // Run Allure command to generate the report
                sh '/home/jenkins/allure/bin/ generate /Users/evgeniapasko/jenkins_agent/workspace/Playwright-pipeline/allure-results -c -o /Users/evgeniapasko/jenkins_agent/workspace/Playwright-pipeline/allure-report'
            }
        }
    }
    post {
        always {
            // Publish Allure report in Jenkins
            allure includeProperties: false, jdk: '', reportBuildPolicy: 'ALWAYS', results: [[path: 'allure-results']]
        }
    }
}
