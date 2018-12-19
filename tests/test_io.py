"""Test cases for kristal.io package."""
from lark import Token, Tree
import pandas as pd
import pytest
from kristal.io import read_cif, GRAMMAR
from kristal.io.transform import CIFTransformer

@pytest.fixture(name='transformer', scope='session')
def create_transformer():
    """Create default transformer for use with tests."""
    return CIFTransformer()

@pytest.fixture(name='lark')
def patch_lark(mocker):
    """Replace lark module in kristal.io with mock object."""
    return mocker.patch('kristal.io.lark')

@pytest.fixture(name='mock_open')
def patch_mock_open(mocker):
    """Replace open function in kristal.io module."""
    return mocker.patch('kristal.io.open', mocker.mock_open(read_data='test_content'))

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
    """CIFTransformer.loop should transform correct loop into DataFrame."""
    header_tree = Tree('loop_header', ['x', 'y', 'label'])
    body_tree = Tree('loop_body', [1.2, 2.0, 'a', -3.1, -2.8, 'b'])
    expected_df = pd.DataFrame(
        [[1.2, 2.0, 'a'], [-3.1, -2.8, 'b']],
        columns=['x', 'y', 'label'])
    actual_tree = transformer.loop([header_tree, body_tree])
    assert actual_tree.data == 'loop'
    assert actual_tree.children[0].equals(expected_df)

def test_loop_raises_on_incorrect_input(transformer):
    """CIFTransformer.loop functoin should raise ValueError on incorrect input.

    Criterion for the input to be invalid is that number of elements in
    loop_body is not divisible by number of elements in header.
    """
    header_tree = Tree('loop_header', ['a', 'b', 'c'])
    body_tree = Tree('loop_body', [1, 5, 5, 6, 2])

    with pytest.raises(ValueError) as exc_info:
        transformer.loop([header_tree, body_tree])

    assert 'Invalid number of items in loop' in str(exc_info.value)

@pytest.mark.usefixtures('mock_open')
def test_read_cif_uses_lark(lark, mocker):
    """The read_cif function should correctly create Lark instance."""
    read_cif('BENZEN01.cif', transformer=mocker.Mock())
    lark.Lark.assert_called_once_with(GRAMMAR, parser='earley', start='cif')

@pytest.mark.usefixtures('lark')
def test_read_cif_opens_file(mocker, mock_open):
    """The read_cif function should open file passed as parameter."""
    read_cif('BENZEN01.cif', transformer=mocker.Mock())
    mock_open.assert_called_once_with('BENZEN01.cif')

@pytest.mark.usefixtures('mock_open')
def test_read_cif_parses_content(lark, mocker):
    """The read_cif function use Lark to parse content read from input file."""
    read_cif('BENZEN01.cif', transformer=mocker.Mock())
    lark.Lark().parse.assert_called_once_with('test_content')

@pytest.mark.usefixtures('mock_open')
def test_read_cif_returns_transformed_tree(lark, mocker):
    """The read_cif function should return transformed tree."""
    transformer = mocker.Mock()
    result = read_cif('BENZEN01.cif', transformer=transformer)
    transformer.transform.assert_called_once_with(lark.Lark().parse())
    assert result == transformer.transform()
