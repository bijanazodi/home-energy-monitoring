output "dynamodb_table_name" {
  value = aws_dynamodb_table.energy_usage.name
}

output "s3_bucket_name" {
  value = aws_s3_bucket.csv_bucket.bucket
}

output "cognito_user_pool_id" {
  value = aws_cognito_user_pool.user_pool.id
}

output "sns_topic_arn" {
  value = aws_sns_topic.energy_alerts.arn
}