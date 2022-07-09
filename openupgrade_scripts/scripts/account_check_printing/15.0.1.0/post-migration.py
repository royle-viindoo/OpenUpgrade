from openupgradelib import openupgrade


def _create_account_payment_method_line(env):
    # Create account payment method lines from account payment methods
    openupgrade.logged_query(
        env.cr,
        """
        INSERT INTO account_payment_method_line
        (name, payment_method_id, journal_id)
        SELECT apm.name, apm.id, aj.id
        FROM account_payment_method apm
        JOIN account_journal aj ON aj.type = 'bank'
        WHERE apm.code = 'check_printing'
            AND (
                SELECT COUNT (*)
                FROM payment_acquirer pa
                WHERE pa.provider NOT IN ('none', 'manual')
                    AND aj.id = pa.journal_id LIMIT 1) = 0
        """,
    )


@openupgrade.migrate()
def migrate(env, version):
    _create_account_payment_method_line(env)
