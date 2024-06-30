def reset_inv(env):
    """
    Delete ALL Inventory movement history.

    Args:
        env (_type_): _description_
    """
    pickings = env["stock.picking"].search([])

    # Pickings and associated moves need to be in draft state to delete
    for picking in pickings:
        moves = picking.move_ids
        move_lines = picking.move_line_ids

        # Update the states of each move
        for move in moves:
            move["state"] = "draft"
        for ml in move_lines:
            ml["state"] = "draft"
        picking["state"] = "draft"

        # Deleting the picking will delete associated moves
        picking.unlink()

    # Not all move lines come from pickings
    for ml in env["stock.move.line"].search([]):
        ml["state"] = "draft"
        ml.unlink()

    # clear reserved quantities from past orders
    for quant in env["stock.quant"].search([]):
        quant["reserved_quantity"] = 0


reset_inv(env)
