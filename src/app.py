from flask import Flask, redirect, url_for, request
from web3 import Web3
from apscheduler.schedulers.background import BackgroundScheduler
from prometheus_client import Counter, Histogram, make_wsgi_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from flask_restx import Api, Resource, fields
import logging
import time
import werkzeug.serving


# Initialize Flask application
app = Flask(__name__)

# Initialize Flask-RESTX API
api = Api(app, version='1.0', title='PolygonRPC API', description='API for fetching Polygon block numbers')

# Initialize Prometheus metrics
REQUEST_COUNT = Counter('flask_app_request_count', 'App Request Count', ['method', 'endpoint', 'http_status'])
REQUEST_LATENCY = Histogram('flask_app_request_latency_seconds', 'Request latency', ['method', 'endpoint'], buckets=[0.1, 0.5, 1, 2, 5, 10])

# Initialize PolygonRPC class for interacting with Polygon RPC
class PolygonRPC():
    def __init__(self):
        self.url = 'https://rpc.ankr.com/polygon_zkevm/ec2159070bc430950775b36f11d6a78ae27b75bb79d45965c37b950a587ee000'
        self.web3 = Web3(Web3.HTTPProvider(self.url))
        self.block_number = None
    
    def fetch_block_number(self):
        self.block_number = self.web3.eth.block_number
        logging.info(f"Fetched block number: {self.block_number}")
    
    def get_block_number(self):
        if self.block_number is None:
            self.fetch_block_number()
        return self.block_number

# Create an instance of the PolygonRPC class
polygon_rpc = PolygonRPC()

# RESTX model for response structure
block_model = api.model('Block', {
    'block_number': fields.Integer(description='Polygon block number'),
})

# Flask-RESTX Resource for block number endpoint
@api.route('/block_number')
class BlockNumber(Resource):
    @api.marshal_with(block_model)
    def get(self):
        """Fetch the current Polygon block number."""
        start_time = time.time()
        block_number = polygon_rpc.get_block_number()
        latency = time.time() - start_time
        
        # Log the request details
        request_details = {
            'method': request.method,
            'endpoint': request.path,
            'http_status': 200,  # Assuming successful response
            'latency': latency
        }
        REQUEST_COUNT.labels(request.method, request.path, '200').inc()
        REQUEST_LATENCY.labels(request.method, request.path).observe(latency)
        
        logging.info(f"Request details: {request_details}")
        
        return {'block_number': block_number}

# Flask route for index page redirecting to block_number endpoint
@app.route('/', methods=['GET'])
def index():
    return redirect(url_for('blocknumber'))  # Corrected endpoint

# Background job to fetch block number every 5 minutes
def fetch_block_number_job():
    polygon_rpc.fetch_block_number()

if __name__ == '__main__':
    # Set up logging
    logging.basicConfig(level=logging.INFO)

    # Set up scheduler to fetch block number every 5 minutes
    scheduler = BackgroundScheduler()
    scheduler.add_job(fetch_block_number_job, 'interval', minutes=5)
    scheduler.start()

    # Fetch the block number once at startup
    fetch_block_number_job()

    # Run Flask app with Prometheus WSGI middleware for metrics
    # Make sure the server is using app_dispatch with DispatcherMiddleware
    werkzeug.serving.run_simple(
        hostname='0.0.0.0',
        port=5001,
        application=DispatcherMiddleware(app, {'/metrics': make_wsgi_app()}),
        use_debugger=False,
        use_reloader=False
    )