# Copyright 2023 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade


def _set_last_seen_message(env):
    # do not show new messages separator for own messages
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE mail_channel_member
            SET seen_message_id = fetched_message_id
        WHERE seen_message_id IS NULL OR seen_message_id < fetched_message_id
        """,
    )


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.load_data(env.cr, "mail", "16.0.1.10/noupdate_changes.xml")
    _set_last_seen_message(env)
