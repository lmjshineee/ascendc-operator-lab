"""L09: sequential CPU integration; no hardware overlap is simulated."""

def tiled_add(x, y, cores, tile, partition):
    """Use partition(n, cores, tile); copy slices in, add, copy out.

    Follow exercise 01 finite/equal-length input contract, preserve inputs.
    """
    raise NotImplementedError('TODO L09: implement tiled add')


def row_softmax(rows, cores, rows_per_tile, partition):
    """Partition whole rows, compute stable softmax within each full row.

    Reject ragged/empty rows/nonfinite values; [] returns [].
    """
    raise NotImplementedError('TODO L09: implement row-partitioned softmax')
