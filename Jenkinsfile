pipeline {
    agent any

    environment {
        // Define variables
        EC2_USER = 'ec2-user'
        EC2_HOST = '52.208.23.177'
        PROJECT_DIR = '/home/ec2-user/app'
        CREDENTIALS_ID = credentials('keypair')
    }

    stages {
        stage('Checkout') {
            steps {
                sh 'rm -rf *'
                checkout scm
            }
        }

        // stage('Test') {
        //     steps {
        //         // Run Django unit tests
        //         sh 'sudo yum install -y sqlite-devel'
        //         sh 'sudo yum install -y gcc'
        //         sh 'sudo yum install python-devel'
        //         sh 'python -m venv venv'
        //         sh '. venv/bin/activate'
        //         sh 'pip install -r requirements.txt'
        //         sh 'python manage.py test'
        //     }
        // }

        // stage('Build') {
        //     steps {
        //         // Collect static files, etc.
        //         sh 'python manage.py collectstatic --noinput'
        //     }
        // }

        stage('Deploy') {
            steps {
                // Transfer files to EC2
                script {
                    sshagent(credentials: ['keypair']) {
                        sh "ssh -o StrictHostKeyChecking=no ${EC2_USER}@${EC2_HOST} mkdir -p ${PROJECT_DIR}"
                        //sh "rsync -avz --exclude './eshopenv/lib64' * ${EC2_USER}@${EC2_HOST}:${PROJECT_DIR}"
                        sh "rsync -avz --exclude './eshopenv/lib64' * ${EC2_USER}@${EC2_HOST}:${PROJECT_DIR}"
                    }
                }
            }
        }

        stage('Install Requirements and Migrate') {
            steps {
                // Install dependencies and run migrations on EC2
                script {
                    sshagent(credentials: ['keypair']) {
                        sh "ssh -o StrictHostKeyChecking=no ${EC2_USER}@${EC2_HOST} 'cd ${PROJECT_DIR} && sudo yum install python3 -y && sudo yum install -y sqlite-devel && sudo yum install -y gcc && sudo yum install -y python3-devel && pip3 install -r requirements.txt && python3 manage.py migrate'"
                    }
                }
            }
        }

        stage('Restart Application') {
            steps {
                // Restart your application (e.g., using Gunicorn)
                script {
                    sshagent(credentials: ['keypair']){
                        sh "ssh -o StrictHostKeyChecking=no ${EC2_USER}@${EC2_HOST} 'cd ${PROJECT_DIR} && nohup python3 manage.py runserver 0.0.0.0:80 >/dev/null 2>&1"
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
