# README
The following code is designed to rotate Clickhouse Cloud database password using AWS Lambda Service. After password rotating, code will update AWS SecretsManager secret.

The following environments must be provided:

```
CLICKHOUSE_CLOUD_API_SECRET_NAME = "" # Name of secrets manager secret that contains ClickHouse cloud API token with write permissions
ENVIRONMENT = "" # Environment name, could be anything you want, refers to function/secret name
CL_CLOUD_API = "https://api.clickhouse.cloud/v1" # Moved to env in case it will be changed later
ORGANIZATION_ID = "" # Your Clickhouse Cloud organization ID
SERVICE_NAME = "" # Your Clickhouse Cloud service (database) name
```

Code expects the name of secrets manager secret to be modified has the following structure: `<ENVIRONMENT>-clickhouse-credentials`.

If you don’t want to update secret, comment `update_secret(new_password=new_password)` line