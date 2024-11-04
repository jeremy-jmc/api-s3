import boto3
import boto3.exceptions

def lambda_handler(event, context):
    # Entrada (json)
    if event["body"] is None:
        return {
            'statusCode': 400,
            'message': 'No se ha enviado el nombre del bucket'
        }
    elif "bucket_name" not in event["body"]:
        return {
            'statusCode': 400,
            'message': 'No se ha enviado el nombre del bucket (bucket_name)'
        }

    bucket_name = event["body"]["bucket_name"]

    # Proceso: Crear un bucket
    s3 = boto3.client('s3')
    # print(type(s3))
    try:
        response = s3.create_bucket(Bucket=bucket_name, 
                                        ObjectOwnership='BucketOwnerPreferred')

        # Block public access
        s3.put_public_access_block(
            Bucket=bucket_name,
            PublicAccessBlockConfiguration={
                'BlockPublicAcls': True,
                'IgnorePublicAcls': True,
                'BlockPublicPolicy': True,
                'RestrictPublicBuckets': True
            }
        )

        # Change bucket ACL (Access Control List) to public-read-write
        # See: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/client/put_bucket_acl.html
        s3.put_bucket_acl(
            Bucket=bucket_name,
            ACL='public-read-write'
        )

        return {
            'statusCode': 200,
            'bucket_name': bucket_name,
            'response': response
        }
    except s3.exceptions.BucketAlreadyExists:
        return {
            'statusCode': 409,
            'message': f'El bucket {bucket_name} ya existe'
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'message': f'Error: {str(e)}'
        }

