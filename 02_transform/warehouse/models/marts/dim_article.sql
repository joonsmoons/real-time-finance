{{
    config(
        materialized="view"
    )
}}

with a as (
    select distinct article_id,
    title,
    description,
    published_utc,
    publisher
    from {{ source('raw', 'news_sentiment') }}
    WHERE toDate(toDateTime(published_utc, 'America/New_York')) = yesterday()
)

select  {{ dbt_utils.generate_surrogate_key(['article_id']) }} as article_key,
    article_id,
    title,
    description,
    published_utc,
    publisher
from a
