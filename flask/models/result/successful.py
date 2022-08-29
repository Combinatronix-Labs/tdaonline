from io import BytesIO
from numpy import ndarray, savetxt, load, genfromtxt
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
        totald: List[int]
    ) -> None:
        super().__init__()
        self.diagram = diagram
        self.barcode = barcode
        self.betti = betti
        self.stats = stats
        self.dgms = dgms
        self.totald = totald

    def toJSON(self) -> str:
        raw = []
        for a in self.dgms:
            memfile = BytesIO()
            savetxt(memfile, a)
            raw.append(memfile.getvalue().decode('latin-1'))

        return json.dumps({
            'diagram': self.diagram,
            'barcode': self.barcode,
            'betti': self.betti,
            'stats': self.stats,
            'raw': raw,
            'dim': self.totald,
        })

    @staticmethod
    def fromJson(encoded: str):
        decoded = json.loads(encoded)
        dgms = []
        for a in decoded['raw']:
            memfile = BytesIO()
            memfile.write(a.encode('latin-1'))
            memfile.seek(0)
            # dgms.append(load(file=memfile, encoding='latin1', mmap_mode='r'))
            dgms.append(genfromtxt(memfile))
        return SuccessfulResult(
            diagram=decoded['diagram'],
            barcode=decoded['barcode'],
            betti=decoded['betti'],
            stats=decoded['stats'],
            dgms=dgms,
            totald=decoded['dim'],
        )
