To set up a CI/CD pipeline using Jenkins and ArgoCD in your Kubernetes cluster for automating the build, update, and deployment process of your Python application to Docker Hub, we'll go through the following steps:

1. **Set up Jenkins for CI/CD**:

   - Create a Jenkins pipeline to build and push the Docker image to Docker Hub.
   - Configure Jenkins to trigger builds automatically on code changes.

2. **Set up ArgoCD for Continuous Deployment**:

   - Deploy ArgoCD in your Kubernetes cluster to handle application deployments.
   - Create an ArgoCD application to manage and synchronize the deployment.

3. **Integrate Jenkins with ArgoCD**:
   - Use Jenkins to update the Kubernetes manifests and trigger ArgoCD to deploy the changes.

Below are the detailed steps for each part of the setup:

---

## Part 1: Setting Up Jenkins for CI/CD

### 1. Install Jenkins in Kubernetes

First, you'll need to deploy Jenkins in your Kubernetes cluster. You can use Helm to simplify the deployment process:

```bash
helm repo add jenkins https://charts.jenkins.io
helm repo update
helm install jenkins jenkins/jenkins --namespace jenkins --create-namespace
```

You can customize the Helm chart values to fit your needs, such as adding persistence, configuring service types, etc.

### 2. Configure Jenkins

1. **Access Jenkins**:

   - Get the admin password:
     ```bash
     kubectl exec --namespace jenkins -it svc/jenkins -c jenkins -- /bin/cat /run/secrets/additional/chart-admin-password && echo
     ```
     ```bash
     echo http://127.0.0.1:8080
     kubectl --namespace jenkins port-forward svc/jenkins 8080:8080
     ```
   - Open Jenkins in your browser and log in with the admin password.

2. **Install Required Plugins**: Install the following plugins via the Jenkins Plugin Manager:

   - **Docker Pipeline**: To build and push Docker images.
   - **Kubernetes Plugin**: If you want Jenkins to run builds on Kubernetes pods ().
   - **Git**: To pull code from your repository.

Based on your requirements, here are the plugins you should choose and why:

### Kubernetes Plugins

1. **Kubernetes CLI**: This plugin allows you to configure `kubectl` to interact with Kubernetes clusters from within your Jenkins jobs. It's useful if you need to run `kubectl` commands directly in your pipelines¹.
2. **Kubernetes Credentials Provider**: This plugin provides a read-only credentials store backed by Kubernetes. It's useful if you need to manage credentials securely within Kubernetes²¹.
3. **Kubernetes :: Pipeline :: DevOps Steps**: This plugin extends Jenkins Pipeline to allow building and testing inside Kubernetes Pods. It leverages Kubernetes features like pods, build images, service accounts, volumes, and secrets¹³.

### GitHub Plugins

1. **GitHub API**: This plugin provides the GitHub API for other plugins. It's a library plugin and doesn't have user-visible features by itself[^10^].
2. **GitHub**: This plugin integrates GitHub with Jenkins. It allows you to create hyperlinks between your Jenkins projects and GitHub, trigger jobs when you push to the repository, and report build status back to GitHub⁶.
3. **GitHub Branch Source**: This plugin allows you to create multibranch projects and organization folders from GitHub. It's useful for managing multiple branches and repositories in Jenkins¹⁶.

### Recommendations

- **For Kubernetes Integration**: Use the **Kubernetes CLI** and **Kubernetes :: Pipeline :: DevOps Steps** plugins. These will allow you to run `kubectl` commands and build/test inside Kubernetes Pods.
- **For GitHub Integration**: Use the **GitHub** and **GitHub Branch Source** plugins. These will help you integrate Jenkins with GitHub, manage branches, and trigger builds based on GitHub events.

3. **Create Jenkins Pipeline Job**:
   - Create a new Pipeline job in Jenkins.
   - Configure the pipeline script in Jenkins to include the following stages:

### Jenkins Pipeline Script

Here's an example Jenkins pipeline script for building and pushing a Docker image to Docker Hub:

File name: JenkinsFile

```groovy
pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS_ID = 'dockerhub-credentials' // Jenkins credentials ID for Docker Hub
        DOCKER_IMAGE = 'chukwuka1488/polygon-rpc-app'
    }

    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/your-repo-url' // Replace with your Git repository URL
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build(DOCKER_IMAGE)
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                script {
                    docker.withRegistry('https://registry.hub.docker.com', DOCKERHUB_CREDENTIALS_ID) {
                        docker.image(DOCKER_IMAGE).push('latest')
                    }
                }
            }
        }
    }
}
```

