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

resource "aws_lambda_permission" "allow_cloudwatch" {
  statement_id  = "AllowExecutionFromCloudWatch-${var.environment}"
  action        = "lambda:InvokeFunction"
  function_name = module.lambda_function.lambda_function_name
  principal     = "events.amazonaws.com"
  source_arn    = "arn:aws:events:${var.region}:${data.aws_caller_identity.current.account_id}:rule/Codepipeline-${var.appname}-${var.environment}"
#  qualifier     = aws_lambda_alias.test_alias.name
}