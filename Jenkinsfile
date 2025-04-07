pipeline {
    agent any
    environment {
        S3_BUCKET = 'team12-flask-artifact'
        AWS_REGION = 'us-east-2'
    }
    stages {
        stage('Checkout') {
            steps {
                checkout([
                    $class: 'GitSCM',
                    branches: [[name: '*/Dizzy_features']],
                    doGenerateSubmoduleConfigurations: false,
                    extensions: [],
                    submoduleCfg: [],
                    userRemoteConfigs: [[url: 'https://github.com/EssEbigwei/Team12-flask-sqlite-devops.git']]
                ])
            }
        }
        stage('Install Dependencies') {
            steps {
                sh '''
                    if ! command -v pip3 &> /dev/null; then
                        echo "pip3 not found, installing..."
                        sudo apt update && sudo apt install -y python3-pip
                    fi
                    pip3 install -r requirements.txt
                '''
            }
        }
        stage('Package App') {
            steps {
                sh 'tar -czf flask_app.tar.gz app requirements.txt templates init_db.sql'
            }
        }
        stage('Upload to S3') {
            steps {
                withAWS(region: "${AWS_REGION}", credentials: 'aws-creds') {
                    s3Upload(bucket: "${S3_BUCKET}", file: 'flask_app.tar.gz', path: 'artifacts/')
                }
            }
        }
        stage('Deploy with Ansible') {
            steps {
                sh 'ansible-playbook -i ansible/dynamic_inventory.py ansible/playbook.yml'
            }
        }
    }
}