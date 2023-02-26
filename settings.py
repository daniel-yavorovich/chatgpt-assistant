import os

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
LANG = os.environ.get('LANG', 'en-US')

try:
    from local_settings import *
except ImportError:
    pass
