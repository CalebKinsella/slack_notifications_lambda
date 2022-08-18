module "lambda_function" {
  source = "terraform-aws-modules/lambda/aws"

  function_name = "notifitcations-${var.environment}"
  description   = "My awesome lambda function"
  handler       = "handler.lambda_handler"
  runtime       = "python3.8"

  source_path = "./notifications"
  environment_variables = {
    "SLACK_WEBHOOK_URL" : var.SLACK_WEBHOOK_URL,
    "SLACK_CHANNEL" : var.SLACK_CHANNEL,
    "SLACK_USER" : var.SLACK_USER
  }
  tags = {
    Name = "terraform managed notifications"
  }
}