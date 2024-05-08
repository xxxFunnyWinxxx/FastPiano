from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_FILE = BASE_DIR / Path("content/music.json").resolve()
COMPILER_FILE = BASE_DIR / Path('compilers/MuseScore-Studio-4.3.0.241231431-x86_64.AppImage').resolve()
PDF_DIR = BASE_DIR / Path('content/pdf').resolve()
DATA_DIR = BASE_DIR / Path('content/data').resolve()
PASSWORD = 'parol'

PURPOSE_OPTS = [
    ('беглость'),
    ('широкая ладонь'),
    ('арпеджио'),
    ('двойные пассажи')
]
"""
Арпеджио
Октавы и широкие интервалы
Быстрые движение
Синхронность рук

"""

LEVEL_OPTS = [
    ('легкий'),
    ('средний'),
    ('сложный')
]