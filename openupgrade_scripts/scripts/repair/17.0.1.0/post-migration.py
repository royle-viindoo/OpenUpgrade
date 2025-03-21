# Copyright 2025 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade


def fill_picking_type_for_warehouse(env):
    warehouses = env['stock.warehouse'].search([])
    for wh in warehouses:
        picking_type_vals = wh._create_or_update_sequences_and_picking_types()
        if picking_type_vals:
            wh.write(picking_type_vals)


def fill_picking_type_for_repair_order(env):
    ros = env['repair.order'].search([])
    ros._compute_picking_type_id()


def fill_product_template_create_repair(env):
    # If fees where created for some service,
    # they should create repair orders automatically
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE product_template pt
        SET create_repair = TRUE
        FROM repair_fee rf
        JOIN product_product pp ON rf.product_id = pp.id
        WHERE pp.product_tmpl_id = pt.id""",
    )


def fill_stock_move_repair_lines(env):
    # Insert moves for repairs lines not done yet
    openupgrade.logged_query(
        env.cr,
        """
        INSERT INTO stock_move (old_repair_line_id,
        create_uid, create_date, write_uid, write_date,
        repair_id, repair_line_type, ...
        )
        SELECT id, create_uid, create_date, write_uid, write_date,
        repair_id, type as repair_line_type, ...
        FROM repair_line rl
        WHERE rl.move_id IS NULL AND rl.type IS NOT NULL
        """,
    )


def fill_parts_from_repair_line(env):
    # Specific 'repair.line' model is now replaced by a 'stock.move' inheritance
    env.cr.execute(
        """
        SELECT
            rl.company_id,
            rl.id repair_line_id,
            rl.repair_id repair_id,
            rl.type repair_line_type,
            rl.location_id,
            rl.location_dest_id,
            rl.product_id,
            rl.product_uom_qty,
            rl.product_uom,
            rl.lot_id,
            rl.state,
            r.schedule_date,
            r.name repair_name,
            r.address_id partner_id,
            rl.type repair_line_type
        FROM repair_line rl
        LEFT JOIN stock_move sm ON rl.move_id = sm.id
        LEFT JOIN repair_order r ON rl.repair_id = r.id
        WHERE rl.type IS NOT NULL AND sm.id IS NULL
        ORDER BY rl.company_id, rl.repair_id
        """
    )
    data_vals = env.cr.dictfetchall()
    Move = env['stock.move']
    stock_move_vals = []
    for repair_line_val in data_vals:
        # Create stock move for repair line
        stock_move_vals.append({
            'name': repair_line_val['repair_name'],
            'product_id': repair_line_val['product_id'],
            'product_uom_qty': repair_line_val['product_uom_qty'],
            'product_uom': repair_line_val['product_uom'],
            'partner_id': repair_line_val['partner_id'],
            'location_id': repair_line_val['location_id'],
            'location_dest_id': repair_line_val['location_dest_id'],
            'repair_id': repair_line_val['repair_id'],
            'origin': repair_line_val['repair_name'],
            'company_id': repair_line_val['company_id'],
            'repair_line_type': repair_line_val['repair_line_type'],
        })
    Move.create(stock_move_vals)


@openupgrade.migrate()
def migrate(env, version):
    # openupgrade.load_data(env, "repair", "17.0.1.0/noupdate_changes.xml")
    # fill_stock_move_repair_lines_and_fees(env)
    fill_picking_type_for_warehouse(env)
    fill_picking_type_for_repair_order(env)
    fill_product_template_create_repair(env)
    fill_parts_from_repair_line(env)
    openupgrade.delete_records_safely_by_xml_id(
        env,
        [
            "repair.repair_fee_rule",
            "repair.repair_line_rule",
            "repair.seq_repair",
            "repair.mail_template_repair_quotation",
        ],
    )
