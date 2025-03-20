resource "aws_s3_bucket" "csv_bucket" {
  bucket = var.s3_bucket_name

  tags = {
    Name        = "EnergyCSVBucket"
    Environment = "dev"
  }
}