from openupgradelib import openupgrade


def _correct_utm_campaign_name(env):
    # correct utm_campaign'name to add unique_name
    env.cr.execute(
        """WITH utm_campaign_tmp AS (
                SELECT DISTINCT(uc1.name) as name
                FROM utm_campaign uc1
                WHERE EXISTS (
                    SELECT 1
                    FROM utm_campaign uc2
                    WHERE uc1.id != uc2.id AND uc1.name = uc2.name
                )
            )
            SELECT ARRAY_AGG(uc1.id)
            FROM utm_campaign uc1
            JOIN utm_campaign_tmp uc2 ON uc1.name = uc2.name
            GROUP BY uc1.name
        """
    )
    for _ids in env.cr.dictfetchall():
        _ids = list(_ids)
        if len(_ids) == 2:
            uc = env["utm.campaign"].browse(_ids[-1])
            uc.write({"name": uc.name + " (copy)"})
            continue

        for i in range(1, len(_ids)):
            uc = env["utm.campaign"].browse(_ids[i])
            uc.write({"name": uc.name + " (copy)" * i})


def _correct_utm_medium_name(env):
    # correct utm_medium'name to add unique_name
    env.cr.execute(
        """WITH utm_medium_tmp AS (
                SELECT DISTINCT(uc1.name) as name
                FROM utm_medium uc1
                WHERE EXISTS (
                    SELECT 1
                    FROM utm_medium uc2
                    WHERE uc1.id != uc2.id AND uc1.name = uc2.name
                )
            )
            SELECT ARRAY_AGG(uc1.id)
            FROM utm_medium uc1
            JOIN utm_medium uc2 ON uc1.name = uc2.name
            GROUP BY uc1.name
        """
    )
    for _ids in env.cr.dictfetchall():
        _ids = list(_ids)
        if len(_ids) == 2:
            uc = env["utm.medium"].browse(_ids[-1])
            uc.write({"name": uc.name + " (copy)"})
            continue

        for i in range(1, len(_ids)):
            uc = env["utm.medium"].browse(_ids[i])
            uc.write({"name": uc.name + " (copy)" * i})


def _correct_utm_source_name(env):
    # correct utm_campaign'name to add unique_name
    env.cr.execute(
        """WITH utm_source_tmp AS (
                SELECT DISTINCT(uc1.name) as name
                FROM utm_source uc1
                WHERE EXISTS (
                    SELECT 1
                    FROM utm_source uc2
                    WHERE uc1.id != uc2.id AND uc1.name = uc2.name
                )
            )
            SELECT ARRAY_AGG(uc1.id)
            FROM utm_source uc1
            JOIN utm_source uc2 ON uc1.name = uc2.name
            GROUP BY uc1.name
        """
    )
    for _ids in env.cr.dictfetchall():
        _ids = list(_ids)
        if len(_ids) == 2:
            uc = env["utm.source"].browse(_ids[-1])
            uc.write({"name": uc.name + " (copy)"})
            continue

        for i in range(1, len(_ids)):
            uc = env["utm.source"].browse(_ids[i])
            uc.write({"name": uc.name + " (copy)" * i})


@openupgrade.migrate()
def migrate(env, version):
    _correct_utm_campaign_name(env)
    _correct_utm_medium_name(env)
    _correct_utm_source_name(env)
