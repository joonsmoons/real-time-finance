CREATE DATABASE IF NOT EXISTS raw;

CREATE TABLE raw.news_sentiment (
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


