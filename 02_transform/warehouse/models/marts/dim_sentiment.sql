{{
    config(
        materialized="view"
    )
}}

select
    {{ dbt_utils.generate_surrogate_key(['sentiment_label']) }} as sentiment_label_key,
    sentiment_label
from {{ source('raw', 'news_sentiment') }}
where toDate(toDateTime(published_utc, 'America/New_York')) = yesterday()