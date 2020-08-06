from ..testbook import testbook
from ..exceptions import TestbookRuntimeError

import pytest


@pytest.fixture(scope='module')
def tb():
    with testbook('testbook/tests/resources/patch.ipynb', execute=True) as tb:
        yield tb


class TestPatch:
    @pytest.mark.parametrize(
        "target, func", [("os.listdir", "listdir"), ("os.popen", "get_branch")]
    )
    def test_patch_basic(self, target, func, tb):
        with tb.patch(target) as mock_obj:
            tb.ref(func)()
            mock_obj.assert_called_once()

    @pytest.mark.parametrize(
        "target, func", [("os.listdir", "listdir"), ("os.popen", "get_branch")]
    )
    def test_patch_raises_error(self, target, func, tb):
        with pytest.raises(TestbookRuntimeError), tb.patch(target) as mock_obj:
            mock_obj.assert_called_once()

    def test_patch_return_value(self, tb):
        with tb.patch("os.listdir", return_value=['file1', 'file2']) as mock_listdir:
            assert tb.ref("listdir")() == ['file1', 'file2']
            mock_listdir.assert_called_once()


class TestPatchDict:
    @pytest.mark.parametrize(
        "in_dict, values", [("os.environ", {"PATH": "/usr/bin"})],
    )
    def test_patch_dict(self, in_dict, values, tb):
        with tb.patch_dict(in_dict, values, clear=True):
            assert tb.ref(in_dict) == values
