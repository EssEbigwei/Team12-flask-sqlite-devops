pipeline {
    agent any
    environment {
        S3_BUCKET = 'team12-flask-artifact'
        AWS_REGION = 'us-east-2'
    }
    
    stages {
        stage('Install Python Dependencies') {
            steps {
                sh '''
                    sudo apt-get update
                    sudo apt-get install -y python3-venv python3-pip
                '''
            }
        }
        
        stage('Checkout') {
            steps {
                checkout([
                    $class: 'GitSCM',
                    branches: [[name: '*/Dizzy_features']],
                    extensions: [[
                        $class: 'CleanBeforeCheckout',
                        deleteUntrackedNestedRepositories: true
                    ]],
                    userRemoteConfigs: [[
                        url: 'https://github.com/EssEbigwei/Team12-flask-sqlite-devops.git'
                    ]]
                ])
            }
        }
        
        stage('Setup Environment') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }
        
        stage('Package App') {
            steps {
                sh '''
                    . venv/bin/activate
                    tar -czf flask_app.tar.gz app requirements.txt templates init_db.sql
                '''
            }
        }
        
        stage('Upload to S3') {
            steps {
                withAWS(region: "${AWS_REGION}", credentials: 'aws-creds') {
                    s3Upload(
                        bucket: "${S3_BUCKET}",
                        file: 'flask_app.tar.gz',
                        path: "artifacts/${BUILD_NUMBER}/"
                    )
                }
            }
        }
        
        stage('Deploy with Ansible') {
            steps {
                withAWS(region: "${AWS_REGION}", credentials: 'aws-creds') {
                    sh '''
                        export AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
                        export AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}
                        export AWS_SESSION_TOKEN=${AWS_SESSION_TOKEN}
                        export ANSIBLE_HOST_KEY_CHECKING=False
                        export ANSIBLE_SSH_PRIVATE_KEY_FILE=/var/lib/jenkins/.ssh/id_rsa

                        ansible-playbook -i ansible/inventory ansible/playbook.yaml -v
                    '''
                }
            }
        }
    }
    
    post {
        always {
            sh 'rm -rf venv || true'
            deleteDir()  # Alternative to cleanWs
        }
    }
}