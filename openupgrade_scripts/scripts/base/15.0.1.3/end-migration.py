# Copyright 2022 ForgeFlow S.L.  <https://www.forgeflow.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openupgradelib import openupgrade


def _re_validate_views(env):
    """Re validate views when all views is loaded"""
    views_to_write = env["ir.ui.view"]
    views = views_to_write.search([("active", "=", False), ("type", "!=", "qweb")])
    for view in views:
        try:
            view._check_xml()
            views_to_write |= view
        except ValueError:
            pass
    if views_to_write:
        views_to_write.write({"active": True})


@openupgrade.migrate()
def migrate(env, version):
    """Call disable_invalid_filters in every edition of openupgrade"""
    openupgrade.disable_invalid_filters(env)
    _re_validate_views(env)
