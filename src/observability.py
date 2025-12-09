import logging
import os
from typing import Dict, Optional

from opentelemetry import metrics, trace
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.resources import Resource, SERVICE_NAME
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter, SimpleSpanProcessor


def setup_logging(log_level: str | None = None) -> None:
    """
    Configure application-wide logging.
    LOG_LEVEL can be overridden via environment variable.
    """
    level = (log_level or os.getenv("LOG_LEVEL", "INFO")).upper()
    logging.basicConfig(
        level=getattr(logging, level, logging.INFO),
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
    )


def _parse_headers(raw_headers: Optional[str]) -> Optional[Dict[str, str]]:
    if not raw_headers:
        return None
    headers: Dict[str, str] = {}
    for item in raw_headers.split(","):
        if "=" in item:
            key, value = item.split("=", 1)
            headers[key.strip()] = value.strip()
    return headers or None


def setup_tracing(service_name: str = "trendnest") -> trace.Tracer:
    """
    Initialize OpenTelemetry tracing.
    - If OTEL_EXPORTER_OTLP_ENDPOINT is set, spans are sent to that collector.
    - Otherwise, spans are logged to stdout via ConsoleSpanExporter.
    """
    provider = TracerProvider(
        resource=Resource.create(
            {
                SERVICE_NAME: service_name,
                "service.namespace": "trendnest",
                "deployment.environment": os.getenv("ENVIRONMENT", "dev"),
                "service.version": os.getenv("SERVICE_VERSION", "local"),
            }
        )
    )
    trace.set_tracer_provider(provider)

    endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT")
    headers = _parse_headers(os.getenv("OTEL_EXPORTER_OTLP_HEADERS"))

    if endpoint:
        exporter = OTLPSpanExporter(endpoint=endpoint, headers=headers)
        processor = BatchSpanProcessor(exporter)
    else:
        exporter = ConsoleSpanExporter()
        processor = SimpleSpanProcessor(exporter)

    provider.add_span_processor(processor)

    # Instrument outbound HTTP requests (used by yfinance/requests).
    RequestsInstrumentor().instrument()

    return trace.get_tracer(service_name)


def setup_metrics(service_name: str = "trendnest"):
    """
    Initialize OpenTelemetry metrics.
    If no OTLP endpoint is configured, metrics will not be exported (but meter is still usable).
    """
    endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT")
    headers = _parse_headers(os.getenv("OTEL_EXPORTER_OTLP_HEADERS"))

    resource = Resource.create(
        {
            SERVICE_NAME: service_name,
            "service.namespace": "trendnest",
            "deployment.environment": os.getenv("ENVIRONMENT", "dev"),
        }
    )

    metric_readers = []
    if endpoint:
        exporter = OTLPMetricExporter(endpoint=endpoint, headers=headers)
        metric_readers.append(PeriodicExportingMetricReader(exporter))

    provider = MeterProvider(resource=resource, metric_readers=metric_readers or None)
    metrics.set_meter_provider(provider)
    return metrics.get_meter(service_name)
