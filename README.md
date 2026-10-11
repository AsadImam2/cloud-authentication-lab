# Cloud Authentication Lab

## Overview
A beginner-friendly Python Flask project demonstrating authentication between two local services.

## Architecture
- **Service A:** Runs on port 5000 and validates user bearer tokens.
- **Service B:** Runs on port 5001 and validates service-to-service authentication.
- Service A calls Service B to retrieve inventory data.

## Technologies
- Python
- Flask
- Requests
- Bearer token authentication
- Environment variables
- Application logging

## Features
- Demo access-token generation with expiration.
- Authentication checks for protected endpoints.
- Service-to-service authentication using an environment variable.
- Logging of authentication successes and failures.
- Inventory API response through Service A.

## Endpoints

| Method | Endpoint     | Purpose |
|--------|--------------|---------|
| POST   | `/api/token` | Generate a demo token |
| GET    | `/api/profile` | Access a protected profile |
| GET    | `/api/inventory` | Retrieve inventory through Service A |
| GET    | `/internal/inventory` | Internal inventory endpoint on Service B |

## Evidence and Test Results

### Service A Logs
![Service A logs](screenshots/service-a-logs.png)

### Service B Logs
![Service B logs](screenshots/service-b-logs.png)

### Inventory API Response
![Inventory response](screenshots/inventory-response.png)

## Security Concepts Practiced
- Authentication and bearer tokens
- Token expiration
- Service-to-service authentication
- Environment-based secret configuration
- Logging and error handling

## Limitations
This is a local educational lab, not a production-ready authentication system. Tokens are stored in memory and reset when Service A restarts. The demo token endpoint does not implement client authentication.

## Disclaimer
Created for educational purposes and authorized security learning only.
