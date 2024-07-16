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


reset_pos(env)
