import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import types
from pathlib import Path

# Dummy pandas module
pandas = types.ModuleType('pandas')

class DummyDataFrame(list):
    def __init__(self, data=None, columns=None):
        super().__init__(data or [])
        self.columns = columns
        self.empty = not bool(data)

    def to_csv(self, *args, **kwargs):
        pass

pandas.DataFrame = DummyDataFrame
sys.modules['pandas'] = pandas

# Dummy pdfplumber module
pdfplumber = types.ModuleType('pdfplumber')

class DummyPage:
    def __init__(self, text: str):
        self._text = text

    def extract_text(self):
        return self._text

class DummyPDF:
    def __init__(self, pages):
        self.pages = pages

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        pass

def dummy_open(path):
    text = "001 Salario base        30,00 2.228,35 2.228,35 0,00"
    return DummyPDF([DummyPage(text)])

pdfplumber.open = dummy_open
sys.modules['pdfplumber'] = pdfplumber

import extract_nomina as en


def test_parse_nomina_returns_dataframe(monkeypatch):
    df = en.parse_nomina(Path('dummy.pdf'))
    assert isinstance(df, pandas.DataFrame)
    assert not df.empty
    assert df.columns == [
        'concepto',
        'unidades',
        'base',
        'devengo',
        'deduccion',
    ]


def test_number_conversion_handles_comma_decimal():
    assert en.parse_number('2.173,52') == 2173.52


def test_parse_number_returns_none_for_invalid():
    assert en.parse_number('invalid') is None


def test_downloads_path_exists(monkeypatch):
    monkeypatch.delenv('USERPROFILE', raising=False)
    path = en.detect_downloads()
    assert path.exists()
