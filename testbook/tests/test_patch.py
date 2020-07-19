from ..testbook import testbook

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
        with pytest.raises(AssertionError), tb.patch(target) as mock_obj:
            mock_obj.assert_called_once()
