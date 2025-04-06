import json
import boto3
import os

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['PRODUCTS_TABLE'])

def handler(event, context):
    try:
        # Get product ID from path parameters
        product_id = event['pathParameters']['id']
        
        # Check if product exists
        response = table.get_item(Key={'id': product_id})
        if 'Item' not in response:
            return {
                'statusCode': 404,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': 'Product not found'})
            }
        
        # Delete product from DynamoDB
        table.delete_item(Key={'id': product_id})
        
        # Return success response
        return {
            'statusCode': 204,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            }
        }
    except Exception as e:
        # Return error response
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': str(e)})
        }
