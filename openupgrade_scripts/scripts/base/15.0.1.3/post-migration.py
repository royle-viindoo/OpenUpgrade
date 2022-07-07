# Copyright 2021 Odoo Community Association (OCA)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade


def full_module_dependencies(env, modules):
    dependencies = env["ir.module.module"]
    if modules.dependencies_id:
        dependencies = env["ir.module.module"].search(
            [("name", "in", modules.dependencies_id.mapped("name"))]
        )
        if dependencies:
            dependencies |= full_module_dependencies(env, dependencies)
    return dependencies


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.load_data(env.cr, "base", "15.0.1.3/noupdate_changes.xml")
    # Assure all modules are set to update.
    installed = env["ir.module.module"].search(
        [("state", "in", ("installed", "to install"))]
    )
    for mod in installed:
        terp = env["ir.module.module"].get_module_info(mod.name)
        mod._update_dependencies(terp.get("depends", []), terp.get("auto_install"))
    uninstalled_dependencies = full_module_dependencies(env, installed).filtered(
        lambda m: m.state == "uninstalled"
    )
    if uninstalled_dependencies:
        openupgrade.logged_query(
            env.cr,
            """
            UPDATE ir_module_module
            SET state='to install'
            WHERE name IN %s AND state='uninstalled'""",
            (tuple(uninstalled_dependencies.mapped("name")),),
        )
