import json
import boto3
import pandas as pd
import requests
from io import BytesIO

# S3 Client
s3 = boto3.client('s3')

# Configuration
BUCKET_NAME = "amazon.sales.data"
API_URL = "https://b2oslamoiw3vlj2qnbstihqviy0lirxb.lambda-url.ap-south-1.on.aws/"


def lambda_handler(event, context):

    try:

        # Fetch data from Instructor API
        response = requests.get(API_URL, timeout=30)
        response.raise_for_status()

        api_response = response.json()

        # Save raw API response to S3
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key="raw/api_response.json",
            Body=json.dumps(api_response),
            ContentType="application/json"
        )

        # Create DataFrame
        df = pd.DataFrame(api_response["data"])

        rows_before = len(df)

        print(f"Rows before cleaning: {rows_before}")

        # Remove duplicate records
        df.drop_duplicates(inplace=True)

        rows_after = len(df)

        print(f"Rows after cleaning: {rows_after}")

        # Convert DataFrame to Parquet
        parquet_buffer = BytesIO()

        df.to_parquet(
            parquet_buffer,
            engine="pyarrow",
            index=False
        )

        # Upload Parquet file to S3
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key="parquet/sales_data.parquet",
            Body=parquet_buffer.getvalue()
        )

        print("Parquet file uploaded successfully.")

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Data fetched from API and stored as Parquet",
                "rows_before_cleaning": rows_before,
                "rows_after_cleaning": rows_after,
                "duplicates_removed": rows_before - rows_after,
                "parquet_file": "parquet/sales_data.parquet"
            })
        }

    except requests.exceptions.RequestException as e:

        print(f"API Error: {str(e)}")

        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": f"API Error: {str(e)}"
            })
        }

    except Exception as e:

        print(f"Processing Error: {str(e)}")

        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": str(e)
            })
        }
