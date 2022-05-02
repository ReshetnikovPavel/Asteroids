def check_collision(outer, inner):
    out_pos = outer.position
    in_pos = inner.position
    center_x = out_pos.x <= in_pos.x <= out_pos.x + outer.width
    edge_x = out_pos.x <= in_pos.x + inner.width <= out_pos.x + outer.width
    center_y = out_pos.y <= in_pos.y <= out_pos.y + outer.height
    edge_y = out_pos.y <= in_pos.y + inner.height <= out_pos.y + outer.height
    return (center_x or edge_x) and (center_y or edge_y)
