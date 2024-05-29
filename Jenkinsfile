pipeline {
    agent any

    environment {
        PYTHON_VERSION = '3.9'
        VENV_NAME = 'venv'
        SSH_KEY_CREDENTIALS_ID = 'aws-ssh-key' // Jenkins credential ID for SSH key
        AWS_EC2_HOST = '44.203.255.73' // The hostname or IP address of your EC2 instance
        REMOTE_USER = 'ec2-user' // The username for SSH login (typically 'ec2-user' for Amazon Linux)
        DEPLOY_DIR = '/home/ec2-user/deployment' // The deployment directory on the EC2 instance
    }

    stages {
        stage('Checkout') {
            steps {
                // Use SSH key credentials to checkout from Git
                sshagent(credentials: [SSH_KEY_CREDENTIALS_ID]) {
                    sh 'git clone git@github.com:EvgeniyaP/test_playwright.git'
                }
            }
        }
        stage('Transfer Code to EC2') {
            steps {
                // Transfer the code to the AWS EC2 instance
                sshagent([SSH_KEY_CREDENTIALS_ID]) {
                    sh """
                    scp -o StrictHostKeyChecking=no -r * ${REMOTE_USER}@${AWS_EC2_HOST}:${DEPLOY_DIR}
                    """
                }
            }
        }
        stage('Run Tests on EC2') {
            steps {
                // Connect to the EC2 instance and run tests
                sshagent([SSH_KEY_CREDENTIALS_ID]) {
                    sh """
                    ssh -o StrictHostKeyChecking=no ${REMOTE_USER}@${AWS_EC2_HOST} << 'EOF'
                        cd ${DEPLOY_DIR}
                        python${PYTHON_VERSION} -m venv ${VENV_NAME}
                        source ${VENV_NAME}/bin/activate
                        pip install -r requirements.txt
                        python -m playwright install --with-deps
                        pytest
                    EOF
                    """
                }
            }
        }
    }

    post {
    always {
            // Clean up actions, e.g., remove temporary files or resources
            sh 'rm -rf test_results/'
        }
        success {
            echo 'Pipeline succeeded!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}
