{{
    config(
        materialized='materialized_view',
        engine='MergeTree()',
        order_by='(sym,s)'
    )
}}

with polygon_stocks_topic as (
    select *, row_number() OVER (PARTITION BY sym, s ORDER BY s) AS rnk
    from {{ source('raw', 'polygon_stocks_topic') }}
)
select {{ dbt_utils.generate_surrogate_key(['sym', 's']) }} as stocks_aggregate_key,
    ev as event_type,
    sym as ticker,
    v as volume,
    av as accumulated_volume,
    op as open_today,
    vw as weighted_avg_price_tick,
    o as open_tick,
    c as close_tick,
    h as high_tick,
    l as low_tick,
    a as weighted_avg_price_today,
    z as avg_trade_size_tick,
    toDateTime64(s / 1000, 3, 'America/New_York') AS starting_timestamp,
    toDateTime64(e / 1000, 3, 'America/New_York') as ending_timestamp,
    sym,
    s
from polygon_stocks_topic
where 1 = 1
and toDate(toDateTime(toDateTime64(s / 1000, 3, 'America/New_York'), 'America/New_York')) >= toDate(toDateTime(now(), 'America/New_York')) - 28
and toDate(toDateTime(toDateTime64(e / 1000, 3, 'America/New_York'), 'America/New_York')) <= toDate(toDateTime(now(), 'America/New_York'))
and ev = 'AM'
and rnk = 1
