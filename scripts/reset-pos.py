def reset_pos(env):
    """
    Reset all sessions, orders, and payments.

    Must manually enable delete privilege in pos.session access rights.

    Args:
        env (_type_): _description_
    """
    sessions = env["pos.session"].search([])

    for session in sessions:
        orders = session.order_ids

        for order in orders:
            order["state"] = "draft"

            payments = order.payment_ids

            for payment in payments:
                payment.unlink()

            order.unlink()
        session.unlink()

    # Uncomment to delete combo line items
    # These don't seem to unlink properly when combos are deleted
    # combo_lines = env["pos.combo.line"].search([])
    #
    # for combo_line in combo_lines:
    #    combo_line.unlink()


reset_pos(env)
