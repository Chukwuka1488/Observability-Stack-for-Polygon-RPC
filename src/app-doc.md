To integrate Prometheus metrics and Flask-RESTPlus for API documentation into your Flask application:

### Modified Flask Application with Prometheus Metrics and Flask-RESTPlus

1. **Adding Prometheus Metrics**:

   - We'll integrate Prometheus metrics using `prometheus_client` to monitor request counts and latencies.

2. **Integrating Flask-RESTPlus**:
   - Flask-RESTPlus will be used for API documentation, providing automatic Swagger UI generation.

### Explanation:

- **Prometheus Metrics**:

  - Metrics are defined using `Counter` for counting requests (`flask_app_request_count`) and `Histogram` for measuring request latency (`flask_app_request_latency_seconds`).
  - These metrics are incremented and observed within middleware functions (`before_request` and `after_request`).

- **Flask-RESTx Integration**:

  - A `block_model` is defined using Flask-RESTx `api.model` for defining the structure of the response.
  - A Flask-RESTx `Resource` class `BlockNumber` is used to define the `/block_number` endpoint, which fetches and returns the current Polygon block number.

- **Scheduler and Logging**:

  - A background scheduler (`BackgroundScheduler`) is used to fetch the block number every 5 minutes.
  - Logging is configured (`logging.basicConfig`) to log informational messages, such as fetched block numbers.

- **Running the Application**:
  - The application is run with Prometheus WSGI middleware (`DispatcherMiddleware`) to serve Prometheus metrics on `/metrics`.

This setup provides a robust Flask application with integrated Prometheus metrics and Flask-RESTPlus for API documentation, suitable for monitoring and documenting your Polygon RPC interactions effectively. Adjust the `block_model` and endpoint logic as per your specific API requirements.

\***\*\*\*\*\*** DOCKER FILE \***\*\*\*\*\*\*\***

### Explanation:

- **WORKDIR**: Sets the working directory for subsequent instructions to `/app`, where your application code will reside inside the container.

- **COPY**: Copies all files from the current directory (`.`) to the `/app` directory inside the container.

- **RUN pip install**: Installs all dependencies listed in `requirements.txt` using pip.

- **EXPOSE**: Exposes port 5001 on the container, allowing external access.

- **ENV FLASK_APP**: Sets the Flask application entry point to `src.app`. This assumes that your Flask application object (`app`) is defined in `src/app.py`.

- **CMD**: Specifies the command to run when the container starts. In this case, Gunicorn is used to serve the Flask application (`src.app:app`) and bind it to `0.0.0.0:5001`, making it accessible externally.

Ensure that your directory structure and naming conventions match what is specified in the Dockerfile (`src/app.py` for the Flask application file). This Dockerfile should build and run your Flask application effectively inside a Docker container.

export KUBECONFIG=/Users/simplymenah/Downloads/SRE/Observability-Stack-for-Polygon-RPC/terraform/civo-sre-cluster-kubeconfig
kubectl config get-contexts
alias k=kubectl

- port forward prometheus

kubectl get pods -n monitoring
kubectl port-forward -n monitoring prometheus-prometheus-kube-prometheus-prometheus-0 9090:9090

helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm search repo prometheus-community/kube-prometheus-stack
helm upgrade prometheus prometheus-community/kube-prometheus-stack -n monitoring -f values.yml

Combining the Blackbox Exporter with your existing ServiceMonitor can provide a comprehensive monitoring solution that covers both internal and external perspectives of your service's health and performance. Here's why and how you can combine them:
A blackbox exporter can be useful in this context to perform synthetic monitoring, which involves externally probing your microservice to ensure it is reachable and performing correctly from an external perspective. Here are a few reasons why you might need a blackbox exporter:

1. Availability Monitoring
   The blackbox exporter can perform HTTP checks to verify that your endpoints are accessible. This ensures that your service is not only running but also reachable and responsive to end-user requests.

2. Latency Measurements
   While your internal metrics give you insights into request latencies from within the service, a blackbox exporter can measure the end-to-end latency experienced by users. This helps in identifying network-related issues that might not be visible from internal metrics alone.

