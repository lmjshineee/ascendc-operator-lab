"""Sequential slice-copy demonstration, not NPU code or a timing model."""
import math


def tiled_add(x, y, cores, tile, partition):
    if len(x) != len(y):
        raise ValueError('shape mismatch')
    if any(not math.isfinite(v) for seq in (x, y) for v in seq):
        raise ValueError('finite inputs required')
    output = [None] * len(x)
    for _core, start, end in partition(len(x), cores, tile):
        local_x, local_y = x[start:end], y[start:end]  # CopyIn model
        local_z = [a + b for a, b in zip(local_x, local_y)]
        output[start:end] = local_z  # CopyOut model
    return output


def row_softmax(rows, cores, rows_per_tile, partition):
    chunks = partition(len(rows), cores, rows_per_tile)
    if not rows:
        return []
    cols = len(rows[0])
    if cols == 0 or any(len(row) != cols for row in rows):
        raise ValueError('nonempty rectangular rows required')
    if any(not math.isfinite(v) for row in rows for v in row):
        raise ValueError('finite inputs required')
    output = [None] * len(rows)
    for _core, start, end in chunks:
        local_rows = [list(row) for row in rows[start:end]]
        local_output = []
        for row in local_rows:
            maximum = max(row)
            exp_values = [math.exp(v - maximum) for v in row]
            total = math.fsum(exp_values)
            local_output.append([v / total for v in exp_values])
        output[start:end] = local_output
    return output
