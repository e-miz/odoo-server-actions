def reset_acct(env):
    """
    Reset ALL account moves (journal entries). Also deletes all attachments (e.g. files) on account moves.

    Must un-reconcile all account moves first.


    Args:
        env (_type_): _description_
    """
    moves = env["account.move"].search([])

    for move in moves:
        move["state"] = "draft"

        atts = move.attachment_ids

        for att in atts:
            att.unlink()

        move.unlink()


reset_acct(env)
