
pipeline {
    agent any

    environment {
        DOCKER_HUB_CREDS = credentials('docker-hub-creds') // Reference the Jenkins credentials ID
    }

    stages {
        stage('Clone Repository') {
            steps {
                echo 'Cloning the repository from GitHub...'
                git url: 'https://github.com/eya-ghodhben/uber2.git', branch: 'main'

            }
        }

        stage('Build Docker Images') {
            steps {
                echo 'Building Docker images for all microservices...'
                sh 'docker build -t islem0512/payment-service:latest -f payment-service/Dockerfile .'
                sh 'docker build -t islem0512/driver-service:latest -f driver-service/Dockerfile .'
                sh 'docker build -t islem0512/rider-service:latest -f rider-service/Dockerfile .'
                sh 'docker build -t islem0512/ride-service:latest -f ride-service/Dockerfile .'
            }
        }

        stage('Push to Docker Hub') {
            steps {
                echo 'Logging in to Docker Hub...'
                sh """
                    echo ${DOCKER_HUB_CREDS_PSW} | docker login -u ${DOCKER_HUB_CREDS_USR} --password-stdin
                """
                echo 'Pushing Docker images to Docker Hub...'
                sh 'docker push islem0512/payment-service:latest'
                sh 'docker push islem0512/driver-service:latest'
                sh 'docker push islem0512/rider-service:latest'
                sh 'docker push islem0512/ride-service:latest'
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                echo 'Deploying microservices to Kubernetes...'
                sh 'kubectl apply -f payment-service/payment-service.yaml --validate=false' 
                sh 'kubectl apply -f driver-service/driver-service.yaml --validate=false'
                sh 'kubectl apply -f rider-service/rider-service.yaml --validate=false'
                sh 'kubectl apply -f ride-service/ride-service.yaml --validate=false'
            }
        }
    }

    post {
        always {
            echo 'Pipeline execution completed!'
        }
        success {
            echo 'Pipeline executed successfully!'
        }
        failure {
            echo 'Pipeline failed. Please check.'
        }
    }
}
