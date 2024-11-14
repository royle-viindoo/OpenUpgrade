# Copyright 2024 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openupgradelib import openupgrade

_deleted_xml_records = [
    "event.event_type_data_conference",
    "event.event_type_data_ticket",
]


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.load_data(env, "event", "17.0.1.8/noupdate_changes.xml")
    openupgrade.delete_records_safely_by_xml_id(
        env,
        _deleted_xml_records,
    )
