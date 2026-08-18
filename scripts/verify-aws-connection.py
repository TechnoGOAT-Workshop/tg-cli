import boto3

session = boto3.Session(
    profile_name="uts-admin",
    region_name="us-east-1"
)

sts = session.client("sts")

identity = sts.get_caller_identity()

print(f"Account: {identity['Account']}")
print(f"ARN: {identity['Arn']}")