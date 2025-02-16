-- public.report_pos_order source

CREATE OR REPLACE VIEW public.report_pos_order
AS WITH payment_method_by_order_line AS (
         SELECT pol.id AS pos_order_line_id,
            pm_1.pos_order_id,
            (array_agg(pm_1.payment_method_id))[1] AS payment_method_id
           FROM pos_order_line pol
             LEFT JOIN pos_order po ON po.id = pol.order_id
             LEFT JOIN pos_payment pm_1 ON pm_1.pos_order_id = po.id
          GROUP BY pol.id, pm_1.pos_order_id
        ), first_pos_category AS (
         SELECT pt_1.id AS product_template_id,
            (array_agg(pc.id))[1] AS id
           FROM product_template pt_1
             LEFT JOIN pos_category_product_template_rel pcpt ON pt_1.id = pcpt.product_template_id
             LEFT JOIN pos_category pc ON pcpt.pos_category_id = pc.id
          GROUP BY pt_1.id
        )
 SELECT l.id,
    1 AS nbr_lines,
    s.date_order AS date,
    round(l.price_subtotal /
        CASE COALESCE(s.currency_rate, 0::numeric)
            WHEN 0 THEN 1.0
            ELSE s.currency_rate
        END, cu.decimal_places) AS price_subtotal_excl,
    l.qty AS product_qty,
    l.qty * l.price_unit / COALESCE(NULLIF(s.currency_rate, 0::numeric), 1.0) AS price_sub_total,
    round(l.price_subtotal_incl / COALESCE(NULLIF(s.currency_rate, 0::numeric), 1.0), cu.decimal_places) AS price_total,
    l.qty * l.price_unit * (l.discount / 100::numeric) / COALESCE(NULLIF(s.currency_rate, 0::numeric), 1.0) AS total_discount,
        CASE
            WHEN (l.qty * u.factor) = 0::numeric THEN NULL::numeric
            ELSE l.qty * l.price_unit / COALESCE(NULLIF(s.currency_rate, 0::numeric), 1.0) / (l.qty * u.factor)
        END AS average_price,
    to_char(date_trunc('day'::text, s.date_order) - date_trunc('day'::text, s.create_date), 'DD'::text)::integer AS delay_validation,
    s.id AS order_id,
    s.partner_id,
    s.state,
    s.user_id,
    s.company_id,
    s.sale_journal AS journal_id,
    l.product_id,
    pt.categ_id AS product_categ_id,
    p.product_tmpl_id,
    ps.config_id,
    s.pricelist_id,
    s.session_id,
    s.account_move IS NOT NULL AS invoiced,
    l.price_subtotal - COALESCE(l.total_cost, 0::numeric) / COALESCE(NULLIF(s.currency_rate, 0::numeric), 1.0) AS margin,
    pm.payment_method_id,
    fpc.id AS pos_categ_id,
    s.employee_id
   FROM pos_order_line l
     JOIN pos_order s ON s.id = l.order_id
     LEFT JOIN product_product p ON l.product_id = p.id
     LEFT JOIN product_template pt ON p.product_tmpl_id = pt.id
     LEFT JOIN uom_uom u ON u.id = pt.uom_id
     LEFT JOIN pos_session ps ON s.session_id = ps.id
     LEFT JOIN res_company co ON s.company_id = co.id
     LEFT JOIN res_currency cu ON co.currency_id = cu.id
     LEFT JOIN payment_method_by_order_line pm ON pm.pos_order_line_id = l.id
     LEFT JOIN pos_payment_method ppm ON pm.payment_method_id = ppm.id
     LEFT JOIN first_pos_category fpc ON pt.id = fpc.product_template_id;