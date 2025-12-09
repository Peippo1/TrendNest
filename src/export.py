import logging
from opentelemetry import trace

logger = logging.getLogger(__name__)
tracer = trace.get_tracer(__name__)


def export_to_csv(df, path):
    with tracer.start_as_current_span("export_to_csv", attributes={"path": path}):
        df.to_csv(path, index=False)
        logger.info("Data exported to %s", path)
