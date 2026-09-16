#!/usr/bin/env python3
"""Local study runner. No CANN dependency and no NPU speed claims."""
import argparse
import importlib.util
import json
import math
from pathlib import Path
import random
import sys
import unittest

ROOT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('learning_tests', ROOT / 'tests/test_learning.py')
learning = importlib.util.module_from_spec(spec)
spec.loader.exec_module(learning)


def demo(variant):
    ops = learning.load('01_golden', 'ops.py', variant)
    partition = learning.load('02_tiling', 'tiling.py', variant).tiles
    pipeline = learning.load('03_pipeline', 'pipeline.py', variant)
    cases = json.loads((ROOT / 'configs/cases.json').read_text())
    rng = random.Random(cases['seed'])
    add_cases, softmax_cases = 0, 0
    max_add_error, max_softmax_error = 0.0, 0.0
    for n in [v for v in cases['add_lengths'] if v <= 1024]:
        x, y = [rng.uniform(-3, 3) for _ in range(n)], [rng.uniform(-3, 3) for _ in range(n)]
        actual = pipeline.tiled_add(x, y, 4, 17, partition)
        expected = ops.add(x, y)
        if len(actual) != len(expected):
            raise AssertionError('Add output length mismatch')
        for a, e in zip(actual, expected):
            if not math.isfinite(a) or not math.isclose(a, e, rel_tol=1e-12, abs_tol=1e-12):
                raise AssertionError('Add mismatch')
            max_add_error = max(max_add_error, abs(a-e))
        add_cases += 1
    for r, c in [s for s in cases['softmax_shapes'] if s[0]*s[1] <= 264]:
        rows = [[rng.uniform(-1000, 1000) for _ in range(c)] for _ in range(r)]
        actual = pipeline.row_softmax(rows, 4, 2, partition)
        expected = ops.softmax(rows)
        if len(actual) != r:
            raise AssertionError('Softmax row count mismatch')
        for arow, erow in zip(actual, expected):
            if len(arow) != c or not math.isclose(math.fsum(arow), 1, abs_tol=1e-12):
                raise AssertionError('Softmax shape or row sum mismatch')
            for a, e in zip(arow, erow):
                if not math.isfinite(a) or a < 0 or not math.isclose(a, e, rel_tol=1e-12, abs_tol=1e-12):
                    raise AssertionError('Softmax mismatch')
                max_softmax_error = max(max_softmax_error, abs(a-e))
        softmax_cases += 1
    print(json.dumps({'scope':'CPU mathematical integration only', 'variant':variant,
                     'seed':cases['seed'], 'add_cases':add_cases, 'softmax_cases':softmax_cases,
                     'max_add_abs_error':max_add_error, 'max_softmax_abs_error':max_softmax_error,
                     'status':'passed', 'npu_validated':False}, indent=2))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    test = sub.add_parser('test')
    test.add_argument('stage', choices=['01', '02', '03', 'all'])
    test.add_argument('--solution', action='store_true', help='use reference answers')
    demo_parser = sub.add_parser('demo')
    demo_parser.add_argument('--solution', action='store_true')
    args = parser.parse_args()
    variant = 'solution' if args.solution else 'problem'
    if args.command == 'test':
        print(f'Local tests, variant={variant}; not an NPU validation.', flush=True)
        result = unittest.TextTestRunner(verbosity=2, failfast=(variant == 'problem')).run(
            learning.suite(args.stage, variant))
        return 0 if result.wasSuccessful() else 1
    try:
        demo(variant)
    except NotImplementedError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
