output "bucket_name" {
  description = "Name of the S3 bucket"
  value       = aws_s3_bucket.pipeline.id
}

output "bucket_arn" {
  description = "ARN of the S3 bucket"
  value       = aws_s3_bucket.pipeline.arn
}

output "lambda_function_name" {
  description = "Name of the Lambda function"
  value       = aws_lambda_function.csv_processor.function_name
}

output "lambda_function_arn" {
  description = "ARN of the Lambda function"
  value       = aws_lambda_function.csv_processor.arn
}

output "upload_command" {
  description = "Example AWS CLI command to upload a test CSV"
  value       = "aws s3 cp sample.csv s3://${aws_s3_bucket.pipeline.id}/uploads/sample.csv"
}
