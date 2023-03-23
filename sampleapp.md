For the sample app, there is a multi-pass deployment necessary because the code needs uploaded to S3, which is not supported directly in a single CFN template.
Instead, we deploy a foundational template which includes a bucket, then use the AWS CLI CloudFormation `package` command to upload our code to an object in that bucket.
Then we can deploy the stack which includes the CodeCommit repo, referencing the new object. This is a "fully native" alternative to using an e.g. Lambda based solution

aws cloudformation create-stack --stack-name foundation --template-body file://foundation.cf.yaml --capabilities CAPABILITY_NAMED_IAM --disable-rollback
BUCKET=$(aws cloudformation describe-stacks --stack-name foundation --query 'Stacks[0].Outputs[?OutputKey==`BucketName`].OutputValue' --output text)
aws cloudformation package --template-file cicd.cf.yaml --s3-bucket $BUCKET --output-template-file rendered.cicd.cf.yaml
aws cloudformation create-stack --template-body file://rendered.cicd.cf.yaml --stack-name cicd --parameters ParameterKey=FoundationStackName,ParameterValue=foundation --capabilities CAPABILITY_NAMED_IAM
