# Google OAuth setup

1. Create a Google Cloud project.
2. Configure the OAuth consent screen and create an OAuth client ID.
3. Add authorized JavaScript origins, such as https://example.amplifyapp.com and http://localhost:5173.
4. Add the redirect URI https://<your-domain>/oauth/callback.
5. Store the client secret in AWS Secrets Manager or SSM Parameter Store and pass it to the SAM deployment as the Google client secret parameter.
6. Do not commit the secret to source control.
