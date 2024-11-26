pipeline {
    agent any

    environment {
        DOCKER_HUB_USERNAME = 'eyaghodhben' // Votre nom d'utilisateur Docker Hub
        DOCKER_HUB_PASSWORD = 'eya@09112002' // Votre mot de passe Docker Hub
    }

    stages {
        stage('Clone Repository') {
            steps {
                echo 'Cloning the repository from GitHub...'
                git url: 'https://github.com/eya-ghodhben/uber2.git'

            }
        }

        stage('Build Docker Images') {
            steps {
                echo 'Building Docker images for all microservices...'
                // Construction des images pour chaque microservice
                sh 'docker build -t payment-service:latest -f Dockerfile .'
                sh 'docker build -t driver-service:latest -f Dockerfile .'
                sh 'docker build -t rider-service:latest -f Dockerfile .'
                sh 'docker build -t ride-service:latest -f Dockerfile .'
            }
        }

        stage('Push to Docker Hub') {
            steps {
                echo 'Logging in to Docker Hub...'
                // Connexion sécurisée à Docker Hub
                sh """
                    echo $DOCKER_HUB_PASSWORD | docker login -u $DOCKER_HUB_USERNAME --password-stdin
                """
                echo 'Pushing Docker images to Docker Hub...'
                // Push des images vers Docker Hub
                sh 'docker push payment-service:latest'
                sh 'docker push driver-service:latest'
                sh 'docker push rider-service:latest'
                sh 'docker push ride-service:latest'
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                echo 'Deploying microservices to Kubernetes...'
                // Application des fichiers de déploiement Kubernetes
                sh 'kubectl apply -f mongo-deployment.yaml'
                sh 'kubectl apply -f payment-deployment.yaml'
                sh 'kubectl apply -f deployment.yaml'
                sh 'kubectl apply -f rider-deployment.yaml'
                sh 'kubectl apply -f ride-deployment.yaml'
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
            echo 'Pipeline failed. Please check the logs.'
        }
    }
}
