"""CPU mathematical reference, Python float; not a dtype/NPU emulator."""
import math


def add(x, y):
    if len(x) != len(y):
        raise ValueError('shape mismatch: broadcasting is not supported')
    if any(not math.isfinite(v) for seq in (x, y) for v in seq):
        raise ValueError('finite inputs required')
    return [a + b for a, b in zip(x, y)]


def softmax(rows):
    if not rows:
        return []
    cols = len(rows[0])
    if cols == 0 or any(len(row) != cols for row in rows):
        raise ValueError('nonempty rectangular rows required')
    if any(not math.isfinite(v) for row in rows for v in row):
        raise ValueError('finite inputs required')
    output = []
    for row in rows:
        maximum = max(row)
        values = [math.exp(v - maximum) for v in row]
        total = math.fsum(values)
        output.append([v / total for v in values])
    return output
