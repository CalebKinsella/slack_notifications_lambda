module "lambda_function" {
  source = "terraform-aws-modules/lambda/aws"

  function_name = "notifitcations-${var.environment}"
  description   = "My awesome lambda function"
  handler       = "handler.lambda_handler"
  runtime       = "python3.8"

  source_path = "./app"

  tags = {
    Name = "terraform managed notifications"
  }
}