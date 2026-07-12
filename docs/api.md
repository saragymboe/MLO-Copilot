# API reference

## Health

GET /health

Response:

```json
{
  "success": true,
  "data": {
    "status": "ok"
  },
  "requestId": "local"
}
```

## Products

GET /products

GET /products/{productId}

POST /admin/products

PUT /admin/products/{productId}

DELETE /admin/products/{productId}

POST /admin/products/import

## Scenario analysis

POST /scenarios/analyze

Example body:

```json
{
  "scenario": {
    "borrowerScenario": "Self-employed borrower with one year in business",
    "state": "CA",
    "transactionType": "purchase",
    "occupancy": "primary",
    "propertyType": "single_family"
  }
}
```

## Chat

POST /chat

## Conversations

GET /conversations

GET /conversations/{conversationId}

DELETE /conversations/{conversationId}

## Current user

GET /users/me
