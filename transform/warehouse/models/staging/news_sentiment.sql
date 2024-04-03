{{
    config(
        materialized='materialized_view',
        engine='MergeTree()',
        order_by='(article_id)'
    )
}}

select article_id,
    tickers,
    title,
    description,
    published_utc,
    toStartOfMinute(toDateTime(published_utc, 'America/New_York')) AS published_at,
    keywords,
    publisher,
    sentiment_label,
    CASE
        WHEN sentiment_label = 'neutral' THEN 0
        WHEN sentiment_label = 'negative' THEN -abs(sentiment_score)
        ELSE sentiment_score
    END AS sentiment_score
from {{ source('raw', 'news_sentiment') }}
where toDate(toDateTime(published_utc, 'America/New_York')) >= toDate(toTimezone(now(), 'America/New_York')) - 7
AND toDate(toDateTime(published_utc, 'America/New_York')) < toDate(toTimezone(now(), 'America/New_York'))
and length(tickers) > 0
