"""Chart styling keeps feature coordinates and uses accessible dimension keys."""

from io import StringIO
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

import numpy

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import ctda


def contrast_on_white(colour):
    channels = [int(colour[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    channels = [c / 12.92 if c <= .04045 else ((c + .055) / 1.055) ** 2.4
                for c in channels]
    luminance = sum(c * weight for c, weight in
                    zip(channels, (.2126, .7152, .0722)))
    return 1.05 / (luminance + .05)


class AccessiblePlotTests(unittest.TestCase):
    def test_dimension_keys_preserve_numeric_results_and_plot_coordinates(self):
        diagrams = [
            numpy.array([[0., 1.], [0., 2.], [0., 3.], [0., numpy.inf]]),
            numpy.array([[.5, 1.5], [1., 3.]]),
            numpy.array([[1.5, 2.5]]),
        ]
        original = [diagram.copy() for diagram in diagrams]
        scatter = ctda.matplotlib.pyplot.scatter
        plot = ctda.matplotlib.pyplot.plot
        legend = ctda.matplotlib.pyplot.legend
        with patch.object(ctda, 'ripser', return_value={'dgms': diagrams}), \
                patch.object(ctda.matplotlib.pyplot, 'scatter', wraps=scatter) as scatter_calls, \
                patch.object(ctda.matplotlib.pyplot, 'plot', wraps=plot) as plot_calls, \
                patch.object(ctda.matplotlib.pyplot, 'legend', wraps=legend) as legends:
            result = ctda.analyze(StringIO('0,0,0\n1,0,0\n0,1,0\n0,0,1\n'),
                                  'csv', maxdim=2)

        self.assertEqual(result.totald, [0, 1, 2])
        self.assertEqual(result.betti, [
            [0., .5, 1., 1.5, 2., 2.5, 3.],
            [4, 4, 3, 3, 2, 2, 1], [0, 1, 2, 1, 1, 1, 0],
            [0, 0, 0, 1, 1, 0, 0], [4, 3, 1, 3, 2, 1, 1],
        ])
        self.assertEqual(result.stats, [
            [4, 1., 3., 2., 2.], [2, 1., 2., 1.5, 1.5],
            [1, 1., 1., 1., 1.], [2., 4 / 3, 4., 2., 2., 1.5],
        ])
        for expected, actual in zip(original, result.dgms):
            numpy.testing.assert_array_equal(actual, expected)

        calls = scatter_calls.call_args_list
        self.assertEqual(len(calls), 3)
        self.assertEqual(len({call.kwargs['marker'] for call in calls}), 3)
        for expected, call in zip(original, calls):
            numpy.testing.assert_array_equal(call.args[0], expected[:, 0])
            numpy.testing.assert_array_equal(call.args[1], expected[:, 1])
            self.assertGreaterEqual(contrast_on_white(call.kwargs['color']), 3)

        # The first plotted line is the unchanged diagonal reference line.
        bars = plot_calls.call_args_list[1:]
        self.assertEqual(len(bars), 7)
        self.assertEqual(len({bar.kwargs['linestyle'] for bar in bars}), 3)
        expected_bars = [(0., numpy.inf), (0., 3.), (0., 2.), (0., 1.),
                         (1., 3.), (.5, 1.5), (1.5, 2.5)]
        for step, (expected, bar) in enumerate(zip(expected_bars, bars)):
            self.assertEqual(bar.args[0], expected)
            self.assertEqual(bar.args[1], (step, step))

        self.assertEqual(legends.call_args_list[0].args[0], [0, 1, 2])
        handles = legends.call_args_list[1].kwargs['handles']
        self.assertEqual([handle.get_label() for handle in handles], ['0', '1', '2'])
        for handle, bar in zip(handles, (bars[0], bars[4], bars[6])):
            self.assertIsInstance(handle, ctda.matplotlib.lines.Line2D)
            self.assertEqual(handle.get_color(), bar.kwargs['color'])
            expected = ctda.matplotlib.lines.Line2D([], [], linestyle=bar.kwargs['linestyle'])
            self.assertEqual(handle.get_linestyle(), expected.get_linestyle())


if __name__ == '__main__':
    unittest.main()
