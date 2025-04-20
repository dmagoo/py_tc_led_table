def convert_flat_to_pointy(flat_rows):
    total_diagonals = sum(len(row) for row in flat_rows)
    num_rows = len(flat_rows)
    num_diagonals = num_rows * 2 - 1  # e.g., 7 → 13

    # Create empty target structure
    diagonals = [[] for _ in range(num_diagonals)]

    for row_index, row in enumerate(flat_rows):
        offset = row_index  # shift right with each lower row
        for i, val in enumerate(row):
            diagonals[i + offset].append(val)

    return diagonals


def get_row_grouped_node_ids(api, ring_count, scan_axis='r', reverse=False):
    if scan_axis not in ('q', 'r', 's'):
        raise ValueError("scan_axis must be 'q', 'r', or 's'")

    # Build all valid cube coordinates in a hex with center (0,0,0)
    coords = []
    for q in range(-ring_count + 1, ring_count):
        for r in range(-ring_count + 1, ring_count):
            s = -q - r
            if abs(s) < ring_count:
                coords.append((q, r, s))

    # Compute group key for each cube coordinate
    cube_with_ids = []
    for q, r, s in coords:
        if scan_axis == 'q':
            key = q
        elif scan_axis == 'r':
            key = r
        else:  # scan_axis == 's'
            key = s
        node_id = api.getNodeId(api.CubeCoordinate(q, r, s))
        cube_with_ids.append((key, q, r, node_id))  # use q/r for left-right sorting

    # Sort: top-down (by key descending), then left to right (by q then r)
    cube_with_ids.sort(key=lambda t: (-t[0], t[1], t[2]))

    # Group by key
    rows = []
    current_key = None
    current_row = []
    for key, q, r, node_id in cube_with_ids:
        if key != current_key:
            if current_row:
                rows.append(current_row)
            current_row = [node_id]
            current_key = key
        else:
            current_row.append(node_id)
    if current_row:
        rows.append(current_row)

    if reverse:
        rows.reverse()

    return rows

