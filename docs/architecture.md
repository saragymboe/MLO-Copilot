# Architecture

## Request flow

1. The React app authenticates users through Amazon Cognito with Google federation.
2. The frontend calls the API Gateway HTTP API with Cognito-issued JWTs.
3. Lambda handlers verify the request context and enforce authorization.
4. Product and conversation data is stored in DynamoDB with a single-table design.
5. The scenario analysis and chat endpoints call OpenAI through a shared abstraction that reads the API key from Secrets Manager.

## Authentication flow

Users sign in via the Cognito Hosted UI or managed OAuth flow. The frontend uses AWS Amplify and PKCE with no client secret in browser code.

## Data model

Products are stored as `PRODUCT#{productId}` records with metadata in the `METADATA` record. Conversations and scenarios are stored under the user identity.

## DynamoDB access patterns

- Products: read via `GET /products` and `GET /products/{productId}`.
- Category filtering uses the `GSI1` global secondary index.
- Conversations are isolated by user sub.

## AI retrieval flow

The scenario and chat handlers gather a limited product context set from DynamoDB and send only summaries and sanitized scenario text to OpenAI.

## Deployment flow

GitHub Actions builds and tests the backend and frontend, deploys the SAM stack, and triggers Amplify hosting for the frontend.
