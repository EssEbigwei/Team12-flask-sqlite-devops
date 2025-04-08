pipeline {
    agent any
    environment {
        S3_BUCKET = 'team12-flask-artifact'
        AWS_REGION = 'us-east-2'
        VENV_DIR = "${WORKSPACE}/venv"
        ARTIFACT_NAME = "flask_app_${BUILD_NUMBER}.tar.gz"
        DEPLOY_ENV = "production" // Can be parameterized
    }
    
    stages {
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
                sh """
                    python3 -m venv "${VENV_DIR}"
                    . "${VENV_DIR}/bin/activate"
                    pip install --upgrade pip wheel
                    pip install -r requirements.txt
                """
            }
        }
        
        stage('Run Tests') {
            steps {
                sh """
                    . "${VENV_DIR}/bin/activate"
                    python -m pytest tests/ -v --junitxml=test-results.xml
                """
            }
            post {
                always {
                    junit 'test-results.xml'
                }
            }
        }
        
        stage('Package App') {
            steps {
                sh """
                    # Include only necessary files
                    tar -czf "${ARTIFACT_NAME}" \
                        app/ \
                        requirements.txt \
                        templates/ \
                        init_db.sql \
                        ansible/
                    
                    # Generate checksum
                    sha256sum "${ARTIFACT_NAME}" > "${ARTIFACT_NAME}.sha256"
                """
            }
        }
        
        stage('Upload to S3') {
            steps {
                withAWS(region: "${AWS_REGION}", credentials: 'aws-creds') {
                    s3Upload(
                        bucket: "${S3_BUCKET}",
                        file: "${ARTIFACT_NAME}",
                        path: "artifacts/${BUILD_NUMBER}/",
                        metadata: [
                            'commit': env.GIT_COMMIT,
                            'build': "${BUILD_NUMBER}"
                        ]
                    )
                    s3Upload(
                        bucket: "${S3_BUCKET}",
                        file: "${ARTIFACT_NAME}.sha256",
                        path: "artifacts/${BUILD_NUMBER}/"
                    )
                }
            }
        }
        
        stage('Deploy with Ansible') {
            steps {
                sshagent(['jenkins-to-deploy']) {
                    withAWS(region: "${AWS_REGION}", credentials: 'aws-creds') {
                        sh """
                            export ANSIBLE_CONFIG="${WORKSPACE}/ansible/ansible.cfg"
                            ansible-playbook \
                                -i ansible/inventory \
                                ansible/playbook.yaml \
                                -e "build_number=${BUILD_NUMBER}" \
                                -e "artifact_name=${ARTIFACT_NAME}" \
                                -e "deployment_env=${DEPLOY_ENV}" \
                                -v
                        """
                    }
                }
            }
        }
    }
    
    post {
        always {
            sh "rm -rf '${VENV_DIR}' || true"
            cleanWs()
        }
        success {
            slackSend(
                color: 'good',
                message: "SUCCESS: ${env.JOB_NAME} #${env.BUILD_NUMBER} deployed to ${DEPLOY_ENV}"
            )
        }
        failure {
            slackSend(
                color: 'danger',
                message: "FAILED: ${env.JOB_NAME} #${env.BUILD_NUMBER}"
            )
        }
    }
}