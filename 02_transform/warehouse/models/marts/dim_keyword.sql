{{
    config(
        materialized="view"
    )
}}

WITH k AS (
    SELECT
        arrayJoin(keywords) AS keyword,
        article_id
    FROM {{ source('raw', 'news_sentiment') }}
    WHERE toDate(toDateTime(published_utc, 'America/New_York')) = yesterday()
)
SELECT {{ dbt_utils.generate_surrogate_key(['keyword']) }} AS keyword_key,
    keyword,
    count(distinct article_id) article_count
FROM k
GROUP BY keyword