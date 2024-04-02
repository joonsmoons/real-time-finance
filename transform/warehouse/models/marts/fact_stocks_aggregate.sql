{{
    config(
        materialized="incremental",
        unique_key=["sym", "s"],
        incremental_strategy="delete+insert"
    )
}}

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
    s,
from {{ source('raw', 'stocks_minute_aggregate') }}
where toDate(toDateTime(toDateTime64(s / 1000, 3, 'America/New_York'), 'America/New_York')) = yesterday()
and ev = 'AM'
{% if is_incremental() %}
    and s > (select max(s) from {{ this }} )
{% endif %}
