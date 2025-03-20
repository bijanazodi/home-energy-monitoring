module "api_gateway" {
  source = "./modules/api_gateway"
}

module "lambda" {
  source = "./modules/lambda"
}

module "dynamodb" {
  source = "./modules/dynamodb"
}

module "s3" {
  source = "./modules/s3"
}

module "cognito" {
  source = "./modules/cognito"
}

module "sns" {
  source = "./modules/sns"
}