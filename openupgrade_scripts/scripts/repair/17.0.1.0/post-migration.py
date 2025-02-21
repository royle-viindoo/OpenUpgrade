# Copyright 2025 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade


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


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.load_data(env, "repair", "17.0.1.0/noupdate_changes.xml")
    # fill_stock_move_repair_lines_and_fees(env)
    fill_product_template_create_repair(env)
    openupgrade.delete_records_safely_by_xml_id(
        env,
        [
            "repair.repair_fee_rule",
            "repair.repair_line_rule",
            "repair.seq_repair",
            "repair.mail_template_repair_quotation",
        ],
    )
