from ._version import version as __version__
from .testbook import testbook

import warnings
warnings.warn("'nteract-testbook' package has been renamed to `testbook`. No new releases are going out for this old package name.", FutureWarning)
