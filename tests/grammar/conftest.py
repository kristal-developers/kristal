"""Common functionallities for grammar tests."""
from pkg_resources import resource_filename
import lark
import pytest

GRAMMAR_PATH = 'io/cifgrammar.lark'

@pytest.fixture(scope='session', name='grammar')
def read_grammar():
    """Fixture providing grammar of CIF file."""
    with open(resource_filename('kristal', GRAMMAR_PATH)) as grammar_file:
        yield grammar_file.read()

@pytest.fixture(scope='session', name='create_parser')
def create_lark_parser_factory(grammar):
    """Fixture providing Lark parser factory."""
    def create_parser(start_rule):
        return lark.Lark(grammar, start=start_rule)
    return create_parser
