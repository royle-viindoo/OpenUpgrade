# Copyright 2023 Coop IT Easy SC
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade


def fill_payment_provider_is_published(env):
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE payment_provider
            SET is_published = True
        WHERE state IN ('enabled', 'test')
        """,
    )


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.load_data(env.cr, "payment", "16.0.2.0/noupdate_changes.xml")
    fill_payment_provider_is_published(env)
