CREATE DATABASE IF NOT EXISTS raw;

CREATE OR REPLACE TABLE raw.news_sentiment (
    article_id String,
    title String,
    description String,
    published_utc DateTime,
    tickers Array(String),
    keywords Array(String),
    publisher LowCardinality(String),
    sentiment_label Enum('neutral' = 0, 'positive' = 1, 'negative' = 2),
    sentiment_score Float32
) ENGINE = MergeTree()
ORDER BY article_id

CREATE TABLE raw.stocks_minute_aggregate
(
    ev String,
    sym String,
    v UInt32,
    av UInt64,
    op Float32,
    vw Float32,
    o Float32,
    c Float32,
    h Float32,
    l Float32,
    a Float32,
    z UInt32,
    s UInt64,
    e UInt64
)
ENGINE = MergeTree
ORDER BY (sym, s);


