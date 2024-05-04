from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_FILE = BASE_DIR / Path("content/music.json").resolve()
COMPILER_FILE = BASE_DIR / Path('compilers/MuseScore-4.2.1.240230938-x86_64.AppImage').resolve()
#IMAGES_DIR = Path('../content/images').resolve()
PDF_DIR = BASE_DIR / Path('content/pdf').resolve()
DATA_DIR = BASE_DIR / Path('content/data').resolve()


PURPOSE_OPTS = [
    ('fast', 'беглость'),
    ('octaves', 'октавные движения')
]
"""
Арпеджио
Октавы и широкие интервалы
Быстрые движение
Синхронность рук

"""

LEVEL_OPTS = [
    ('easy', 'легкий'),
    ('medium', 'средний'),
    ('hard', 'сложный')
]

SOURCE_OPTS = [
    ('data', 'data'),
    ('pdf', 'pdf')
]