3. Health Check
   It can serve as an additional layer of health checks, complementing internal health checks provided by the application. By simulating user requests, it ensures that your service's critical endpoints are functioning as expected.

4. Alerting on Downtime
   Using the blackbox exporter, you can configure Prometheus to alert you if your service becomes unreachable. This is especially important for detecting and responding to outages promptly.

5. Service Level Objectives (SLOs) and Service Level Agreements (SLAs)
   If you have defined SLOs or SLAs for availability and response times, the blackbox exporter can provide the data necessary to measure and report on these objectives.

6. Dependency Monitoring
   If your service depends on external services or APIs, the blackbox exporter can monitor these dependencies to ensure they are available and performing as expected.

A Blackbox Exporter in the context of your microservice monitoring setup would be useful for several reasons:

1. External Monitoring of Service Availability
   The Blackbox Exporter allows you to perform end-to-end monitoring of your service from an external perspective, ensuring that it is accessible and functioning correctly from outside the cluster. This type of monitoring checks not just the internal health but the actual ability of clients to interact with your service.

2. HTTP and HTTPS Probing
   You can use the Blackbox Exporter to probe your Flask application's HTTP endpoints. This helps in monitoring the availability and performance of the specific endpoints like /block_number and /metrics. It can verify that these endpoints are reachable and responding as expected.

3. Latency and Response Time Monitoring
   While your current setup monitors internal request latency, the Blackbox Exporter can measure the latency from an external client's perspective. This gives a holistic view of the user experience by measuring the response time from outside the cluster.

4. Comprehensive Alerting
   Using the Blackbox Exporter, you can set up alerts based on the availability and performance of your endpoints. For example, you can configure Prometheus to alert you if an endpoint becomes unreachable or if response times exceed a certain threshold.

5. Multi-Protocol Support
   Besides HTTP/HTTPS, the Blackbox Exporter can also monitor other protocols such as ICMP, DNS, TCP, and more. This flexibility can be beneficial if your service expands to include other types of endpoints in the future.

### Why Combine Blackbox Exporter with ServiceMonitor?

1. **Internal Metrics**: ServiceMonitor collects metrics exposed by your application, such as request counts, latencies, and error rates.
2. **External Probes**: Blackbox Exporter performs end-to-end checks from an external perspective, ensuring the service is reachable and performing well from outside the cluster.
3. **Holistic Monitoring**: Combining both methods gives a complete view of your service's health, helping to identify issues that might not be visible from internal metrics alone (e.g., network issues).

### How to Combine Them

Here’s a step-by-step guide to combine the Blackbox Exporter with your existing ServiceMonitor setup:

1. **Deploy Blackbox Exporter**:
   Ensure Blackbox Exporter is deployed as previously described.

2. **Update ServiceMonitor for Internal Metrics**:
   Ensure you have a `ServiceMonitor` that targets your Python service to collect internal metrics.

3. **Update Prometheus Configuration**:
   Configure Prometheus to scrape both internal metrics (via ServiceMonitor) and external probes (via Blackbox Exporter).

4. **Define Alert Rules for Both Metrics**:
   Create Prometheus alert rules that consider both internal metrics and external probe results.

### Step-by-Step Implementation

#### Step 1: Deploy Blackbox Exporter

(As previously described)

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: blackbox-exporter
  namespace: monitoring
  labels:
    app: blackbox-exporter
spec:
  replicas: 1
  selector:
    matchLabels:
      app: blackbox-exporter
  template:
    metadata:
      labels:
        app: blackbox-exporter
    spec:
      containers:
        - name: blackbox-exporter
          image: prom/blackbox-exporter:latest
          ports:
            - containerPort: 9115
          volumeMounts:
            - name: config
              mountPath: /etc/blackbox_exporter
              subPath: blackbox.yml
      volumes:
        - name: config
          configMap:
            name: blackbox-exporter-config
---
apiVersion: v1
kind: Service
metadata:
  name: blackbox-exporter
  namespace: monitoring
  labels:
    app: blackbox-exporter
spec:
  ports:
    - port: 9115
      targetPort: 9115
  selector:
    app: blackbox-exporter
