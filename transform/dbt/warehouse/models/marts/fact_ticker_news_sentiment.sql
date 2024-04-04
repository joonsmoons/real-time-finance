{{
    config(
        materialized='materialized_view',
        engine='MergeTree()',
        order_by='(stocks_aggregate_key)'
    )
}}
with news_sentiment as (
    select arrayJoin(tickers) as ticker,
        published_at,
        article_id,
        sentiment_label,
        sentiment_score
    from {{ ref('fact_news_sentiment') }} as fact_news_sentiment
)
select {{ dbt_utils.generate_surrogate_key(['stocks_aggregate.ticker', 'stocks_aggregate.starting_timestamp', 'news_sentiment.article_id']) }} as stocks_aggregate_key,
    stocks_aggregate.ticker as ticker,
    stocks_aggregate.starting_timestamp as starting_timestamp,
    news_sentiment.article_id as article_id,
    stocks_aggregate.open_tick,
    stocks_aggregate.close_tick,
    stocks_aggregate.high_tick,
    stocks_aggregate.low_tick,
    stocks_aggregate.weighted_avg_price_tick,
    stocks_aggregate.volume,
    stocks_aggregate.accumulated_volume,
    stocks_aggregate.open_today,
    stocks_aggregate.ending_timestamp,
    news_sentiment.sentiment_label,
    news_sentiment.sentiment_score
from {{ref("stocks_aggregate")}} as stocks_aggregate
left join news_sentiment
on news_sentiment.ticker = stocks_aggregate.ticker
and news_sentiment.published_at = stocks_aggregate.starting_timestamp