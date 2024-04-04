{{
    config(
        materialized='materialized_view',
        engine='MergeTree()',
        order_by='(article_key)'
    )
}}

select
    {{ dbt_utils.generate_surrogate_key(['article_id']) }} as article_key,
    article_id,
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
from {{ source('raw', 'polygon_sentiment_news_topic') }}
where 1 = 1
AND toMonth(toDateTime(published_utc, 'America/New_York')) >= toMonth(toDateTime(NOW(), 'America/New_York')) - 3  -- Three months ago
AND toMonth(toDateTime(published_utc, 'America/New_York')) <= toMonth(toDateTime(NOW(), 'America/New_York'))  -- Current month
