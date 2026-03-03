resource "random_id" "bucket_suffix" {
  byte_length = 4
}

resource "aws_s3_bucket" "pipeline" {
  bucket = "${var.project_name}-${random_id.bucket_suffix.hex}"
}

# Create prefix placeholder objects
resource "aws_s3_object" "uploads_prefix" {
  bucket  = aws_s3_bucket.pipeline.id
  key     = "uploads/"
  content = ""
}

resource "aws_s3_object" "processed_prefix" {
  bucket  = aws_s3_bucket.pipeline.id
  key     = "processed/"
  content = ""
}

resource "aws_s3_object" "reports_prefix" {
  bucket  = aws_s3_bucket.pipeline.id
  key     = "reports/"
  content = ""
}
