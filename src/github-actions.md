Sure! Here's how you can convert your Jenkins pipeline to a GitHub Actions workflow. I'll provide the step-by-step process along with the necessary file names.

### Step-by-Step Process

1. **Create a GitHub Actions Workflow File**:

   - File Name: `.github/workflows/ci.yml`

2. **Define the Workflow**:
   - The workflow will include the steps to test Git, checkout the repository, build and push the Docker image, update Kubernetes manifests, and deploy to Kubernetes.

### GitHub Actions Workflow File (`.github/workflows/ci.yml`)

```yaml
name: CI Pipeline

on:
  push:
    branches:
      - main

jobs:
  build:
    runs-on: ubuntu-latest

    env:
      DOCKER_TAG: ${{ steps.increment_version.outputs.version }}
      DOCKERHUB_CREDENTIALS_ID: ${{ secrets.DOCKERHUB_CREDENTIALS_ID }}
      DOCKER_IMAGE: chukwuka1488/polygon-rpc-app:${{ steps.increment_version.outputs.version }}
      DOCKERFILE_DIR: src
      KUBECONFIG_CREDENTIALS_ID: ${{ secrets.KUBECONFIG_CREDENTIALS_ID }}

    steps:
      - name: Test Git
        run: git --version

      - name: Checkout Repository
        uses: actions/checkout@v2

      - name: Increment Version
        id: increment_version
        run: |
          versionFile=version.txt
          version=v1.0.0
          if [ -f "$versionFile" ]; then
            version=$(cat $versionFile)
            IFS='.' read -r -a versionParts <<< "${version//v/}"
            major=${versionParts[0]}
            minor=${versionParts[1]}
            patch=${versionParts[2]}
            patch=$((patch + 1))
            if [ "$patch" -eq 100 ]; then
              patch=0
              minor=$((minor + 1))
            fi
            version="v${major}.${minor}.${patch}"
          fi
          echo $version > $versionFile
          echo "::set-output name=version::$version"

      - name: Build Docker Image
        run: docker build -t $DOCKER_IMAGE $DOCKERFILE_DIR

      - name: Log in to Docker Hub
        uses: docker/login-action@v2
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}

      - name: Push Docker Image
        run: docker push $DOCKER_IMAGE

      - name: Update Kubernetes Manifests
        run: ./changeTag.sh $DOCKER_TAG

      - name: Set up Kubernetes
        uses: azure/setup-kubectl@v1
        with:
          version: "latest"

      - name: Deploy to Kubernetes
        env:
          KUBECONFIG: ${{ secrets.KUBECONFIG }}
        run: kubectl apply -f kubernetes-manifest/deployment.yaml
```

### Explanation of the Workflow

1. **Trigger**:

   - The workflow is triggered on a push to the `main` branch.

2. **Environment Variables**:

   - The environment variables are set using GitHub secrets and the output from the `Increment Version` step.

3. **Steps**:
   - **Test Git**: Checks the Git version.
   - **Checkout Repository**: Uses the `actions/checkout` action to clone the repository.
   - **Increment Version**: Reads and increments the version number from `version.txt`.
   - **Build Docker Image**: Builds the Docker image using the specified Dockerfile directory.
   - **Log in to Docker Hub**: Logs in to Docker Hub using the `docker/login-action`.
   - **Push Docker Image**: Pushes the Docker image to Docker Hub.
   - **Update Kubernetes Manifests**: Updates the Kubernetes deployment manifest with the new Docker tag.
   - **Set up Kubernetes**: Sets up `kubectl` for deploying to Kubernetes.
   - **Deploy to Kubernetes**: Applies the Kubernetes deployment manifest using `kubectl`.

### GitHub Secrets

Make sure to add the following secrets to your GitHub repository:

- `DOCKERHUB_CREDENTIALS_ID`
- `DOCKER_USERNAME`
- `DOCKER_PASSWORD`
- `KUBECONFIG`

This should help you set up your CI pipeline using GitHub Actions. Let me know if you have any questions or need further assistance!
Sure! Here are the step-by-step instructions to add GitHub secrets to your repository:

### Step-by-Step Process to Add GitHub Secrets

1. **Navigate to Your Repository**:

   - Go to your GitHub repository where you want to add the secrets.

2. **Access the Settings**:

   - Click on the `Settings` tab at the top of the repository page.

3. **Go to Secrets**:

   - In the left sidebar, click on `Secrets and variables` and then select `Actions`.

4. **Add a New Secret**:

   - Click on the `New repository secret` button.

5. **Add Each Secret**:

   - For each secret, you will need to provide a name and a value. Here are the secrets you need to add along with their variable names:

   - **DOCKERHUB_CREDENTIALS_ID**:

     - **Name**: `DOCKERHUB_CREDENTIALS_ID`
     - **Value**: Your Docker Hub credentials ID.

   - **DOCKER_USERNAME**:

     - **Name**: `DOCKER_USERNAME`
     - **Value**: Your Docker Hub username.

   - **DOCKER_PASSWORD**:

     - **Name**: `DOCKER_PASSWORD`
     - **Value**: Your Docker Hub password.

   - **KUBECONFIG**:
     - **Name**: `KUBECONFIG`
     - **Value**: Your Kubernetes configuration file content (you can copy the content of your `kubeconfig.yaml` file).

6. **Save Each Secret**:
   - After entering the name and value for each secret, click the `Add secret` button to save it.

### Example

Here's an example of how to add the `DOCKER_USERNAME` secret:

1. Click on `New repository secret`.
2. Enter `DOCKER_USERNAME` in the `Name` field.
3. Enter your Docker Hub username in the `Value` field.
4. Click `Add secret`.

Repeat these steps for each of the other secrets (`DOCKERHUB_CREDENTIALS_ID`, `DOCKER_PASSWORD`, `KUBECONFIG`).

Once you have added all the secrets, they will be available for use in your GitHub Actions workflow.

Let me know if you need any further assistance or have any other questions!
