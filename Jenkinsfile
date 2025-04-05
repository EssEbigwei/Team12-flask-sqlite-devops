pipeline {
    agent { label 'aws-agent' }
    
    environment {
        S3_BUCKET = 'team12-flask-artifacts'
        AWS_REGION = 'us-east-1'
        ANSIBLE_HOST_KEY_CHECKING = 'False'
    }

    stages {
        stage('Build') {
            steps {
                sh 'pip3 install -r requirements.txt'
                sh 'tar -czf flask_app.tar.gz app/ requirements.txt'
            }
        }

        stage('Upload to S3') {
            steps {
                withCredentials([aws(credentialsId: 'aws-creds', accessKeyVariable: 'AWS_ACCESS_KEY_ID', secretKeyVariable: 'AWS_SECRET_ACCESS_KEY')]) {
                    sh "aws s3 cp flask_app.tar.gz s3://${S3_BUCKET}/artifacts/"
                }
            }
        }

        stage('Deploy') {
            steps {
                sh 'ansible-playbook -i ansible/dynamic_inventory.py ansible/playbook.yml'
            }
        }
    }
}