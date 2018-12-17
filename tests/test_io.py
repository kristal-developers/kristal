"""Test cases for kristal.io package."""
from lark import Token, Tree
import pandas as pd
import pytest
from kristal.io import read_cif, GRAMMAR
from kristal.io.transform import CIFTransformer

@pytest.fixture(name='transformer', scope='session')
def transformer_factory():
    return CIFTransformer()

@pytest.fixture(name='lark')
def patch_lark(mocker):
    return mocker.patch('kristal.io.lark')

@pytest.fixture(name='mock_transformer')
def create_mock_transformer(mocker):
    return mocker.Mock()

@pytest.fixture(name='mock_open')
def create_mock_open(mocker):
    return mocker.patch('kristal.io.open', mocker.mock_open())

def test_string_transform(transformer):
    """CIFTransformer should correctly transform string terminals."""
    assert transformer.string([Token('NON_BLANK_STRING', 'Bozon')]) == 'Bozon'

@pytest.mark.parametrize(
    'float_str,expected',
    [['21.37', 21.37],
     ['2.1e-2', 0.021],
     ['-5e3', -5000],
     ['-0.3', -0.3]])
def test_float_transform(transformer, float_str, expected):
    """CIFTransformer should correctly transform float terminals."""
    assert transformer.float([Token('FLOAT', float_str)]) == expected

def test_loop_transform_correct_input(transformer):
    header_tree = Tree('loop_header', ['x', 'y', 'label'])
    body_tree = Tree('loop_body', [1.2, 2.0, 'a', -3.1, -2.8, 'b'])
    expected_df = pd.DataFrame(
        [[1.2, 2.0, 'a'], [-3.1, -2.8, 'b']],
        columns=['x', 'y', 'label'])
    actual_tree = transformer.loop([header_tree, body_tree])
    assert actual_tree.data == 'loop'
    assert actual_tree.children[0].equals(expected_df)

def test_loop_raises_on_incorrect_input(transformer):
    header_tree = Tree('loop_header', ['a', 'b', 'c'])
    body_tree = Tree('loop_body', [1, 5, 5, 6, 2])

    with pytest.raises(ValueError) as exc_info:
        transformer.loop([header_tree, body_tree])

    assert 'Invalid number of items in loop' in str(exc_info.value)

def test_read_cif_uses_lark(lark, mock_transformer, mock_open):
    """Lark instance should be created with correct parameters."""
    read_cif('BENZEN01.cif', transformer=mock_transformer)
    lark.Lark.assert_called_once_with(GRAMMAR, parser='earley', start='cif')
