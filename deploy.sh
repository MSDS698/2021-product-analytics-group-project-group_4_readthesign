ECHO "Hello, World!"
eb init group-4-readthesign-app --region us-west-2 --platform Docker
eb create group-4-readthesign-env --verbose --envvars AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID --envvars AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY --key $PEM_NAME
