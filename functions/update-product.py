import json
import boto3
import os
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['PRODUCTS_TABLE'])

def handler(event, context):
    try:
        # Get product ID from path parameters
        product_id = event['pathParameters']['id']
        
        # Parse request body
        body = json.loads(event.get('body', '{}'))
        
        # Check if product exists
        response = table.get_item(Key={'id': product_id})
        if 'Item' not in response:
            return {
                'statusCode': 404,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': 'Product not found'})
            }
        
        # Prepare update expression
        update_expression = 'SET updatedAt = :updatedAt'
        expression_attribute_values = {
            ':updatedAt': datetime.utcnow().isoformat()
        }
        
        # Add fields to update expression
        updateable_fields = ['name', 'price', 'category', 'description', 'stock']
        for field in updateable_fields:
            if field in body:
                update_expression += f', {field} = :{field}'
                expression_attribute_values[f':{field}'] = body[field]
        
        # Update item in DynamoDB
        updated_item = table.update_item(
            Key={'id': product_id},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues='ALL_NEW'
        )
        
        # Return updated product
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(updated_item['Attributes'])
        }
    except Exception as e:
        # Return error response
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': str(e)})
        }
