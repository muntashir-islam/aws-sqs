//Demo Pipeline. Need work
pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-credentials-id')
        AWS_ACCESS_KEY_ID = credentials('aws-access-key-id')
        AWS_SECRET_ACCESS_KEY = credentials('aws-secret-access-key')
        DOCKER_IMAGE = "muntashir/flask-sqs-app:latest"
        KUBECONFIG_CREDENTIALS = credentials('kubeconfig-credentials-id')
    }

    stages {
        stage('Checkout') {
            steps {
                // Checkout the code from your repository
                git url: 'https://github.com/muntashir-islam/aws-sqs.git', branch: 'main'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${DOCKER_IMAGE}").inside {
                        sh 'pip install -r requirements.txt'
                    }
                }
            }
        }

        stage('Run Unit Tests') {
            steps {
                script {
                    docker.image("${DOCKER_IMAGE}").inside {
                        sh 'python -m unittest discover -s tests'
                    }
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    docker.withRegistry('https://registry-1.docker.io', DOCKERHUB_CREDENTIALS) {
                        docker.image("${DOCKER_IMAGE}").push()
                    }
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                withKubeConfig([credentialsId: 'kubeconfig-credentials-id']) {
                    sh '''
                    kubectl apply -f k8s-deployments/secret.yaml
                    kubectl apply -f k8s-deployments/deployments.yaml
                    kubectl apply -f k8s-deployments/service.yaml
                    '''
                }
            }
        }
    }

    post {
        always {
            cleanWs() // Clean workspace after the build
        }
    }
}
