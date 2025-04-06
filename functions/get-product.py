import json
import boto3
import os
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['PRODUCTS_TABLE'])

def handler(event, context):
    try:
        # Get product ID from path parameters
        product_id = event['pathParameters']['id']
        
        # Query DynamoDB for the product
        response = table.get_item(Key={'id': product_id})
        
        # Check if product exists
        if 'Item' not in response:
            return {
                'statusCode': 404,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': 'Product not found'})
            }
        
        # Return product data
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(response['Item'])
        }
    except Exception as e:
        # Return error response
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': str(e)})
        }
