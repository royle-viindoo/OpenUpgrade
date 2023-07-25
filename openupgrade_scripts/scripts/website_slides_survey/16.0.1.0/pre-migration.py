from openupgradelib import openupgrade


def _fast_fill_name_on_slide_slide(env):
    openupgrade.logged_query(
        env.cr,
        """
        ALTER TABLE slide_slide
        ADD COLUMN IF NOT EXISTS name VARCHAR
        """,
    )
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE slide_slide slide
            SET name = survey.title
        FROM survey_survey survey
        WHERE slide.name IS NULL AND slide.survey_id = survey.id
        """,
    )


def _fast_fill_slide_category_on_slide_slide(env):
    openupgrade.logged_query(
        env.cr,
        """
        ALTER TABLE slide_slide
        ADD COLUMN IF NOT EXISTS slide_category VARCHAR
        """,
    )
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE slide_slide
        SET slide_category = 'certification'
        WHERE slide_type = 'certification'
        """,
    )


def _set_is_preview_on_slide_slide_for_certification(env):
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE slide_slide
        SET is_preview = false
        WHERE slide_category = 'certification'
        """,
    )


@openupgrade.migrate()
def migrate(env, version):
    _fast_fill_name_on_slide_slide(env)
    _fast_fill_slide_category_on_slide_slide(env)
    _set_is_preview_on_slide_slide_for_certification(env)
