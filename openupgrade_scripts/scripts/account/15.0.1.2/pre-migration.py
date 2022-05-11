from openupgradelib import openupgrade


def fast_fill_account_payment_payment_method_line_id(env):
    openupgrade.logged_query(
        env.cr,
        """
        ALTER TABLE account_payment
        ADD COLUMN IF NOT EXISTS payment_method_line_id integer""",
    )
    # TODOs: fill account_payment's payment_method_line_id


@openupgrade.migrate()
def migrate(env, version):
    fast_fill_account_payment_payment_method_line_id(env)
