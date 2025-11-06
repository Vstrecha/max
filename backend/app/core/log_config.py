import json
import logging


class CustomFormatter(logging.Formatter):
    """Custom formatter that handles extra fields for structured logging."""

    def format(self, record: logging.LogRecord) -> str:
        # Create base log entry
        log_entry = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        # Add extra fields if present
        if hasattr(record, "request_id"):
            log_entry["request_id"] = record.request_id
        if hasattr(record, "method"):
            log_entry["method"] = record.method
        if hasattr(record, "url"):
            log_entry["url"] = record.url
        if hasattr(record, "path"):
            log_entry["path"] = record.path
        if hasattr(record, "query"):
            log_entry["query"] = record.query
        if hasattr(record, "client_ip"):
            log_entry["client_ip"] = record.client_ip
        if hasattr(record, "user_agent"):
            log_entry["user_agent"] = record.user_agent
        if hasattr(record, "user_id"):
            log_entry["user_id"] = record.user_id
        if hasattr(record, "status_code"):
            log_entry["status_code"] = record.status_code
        if hasattr(record, "process_time"):
            log_entry["process_time"] = record.process_time
        if hasattr(record, "content_length"):
            log_entry["content_length"] = record.content_length
        if hasattr(record, "body_preview"):
            log_entry["body_preview"] = record.body_preview
        if hasattr(record, "body_error"):
            log_entry["body_error"] = record.body_error
        if hasattr(record, "error"):
            log_entry["error"] = record.error

        return json.dumps(log_entry, ensure_ascii=False)


def setup_logging():
    if not logging.getLogger().handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(CustomFormatter())
        logging.getLogger().addHandler(handler)
        logging.getLogger().setLevel(logging.INFO)


logger = logging.getLogger(__name__)
