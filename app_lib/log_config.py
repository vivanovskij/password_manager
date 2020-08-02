import os

DEBUG = True
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '%(levelname)-8s %(asctime)s - %(name)-16s %(message)s',
            'datefmt': '%Y-%b-%d %H:%M:%S'
        }
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': f'{BASE_DIR}\\app.log',
            'mode': 'w' if DEBUG else 'a',
            'formatter': 'simple',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
            'stream': 'ext://sys.stdout',
        }
    },
    'loggers': {
        'file': {
            'handlers': ['file'],
            'level': 'DEBUG' if DEBUG else 'WARNING',
            'propagate': True
        },
        'console': {
            'handlers': ['console'],
            'level': 'DEBUG',
        }
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG' if DEBUG else 'WARNING'
    }
}
