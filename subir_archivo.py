import base64
import boto3

def lambda_handler(event, context):
    # Entrada (json)
    if event["body"] is None:
        return {
            'statusCode': 400,
            'message': 'No se ha enviado el nombre del bucket'
        }
    
    required_keys = ["bucket_name", "file_name", "bucket_folder", "file_str"]
    key_bools= any([key not in event["body"] for key in required_keys])
    if key_bools:
        keys_to_request = [key for key in key_bools if key not in event["body"]]
        return {
            'statusCode': 400,
            'message': f'No se han enviado los siguientes datos: {keys_to_request}'
        }

    json_body = event["body"]

    bucket_name = json_body["bucket_name"]
    file_name = json_body["file_name"]
    folder_name = json_body["bucket_folder"]
    base_64_str = json_body["file_str"]

    # Proceso: Subir un archivo a un bucket a partir de un string en base64
    s3 = boto3.client("s3")
    response = s3.put_object(Bucket=bucket_name, Key=f"{folder_name}/{file_name}",
                             Body=base64.b64decode(base_64_str))

    return {
        "statusCode": 200,
        "file_path": f"{bucket_name}/{folder_name}/{file_name}",
        "response": response
    }

