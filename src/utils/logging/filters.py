import logging


class SuppressDeprecated(logging.Filter):
    def filter(self, record):
        WARNINGS_TO_SUPPRESS = ["RemovedInDjango18Warning", "RemovedInDjango19Warning"]
        # Return false to suppress message.
        return not any([warn in record.getMessage() for warn in WARNINGS_TO_SUPPRESS])
