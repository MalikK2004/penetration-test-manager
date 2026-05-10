import time
from flask import request

class MetricsCollector:
    def __init__(self):
        self.request_count = 0
        self.error_count = 0
        self.total_latency = 0.0

    def record_request(self, latency, is_error=False):
        self.request_count += 1
        self.total_latency += latency
        if is_error:
            self.error_count += 1

    def get_metrics(self):
        avg_latency = self.total_latency / self.request_count if self.request_count > 0 else 0
        return {
            "total_requests": self.request_count,
            "total_errors": self.error_count,
            "average_latency_ms": round(avg_latency * 1000, 2)
        }

metrics_collector = MetricsCollector()

def metrics_middleware(app):
    @app.before_request
    def start_timer():
        request.start_time = time.time()

    @app.after_request
    def record_metrics(response):
        if hasattr(request, 'start_time'):
            latency = time.time() - request.start_time
            is_error = response.status_code >= 400
            metrics_collector.record_request(latency, is_error)
        return response
