"""Invariants and analytical cases, selectable problem/solution modules."""
import copy
import importlib.util
import math
from pathlib import Path
import random
import unittest

ROOT = Path(__file__).resolve().parents[1]
VARIANT = 'problem'


def load(exercise, filename, variant=None):
    path = ROOT / 'exercises' / exercise / (variant or VARIANT) / filename
    spec = importlib.util.spec_from_file_location(f'{exercise}_{variant or VARIANT}', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class GoldenTests(unittest.TestCase):
    def setUp(self):
        self.ops = load('01_golden', 'ops.py')

    def test_add_contract_and_no_mutation(self):
        x, y = [1, -2, 0.5], [2, 4, -0.5]
        self.assertEqual(self.ops.add(x, y), [3, 2, 0])
        self.assertEqual(x, [1, -2, 0.5])
        self.assertEqual(y, [2, 4, -0.5])
        self.assertEqual(self.ops.add([], []), [])

    def test_add_rejects_bad_inputs(self):
        for x, y in [([1], []), ([math.nan], [0]), ([0], [math.inf])]:
            with self.subTest(x=x, y=y), self.assertRaises(ValueError):
                self.ops.add(x, y)

    def test_softmax_analytical(self):
        got = self.ops.softmax([[0, math.log(2), math.log(3)]])[0]
        for actual, expected in zip(got, [1/6, 2/6, 3/6]):
            self.assertAlmostEqual(actual, expected, places=12)
        self.assertEqual(self.ops.softmax([[8], [-9]]), [[1], [1]])

    def test_softmax_stability_translation_and_no_mutation(self):
        original = [[0, 1, 2], [-4, -4, -4]]
        saved = copy.deepcopy(original)
        base = self.ops.softmax(original)
        large = self.ops.softmax([[1000, 1001, 1002]])[0]
        self.assertEqual(original, saved)
        for a, b in zip(base[0], large):
            self.assertAlmostEqual(a, b, places=12)
        for row in base:
            self.assertTrue(all(math.isfinite(v) and v >= 0 for v in row))
            self.assertAlmostEqual(math.fsum(row), 1, places=12)

    def test_softmax_shape_and_nonfinite(self):
        self.assertEqual(self.ops.softmax([]), [])
        for rows in [[[]], [[1], [1, 2]], [[math.inf]], [[math.nan]]]:
            with self.subTest(rows=rows), self.assertRaises(ValueError):
                self.ops.softmax(rows)


class TilingTests(unittest.TestCase):
    def setUp(self):
        self.tiles = load('02_tiling', 'tiling.py').tiles

    def check_invariants(self, n, cores, tile):
        counts, loads, positions = [0] * n, [0] * cores, []
        for core, start, end in self.tiles(n, cores, tile):
            self.assertTrue(0 <= core < cores)
            self.assertTrue(0 <= start < end <= n)
            self.assertLessEqual(end - start, tile)
            loads[core] += end - start
            positions.append(start)
            for i in range(start, end):
                counts[i] += 1
        self.assertEqual(counts, [1] * n)
        self.assertEqual(positions, sorted(positions))
        q, r = divmod(n, cores)
        self.assertEqual(loads, [q + (c < r) for c in range(cores)])

    def test_handworked_tail(self):
        self.assertEqual(self.tiles(17, 4, 3), [
            (0, 0, 3), (0, 3, 5), (1, 5, 8), (1, 8, 9),
            (2, 9, 12), (2, 12, 13), (3, 13, 16), (3, 16, 17)])

    def test_boundary_coverage(self):
        for n in [0, 1, 2, 17, 31, 32, 33, 257]:
            for cores in [1, 2, 4, 16]:
                for tile in [1, 3, 16, 256]:
                    with self.subTest(n=n, cores=cores, tile=tile):
                        self.check_invariants(n, cores, tile)

    def test_seeded_coverage(self):
        rng = random.Random(20260917)
        for _ in range(60):
            self.check_invariants(rng.randrange(300), rng.randrange(1, 33), rng.randrange(1, 65))

    def test_invalid_config(self):
        for args in [(-1, 2, 3), (1, 0, 3), (1, 2, 0), (1.0, 2, 3), (True, 2, 3)]:
            with self.subTest(args=args), self.assertRaises(ValueError):
                self.tiles(*args)


class PipelineTests(unittest.TestCase):
    def setUp(self):
        self.pipeline = load('03_pipeline', 'pipeline.py')
        self.partition = load('02_tiling', 'tiling.py', 'solution').tiles
        self.golden = load('01_golden', 'ops.py', 'solution')

    def test_add_against_golden_and_no_mutation(self):
        rng = random.Random(17)
        for n in [0, 1, 17, 33, 257]:
            x, y = [rng.uniform(-2, 2) for _ in range(n)], [rng.uniform(-2, 2) for _ in range(n)]
            saved = copy.deepcopy((x, y))
            for cores, tile in [(1, 1), (4, 3), (32, 16)]:
                self.assertEqual(self.pipeline.tiled_add(x, y, cores, tile, self.partition), self.golden.add(x, y))
            self.assertEqual((x, y), saved)

    def test_add_rejects_invalid(self):
        for x, y in [([1], []), ([math.nan], [0])]:
            with self.assertRaises(ValueError):
                self.pipeline.tiled_add(x, y, 1, 2, self.partition)

    def test_softmax_analytical_row_independence(self):
        rows = [[0, math.log(2), math.log(3)], [1000, 1000, 1000]]
        saved = copy.deepcopy(rows)
        output = self.pipeline.row_softmax(rows, 4, 1, self.partition)
        for actual, expected in zip(output[0], [1/6, 2/6, 3/6]):
            self.assertAlmostEqual(actual, expected, places=12)
        for actual in output[1]:
            self.assertAlmostEqual(actual, 1/3, places=12)
        self.assertEqual(rows, saved)

    def test_softmax_random_shapes_against_golden(self):
        rng = random.Random(19)
        for r, c in [(1, 1), (2, 3), (3, 17), (8, 33)]:
            rows = [[rng.uniform(-1000, 1000) for _ in range(c)] for _ in range(r)]
            expected = self.golden.softmax(rows)
            actual = self.pipeline.row_softmax(rows, 3, 2, self.partition)
            self.assertEqual(len(actual), r)
            for arow, erow in zip(actual, expected):
                self.assertEqual(len(arow), c)
                self.assertAlmostEqual(math.fsum(arow), 1, places=12)
                for a, e in zip(arow, erow):
                    self.assertAlmostEqual(a, e, places=12)

    def test_empty_and_rejections(self):
        self.assertEqual(self.pipeline.row_softmax([], 2, 3, self.partition), [])
        for rows in [[[]], [[1], [1, 2]], [[math.inf]]]:
            with self.assertRaises(ValueError):
                self.pipeline.row_softmax(rows, 2, 3, self.partition)


def suite(stage, variant):
    global VARIANT
    VARIANT = variant
    classes = {'01': GoldenTests, '02': TilingTests, '03': PipelineTests}
    selected = classes.values() if stage == 'all' else [classes[stage]]
    return unittest.TestSuite(unittest.defaultTestLoader.loadTestsFromTestCase(c) for c in selected)
