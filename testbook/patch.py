from .utils import random_varname
from .translators import PythonTranslator


class patch:
    def __init__(self, tb, target, **kwargs):
        self.tb = tb
        self.target = target
        self.kwargs = kwargs

    def __enter__(self):
        self.patcher = f'_patcher_{random_varname()}'
        self.tb.inject(
            f"""
            from unittest.mock import patch
            {self.patcher} = patch(
                {PythonTranslator.translate(self.target)},
                **{PythonTranslator.translate(self.kwargs)}
            )
            {self.patcher}.start()
        """
        )

    def __exit__(self, *args):
        self.tb.inject(
            f"""
            {self.patcher}.stop()
        """
        )
