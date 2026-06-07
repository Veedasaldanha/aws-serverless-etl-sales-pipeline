# AWS Serverless ETL Sales Pipeline

## Project Overview

This project demonstrates a serverless ETL pipeline built using AWS services.

### Architecture

Mentor API
↓
AWS Lambda
↓
Raw JSON stored in Amazon S3
↓
Data Cleaning using Pandas
↓
JSON to Parquet Conversion
↓
Amazon S3 (Parquet)
↓
AWS Glue Crawler
↓
AWS Glue Data Catalog
↓
Amazon Athena
↓
SQL Analytics

## Technologies Used

- AWS Lambda
- Amazon S3
- AWS Glue Crawler
- AWS Glue Data Catalog
- Amazon Athena
- Python
- Pandas
- PyArrow

## Features

- Extract data from REST API
- Store raw JSON in S3
- Remove duplicate records
- Convert JSON to Parquet
- Automatic schema discovery
- Query data using Athena

## Architecture Diagram

<img width="1412" height="549" alt="Architecture_AWS_serverless" src="https://github.com/user-attachments/assets/ecc900ca-30d4-4f22-a33c-127df55c7b05" />
