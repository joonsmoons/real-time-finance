{{
    config(
        materialized="view"
    )
}}

select
    {{ dbt_utils.generate_surrogate_key(['sentiment_label']) }} as sentiment_label_key,
    sentiment_label
from {{ ref('news_sentiment') }}
