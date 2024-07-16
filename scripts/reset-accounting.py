def reset_acct(env):
    """
    Reset ALL account moves (journal entries). Also deletes all attachments (e.g. files) on account moves.

    Args:
        env (_type_): _description_
    """
    moves = env["account.move"].search([])

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
