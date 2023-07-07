#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

def main():
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))

    # realpath() trae la ruta real si en caso apunta a un enlace simbólico
    PATHS = [os.path.realpath(os.path.join(BASE_DIR, "apps")), os.path.realpath(os.path.join(BASE_DIR, "tests"))]
    for path in PATHS:
        sys.path.insert(0, path)

    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()