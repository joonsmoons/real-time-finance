# Real Time Finance Data Pipeline

## Table of Contents

- [Source Dataset](#source-dataset)
- [Architecture](#architecture)
   - [Produce](#produce)
   - [Extract Load](#extract-load)
   - [Transform](#transform)
   - [Reporting](#reporting)
- [CI/CD](#cicd)

This data engineering project integrates stock price data from websockets and news data from Polygon.io API, streaming them into Kafka via Confluent Cloud. Utilizing Hugging Face's sentiment analysis model on Databricks with PySpark, sentiment is tagged onto news articles in real-time before being processed through ClickHouse with dbt and materialized views. Real-time visualization on Preset hosting Superset updates every 30 seconds, displaying dynamic insights like stock price, volume, and news sentiment.

![Preset Dashboard](https://github.com/joonsmoons/real_time_finance/assets/113525606/c0c5a552-08c0-43fb-b993-d05c43ec2f94)

## Problem Statement
This project solves the challenge of accessing real-time insights into financial market trends. By combining stock price data with news analysis, it enables users to track market sentiment and stock performance dynamically, aiding in timely investment decisions.

### Key Questions Addressed by this Solution:
- What are the top trending stocks based on the number of news articles published about them in the past week?
- How do stock prices change throughout the day, and what is the trading volume associated with these changes?
- What is the sentiment associated with the latest news articles about certain stocks, and how does it correlate with changes in stock prices?
- Can users search for specific keywords or ticker symbols to find relevant news articles, and what insights can be derived from this data?

## Source Dataset
[Polygon.io](https://polygon.io) - A financial data provider offering real-time and historical market data. Polygon.io provides various APIs for accessing financial market data, including stock prices, trade volumes, and news articles related to financial markets. This project utilizes Polygon.io's API to ingest real-time stock price and news data into the system, facilitating the analysis and visualization of financial market trends. 

## Architecture
![Architecture](https://github.com/joonsmoons/real_time_finance/assets/113525606/145a6284-0467-4bbc-bf2e-2a90c3d45a30)

### Produce
Continuously generating real-time news and stock data involves fetching news API information every 20 seconds in Python, integrating it into Kafka topics using Confluent, and hosting the entire process within Docker containers deployed on EC2 instances for seamless streaming. Additionally, real-time stock data is aggregated using websockets in Python and integrated into the Kafka pipeline alongside the news data. This setup ensures a continuous flow of up-to-date news information every 20 seconds for analysis and consumption, while stock data is collected separately and integrated into the pipeline as it becomes available.

### Extract Load
Upon producing the news data into the Kafka topic, the stream is consumed and read from PySpark in Databricks. Within this environment, a sentiment analysis model using Hugging Face Transformers is executed. This model operates on mini-batches of data and processes the batch data through a custom Python User Defined Function (UDF). Once the sentiment analysis is complete, the data is transformed and tagged results are produced into another Kafka topic for further processing and analysis.

### Transform
The next step involves streaming the data into ClickHouse using ClickPipes. Following this, transformations are performed, leading to the creation of several materialized views in ClickHouse. These materialized views ensure that the data remains consistently updated whenever an insert action occurs. To accomplish this, Data Build Tool (DBT) is employed, leveraging modular transformation, data lineage, and data quality tests. This approach facilitates dimension modeling into fact, dimension, and reporting tables, thereby enhancing data organization and accessibility.

![DBT Data Lineage](https://github.com/joonsmoons/real_time_finance/assets/113525606/a0391366-617e-4c9c-af75-0cc6bf55a0b1)

### Reporting
Finally, reporting is conducted through Preset, a cloud service that hosts Apache Superset on the backend. The dashboard showcases various insights, including the top 50 trending stocks by article count for the past week, an intraday stock price chart, an intraday stock volume chart, and the latest news. Additionally, the dashboard features a search bar allowing users to search for specific keywords or ticker symbols, enhancing the interactivity and usability of the reporting interface. This dashboard refreshes every 30 seconds. 

![Preset Dashboard](https://github.com/joonsmoons/real_time_finance/assets/113525606/c0c5a552-08c0-43fb-b993-d05c43ec2f94)

### CI/CD
To streamline the development process, GitHub Actions is leveraged for continuous integration and deployment (CI/CD). This automated pipeline includes linting of Python scripts to maintain code quality standards and seamless deployment of Docker images to Amazon Elastic Container Registry (ECR), ensuring efficient management and dissemination of updated Docker containers.

![CI/CD](https://github.com/joonsmoons/real_time_finance/assets/113525606/24685e99-0426-424d-8a4b-d78ce3234405)
