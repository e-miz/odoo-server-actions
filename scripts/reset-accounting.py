def reset_acct(env):
    """
    Reset ALL account moves (journal entries). Also deletes all attachments (e.g. files) on account moves.

    Args:
        env (_type_): _description_
    """
    moves = env["account.move"].search([])

    # Delete ALL XML attachments across the database
    # This bypasses the EDI check which is hardcoded in Python
    #sql = "DELETE FROM ir_attachment WHERE name ILIKE '%.xml%'"
    
    #env.cr.execute(sql)

    for move in moves:
        move["state"] = "draft"

        atts = move.attachment_ids

        # delete attached files
        for att in atts:
            att.unlink()

        lines = move.line_ids

        for line in lines:
            line.remove_move_reconcile()

        move.unlink()


reset_acct(env)
