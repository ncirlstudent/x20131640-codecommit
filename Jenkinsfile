pipeline {
    agent any

    environment {
        EC2_USER = 'ec2-user'
        EC2_HOST = '52.208.23.177'
        PROJECT_DIR = '/home/ec2-user/app'
        ZAP_TARGET_URL = 'http://ec2-52-208-23-177.eu-west-1.compute.amazonaws.com:8080/'
        ZAP_PATH = '/opt/zaproxy'
        ZAP_CLI_PATH = '/local/bin/zap-cli'
    }

    stages {
        stage('Checkout') {
            steps {
                sh 'rm -rf *'
                checkout scm
            }
        }

        // ... Other stages ...

        stage('SonarQube Analysis') {
            steps {
                withCredentials([string(credentialsId: '4fb67c25-fb98-4bae-844a-c4a16c66c39e', variable: 'SONARQUBE_TOKEN')]) {
                    sh '''
                        /opt/sonar-scanner/bin/sonar-scanner -X \
                        -Dsonar.projectKey="x20131640-SonarQube" \
                        -Dsonar.sources=. \
                        -Dsonar.host.url="http://54.75.57.149:9000" \
                        -Dsonar.login="$SONARQUBE_TOKEN"
                    '''
                }
            }
        }

        stage('Deploy') {
            steps {
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
                script {
                    sshagent(credentials: ['keypair']) {
                        sh "ssh -o StrictHostKeyChecking=no ${EC2_USER}@${EC2_HOST} 'cd ${PROJECT_DIR} && sudo yum install python3 -y && sudo yum install -y sqlite-devel && sudo yum install -y gcc && sudo yum install -y python3-devel && sudo pip3 install -r requirements.txt && sudo python3 manage.py migrate'"
                    }
                }
            }
        }

        stage('Restart Application') {
            steps {
                script {
                    sshagent(credentials: ['keypair']) {
                        sh "ssh -o StrictHostKeyChecking=no ${EC2_USER}@${EC2_HOST} 'cd ${PROJECT_DIR} && chmod +x start.sh && ./start.sh'"
                    }
                }
            }
        }

        stage('OWASP ZAP Scan') {
            steps {
                script {
                    // Start ZAP in daemon mode
                    sh "${ZAP_PATH}/zap.sh -daemon -port 8090 -host 0.0.0.0 -config api.disablekey=true &"
                    sh 'sleep 10' // Allow time for ZAP to start
                    // Example: Start a Spider scan using ZAP's REST API
                    sh 'curl http://localhost:8090/JSON/spider/action/scan/?url=${ZAP_TARGET_URL}'
                    // ... additional commands for scan control and result retrieval ...
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
