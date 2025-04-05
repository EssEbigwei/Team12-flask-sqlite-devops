pipeline {
    agent any

    environment {
        S3_BUCKET = 'team12-flask-artifacts'
        AWS_REGION = 'us-east-1'
    }

    stages {
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
