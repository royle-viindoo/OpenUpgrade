from openupgradelib import openupgrade

renamed_fields = [
    ("slide.slide", "slide_slide", "datas", "binary_content"),
    ("slide.channel", "slide_channel", "share_template_id", "share_slide_template_id"),
]

xml_ids_to_rename = [
    (
        "website_slides.rule_slide_slide_resource_manager",
        "website_slides.rule_slide_slide_resource_downloadable_manager",
    ),
]

# slide_slide


def create_and_fill_data_from_slide_type_to_slide_category(env):
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
        SET slide_category = CASE
            WHEN slide_type = 'webpage' THEN 'article'
            WHEN slide_type = 'presentation' THEN 'document'
            ELSE slide_type
        END
        """,
    )


def create_and_fill_data_for_source_type(env):
    openupgrade.logged_query(
        env.cr,
        """
        ALTER TABLE slide_slide
        ADD COLUMN IF NOT EXISTS source_type VARCHAR
        """,
    )

    openupgrade.logged_query(
        env.cr,
        """
        UPDATE slide_slide
        SET source_type = CASE
            WHEN url IS NOT NULL THEN 'external'
            ELSE 'local_file'
        END
        """,
    )


# slide_slide_resource


def create_column_and_migrate_data_from_slide_link_to_slide_resource(env):
    openupgrade.logged_query(
        env.cr,
        """
        ALTER TABLE slide_slide_resource
        ADD COLUMN IF NOT EXISTS link VARCHAR,
        ADD COLUMN IF NOT EXISTS resource_type VARCHAR
        """,
    )

    openupgrade.logged_query(
        env.cr,
        """
        UPDATE slide_slide_resource
        SET resource_type = 'file'
        """,
    )

    openupgrade.logged_query(
        env.cr,
        """
        INSERT INTO slide_slide_resource (
            name,
            link,
            slide_id,
            resource_type
        )
        SELECT
            name,
            link,
            slide_id,
            'url'
        FROM slide_slide_link
        """,
    )


def _create_nbr_article_on_slide_channel(env):
    # Manually create column for avoiding the automatic launch of the compute or default
    # Fill value in post-migration
    openupgrade.logged_query(
        env.cr,
        """
        ALTER TABLE slide_channel
        ADD COLUMN IF NOT EXISTS nbr_article INTEGER
        """,
    )


def _create_nbr_article_on_slide_slide(env):
    # Manually create column for avoiding the automatic launch of the compute or default
    # Fill value in post-migration
    openupgrade.logged_query(
        env.cr,
        """
        ALTER TABLE slide_slide
        ADD COLUMN IF NOT EXISTS nbr_article INTEGER
        """,
    )


def _delete_slide_channel_partner_duplicate_records(env):
    # Cleanup potential duplicates to comply with
    # the new constraint slide_channel_partner_channel_partner_uniq
    openupgrade.logged_query(
        env.cr,
        """
        DELETE FROM slide_channel_partner scp1
        USING slide_channel_partner scp2
        WHERE scp1.id < scp2.id
            AND scp1.partner_id = scp2.partner_id
            AND scp1.channel_id = scp2.channel_id;
        """,
    )


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.rename_fields(env, renamed_fields)
    openupgrade.rename_xmlids(env.cr, xml_ids_to_rename)
    create_and_fill_data_from_slide_type_to_slide_category(env)
    create_column_and_migrate_data_from_slide_link_to_slide_resource(env)
    create_and_fill_data_for_source_type(env)
    _create_nbr_article_on_slide_channel(env)
    _create_nbr_article_on_slide_slide(env)
    _delete_slide_channel_partner_duplicate_records(env)
