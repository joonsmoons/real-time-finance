{{
    config(
        materialized='materialized_view',
        engine='MergeTree()',
        order_by='(article_key)'
    )
}}

select
    {{ dbt_utils.generate_surrogate_key(['id']) }} as article_key,
    id,
    tickers,
    title,
    description,
    published_utc,
    keywords,
    publisher,
    article_url,
    toStartOfMinute(toDateTime(published_utc, 'America/New_York'))
        as published_at,
    sentiment_label,
    case
        when sentiment_label = 'neutral' then 0
        when sentiment_label = 'negative' then -ABS(sentiment_score)
        else sentiment_score
    end as sentiment_score
from {{ source('raw', 'polygon_news_sentiment_topic') }}
where 1 = 1
AND toMonth(toDateTime(published_utc, 'America/New_York')) > toMonth(toDateTime(NOW(), 'America/New_York')) - 3  -- Three months ago
