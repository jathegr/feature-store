import pickle
import boto3
from feature_store.config import S3_BUCKET, AWS_REGION

s3 = boto3.client("s3", region_name=AWS_REGION)

class S3Cache:
    def __init__(self, namespace: str):
        self.key = f"{namespace}.pkl"

    def get(self):
        try:
            resp = s3.get_object(Bucket=S3_BUCKET, Key=self.key)
            return pickle.loads(resp["Body"].read())
        except s3.exceptions.NoSuchKey:
            return None

    def set(self, obj):
        s3.put_object(
            Bucket=S3_BUCKET,
            Key=self.key,
            Body=pickle.dumps(obj)
        )