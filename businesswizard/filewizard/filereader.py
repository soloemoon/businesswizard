import os
import pandas as pd

from abc import ABC, abstractmethod
from typing import Dict, Any

class ReadHandler(ABC):
    '''
    Base class for reading tabular flat files

    Attributes
    ----------
    nxt: ReadHandler
        Next handler to pass input to if unsupported by current handler

    Methods
    -------
    read: pd.DataFrame
        Read contents of file
    '''