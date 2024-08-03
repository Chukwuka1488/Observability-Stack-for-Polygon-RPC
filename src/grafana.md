To create dashboards in Grafana for monitoring the metrics collected by Prometheus through the listed ServiceMonitors, follow these steps:

### Step 1: Access Grafana

1. **Port Forward Grafana**:

   ```bash
   kubectl port-forward -n monitoring svc/grafana 3000:3000
   ```

   This forwards your local port 3000 to the Grafana server.

2. **Open Grafana**:
   Open your browser and navigate to `http://localhost:3000`. Log in with the default credentials (usually `admin/admin` unless changed).

### Step 2: Add Prometheus as a Data Source

1. **Go to Configuration**:

   - Click on the gear icon (Configuration) in the left sidebar.
   - Select **Data Sources**.

2. **Add Data Source**:

   - Click on **Add data source**.
   - Select **Prometheus** from the list.

3. **Configure Data Source**:
   - Set the **URL** to `http://prometheus-k8s.monitoring.svc.cluster.local:9090`.
   - Click **Save & Test** to ensure the data source is working.

### Step 3: Create Dashboards for Each Metric

#### General Steps to Create a Dashboard

1. **Create a New Dashboard**:

   - Click on the **+** icon (Create) in the left sidebar.
   - Select **Dashboard**.
   - Click **Add new panel**.

2. **Configure the Panel**:

   - In the **Query** section, select the Prometheus data source.
   - Enter your PromQL query in the **Query** field.
   - Configure the visualization options as needed.

3. **Save the Dashboard**:
   - Click on the **Save** icon at the top of the page.
   - Give your dashboard a name and save it.

#### Specific Metrics and Queries

1. **ServiceMonitor Status**:

   - **Query**: `up{job="kube-prometheus"}` (Adjust `job` label as per your Prometheus configuration)
   - **Visualization**: Stat or Table
   - **Steps**:
     - Add new panel.
     - Set the query to `up{job="kube-prometheus"}`.
     - Choose Stat or Table visualization.
     - Save the panel.

2. **Polygon RPC App Metrics**:

   - **Request Count**:

     - **Query**: `sum(rate(flask_app_request_count_total[5m]))`
     - **Visualization**: Graph or Stat
     - **Steps**:
       - Add new panel.
       - Set the query to `sum(rate(flask_app_request_count_total[5m]))`.
       - Choose Graph or Stat visualization.
       - Save the panel.

   - **Request Latency**:
     - **Query**: `histogram_quantile(0.99, sum(rate(flask_app_request_latency_seconds_bucket[5m])) by (le))`
     - **Visualization**: Graph
     - **Steps**:
       - Add new panel.
       - Set the query to `histogram_quantile(0.99, sum(rate(flask_app_request_latency_seconds_bucket[5m])) by (le))`.
       - Choose Graph visualization.
       - Save the panel.

3. **Alertmanager Metrics**:

   - **Query**: `ALERTS`
   - **Visualization**: Table or Alert List
   - **Steps**:
     - Add new panel.
     - Set the query to `ALERTS`.
     - Choose Table or Alert List visualization.
     - Save the panel.

4. **Kubernetes Components Metrics**:

   - **API Server**:

     - **Query**: `up{job="apiserver"}`
     - **Visualization**: Stat or Graph
     - **Steps**:
       - Add new panel.
       - Set the query to `up{job="apiserver"}`.
       - Choose Stat or Graph visualization.
       - Save the panel.

   - **CoreDNS**:

     - **Query**: `up{job="coredns"}`
     - **Visualization**: Stat or Graph
     - **Steps**:
       - Add new panel.
       - Set the query to `up{job="coredns"}`.
       - Choose Stat or Graph visualization.
       - Save the panel.

   - **Kubelet**:

     - **Query**: `up{job="kubelet"}`
     - **Visualization**: Stat or Graph
     - **Steps**:
       - Add new panel.
       - Set the query to `up{job="kubelet"}`.
       - Choose Stat or Graph visualization.
       - Save the panel.

   - **Kube State Metrics**:

     - **Query**: `up{job="kube-state-metrics"}`
     - **Visualization**: Stat or Graph
     - **Steps**:
       - Add new panel.
       - Set the query to `up{job="kube-state-metrics"}`.
       - Choose Stat or Graph visualization.
       - Save the panel.

   - **Node Exporter**:
     - **Query**: `up{job="node-exporter"}`
     - **Visualization**: Stat or Graph
     - **Steps**:
       - Add new panel.
       - Set the query to `up{job="node-exporter"}`.
       - Choose Stat or Graph visualization.
       - Save the panel.

### Step 4: Configure Alerts in Grafana

1. **Go to Alerts**:

   - Click on the **Alerting** icon (bell) in the left sidebar.
   - Select **Notification channels**.

2. **Add Notification Channel**:

   - Click **Add channel**.
   - Configure the notification settings (e.g., email, Slack).

3. **Create Alert Rules**:
   - Go back to your dashboard.
   - Click on a panel you want to add an alert to.
   - Click on the **Alert** tab.
   - Define your alert condition.
   - Set up the notification channel.

