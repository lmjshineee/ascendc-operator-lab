"""L05: partition logical work items; no NPU alignment is modeled."""

def tiles(n, cores, tile):
    """Return list of (core_id, start, end), half-open valid ranges.

    n>=0, cores>=1, tile>=1: integers excluding bool; otherwise ValueError.
    Split n by quotient/remainder across cores, then tile each core range.
    Empty cores produce no entries. n=0 returns [].
    """
    raise NotImplementedError('TODO L05: implement balanced core/tile ranges')
