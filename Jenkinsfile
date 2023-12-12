pipeline {
    agent any

    environment {
        // Define variables
        EC2_USER = 'ec2-user'
        EC2_HOST = '63.35.213.44'
        PROJECT_DIR = '/opt'
        CREDENTIALS_ID = credentials('keypair')
    }

    stages {
        stage('Checkout') {
            steps {
               checkout scm
            }
        }

        stage('Test') {
            steps {
                // Run Django unit tests
                sh 'yum install -y sqlite-devel'
                sh 'python -m venv venv'
                sh '. venv/bin/activate'
                sh 'pip install -r requirements.txt'
                sh 'python manage.py test'
            }
        }

        stage('Build') {
            steps {
                // Collect static files, etc.
                sh 'python manage.py collectstatic --noinput'
            }
        }

        stage('Deploy') {
            steps {
                // Transfer files to EC2
                script {
                    sshagent([CREDENTIALS_ID]) {
                        sh "scp -o StrictHostKeyChecking=no -r * ${EC2_USER}@${EC2_HOST}:${PROJECT_DIR}"
                    }
                }
            }
        }

        stage('Install Requirements and Migrate') {
            steps {
                // Install dependencies and run migrations on EC2
                script {
                    sshagent([CREDENTIALS_ID]) {
                        sh "ssh -o StrictHostKeyChecking=no ${EC2_USER}@${EC2_HOST} 'cd ${PROJECT_DIR} && yum install python -y && yum install pip -y && yum install -y sqlite-devel &&python -m venv venv && source venv/bin/activate && pip install -r requirements.txt && python manage.py migrate'"
                    }
                }
            }
        }

        stage('Restart Application') {
            steps {
                // Restart your application (e.g., using Gunicorn)
                script {
                    sshagent([CREDENTIALS_ID]) {
                        sh "ssh -o StrictHostKeyChecking=no ${EC2_USER}@${EC2_HOST} 'sudo systemctl restart your_application_service'"
                    }
                }
            }
        }
    }

    post {
        always {
            // Steps to clean up, notify, etc.
            echo 'Deployment process complete.'
        }
    }
}