```

#### Step 2: Create or Update ServiceMonitor for Internal Metrics

```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: polygon-rpc-app-monitor
  labels:
    release: prometheus
    app: prometheus
spec:
  selector:
    matchLabels:
      app: polygon-rpc-app
  endpoints:
    - interval: 30s
      port: http
      path: /metrics
```

#### Step 3: Update Prometheus Configuration

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: prometheus-config
  namespace: monitoring
data:
  prometheus.yml: |
    global:
      scrape_interval: 15s
    scrape_configs:
      # Internal Metrics
      - job_name: 'polygon-rpc-app'
        kubernetes_sd_configs:
          - role: endpoints
        relabel_configs:
          - source_labels: [__meta_kubernetes_namespace, __meta_kubernetes_service_name, __meta_kubernetes_endpoint_port_name]
            action: keep
            regex: default;polygon-rpc-app;http
      # Blackbox Probes
      - job_name: 'blackbox'
        metrics_path: /probe
        params:
          module: [http_2xx]
        static_configs:
          - targets:
              - http://polygon-rpc-app.default.svc.cluster.local/block_number  # Replace with your actual endpoint
        relabel_configs:
          - source_labels: [__address__]
            target_label: __param_target
          - source_labels: [__param_target]
            target_label: instance
          - target_label: __address__
            replacement: blackbox-exporter.monitoring.svc.cluster.local:9115  # Blackbox Exporter service address
```

#### Step 4: Define Alert Rules

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: polygon-rpc-app-rules
  namespace: monitoring
  labels:
    release: prometheus
    prometheus: k8s
    role: alert-rules
spec:
  groups:
    - name: polygon-rpc-app.rules
      rules:
        # Internal Metrics Alerts
        - alert: HighRequestLatency
          expr: histogram_quantile(0.99, sum(rate(flask_app_request_latency_seconds_bucket[5m])) by (le)) > 1
          for: 5m
          labels:
            severity: critical
          annotations:
            summary: "High request latency detected"
            description: "The 99th percentile request latency is above 1 second for more than 5 minutes."
        - alert: HighRequestCount
          expr: sum(rate(flask_app_request_count_total[5m])) by (endpoint, method) > 100
          for: 5m
          labels:
            severity: warning
          annotations:
            summary: "High request count detected"
            description: "The request count has exceeded 100 requests per second for more than 5 minutes."
        # Blackbox Probes Alerts
        - alert: TargetDown
          expr: probe_success == 0
          for: 5m
          labels:
            severity: critical
          annotations:
            summary: "Target {{ $labels.instance }} is down"
            description: "The target {{ $labels.instance }} has been down for more than 5 minutes."
        - alert: HighLatency
          expr: probe_http_duration_seconds{job="blackbox"} > 1
          for: 5m
          labels:
            severity: warning
          annotations:
            summary: "High latency for target {{ $labels.instance }}"
            description: "The target {{ $labels.instance }} has high latency for more than 5 minutes."
```

### Step 5: Apply Configurations

Apply all the configurations to your Kubernetes cluster:

```sh
kubectl apply -f service-monitor.yaml
kubectl apply -f prometheus-configmap.yaml
kubectl apply -f prometheus-rule.yaml
```

### Summary

By combining the Blackbox Exporter with ServiceMonitor, you can monitor both internal application metrics and external endpoint availability/performance. This approach provides a comprehensive view of your service's health and helps in early detection and resolution of issues.

To get the svc.cluster.local endpoint after creating your service in Kubernetes, you need to understand that Kubernetes services are automatically assigned a DNS name in the format service-name.namespace.svc.cluster.local.

To check the monitoring, logging, and alerts for your microservice using Prometheus, Grafana, and related tools, you can follow these steps:

### 1. **Monitoring with Prometheus and Grafana**

#### Access Prometheus

1. **Port Forward Prometheus**:

   ```bash
   kubectl port-forward -n monitoring svc/prometheus-k8s 9090:9090
   ```

   This command forwards your local port 9090 to the Prometheus server.

2. **Open Prometheus**:
   Open your browser and navigate to `http://localhost:9090`. You can explore metrics using the Prometheus UI.

