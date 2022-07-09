from openupgradelib import openupgrade


def fill_account_payment_method_line_payment_acquirer_id(env):
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE account_payment_method_line apml
            SET payment_acquirer_id = pa.id
        FROM account_payment_method apm
        LEFT JOIN payment_acquirer pa ON pa.provider = apm.code
        WHERE apm.id = apml.payment_method_id
        """,
    )


@openupgrade.migrate()
def migrate(env, version):
    fill_account_payment_method_line_payment_acquirer_id(env)
