{{
    config(
        materialized="table"
    )
}}

select
    {{ dbt_utils.generate_surrogate_key(['article_id', 'ticker']) }} as article_sentiment_key,
    article_id,
    ticker,
    toDate(published_et) AS published_date,
    toHour(published_et) AS published_hour,
    toMinute(published_et) AS published_minute,
    toSecond(published_et) AS published_second,
    sentiment_label,
    sentiment_score,
from {{ ref('news_sentiment') }}
