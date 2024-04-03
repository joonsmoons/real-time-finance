{{
    config(
        materialized='materialized_view',
        engine='MergeTree()',
        order_by='(article_id)'
    )
}}

select
    article_id,
    tickers,
    title,
    description,
    published_utc,
    keywords,
    publisher,
    sentiment_label,
    TOSTARTOFMINUTE(TODATETIME(published_utc, 'America/New_York'))
        as published_at,
    case
        when sentiment_label = 'neutral' then 0
        when sentiment_label = 'negative' then -ABS(sentiment_score)
        else sentiment_score
    end as sentiment_score
from {{ source('raw', 'news_sentiment') }}
where
    TODATE(TODATETIME(published_utc, 'America/New_York'))
    >= TODATE(TOTIMEZONE(NOW(), 'America/New_York')) - 7
    and TODATE(TODATETIME(published_utc, 'America/New_York'))
    < TODATE(TOTIMEZONE(NOW(), 'America/New_York'))
    and LENGTH(tickers) > 0
