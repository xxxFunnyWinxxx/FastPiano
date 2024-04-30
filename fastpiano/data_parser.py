from music21 import corpus

import logging

logger = logging.getLogger(__name__)
logging.basicConfig()
logger.setLevel(logging.DEBUG)

def get_data(name):
    corpus.parse('bwv66.6')