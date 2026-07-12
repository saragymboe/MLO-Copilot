# Deployment

## Preferred deployment

Use the GitHub Amplify app integration for the frontend. GitHub Actions deploys the backend and triggers the Amplify deployment.

## AWS parameters

- EnvironmentName
- AllowedOrigins
- OpenAISecretArn
- OpenAIModel
- GoogleClientId
- GoogleClientSecretParameterOrSecretArn
- CognitoDomainPrefix
- FrontendCallbackUrls
- FrontendLogoutUrls
- LogRetentionDays

## Amplify environment variables

Set the Vite variables in Amplify to the deployed Cognito and API values.