#### Access Grafana

1. **Port Forward Grafana**:

   ```bash
   kubectl port-forward -n monitoring svc/grafana 3000:3000
   ```

   This command forwards your local port 3000 to the Grafana server.

2. **Open Grafana**:
   Open your browser and navigate to `http://localhost:3000`. Log in with the default credentials (usually `admin/admin` unless changed).

3. **Add Prometheus as a Data Source**:

   - Go to Grafana's Configuration > Data Sources > Add data source.
   - Choose Prometheus.
   - Set the URL to `http://prometheus-k8s.monitoring.svc.cluster.local:9090`.
   - Save & Test.

4. **Create Dashboards**:
   - You can either create your own dashboards or import pre-configured ones.
   - Go to the Dashboards section and use `+ New Dashboard` to create a new one.
   - Add panels with relevant metrics, such as `flask_app_request_count_total`, `flask_app_request_latency_seconds`, etc.

### 2. **Logging with Loki and Grafana**

#### Deploy Loki and Promtail (if not already done)

If you haven't deployed Loki and Promtail, you can use Helm:

```bash
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update
helm install loki grafana/loki-stack
```

#### Configure Promtail

Make sure Promtail is configured to scrape logs from your microservice. Here’s a sample configuration:

**promtail-config.yaml**:

```yaml
server:
  http_listen_port: 9080
  grpc_listen_port: 0

positions:
  filename: /tmp/positions.yaml

clients:
  - url: http://loki:3100/loki/api/v1/push

scrape_configs:
  - job_name: kubernetes-pods
    kubernetes_sd_configs:
      - role: pod
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_label_app]
        action: keep
        regex: polygon-rpc-app
      - source_labels: [__meta_kubernetes_pod_uid]
        target_label: __meta_kubernetes_pod_uid
      - replacement: /var/log/pods/*/*/*.log
        target_label: __path__
```

Apply this configuration:

```bash
kubectl apply -f promtail-config.yaml
```

#### Access Logs in Grafana

1. **Add Loki as a Data Source**:

   - In Grafana, go to Configuration > Data Sources > Add data source.
   - Choose Loki.
   - Set the URL to `http://loki.monitoring.svc.cluster.local:3100`.
   - Save & Test.

2. **Explore Logs**:
   - Go to the Explore section in Grafana.
   - Choose Loki as the data source.
   - Use the query `{app="polygon-rpc-app"}` to view logs related to your microservice.

### 3. **Alerts with Prometheus Alertmanager**

#### Configure Alertmanager

Make sure your Alertmanager is configured and running. You can check this by port forwarding and accessing the Alertmanager UI:

```bash
kubectl port-forward -n monitoring svc/alertmanager 9093:9093
```

Open your browser and navigate to `http://localhost:9093` to see the Alertmanager UI.

#### Test Alerts

1. **Trigger an Alert**:
   You can artificially trigger an alert by setting a lower threshold in your PrometheusRule or by simulating high request latency or count.

2. **Check Alerts in Prometheus**:
   Go to Prometheus (`http://localhost:9090`) and navigate to the Alerts section to see active alerts.

3. **Receive Notifications**:
   Ensure that your Alertmanager configuration (`alert.yaml`) has a valid receiver (e.g., webhook, email, Slack). Check the configured endpoint or service for alert notifications.

### Summary

- **Monitoring**: Use Prometheus and Grafana to monitor your microservice’s metrics.
- **Logging**: Use Loki and Promtail to collect and visualize logs in Grafana.
- **Alerts**: Configure Prometheus Alertmanager to handle alerts and send notifications.

By following these steps, you can ensure comprehensive monitoring, logging, and alerting for your microservice, providing a robust observability stack.

### Grafana

helm repo add grafana https://grafana.github.io/helm-charts -n monitoring
helm repo update
helm install grafana grafana/grafana -n monitoring
kubectl get secret --namespace monitoring grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo
kubectl port-forward -n monitoring svc/grafana 3000:80

http://prometheus-kube-prometheus-prometheus.monitoring.svc.cluster.local:9090
