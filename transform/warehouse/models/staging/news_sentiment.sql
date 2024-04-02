{{
    config(
        materialized="incremental",
        unique_key=["article_id", "ticker"],
        incremental_strategy="delete+insert"
    )
}}

select article_id,
    arrayJoin(tickers) AS ticker,
    title,
    description,
    published_utc,
    toDateTime(published_utc, 'America/New_York') AS published_et,
    keywords,
    publisher,
    sentiment_label,
    CASE
        WHEN sentiment_label = 'neutral' THEN 0
        WHEN sentiment_label = 'negative' THEN -abs(sentiment_score)
        ELSE sentiment_score
    END AS sentiment_score
from {{ source('raw', 'news_sentiment') }}
where toDate(toDateTime(published_utc, 'America/New_York')) = yesterday()
and length(tickers) > 0
{% if is_incremental() %}
    and published_utc > (select max(published_utc) from {{ this }} )
{% endif %}
