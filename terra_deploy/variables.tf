variable "aws_region" {
  default = "us-west-2"
}

variable "dynamodb_table_name" {
  default = "EnergyUsage"
}

variable "s3_bucket_name" {
  default = "home-energy-csv"
}

variable "cognito_user_pool_name" {
  default = "HomeEnergyUserPool"
}

variable "sns_topic_name" {
  default = "EnergyAlerts"
}