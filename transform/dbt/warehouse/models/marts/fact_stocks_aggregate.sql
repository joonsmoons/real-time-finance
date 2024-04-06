{{
    config(
        materialized='materialized_view',
        engine='MergeTree()',
        order_by='(sym,s)'
    )
}}

with polygon_stocks_topic as (
    select
        *,
        toDate(toDateTime64(s / 1000, 3, 'America/New_York')) as dt,
        row_number() OVER (PARTITION BY sym, s ORDER BY s) AS unique_rnk
    from {{ source('raw', 'polygon_stocks_topic') }}
), max_date as (
    select max(dt) AS max_dt
    from polygon_stocks_topic
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
cross join max_date
where 1 = 1
and ev = 'AM'
and unique_rnk = 1
and dt = (select max_dt from max_date)