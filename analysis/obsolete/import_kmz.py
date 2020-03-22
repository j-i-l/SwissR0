__author__ = 'Jonas I Liechti'

from zipfile import ZipFile
from pykml import parser

zf = ZipFile('Data/gg25_v2.kmz', 'r')
for fn in zf.namelist():
    if fn.endswith('.kml'):

        with open('Data/cantons.kml', 'r') as f:
            doc = parser.parse(f)
            root = doc.getroot()