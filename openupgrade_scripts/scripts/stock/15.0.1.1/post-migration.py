from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.load_data(env.cr, "stock", "15.0.1.1/noupdate_changes.xml")
    openupgrade.delete_record_translations(
        env.cr,
        "stock",
        ["mail_template_data_delivery_confirmation"],
    )
    # try delete noupdate records
    openupgrade.delete_records_safely_by_xml_id(
        env,
        [
            "stock.stock_inventory_comp_rule",
            "stock.stock_inventory_line_comp_rule",
            "stock.sequence_tracking",
        ],
    )
