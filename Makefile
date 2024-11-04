sd:
	serverless deploy
deploy-stage:
	echo "Deploying to stage $(STAGE)"
	serverless deploy --stage $(STAGE)