### Summary

- **ServiceMonitor Status**: Use `up` metric queries.
- **Application Metrics**: Use specific PromQL queries for request count and latency.
- **Kubernetes Components**: Use `up` metric queries for API server, CoreDNS, Kubelet, etc.
- **Alerts**: Configure alert rules and notification channels in Grafana.

By following these steps, you can create comprehensive dashboards in Grafana to monitor the health and performance of your microservice and related Kubernetes components.

To see metrics for the Blackbox Exporter in Grafana, you need to ensure that the Blackbox Exporter is properly deployed and that Prometheus is configured to scrape its metrics. Here’s a step-by-step guide to achieve this and then create a dashboard in Grafana to visualize the Blackbox Exporter metrics.

### Step 1: Deploy and Configure Blackbox Exporter

If you haven’t already deployed the Blackbox Exporter, follow these steps:

1. **Deploy Blackbox Exporter**:

**blackbox-exporter-deployment.yaml**:

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
```

**blackbox-exporter-service.yaml**:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: blackbox-exporter
  namespace: monitoring
  labels:
    app: blackbox-exporter
spec:
  ports:
    - name: http
      port: 9115
      targetPort: 9115
  selector:
    app: blackbox-exporter
  type: ClusterIP
```

Apply these configurations:

```bash
kubectl apply -f blackbox-exporter-deployment.yaml
kubectl apply -f blackbox-exporter-service.yaml
```

### Step 2: Configure Prometheus to Scrape Blackbox Exporter

1. **Create a ConfigMap for Prometheus Additional Scrape Configs**:

**prometheus-config-bbe.yaml**:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: prometheus-additional-configs
  namespace: monitoring
data:
  prometheus-additional.yaml: |
    scrape_configs:
      - job_name: 'blackbox'
        metrics_path: /probe
        params:
          module: [http_2xx]
        static_configs:
          - targets:
            - http://polygon-rpc-app.default.svc.cluster.local:5001/block_number
        relabel_configs:
          - source_labels: [__address__]
            target_label: __param_target
          - target_label: instance
            replacement: blackbox-exporter
          - source_labels: [__param_target]
            target_label: __address__
            replacement: blackbox-exporter:9115
```

Apply this ConfigMap:

```bash
kubectl apply -f prometheus-config-bbe.yaml
```

2. **Reference the ConfigMap in Prometheus CRD**:

**prometheus-crd.yaml**:

```yaml
apiVersion: monitoring.coreos.com/v1
kind: Prometheus
metadata:
  name: prometheus
  namespace: monitoring
spec:
  serviceAccountName: prometheus
  serviceMonitorSelector: {}
  podMonitorSelector: {}
  additionalScrapeConfigs:
    name: prometheus-additional-configs
    key: prometheus-additional.yaml
  alerting:
    alertmanagers:
      - namespace: monitoring
        name: alertmanager
        port: web
```

Apply this configuration:

```bash
kubectl apply -f prometheus-crd.yaml
```

### Step 3: Create Grafana Dashboard for Blackbox Exporter Metrics

1. **Access Grafana**:

   - Open your browser and navigate to `http://localhost:3000`.
   - Log in with your credentials.

2. **Add Prometheus as a Data Source**:

   - Go to Configuration (gear icon) > Data Sources.
   - Click on Add data source.
   - Choose Prometheus.
   - Set the URL to `http://prometheus-k8s.monitoring.svc.cluster.local:9090`.
   - Click Save & Test.

3. **Create a Dashboard**:

   - Click on the + icon (Create) in the left sidebar.
   - Select Dashboard.
   - Click on Add new panel.

4. **Configure Panel for Blackbox Exporter Metrics**:

   - **Query for Probe Success**:

     - Query: `probe_success`
     - Visualization: Graph or Stat
     - Steps:
       - Set the query to `probe_success`.
       - Choose Graph or Stat visualization.
       - Save the panel.

   - **Query for Probe Duration**:

     - Query: `probe_duration_seconds`
     - Visualization: Graph
     - Steps:
       - Set the query to `probe_duration_seconds`.
       - Choose Graph visualization.
       - Save the panel.

   - **Query for Probe HTTP Status Codes**:
     - Query: `probe_http_status_code`
     - Visualization: Table
     - Steps:
       - Set the query to `probe_http_status_code`.
       - Choose Table visualization.
       - Save the panel.

5. **Save the Dashboard**:
   - Click on the Save icon at the top of the page.
   - Give your dashboard a name and save it.

### Step 4: Configure Alerts (Optional)

1. **Create Alert Rules**:

   - Go to the Dashboard you created.
   - Click on a panel you want to add an alert to.
   - Click on the Alert tab.
   - Define your alert condition (e.g., if `probe_success` is 0).
   - Set up the notification channel.

2. **Configure Notification Channels**:
   - Click on the Alerting icon (bell) in the left sidebar.
   - Select Notification channels.
   - Click Add channel.
   - Configure the notification settings (e.g., email, Slack).

By following these steps, you can create a comprehensive dashboard in Grafana to monitor the Blackbox Exporter metrics and visualize the health and performance of your microservice and related endpoints.
