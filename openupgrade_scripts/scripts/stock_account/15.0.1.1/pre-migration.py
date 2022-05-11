from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.rename_xmlids(
        env.cr,
        [
            ("sale_stock.group_lot_on_invoice", "stock_account.group_lot_on_invoice"),
        ],
    )
