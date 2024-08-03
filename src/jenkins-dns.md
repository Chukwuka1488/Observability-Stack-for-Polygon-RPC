To change your Jenkins service from `ClusterIP` to `LoadBalancer` using the CLI, you can follow these steps:

### 1. Edit the Service YAML

First, you need to edit the service definition to change the type from `ClusterIP` to `LoadBalancer`.

1. **Export the Current Service Definition**:

   ```sh
   kubectl get svc jenkins -n jenkins -o yaml > jenkins-service.yaml
   ```

2. **Edit the YAML File**:
   Open the `jenkins-service.yaml` file in a text editor and change the `type` from `ClusterIP` to `LoadBalancer`:

   ```yaml
   apiVersion: v1
    kind: Service
    metadata:
    annotations:
        meta.helm.sh/release-name: jenkins
        meta.helm.sh/release-namespace: jenkins
    labels:
        app.kubernetes.io/component: jenkins-controller
        app.kubernetes.io/instance: jenkins
        app.kubernetes.io/managed-by: Helm
        app.kubernetes.io/name: jenkins
        helm.sh/chart: jenkins-5.5.2
    name: jenkins
    namespace: jenkins
    spec:
    type: LoadBalancer
    ports:
        - name: http
        port: 8080
        protocol: TCP
        targetPort: 8080
    selector:
        app.kubernetes.io/component: jenkins-controller
    app.kubernetes.io/instance: jenkins
   ```

3. **Apply the Updated Service Definition**:
   ```sh
   kubectl apply -f jenkins-service.yaml
   ```

### 2. Verify the Service

After applying the changes, you can verify that the service has been updated and check for the external IP address:

1. **Get the Service Details**:

   ```sh
   kubectl get svc -n jenkins
   ```

2. **Check for External IP**:
   The output should show the `jenkins` service with the `LoadBalancer` type and an `EXTERNAL-IP` assigned. It may take a few moments for the external IP to be assigned.

### Example Output

```plaintext
NAME            TYPE           CLUSTER-IP     EXTERNAL-IP      PORT(S)     AGE
jenkins         LoadBalancer   10.43.215.68   <external-ip>    8080/TCP    110m
jenkins-agent   ClusterIP      10.43.98.180   <none>           50000/TCP   110m
```

### Access Jenkins

Once the external IP is assigned, you can access Jenkins using the external IP address:

```plaintext
http://<external-ip>:8080
```

By following these steps, you can change your Jenkins service from `ClusterIP` to `LoadBalancer` and make it accessible via a public URL. If you have any further questions or need additional assistance, feel free to ask!

Source: Conversation with Copilot, 03/08/2024
(1) ClusterIP, NodePort, and LoadBalancer: Kubernetes Service Types - Baeldung. https://www.baeldung.com/ops/kubernetes-service-types.
(2) Create an External Load Balancer | Kubernetes. https://kubernetes.io/docs/tasks/access-application-cluster/create-external-load-balancer/.
(3) Service ClusterIP allocation | Kubernetes. https://kubernetes.io/docs/concepts/services-networking/cluster-ip-allocation/.

To update your DNS records to ensure your Jenkins instance is accessible via a public URL, you can add an A record pointing to the external IP address of your Jenkins service. Here's how you can do it:

### Steps to Update DNS Records

1. **Log in to Your DNS Management Console**: Access your DNS management console where you manage the domain `gm-nig-ltd.tech`.
2. **Add an A Record**:
   - **Type**: A
   - **Name**: `jenkins` (or any subdomain you prefer)
   - **Content**: `<external-ip>` (Replace with the external IP address of your Jenkins service)
   - **Proxy Status**: DNS only
   - **TTL**: Auto

### Example DNS Record

```plaintext
Type    Name       Content          Proxy status    TTL
A       jenkins    <external-ip>    DNS only        Auto
```

### Update Your Ingress Resource (If Using Ingress)

If you are using an Ingress controller, you need to update your Ingress resource to reflect the new subdomain.

