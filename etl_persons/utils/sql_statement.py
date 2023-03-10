STMT = """
    SELECT
        p.id,
        p.full_name,
        array_agg(
            DISTINCT CASE WHEN pfw.role = 'director' THEN fw.id::varchar else '' end
        ) AS director,
        array_agg(
            DISTINCT CASE WHEN pfw.role = 'actor' THEN fw.id::varchar else '' end
        ) AS actors,
        array_agg(
            DISTINCT CASE WHEN pfw.role = 'writer' THEN fw.id::varchar else '' END
        ) AS writers,
        MAX(p.updated_at) AS last_modified
    FROM
        content.person p
        LEFT JOIN content.person_film_work pfw ON p.id = pfw.person_id
        LEFT JOIN content.film_work fw ON pfw.film_work_id = fw.id
    GROUP BY p.id
    """
