import pytest

def pytest_addoption(parser):
    """Добавляем опцию командной строки для выбора языка"""
    parser.addoption(
        '--language',
        action='store',
        default='en',
        help='Choose language: --language=es or --language=en etc.'
    )