### Configurations:

- **DOCKERHUB_CREDENTIALS_ID**: Add your Docker Hub credentials to Jenkins (Manage Jenkins > Credentials) and use the credentials ID here.
- **DOCKER_IMAGE**: Specify your Docker image name, including the repository and tag.
- **Git Repository**: Replace `https://github.com/your-repo-url` with your actual Git repository URL.
  The `KUBECONFIG_CREDENTIALS_ID` in your Jenkins pipeline refers to the Jenkins credentials ID for Kubernetes. This ID is used to access the kubeconfig file, which contains the necessary configuration and credentials to interact with your Kubernetes cluster.

### What is a Kubeconfig File?

A kubeconfig file is a YAML file that contains information about clusters, users, and contexts. It allows `kubectl` and other Kubernetes tools to authenticate and interact with a Kubernetes cluster.

### How to Create and Add Kubeconfig Credentials in Jenkins

1. **Generate Kubeconfig File**: If you don't already have a kubeconfig file, you can generate one using the following command:
   ```sh
   kubectl config view --raw > kubeconfig.yaml
   ```
2. **Add Kubeconfig to Jenkins**:
   - Go to your Jenkins instance and click on "Manage Jenkins".
   - Click on "Manage Credentials".
   - Select the appropriate domain (e.g., "Global").
   - Click on "Add Credentials".
   - Choose "Secret file" as the kind.
   - Upload your `kubeconfig.yaml` file.
   - Give it an ID (e.g., `kubeconfig-credentials`) and a description.
   - Save the credentials.

### Using Kubeconfig in Jenkins Pipeline

In your pipeline, the `withCredentials` block uses the `kubeconfigFile` method to temporarily set the `KUBECONFIG` environment variable to the path of the kubeconfig file stored in Jenkins. This allows the `kubectl` command to use the correct configuration to interact with your Kubernetes cluster.

Here's the relevant part of your pipeline:

```groovy
withCredentials([kubeconfigFile(credentialsId: KUBECONFIG_CREDENTIALS_ID, variable: 'KUBECONFIG')]) {
    sh 'kubectl apply -f kubernetes-manifest/deployment.yaml'
}
```

This ensures that the `kubectl apply` command uses the kubeconfig file stored in Jenkins to deploy your application to the Kubernetes cluster.

If you have any further questions or need additional assistance, feel free to ask!

### 3. Set Up Webhooks (Optional)

Configure your Git repository to trigger the Jenkins pipeline on code changes by setting up a webhook pointing to your Jenkins URL.
Setting up webhooks is a great way to automate your CI/CD pipeline by triggering Jenkins builds on code changes. Here's how you can set up webhooks for your Git repository:

### GitHub

1. **Navigate to Your Repository**: Go to your GitHub repository.
2. **Settings**: Click on the "Settings" tab.
3. **Webhooks**: Click on "Webhooks" in the left sidebar.
4. **Add Webhook**: Click the "Add webhook" button.
5. **Payload URL**: Enter your Jenkins URL followed by `/github-webhook/`:
   ```plaintext
   http://jenkins.gm-nig-ltd.tech:8080/github-webhook/
   ```
6. **Content Type**: Set the content type to `application/json`.
7. **Events**: Choose "Just the push event" or select individual events you want to trigger the webhook.
8. **Add Webhook**: Click the "Add webhook" button to save the webhook.

### GitLab

1. **Navigate to Your Repository**: Go to your GitLab repository.
2. **Settings**: Click on "Settings" and then "Integrations".
3. **Add Webhook**: In the "Webhooks" section, click "Add webhook".
4. **URL**: Enter your Jenkins URL followed by `/gitlab-webhook/`:
   ```plaintext
   http://jenkins.gm-nig-ltd.tech:8080/gitlab-webhook/
   ```
5. **Trigger**: Select the events you want to trigger the webhook (e.g., Push events).
6. **Add Webhook**: Click the "Add webhook" button to save the webhook.

### Bitbucket

1. **Navigate to Your Repository**: Go to your Bitbucket repository.
2. **Settings**: Click on "Settings" in the left sidebar.
3. **Webhooks**: Click on "Webhooks".
4. **Add Webhook**: Click the "Add webhook" button.
5. **URL**: Enter your Jenkins URL followed by `/bitbucket-hook/`:
   ```plaintext
   http://jenkins.gm-nig-ltd.tech:8080/bitbucket-hook/
   ```
