import numpy as np

def unpack_dict(input_dict, ):
    # Keys and their lists
    keys = list(input_dict.keys())
    values = [input_dict[k] for k in keys]

    # Ensure all lists are same length
    n = len(values[0])
    if not all(len(v) == n for v in values):
        raise ValueError("All dictionary value lists must have the same length")

    # Prepare a dict of unpacked lists for each key
    unpacked = {k: [] for k in keys}

    # Iterate over all entries in parallel
    for i in range(n):
        entry_items = {k: input_dict[k][i] for k in keys}

        # Detect if any value is a range string (like '3:7' or '3:10:2')
        # and use its length as the expansion length
        main_len = None
        if any(isinstance(v, str) and ":" in v for v in entry_items.values()):
            # Pick the first such range to determine the expansion count
            for v in entry_items.values():
                if isinstance(v, str) and ":" in v:
                    parts = [int(x) for x in v.split(":")]
                    range_vals = list(range(*parts))
                    main_len = len(range_vals)
                    break
        elif any(isinstance(v, (list, tuple)) for v in entry_items.values()):
            for v in entry_items.values():
                if isinstance(v, (list, tuple)):
                    main_len = len(v)
                    break
        else:
            main_len = 1

        # Now expand all keys based on that length
        for k, v in entry_items.items():
            if isinstance(v, str) and ":" in v:
                parts = [int(x) for x in v.split(":")]
                unpacked[k].extend(range(*parts))
            elif isinstance(v, (list, tuple)):
                unpacked[k].extend(v)
            else:
                unpacked[k].extend([v] * main_len)

    return unpacked

def edge_length(nodes):
    """
    nodes: array of shape (..., 2, 3)
       nodes[...,0,:] = first node of edge
       nodes[...,1,:] = second node of edge

    Returns:
        lengths: array of shape (...)
    """

    p0 = nodes[..., 0, :]
    p1 = nodes[..., 1, :]

    diff = p1 - p0

    return np.linalg.norm(diff, axis=-1)

def tri_area(nodes):
    """
    nodes: shape (..., 3, 3)
        For each triangle:
        nodes[i, j] = [x_j, y_j, z_j] for j = 0,1,2

    Returns:
        areas: shape (...,)
        Area of each triangle.
    """

    p0 = nodes[..., 0, :]
    p1 = nodes[..., 1, :]
    p2 = nodes[..., 2, :]

    # Edge vectors
    v1 = p1 - p0
    v2 = p2 - p0

    # Cross product of edges
    cross_prod = np.cross(v1, v2)

    # Triangle area = 0.5 * norm of cross product
    area = 0.5 * np.linalg.norm(cross_prod, axis=-1)

    return area