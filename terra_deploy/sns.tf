resource "aws_sns_topic" "energy_alerts" {
  name = var.sns_topic_name
}

resource "aws_sns_topic_subscription" "alert_subscription" {
  topic_arn = aws_sns_topic.energy_alerts.arn
  protocol  = "email"
  endpoint  = "user@example.com"
}