6. **Triggers**: Select the events you want to trigger the webhook (e.g., Push).
7. **Save**: Click the "Save" button to save the webhook.

### Verify Webhook

After setting up the webhook, you can verify it by making a commit or push to your repository. Jenkins should automatically trigger the pipeline based on the webhook configuration.

If you encounter any issues or need further assistance, feel free to ask!

---

## Part 2: Setting Up ArgoCD for Continuous Deployment

### 1. Install ArgoCD in Kubernetes

Install ArgoCD in your Kubernetes cluster using the following commands:

```bash
kubectl create namespace argocd

kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

### 2. Access ArgoCD UI

1. **Get ArgoCD initial admin password**:

```bash
kubectl get pods -n argocd -l app.kubernetes.io/name=argocd-server
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d; echo
```

2. **Access ArgoCD UI**: Port forward the ArgoCD server service to access the UI:

```bash
kubectl port-forward svc/argocd-server -n argocd 8080:443
```

Open `https://localhost:8080` in your browser and log in with username `admin` and the password you retrieved.

### 3. Create ArgoCD Application

Create an ArgoCD Application YAML file to deploy your application:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: polygon-rpc-app
  namespace: argocd
spec:
  destination:
    namespace: default
    server: "https://kubernetes.default.svc"
  project: default
  source:
    path: path/to/k8s-manifests
    repoURL: "https://github.com/your-repo-url"
    targetRevision: HEAD
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

### Configurations:

- **path/to/k8s-manifests**: Replace with the path to your Kubernetes manifests in your Git repository.
- **repoURL**: Replace with your actual Git repository URL.

Apply the ArgoCD application configuration:

```bash
kubectl apply -f argo-app.yaml
```

---

## Part 3: Integrating Jenkins with ArgoCD

### 1. Jenkins Script for Triggering ArgoCD

After the Docker image is pushed to Docker Hub, Jenkins can trigger ArgoCD to deploy the changes:

```groovy
pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS_ID = 'dockerhub-credentials'
        DOCKER_IMAGE = 'chukwuka1488/polygon-rpc-app'
        ARGOCD_SERVER = 'argocd-server.argocd.svc.cluster.local:80'
        ARGOCD_AUTH_TOKEN = credentials('argocd-auth-token') // Jenkins credentials ID for ArgoCD auth token
    }

    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/your-repo-url'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build(DOCKER_IMAGE)
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                script {
                    docker.withRegistry('https://registry.hub.docker.com', DOCKERHUB_CREDENTIALS_ID) {
                        docker.image(DOCKER_IMAGE).push('latest')
                    }
                }
            }
        }

        stage('Deploy to Kubernetes via ArgoCD') {
            steps {
                script {
                    sh """
                    curl -k -H "Authorization: Bearer ${ARGOCD_AUTH_TOKEN}" -X POST \
                    https://${ARGOCD_SERVER}/api/v1/applications/polygon-rpc-app/sync
                    """
                }
            }
        }
    }
}
```

### Configurations:

- **ARGOCD_AUTH_TOKEN**: Create a token in ArgoCD (Settings > Accounts > Generate Token) and add it to Jenkins credentials.
- **ARGOCD_SERVER**: Ensure that the server URL is correct and accessible from the Jenkins pod.

### 2. ArgoCD GitOps Workflow

- **GitOps**: Ensure the Kubernetes manifests in your Git repository reflect the desired application state.
- **ArgoCD Sync**: When Jenkins triggers ArgoCD, it will pull the latest manifests and apply them to the cluster.

---

## Final Testing

1. **Make a Change**: Update your code or Dockerfile, commit the changes to your Git repository.
2. **Observe Jenkins**: The Jenkins pipeline should trigger, build the Docker image, and push it to Docker Hub.
3. **Check ArgoCD**: Verify that ArgoCD synchronizes the new application state, and the updated version is deployed in your Kubernetes cluster.

---

### Additional Tips

- **Helm Charts**: If you use Helm charts, ArgoCD supports Helm as a source type. You can configure ArgoCD applications to use Helm charts from a Git repository or a Helm repository.
- **RBAC**: Configure Role-Based Access Control (RBAC) in Kubernetes to ensure that Jenkins and ArgoCD have the necessary permissions to perform their operations.
- **Monitoring and Logging**: Set up monitoring and logging for Jenkins and ArgoCD to troubleshoot any issues that may arise during the CI/CD process.

This setup will automate the process of building, testing, and deploying your application using Jenkins and ArgoCD, ensuring a robust CI/CD pipeline for your Python application. Let me know if you have any questions or need further assistance!
