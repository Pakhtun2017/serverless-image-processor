include .env

ENVIRONMENT ?= staging

bootstrap:
	scripts/cdk-cmd.sh $(ENVIRONMENT)

synth:
	scripts/cdk-cmd.sh $(ENVIRONMENT) synth

deploy:
	scripts/cdk-cmd.sh $(ENVIRONMENT) deploy

destroy:
	scripts/cdk-cmd.sh $(ENVIRONMENT) destroy

