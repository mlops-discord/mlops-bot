deploy-local:
	@echo "Deploying to local..."
	heroku local

deploy:
	@echo "Deploying to heroku..."
	git push heroku main