1. **Edit Ingress Resource**:
   ```yaml
   apiVersion: networking.k8s.io/v1
   kind: Ingress
   metadata:
     name: jenkins-ingress
     namespace: jenkins
   spec:
     rules:
       - host: jenkins.gm-nig-ltd.tech
         http:
           paths:
             - path: /
               pathType: Prefix
               backend:
                 service:
                   name: jenkins
                   port:
                     number: 8080
   ```
2. **Apply Ingress Resource**:
   ```sh
   kubectl apply -f jenkins-ingress.yaml
   ```

### Verify Access

After updating the DNS records and Ingress resource, you should be able to access your Jenkins instance via the public URL:

```plaintext
http://jenkins.gm-nig-ltd.tech
```

If you encounter any issues or need further assistance, feel free to ask!
It looks like your Jenkins instance is refusing to connect. Here are a few steps you can take to troubleshoot and resolve the issue:

### 1. Check Jenkins Service Status

Ensure that the Jenkins service is running correctly in your Kubernetes cluster:

```sh
kubectl get pods -n jenkins
```

Look for the Jenkins pod and check its status. If it's not running, you may need to investigate the pod logs:

```sh
kubectl logs <jenkins-pod-name> -n jenkins
```

### 2. Verify Service Configuration

Ensure that the Jenkins service is correctly configured as a `LoadBalancer`:

```sh
kubectl get svc -n jenkins
```

Make sure the `jenkins` service has an `EXTERNAL-IP` assigned. If it shows `<pending>`, wait a few moments and check again.

### 3. Check Firewall and Security Groups

Ensure that your firewall and security groups allow traffic on the port Jenkins is using (e.g., 8080). If you're using a cloud provider, make sure the security group associated with your nodes allows inbound traffic on the required port.

```hcl
  ingress_rule {
    label      = "http"
    protocol   = "tcp"
    port_range = "80"
    cidr       = ["0.0.0.0/0"]
    action     = "allow"
  }


  # for jenkins
  ingress_rule {
    label      = "jenkins"
    protocol   = "tcp"
    port_range = "8080"
    cidr       = ["0.0.0.0/0"]
    action     = "allow"
  }
```

### 4. Verify DNS Configuration

Ensure that your DNS configuration is correct and points to the external IP of your Jenkins service. You can use tools like `nslookup` or `dig` to verify DNS resolution:

```sh
nslookup jenkins.gm-nig-ltd.tech
```

### 5. Check Ingress Configuration (If Using Ingress)

If you're using an Ingress controller, ensure that the Ingress resource is correctly configured and points to the Jenkins service:

```sh
kubectl get ingress -n jenkins
```

Check the Ingress rules and ensure they match your DNS configuration.

### 6. Restart Jenkins Service

Sometimes, simply restarting the Jenkins service can resolve connectivity issues:

```sh
kubectl rollout restart deployment jenkins -n jenkins
```

### 7. Review Logs and Events

Check the logs and events for any errors or warnings that might indicate the cause of the issue:

```sh
kubectl describe svc jenkins -n jenkins
kubectl describe pod <jenkins-pod-name> -n jenkins
```

By following these steps, you should be able to identify and resolve the issue preventing your Jenkins instance from connecting. If you need further assistance, feel free to ask!

Source: Conversation with Copilot, 03/08/2024
(1) linux - Jenkins refused to connect on port 8080 - Stack Overflow. https://stackoverflow.com/questions/44858275/jenkins-refused-to-connect-on-port-8080.
(2) jenkins localhost:8080 is not reached "localhost refused to connect .... https://stackoverflow.com/questions/72750678/jenkins-localhost8080-is-not-reached-localhost-refused-to-connect.
(3) linux - Unable to access Jenkins (Centos 7) - Server Fault. https://serverfault.com/questions/871597/unable-to-access-jenkins-centos-7.
(4) undefined. http://github.com/jenkinsci/jenkins/commit/2fb288474e980d0e7ff9c4a3b768874835a3e92e.
(5) en.wikipedia.org. https://en.wikipedia.org/wiki/Jenkins_(software).
