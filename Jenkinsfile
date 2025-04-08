pipeline {
    agent any
    environment {
        S3_BUCKET = 'team12-flask-artifact'
        AWS_REGION = 'us-east-2'
        ANSIBLE_SSH_PRIVATE_KEY_FILE = '/var/lib/jenkins/.ssh/id_rsa'
    }
    
    stages {
        stage('Check Python Environment') {
            steps {
                script {
                    def pythonEnvCheck = sh(script: 'python3 -m venv --help >/dev/null 2>&1', returnStatus: true)
                    if (pythonEnvCheck != 0) {
                        error("Python virtual environment package not found. Please install python3-venv on the Jenkins server manually.")
                    }
                }
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
                    script {
                        // Get the S3 artifact path for this build
                        def s3ArtifactPath = "artifacts/${BUILD_NUMBER}/flask_app.tar.gz"
                        
                        sh """
                            export ANSIBLE_HOST_KEY_CHECKING=False
                            
                            ansible-playbook -i ansible/inventory ansible/playbook.yaml -v \
                                -e "build_number=${BUILD_NUMBER}" \
                                -e "s3_bucket=${S3_BUCKET}" \
                                -e "s3_path=${s3ArtifactPath}" \
                                -e "aws_region=${AWS_REGION}"
                        """
                    }
                }
            }
        }
    }
    
    post {
        always {
            sh 'rm -rf venv || true'
            deleteDir()
        }
    }
}