import json
import os
import unittest
from unittest.mock import patch, MagicMock
import uuid
import pytest
from moto import mock_dynamodb

# Set environment variables for testing
os.environ['PRODUCTS_TABLE'] = 'coffee-shop-api-products-test'

# Import functions after setting environment variables
import sys
sys.path.append('./')
from functions.create_product import handler as create_handler
from functions.get_product import handler as get_handler
from functions.list_products import handler as list_handler
from functions.update_product import handler as update_handler
from functions.delete_product import handler as delete_handler

@mock_dynamodb
class TestProductFunctions(unittest.TestCase):
    def setUp(self):
        """Set up test environment"""
        import boto3
        self.dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        
        # Create test table
        self.table = self.dynamodb.create_table(
            TableName=os.environ['PRODUCTS_TABLE'],
            KeySchema=[{'AttributeName': 'id', 'KeyType': 'HASH'}],
            AttributeDefinitions=[{'AttributeName': 'id', 'AttributeType': 'S'}],
            BillingMode='PAY_PER_REQUEST'
        )
        
        # Sample product data
        self.product_id = str(uuid.uuid4())
        self.product = {
            'id': self.product_id,
            'name': 'Test Coffee',
            'price': 4.99,
            'category': 'Espresso',
            'description': 'A test coffee product',
            'stock': 10,
            'createdAt': '2023-01-01T12:00:00',
            'updatedAt': '2023-01-01T12:00:00'
        }
        
        # Add sample product to the test table
        self.table.put_item(Item=self.product)
    
    def test_create_product(self):
        """Test create product function"""
        event = {
            'body': json.dumps({
                'name': 'New Coffee',
                'price': 5.99,
                'category': 'Latte',
                'description': 'A new coffee product',
                'stock': 15
            })
        }
        
        response = create_handler(event, {})
        
        self.assertEqual(response['statusCode'], 201)
        body = json.loads(response['body'])
        self.assertIn('id', body)
        self.assertEqual(body['name'], 'New Coffee')
        self.assertEqual(body['price'], 5.99)
        self.assertEqual(body['category'], 'Latte')
    
    def test_get_product(self):
        """Test get product function"""
        event = {
            'pathParameters': {
                'id': self.product_id
            }
        }
        
        response = get_handler(event, {})
        
        self.assertEqual(response['statusCode'], 200)
        body = json.loads(response['body'])
        self.assertEqual(body['id'], self.product_id)
        self.assertEqual(body['name'], 'Test Coffee')
    
    def test_get_product_not_found(self):
        """Test get product function with invalid ID"""
        event = {
            'pathParameters': {
                'id': 'non-existent-id'
            }
        }
        
        response = get_handler(event, {})
        
        self.assertEqual(response['statusCode'], 404)
    
    def test_list_products(self):
        """Test list products function"""
        event = {}
        
        response = list_handler(event, {})
        
        self.assertEqual(response['statusCode'], 200)
        body = json.loads(response['body'])
        self.assertIn('products', body)
        self.assertIn('count', body)
        self.assertGreaterEqual(body['count'], 1)
    
    def test_update_product(self):
        """Test update product function"""
        event = {
            'pathParameters': {
                'id': self.product_id
            },
            'body': json.dumps({
                'name': 'Updated Coffee',
                'price': 6.99
            })
        }
        
        response = update_handler(event, {})
        
        self.assertEqual(response['statusCode'], 200)
        body = json.loads(response['body'])
        self.assertEqual(body['id'], self.product_id)
        self.assertEqual(body['name'], 'Updated Coffee')
        self.assertEqual(body['price'], 6.99)
        self.assertEqual(body['category'], 'Espresso')  # Unchanged field
    
    def test_delete_product(self):
        """Test delete product function"""
        event = {
            'pathParameters': {
                'id': self.product_id
            }
        }
        
        response = delete_handler(event, {})
        
        self.assertEqual(response['statusCode'], 204)
        
        # Verify product is deleted
        response = get_handler(event, {})
        self.assertEqual(response['statusCode'], 404)

if __name__ == '__main__':
    unittest.main()
