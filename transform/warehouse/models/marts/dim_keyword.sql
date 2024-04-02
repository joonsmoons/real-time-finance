{{
    config(
        materialized="view"
    )
}}

WITH k AS (
    SELECT
        arrayJoin(keywords) AS keyword,
        article_id
    FROM {{ ref('news_sentiment') }}
)
SELECT {{ dbt_utils.generate_surrogate_key(['keyword']) }} AS keyword_key,
    keyword,
    count(distinct article_id) article_count
FROM k
GROUP BY keyword