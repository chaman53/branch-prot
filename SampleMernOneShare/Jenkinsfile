pipeline {
    agent any
    stages {
        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("myapp-backend:${env.BUILD_ID}").push()
                }
            }
        }
        stage('Deploy to Kubernetes') {
            steps {
                script {
                    kubectl('apply -f k8s/')
                }
            }
        }
    }
}