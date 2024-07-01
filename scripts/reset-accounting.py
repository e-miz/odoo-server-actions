def reset_acct(env):
    """
    Reset ALL account moves (journal entries).

    Must un-reconcile all account moves first.

    Args:
        env (_type_): _description_
    """
    moves = env["account.move"].search([])

    for move in moves:
        move["state"] = "draft"

        move.unlink()


reset_acct(env)
