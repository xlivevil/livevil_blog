import logging


class MissingVariableErrorFilter(logging.Filter):
    """
    Take log messages from Django for missing template variables and turn them
    into exceptions.
    """

    ignored_prefixes = (
        'admin/',
        'debug_toolbar/',
    )

    def filter(self, record):
        if record.msg.startswith('Exception while resolving variable '):
            variable_name, template_name = record.args
            if not template_name.startswith(self.ignored_prefixes):
                record.level = logging.ERROR
                return True
        return False
