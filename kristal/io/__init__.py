"""Main file of kristal.io package."""
from pkg_resources import resource_filename
import lark
from kristal.io.transform import CIFTransformer

GRAMMAR_PATH = 'io/cifgrammar.lark'

def read_cif(cif_path, transformer=None):
    """Read content of given CIF file.

    :param cif_path: path of the CIF file to be read. Can be given
     as a `str` object or `pathlib.Path` object.
    :type cif_path: `str` or `pathlib.Path`
    :param transformer: an optional transformer object that will be used to
     transformer the parsed tree. It not given, a default transformer will be used.
    :type transformer: a subclass of `lark.Transformer`.
    :returns: a mapping name -> datablock holding information read from
     all datablocks present in CIF file.
    :rtype: A mapping `str` -> :py:class:`kristal.io.transform.DataBlock`.
     The `DataBlock` objects have the following attributes:
     - name: name of the datablock
     - entries: non-loop dataitems
     - loop: list of all loops

     The non-loop dataitems are stored as :py:class:`pandas.Series` (can be
     accessed like a dictionary). The loops are stored as :py:class:`pandas.DataFrame`.
    """
    if transformer is None:
        transformer = CIFTransformer()

    with open(resource_filename('kristal', GRAMMAR_PATH)) as grammar_file:
        grammar = grammar_file.read()

    with open(cif_path) as cif:
        content = cif.read()

    parser = lark.Lark(grammar, parser='earley', start='cif')
    tree = parser.parse(content)
    return transformer.transform(tree)
