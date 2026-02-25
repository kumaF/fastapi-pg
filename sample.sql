WITH date_filter AS (
	SELECT id, full_date
	FROM crop_price_dw.dim_date
	ORDER BY full_date DESC
	LIMIT 2
), crop_filter AS (
	SELECT ref_id, name
	FROM crop_price_dw.crop_translation
	WHERE language_code = 'si'
), unit_filter AS (
	SELECT ref_id, name
	FROM crop_price_dw.unit_translation
	WHERE language_code = 'si'
), price_data_latest_filter AS (
    SELECT
        DISTINCT ON (
            fp.date_id,
            fp.data_source_id,
            fp.crop_id,
            fp.unit_id,
            fp.economic_center_id,
            fp.price_type_id,
            fp.currency_id
        )
        df.full_date AS "date",
		fp.crop_id,
		fp.unit_id,
		fp.price_type_id,
		fp.price
    FROM crop_price_dw.dev_fact_price_data fp
	JOIN date_filter df ON df.id = fp.date_id
	WHERE
		fp.economic_center_id = 3
		AND fp.data_source_id = 1
		AND fp.crop_id = 1
    ORDER BY
        fp.date_id,
        fp.data_source_id,
        fp.crop_id,
        fp.unit_id,
        fp.economic_center_id,
        fp.price_type_id,
        fp.currency_id,
        fp.id DESC
), price_data AS (
	SELECT
		pl.date,
		pl.crop_id,
		pl.unit_id,
		pl.price_type_id,
		pl.price AS "tp",
		LEAD(pl.price, 1) OVER (
			PARTITION BY (
				pl.crop_id,
                pl.unit_id,
				pl.price_type_id
			)
			ORDER BY pl.date DESC
		) AS "yp",
		ROW_NUMBER() OVER (
			PARTITION BY (
				pl.crop_id,
                pl.unit_id,
				pl.price_type_id
			)
			ORDER BY pl.date DESC
		) AS "rn"
	FROM price_data_latest_filter pl
), price_data_categorized AS (
	SELECT
		pf.crop_id,
		pf.unit_id,
		MAX(tp) FILTER (WHERE price_type_id = 2) AS wholesale_price_today,
	    MAX(tp) FILTER (WHERE price_type_id = 1) AS retail_price_today,
		MAX(yp) FILTER (WHERE price_type_id = 2) AS wholesale_price_yesterday,
	    MAX(yp) FILTER (WHERE price_type_id = 1) AS retail_price_yesterday
	FROM price_data pf
	WHERE pf.rn = 1
	GROUP BY (
		pf.date,
		pf.crop_id,
		pf.unit_id
	)
)

SELECT
	cf.ref_id AS "id",
	cf.name AS "crop",
	uf.name AS "unit",
	pdc.wholesale_price_today,
	pdc.wholesale_price_yesterday,
	pdc.retail_price_today,
	pdc.retail_price_yesterday
FROM price_data_categorized pdc
RIGHT JOIN crop_filter cf ON cf.ref_id = pdc.crop_id
JOIN unit_filter uf ON uf.ref_id = pdc.unit_id;

