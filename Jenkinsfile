pipeline {
    agent any

    environment {
        // Define variables
        EC2_USER = 'ec2-user'
        EC2_HOST = '52.208.23.177'
        PROJECT_DIR = '/home/ec2-user/app'
    }

    stages {
        stage('Checkout') {
            steps {
                sh 'rm -rf *'
                checkout scm
            }
        }

        // Uncomment and update these stages as needed
        // stage('Test') {
        //     steps {
        //         // Run Django unit tests
        //         // ...
        //     }
        // }

        // stage('Build') {
        //     steps {
        //         // Collect static files, etc.
        //         // ...
        //     }
        // }

        stage('SonarQube Analysis') {
            steps {
                script {
                    sh '''
                        sonar-scanner \
                        -Dsonar.projectKey="x20131640-SonarQube" \
                        -Dsonar.sources=. \
                        -Dsonar.host.url="http://54.75.57.149:9000" \
                        -Dsonar.login="${credentials('squ_955391d6a10555e7e8130225cd42db9d3e089095')}"
                    '''
                }
            }
        }

        stage('Deploy') {
            steps {
                // Transfer files to EC2
                script {
                    sshagent(credentials: ['keypair']) {
                        sh "ssh -o StrictHostKeyChecking=no ${EC2_USER}@${EC2_HOST} mkdir -p ${PROJECT_DIR}"
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
                        sh "ssh -o StrictHostKeyChecking=no ${EC2_USER}@${EC2_HOST} 'cd ${PROJECT_DIR} && sudo yum install python3 -y && sudo yum install -y sqlite-devel && sudo yum install -y gcc && sudo yum install -y python3-devel && sudo pip3 install -r requirements.txt && sudo python3 manage.py migrate'"
                    }
                }
            }
        }

        stage('Restart Application') {
            steps {
                // Restart your application (e.g., using Gunicorn)
                script {
                    sshagent(credentials: ['keypair']){
                        sh "ssh -o StrictHostKeyChecking=no ${EC2_USER}@${EC2_HOST} 'cd ${PROJECT_DIR} && chmod +x start.sh && ./start.sh'"
                    }
                }
            }
        }
    }

    post {
        always {
            echo 'Deployment process complete.'
        }
    }
}
