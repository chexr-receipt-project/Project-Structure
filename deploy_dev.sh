pip install -r requirements.txt --target ./packages
cd packages && zip -r ../deploy.zip . && cd ..
cd api/ && zip -g -r ../deploy.zip . && cd ..
aws s3 cp deploy.zip s3://cherx-files/dev/source.zip
aws lambda update-function-code --function-name cherx_dev --region ap-south-1 --s3-bucket cherx-files --s3-key dev/source.zip