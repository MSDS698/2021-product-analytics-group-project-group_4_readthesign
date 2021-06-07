ECHO "Hello, World!"
eb init group_4_readthesign-app --region us-west-2 --platform Docker
eb create group_4_readthesign-env --verbose --envvars AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID --envvars AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
