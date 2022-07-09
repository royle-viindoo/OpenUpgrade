from openupgradelib import openupgrade


def fill_account_payment_method_line_payment_account_id(env):
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE account_payment_method_line apml
        SET payment_account_id =
            CASE WHEN apm.payment_type = 'inbound'
                THEN (
                    SELECT aj.payment_debit_account_id
                    FROM account_journal aj
                    WHERE aj.id = apml.journal_id)
                WHEN apm.payment_type = 'outbound'
                THEN (
                    SELECT aj.payment_credit_account_id
                    FROM account_journal aj
                    WHERE aj.id = apml.journal_id)
            END
        FROM account_payment_method apm
        WHERE apml.payment_method_id = apm.id
        """,
    )


def fill_account_payment_outstanding_account_id(env):
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE account_payment ap
        SET outstanding_account_id = CASE
            WHEN apml.payment_account_id IS NOT NULL
                THEN apml.payment_account_id
            END
        FROM account_payment_method_line apml
        WHERE ap.payment_method_line_id IS NOT NULL
            AND apml.id = ap.payment_method_line_id
        """,
    )
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE account_payment ap
        SET outstanding_account_id = CASE
            WHEN ap.payment_type = 'inbound'
                AND c.account_journal_payment_debit_account_id IS NOT NULL
                THEN c.account_journal_payment_debit_account_id
            WHEN ap.payment_type = 'outbound'
                AND c.account_journal_payment_credit_account_id IS NOT NULL
                THEN c.account_journal_payment_credit_account_id
            END
        FROM account_move am
        JOIN account_journal aj ON am.journal_id = aj.id
        JOIN res_company c ON c.id = aj.company_id
        WHERE ap.move_id = am.id AND ap.payment_method_line_id IS NULL
        """,
    )


@openupgrade.migrate()
def migrate(env, version):
    fill_account_payment_method_line_payment_account_id(env)
    fill_account_payment_outstanding_account_id(env)
