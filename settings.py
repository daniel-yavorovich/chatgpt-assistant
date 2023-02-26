import os

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

try:
    import local_settings
except ImportError:
    pass
