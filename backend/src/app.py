import json
import boto3
import qrcode
import io
import os
from uuid import uuid4

s3 = boto3.client('s3')
BUCKET_NAME = os.environ['QR_BUCKET_NAME']

def lambda_handler(event, context):
    try:
        # Parse request body
        body = json.loads(event['body'])
        content = body.get('content', '')
        
        if not content:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Content is required'})
            }

        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(content)
        qr.make(fit=True)

        # Create image
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Save to bytes
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()

        # Generate unique filename
        filename = f"{uuid4()}.png"

        # Upload to S3
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=filename,
            Body=img_byte_arr,
            ContentType='image/png'
        )

        # Generate presigned URL
        url = s3.generate_presigned_url(
            'get_object',
            Params={'Bucket': BUCKET_NAME, 'Key': filename},
            ExpiresIn=3600
        )

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Credentials': True
            },
            'body': json.dumps({
                'url': url,
                'filename': filename
            })
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
