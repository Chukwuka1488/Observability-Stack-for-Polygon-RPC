pipeline {
    agent any // Use any available agent for the pipeline

    environment {
        DOCKER_TAG = getIncrementalVersion() // Get the incremental version
        DOCKERHUB_CREDENTIALS_ID = 'DOCKERHUB_CREDENTIALS_ID' // Jenkins credentials ID for Docker Hub
        DOCKER_IMAGE = "chukwuka1488/polygon-rpc-app:${DOCKER_TAG}" // Docker image name with tag
        DOCKERFILE_DIR = 'src' // Directory containing Dockerfile
        KUBECONFIG_CREDENTIALS_ID = 'kubeconfig-credentials' // Jenkins credentials ID for Kubernetes (kubectl config view --raw > kubeconfig.yaml)
    }

    stages {
        stage('Test Git') {
            steps {
                script {
                    sh 'git --version'
                    echo 'Test Git stage completed'
                }
            }
        }

        stage('Checkout') {
            steps {
                // Clone the repository from GitHub
                git 'https://github.com/Chukwuka1488/Observability-Stack-for-Polygon-RPC' // Replace with your actual Git repository URL
                echo 'Checkout stage completed'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // Navigate to the directory containing Dockerfile and build the Docker image
                    docker.build("${DOCKER_IMAGE}", "${DOCKERFILE_DIR}")
                    echo 'Build Docker Image stage completed'
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                script {
                    // Log in to Docker Hub and push the Docker image
                    docker.withRegistry('https://registry.hub.docker.com', DOCKERHUB_CREDENTIALS_ID) {
                        docker.image("${DOCKER_IMAGE}").push('latest')
                    }
                    echo 'Push to Docker Hub stage completed'
                }
            }
        }

        stage('Update Kubernetes Manifests') {
            steps {
                script {
                    // Update the Kubernetes deployment manifest with the new Docker tag
                    sh './changeTag.sh ${DOCKER_TAG}'
                    echo 'Update Kubernetes Manifests stage completed'
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                script {
                    // Use kubectl to apply the deployment using the credentials stored in Jenkins
                    withCredentials([kubeconfigFile(credentialsId: KUBECONFIG_CREDENTIALS_ID, variable: 'KUBECONFIG')]) {
                        sh 'kubectl apply -f kubernetes-manifest/deployment.yaml'
                    }
                    echo 'Deploy to Kubernetes stage completed'
                }
            }
        }
    }

    post {
        success {
            echo 'Build and Deployment completed successfully!' // Message on successful build and deployment
        }
        failure {
            echo 'Build or Deployment failed!' // Message on build or deployment failure
        }
    }
}

// Function to get the incremental version number
def getIncrementalVersion() {
    def versionFile = 'version.txt'
    def version = 'v1.0.0'
    
    if (fileExists(versionFile)) {
        version = readFile(versionFile).trim()
        def (major, minor, patch) = version.replace('v', '').split('\\.')
        patch = patch.toInteger() + 1
        
        if (patch == 100) {
            patch = 0
            minor = minor.toInteger() + 1
        }
        
        version = "v${major}.${minor}.${patch}"
    }
    
    writeFile(file: versionFile, text: version)
    return version
}
