from openupgradelib import openupgrade


def fast_fill_hr_leave_holiday_allocation_id(env):
    openupgrade.logged_query(
        env.cr,
        """
        ALTER TABLE hr_leave
        ADD COLUMN IF NOT EXISTS holiday_allocation_id integer""",
    )
    # TODOs: fill hr_leave's holiday_allocation_id


def fast_fill_hr_leave_employee_company_id(env):
    openupgrade.logged_query(
        env.cr,
        """
        ALTER TABLE hr_leave
        ADD COLUMN IF NOT EXISTS employee_company_id integer""",
    )
    # TODOs: fill hr_leave's employee_company_id


def fast_fill_hr_leave_multi_employee(env):
    openupgrade.logged_query(
        env.cr,
        """
        ALTER TABLE hr_leave
        ADD COLUMN IF NOT EXISTS multi_employee boolean""",
    )
    # TODOs: fill hr_leave's multi_employee


def fast_fill_hr_leave_allocation_accrual_plan_id(env):
    openupgrade.logged_query(
        env.cr,
        """
        ALTER TABLE hr_leave_allocation
        ADD COLUMN IF NOT EXISTS accrual_plan_id integer""",
    )
    # TODOs: fill hr_leave_allocation's accrual_plan_id


def fast_fill_hr_leave_allocation_multi_employee(env):
    openupgrade.logged_query(
        env.cr,
        """
        ALTER TABLE hr_leave_allocation
        ADD COLUMN IF NOT EXISTS multi_employee boolean""",
    )
    # TODOs: fill hr_leave's multi_employee


@openupgrade.migrate()
def migrate(env, version):
    fast_fill_hr_leave_holiday_allocation_id(env)
    fast_fill_hr_leave_employee_company_id(env)
    fast_fill_hr_leave_multi_employee(env)
    fast_fill_hr_leave_allocation_accrual_plan_id(env)
    fast_fill_hr_leave_allocation_multi_employee(env)
