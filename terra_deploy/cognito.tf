resource "aws_cognito_user_pool" "user_pool" {
  name = var.cognito_user_pool_name
}

resource "aws_cognito_user_pool_client" "user_pool_client" {
  name         = "HomeEnergyAppClient"
  user_pool_id = aws_cognito_user_pool.user_pool.id
}