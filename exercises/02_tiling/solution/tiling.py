"""Logical coverage model only; SDK alignment and UB policy are separate."""

def tiles(n, cores, tile):
    if any(type(v) is not int for v in (n, cores, tile)):
        raise ValueError('integer arguments required (bool excluded)')
    if n < 0 or cores < 1 or tile < 1:
        raise ValueError('require n>=0, cores>=1, tile>=1')
    q, r = divmod(n, cores)
    result = []
    for core in range(cores):
        start = core * q + min(core, r)
        end = start + q + (core < r)
        for pos in range(start, end, tile):
            result.append((core, pos, min(pos + tile, end)))
    return result
