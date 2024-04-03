{{
    config(
        materialized='materialized_view',
        engine='MergeTree()',
        order_by='(article_id)'
    )
}}

with a as (
    select distinct article_id,
    title,
    description,
    published_utc,
    publisher
    from {{ ref('news_sentiment') }}
)

select  {{ dbt_utils.generate_surrogate_key(['article_id']) }} as article_key,
    article_id,
    title,
    description,
    publisher
from a
