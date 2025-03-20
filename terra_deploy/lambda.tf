resource "aws_lambda_function" "user_auth" {
  filename      = "lambda/user_auth.zip"
  function_name = "UserAuthLambda"
  role          = aws_iam_role.lambda_exec.arn
  handler       = "lambda_function.lambda_handler"
  runtime       = "python3.12"
}

resource "aws_lambda_function" "energy_input" {
  filename      = "lambda/energy_input.zip"
  function_name = "EnergyDataInput"
  role          = aws_iam_role.lambda_exec.arn
  handler       = "lambda_function.lambda_handler"
  runtime       = "python3.12"
}