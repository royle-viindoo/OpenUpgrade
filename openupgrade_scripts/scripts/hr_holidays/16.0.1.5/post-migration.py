# Copyright 2023 Coop IT Easy (https://coopiteasy.be)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade


def _map_hr_leave_type_allocation_validation_type(env):
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE hr_leave_type
            SET allocation_validation_type = CASE
                WHEN responsible_id IS NOT NULL THEN 'officer'
                ELSE 'no'
                END
        WHERE allocation_validation_type = 'set'
        """,
    )


def _fix_number_of_days_allocation(env):
    allocations = (
        env["hr.leave.allocation"]
        .with_context(active_test=False)
        .search([("parent_id.type_request_unit", "=", "hour")])
    )
    for allocation in allocations:
        hours_per_day = (
            allocation.employee_id.sudo().resource_id.calendar_id.hours_per_day
        )
        if hours_per_day and hours_per_day != 8.0:
            allocation.number_of_days = (allocation.number_of_days * 8) / hours_per_day


@openupgrade.migrate()
def migrate(env, version):
    _map_hr_leave_type_allocation_validation_type(env)
    openupgrade.load_data(env.cr, "hr_holidays", "16.0.1.5/noupdate_changes.xml")
    _fix_number_of_days_allocation(env)
