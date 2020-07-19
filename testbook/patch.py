from .utils import random_varname
from .translators import PythonTranslator
from .reference import TestbookObjectReference


class patch:
    def __init__(self, tb, target, **kwargs):
        self.tb = tb
        self.target = target
        self.kwargs = kwargs

    def __enter__(self):
        self.mock_object = f'_mock_{random_varname()}'
        self.patcher = f'_patcher_{random_varname()}'
        self.tb.inject(
            f"""
            from unittest.mock import patch
            {self.patcher} = patch(
                {PythonTranslator.translate(self.target)},
                **{PythonTranslator.translate(self.kwargs)}
            )
            {self.mock_object} = {self.patcher}.start()
        """
        )
        return TestbookObjectReference(self.tb, self.mock_object)

    def __exit__(self, *args):
        self.tb.inject(
            f"""
            {self.patcher}.stop()
        """
        )
