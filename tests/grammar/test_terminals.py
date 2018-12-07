"""Test cases for grammar terminals."""
import lark
import pytest

@pytest.fixture(scope='session', name='create_term_parser')
def create_term_parser_factory(grammar):
    """Fixture providing parser that allows starting from terminals.

    .. note::
       This is only a hack that allows start from terminals by introducing
       rule equivalent to the given terminal.
    """
    def create_term_parser(start_terminal):
        new_rule = '\n{0} : {1}'.format(start_terminal.lower(), start_terminal)
        return lark.Lark(grammar+new_rule, start=start_terminal.lower())
    return create_term_parser

@pytest.mark.parametrize('terminal,input_str',
                         [['DATA_', 'dAtA_'],
                          ['DATA_', 'data_'],
                          ['DATA_', 'DATA_'],
                          ['UNSIGNEDINTEGER', '300'],
                          ['INTEGER', '2137'],
                          ['INTEGER', '-1'],
                          ['INTEGER', '+600'],
                          ['EXPONENT', 'e1'],
                          ['EXPONENT', 'E-3'],
                          ['EXPONENT', 'E+08'],
                          ['FLOAT', '1e10'],
                          ['FLOAT', '+1E-13'],                          
                          ['FLOAT', '-1E-13'],
                          ['FLOAT', '1.69'],
                          ['FLOAT', '1.23'],
                          ['COMMENTS', '#somecomm3nt\n'],
                          ['COMMENTS', '##### C0MMENT\n'],
                          ['TOKENIZEDCOMMENTS', '\t \n#COMMent\n'],
                          ['TOKENIZEDCOMMENTS', '\n \t# test\n'],
                          ['NOTEOLUNQUOTEDSTRING', 't3st}&-./:<=>?@\\^'],
                          ['EOLUNQUOTEDSTRING', '\nt3st}&-./:<=>?@\\^']] +
                         [['TEXTLEADCHAR', char] for char in  "zdj37UIO\"#$'_ \t[]"] +
                         [['ANYPRINTCHAR', char] for char in "abc123AB\"#$'_ ^\t;[]"])
def test_terminal_correct(create_term_parser, terminal, input_str):
    """All terminals should accept correct input."""
    parser = create_term_parser(start_terminal=terminal)
    assert parser.parse(input_str).children[0] == input_str

@pytest.mark.parametrize('terminal,input_str',
                         [['DATA_', 'data'],
                          ['UNSIGNEDINTEGER', '12O3'],
                          ['COMMENTS', '# comment']])
def test_terminal_incorrect(create_term_parser, terminal, input_str):
    parser = create_term_parser(start_terminal=terminal)    
    with pytest.raises(lark.UnexpectedCharacters):
        parser.parse(input_str)
