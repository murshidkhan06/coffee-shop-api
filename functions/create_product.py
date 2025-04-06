import json
import uuid
import boto3
import os
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['PRODUCTS_TABLE'])

def handler(event, context):
    try:
        # Parse request body
        body = json.loads(event.get('body', '{}'))
        
        # Validate required fields
        required_fields = ['name', 'price', 'category']
        for field in required_fields:
            if field not in body:
                return {
                    'statusCode': 400,
                    'headers': {'Content-Type': 'application/json'},
                    'body': json.dumps({'error': f'Missing required field: {field}'})
                }
        
        # Create product item
        timestamp = datetime.utcnow().isoformat()
        item = {
            'id': str(uuid.uuid4()),
            'name': body['name'],
            'price': body['price'],
            'category': body['category'],
            'description': body.get('description', ''),
            'stock': body.get('stock', 0),
            'createdAt': timestamp,
            'updatedAt': timestamp
        }
        
        # Save to DynamoDB
        table.put_item(Item=item)
        
        # Return success response
        return {
            'statusCode': 201,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(item)
        }
    except Exception as e:
        # Return error response
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': str(e)})
        }
