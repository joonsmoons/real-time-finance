{{
    config(
        materialized="table"
    )
}}

with ns as (
    select distinct article_id,
        published_utc,
        toDateTime(published_utc, 'America/New_York') AS published_et,
        arrayJoin(tickers) AS ticker,
        sentiment_label,
        sentiment_score
    from {{ source('raw', 'news_sentiment') }}
    where length(tickers) > 0
)
select
    {{ dbt_utils.generate_surrogate_key(['article_id', 'ticker']) }} as article_sentiment_key,
    article_id,
    ticker,
    toDate(published_et) AS published_date,
    toHour(published_et) AS published_hour,
    toMinute(published_et) AS published_minute,
    toSecond(published_et) AS published_second,
    sentiment_label,
    CASE
        WHEN sentiment_label = 'neutral' THEN 0
        WHEN sentiment_label = 'negative' THEN -abs(sentiment_score)
        ELSE sentiment_score
    END AS sentiment_score
from ns
where toDate(published_et) = yesterday()