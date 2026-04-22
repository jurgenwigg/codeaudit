from codeaudit.filehelpfunctions import collect_python_source_files
from pytest import mark
from unittest.mock import patch

_EXCLUDE_DIRS = {"docs", "docker", "dist", "tests"}
_EXAMPLE_DIR = 'example_dir'

@mark.xfail(reason="'dirs' in the 'collect_python_source_files' is not used.")
@mark.parametrize("directory", _EXCLUDE_DIRS)
def test_excluded_dirs(directory):
    with patch("codeaudit.filehelpfunctions.os", autospec=True) as mocked_os:
        mocked_os.walk.return_value = [('.', [directory], ['example.py'])]
        result = collect_python_source_files(directory=directory)
        assert result == []

def test_not_file():
    with patch("codeaudit.filehelpfunctions.os", autospec=True) as mocked_os:
        mocked_os.walk.return_value = [('.', [_EXAMPLE_DIR], ['example.py'])]
        mocked_os.path.isfile.return_value = False
        result = collect_python_source_files(directory=_EXAMPLE_DIR)
        assert result == []

def test_not_ast_parsable():
    with patch("codeaudit.filehelpfunctions.os", autospec=True) as mocked_os, patch('codeaudit.filehelpfunctions.is_ast_parsable', autospec=True) as mocked_is_ast:
        mocked_os.walk.return_value = [('.', [_EXAMPLE_DIR], ['example.py'])]
        mocked_os.path.isfile.return_value = True
        mocked_is_ast.return_value = False
        result = collect_python_source_files(directory=_EXAMPLE_DIR)
        assert result == []

def test_proper_python_file():
    with patch("codeaudit.filehelpfunctions.os", autospec=True) as mocked_os, patch('codeaudit.filehelpfunctions.is_ast_parsable', autospec=True) as mocked_is_ast:
        mocked_os.walk.return_value = [('.', [_EXAMPLE_DIR], ['example.py'])]
        mocked_os.path.isfile.return_value = True
        mocked_os.path.abspath.return_value = './example.py'
        mocked_is_ast.return_value = True
        result = collect_python_source_files(directory=_EXAMPLE_DIR)
        assert result == ['./example.py']
