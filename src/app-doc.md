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

********** DOCKER FILE ************
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
kubectl port-forward -n monitoring prometheus-prometheus-kube-prometheus-prometheus-0  9090:9090
