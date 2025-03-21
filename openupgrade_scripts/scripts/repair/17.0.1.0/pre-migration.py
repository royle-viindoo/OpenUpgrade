# Copyright 2025 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openupgradelib import openupgrade

from odoo.tools import sql
from odoo.tools.sql import column_exists, create_column


def create_column_repair_type_id(env):
    if not column_exists(env.cr, "stock_warehouse", "repair_type_id"):
        create_column(env.cr, "stock_warehouse", "repair_type_id", "int4")
        

def add_helper_repair_move_rel(env):
    openupgrade.logged_query(
        env.cr,
        """
        ALTER TABLE stock_move
        ADD COLUMN old_repair_line_id integer""",
    )
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE stock_move sm
        SET old_repair_line_id = rl.id
        FROM repair_line rl
        WHERE sm.id = rl.move_id
        """,
    )
    # Create index for these columns, as they are going to be accessed frequently
    index_name = "stock_move_old_repair_line_id_index"
    sql.create_index(env.cr, index_name, "stock_move", ['"old_repair_line_id"'])


def map_repair_order_state(env):
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE repair_order
        SET state = CASE WHEN state = 'ready' THEN 'confirmed' ELSE 'done' END
        WHERE state in ('ready', '2binvoiced')
        """,
    )


def fill_repair_order_schedule_date(env):
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE repair_order
        SET schedule_date = create_date
        WHERE schedule_date IS NULL
        """,
    )


@openupgrade.migrate()
def migrate(env, version=None):
    openupgrade.remove_tables_fks(env.cr, ["repair_line", "repair_fee"])
    create_column_repair_type_id(env)
    add_helper_repair_move_rel(env)
    map_repair_order_state(env)
    fill_repair_order_schedule_date(env)
