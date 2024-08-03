Sure! Here are the detailed steps to set up a Jenkins job that automatically triggers a build when you push to GitHub:

### Step 1: Create a Jenkins Job

1. **Access Jenkins Dashboard**:

   - Open your web browser and navigate to `http://<your-jenkins-server>:8080`.

2. **Create a New Item**:

   - Click on "New Item" on the left-hand side of the Jenkins dashboard.
   - Enter a name for your job (e.g., `Observability-Stack-Pipeline`).
   - Select "Pipeline" as the project type.
   - Click "OK" to create the job.

3. **Configure the Pipeline Job**:
   - In the job configuration page, scroll down to the "Pipeline" section.
   - Select "Pipeline script from SCM".
   - Choose "Git" as the SCM.
   - Enter your repository URL (`https://github.com/Chukwuka1488/Observability-Stack-for-Polygon-RPC`).
   - Specify the branch to build (e.g., `main`).
   - Click "Save" to save the job configuration.

### Step 2: Configure Webhooks in GitHub

1. **Access GitHub Repository Settings**:

   - Go to your GitHub repository (`https://github.com/Chukwuka1488/Observability-Stack-for-Polygon-RPC`).
   - Click on "Settings" in the repository menu.

2. **Add a Webhook**:
   - In the settings menu, click on "Webhooks".
   - Click on "Add webhook".
   - In the "Payload URL" field, enter the URL of your Jenkins server followed by `/github-webhook/` (e.g., `http://<your-jenkins-server>:8080/github-webhook/`).
   - Set the "Content type" to `application/json`.
   - Select "Just the push event" under "Which events would you like to trigger this webhook?".
   - Click "Add webhook" to save the webhook configuration.

### Step 3: Configure Jenkins Job to Trigger on Push

1. **Access Jenkins Job Configuration**:

   - Go back to your Jenkins dashboard.
   - Click on the job you created (e.g., `Observability-Stack-Pipeline`).
   - Click on "Configure" on the left-hand side.

2. **Enable GitHub Hook Trigger**:
   - Scroll down to the "Build Triggers" section.
   - Check the box for "GitHub hook trigger for GITScm polling".
   - Click "Save" to save the job configuration.

### Step 4: Verify the Setup

1. **Push Changes to GitHub**:

   - Make a change to your repository and push it to GitHub.
   - For example:
     ```sh
     git add .
     git commit -m "Test webhook trigger"
     git push origin main
     ```

2. **Monitor Jenkins**:
   - Go to your Jenkins dashboard and open the job you created.
   - You should see a new build triggered automatically in the "Build History" section.
   - Click on the build number to view the build details and console output.

By following these steps, you should have a Jenkins job that automatically triggers a build whenever you push changes to your GitHub repository. If you encounter any issues or need further assistance, feel free to ask! 😊

Got it! Since your Jenkins is installed via Helm in a Kubernetes cluster, you can verify and install Git on the Jenkins agent pod using the following steps:

### Step 1: Access the Jenkins Agent Pod

1. **List the Pods**:

   - First, list all the pods in the namespace where Jenkins is installed. For example, if Jenkins is installed in the `jenkins` namespace:
     ```sh
     kubectl get pods -n jenkins
     ```

2. **Identify the Jenkins Agent Pod**:

   - Look for the pod that corresponds to the Jenkins agent. It might have a name like `jenkins-agent-<random-string>`.

3. **Access the Jenkins Agent Pod**:
   - Use `kubectl exec` to access the Jenkins agent pod. Replace `<jenkins-agent-pod>` with the actual pod name:
     ```sh
     kubectl exec -it <jenkins-agent-pod> -n jenkins -- /bin/bash
     ```

### Step 2: Verify Git Installation

1. **Check Git Version**:

   - Once inside the Jenkins agent pod, run the following command to check if Git is installed and to verify its version:
     ```sh
     git --version
     ```
   - You should see an output similar to:
     ```sh
     git version 2.39.2
     ```

2. **Install Git (if not installed)**:
   - If Git is not installed, you can install it using the package manager available in the pod. For example, if the pod is based on a Debian/Ubuntu image:
     ```sh
     apt update
     apt install git
     ```

### Step 3: Restart Jenkins Agent Pod (if necessary)

1. **Restart the Jenkins Agent Pod**:
   - If you had to install Git, you might need to restart the Jenkins agent pod to ensure it picks up the new installation. You can do this by deleting the pod, and Kubernetes will automatically recreate it:
     ```sh
     kubectl delete pod <jenkins-agent-pod> -n jenkins
     ```

By following these steps, you can ensure that Git is installed on your Jenkins agent pod and verify its version. If you encounter any issues or need further assistance, feel free to ask! 😊
