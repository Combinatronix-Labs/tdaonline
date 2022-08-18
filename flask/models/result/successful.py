from io import BytesIO
from numpy import ndarray
import pickle
import base64
from typing import Any, List
from ..result import Result
import json


class SuccessfulResult(Result):
    """Use SuccessfulResult when no issues were found when processing the input data through ctda"""

    def isError(self):
        return False

    def __init__(
        self,
        diagram: str,
        barcode: str,
        betti: List[List[int]],
        stats: List[List[int]],
        dgms: List[ndarray],
        totald: List
    ) -> None:
        super().__init__()
        self.diagram = diagram
        self.barcode = barcode
        self.betti = betti
        self.stats = stats
        self.dgms = dgms
        self.totald = totald

    def toJSON(self) -> str:
        return json.dumps({
            'diagram': self.diagram,
            'barcode': self.barcode,
            'betti': self.betti,
            'stats': self.stats,
            'raw': pickle.dumps(self.dgms).decode('latin-1'),
            'dim': pickle.dumps(self.totald).decode('latin-1'),
        })

    @staticmethod
    def fromJson(encoded: str):
        decoded = json.loads(encoded)
        return SuccessfulResult(
            decoded['diagram'],
            decoded['barcode'],
            decoded['betti'],
            decoded['stats'],
            pickle.loads(decoded['raw'].encode('latin-1')),
            pickle.loads(decoded['dim'].encode('latin-1')),
        )
