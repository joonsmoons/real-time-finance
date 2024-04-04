{{
    config(
        materialized='materialized_view',
        engine='MergeTree()',
        order_by='(sentiment_label)'
    )
}}

with news_segment as (
    select distinct sentiment_label
    from {{ ref('fact_news_sentiment') }}
)
select
    {{ dbt_utils.generate_surrogate_key(['sentiment_label']) }} as sentiment_label_key,
    sentiment_label
from news_segment
