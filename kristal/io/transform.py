"""Features related to transformation of CIF grammer tree."""
from collections import namedtuple
from itertools import islice
import lark
import pandas as pd

DataBlock = namedtuple('DataBlock', ['name', 'loops', 'entries'])


class CIFTransformer(lark.Transformer):
    """Lark Transformer for CIF grammar tree."""
    # pylint: disable=no-self-use

    def cif(self, matches):
        """Transformation of cif nonterminal."""
        return {block.name: block for block in matches}

    def datablock(self, matches):
        """Transformation of datablock nonterminal."""
        loops = []
        entries_data = []
        entries_index = []
        name = str(matches[0])
        for match in islice(matches, 1, len(matches)):
            if match.data == 'loop':
                loops.append(match.children[0])
            else:
                entries_data.append(match.children[1])
                entries_index.append(match.children[0])
        entries = pd.Series(entries_data, index=entries_index)
        return DataBlock(name, loops, entries)

    def datablock_heading(self, matches):
        """Transform datablock heading."""
        return str(matches[0])

    def loop(self, matches):
        """Transform loop into pandas.DataFrame."""
        columns = matches[0].children
        if (len(matches[1].children)) % len(columns):
            raise ValueError('Invalid number of items in loop {}'.format(columns))
        data = list(zip(*(len(columns) * [iter(matches[1].children)])))
        loop_df = pd.DataFrame(data, columns=columns)
        return lark.Tree('loop', [loop_df])

    def integer(self, matches):
        """Transform integer."""
        return int(matches[0])

    def float(self, matches):
        """Transform float."""
        return float(matches[0])

    def string(self, matches):
        """Transform string."""
        return str(matches[0])

    def tag(self, matches):
        """Transform tag."""
        return str(matches[0])
