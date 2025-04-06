import json
import boto3
import os

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['PRODUCTS_TABLE'])

def handler(event, context):
    try:
        # Get query parameters
        query_params = event.get('queryStringParameters', {}) or {}
        category = query_params.get('category')
        
        # Scan DynamoDB for products
        if category:
            # If category is provided, filter by category
            response = table.scan(
                FilterExpression='category = :category',
                ExpressionAttributeValues={':category': category}
            )
        else:
            # Otherwise, get all products
            response = table.scan()
        
        # Return products
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'products': response['Items'],
                'count': len(response['Items'])
            })
        }
    except Exception as e:
        # Return error response
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': str(e)})
        }
