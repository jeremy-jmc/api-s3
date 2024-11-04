import boto3

def lambda_handler(event, context):
    # Entrada (json)
    if event["body"] is None:
        return {
            'statusCode': 400,
            'message': 'No se ha enviado el nombre del bucket'
        }
    elif "bucket_name" not in event["body"] or "directory" not in event["body"]:
        return {
            'statusCode': 400,
            'message': 'No se ha enviado el nombre del bucket (bucket_name)'
        }

    bucket_name = event["body"]["bucket_name"]
    directory_name = event["body"]["directory"]

    # Proceso: Crear un directorio en un bucket
    s3 = boto3.client("s3")
    try:
        response = s3.put_object(Bucket=bucket_name, Key=(f"{directory_name}/"))    # , ACL='public-read-write'

        return {
            'statusCode': 200,
            'bucket_name': bucket_name,
            'directory': directory_name,
            'response': response
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "message": f"Error: {str(e)}"
        }

