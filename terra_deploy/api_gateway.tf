resource "aws_api_gateway_rest_api" "home_energy_api" {
  name        = "HomeEnergyAPI"
  description = "API Gateway for Home Energy Monitoring"
}

resource "aws_api_gateway_resource" "signup" {
  rest_api_id = aws_api_gateway_rest_api.home_energy_api.id
  parent_id   = aws_api_gateway_rest_api.home_energy_api.root_resource_id
  path_part   = "auth/signup"
}

resource "aws_api_gateway_method" "signup_post" {
  rest_api_id   = aws_api_gateway_rest_api.home_energy_api.id
  resource_id   = aws_api_gateway_resource.signup.id
  http_method   = "POST"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "signup_lambda" {
  rest_api_id             = aws_api_gateway_rest_api.home_energy_api.id
  resource_id             = aws_api_gateway_resource.signup.id
  http_method             = aws_api_gateway_method.signup_post.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.user_auth.invoke_arn
}