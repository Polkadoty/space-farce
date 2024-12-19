# Space Farce Network Protocol

## Core Concepts
1. WebSocket-based communication for real-time updates
2. REST endpoints for game setup and authentication
3. Binary protocol for game state updates
4. Deterministic state synchronization

## REST Endpoints

### Authentication
- POST /api/v1/auth/login
- POST /api/v1/auth/register
- POST /api/v1/auth/refresh

### Game Management
- GET /api/v1/games
- POST /api/v1/games/create
- GET /api/v1/games/{id}
- POST /api/v1/games/{id}/join

### Game State
- GET /api/v1/games/{id}/state
- POST /api/v1/games/{id}/orders

## WebSocket Messages

### Server -> Client
- game.state_update
- game.turn_start
- game.combat_result
- game.player_joined
- game.player_left

### Client -> Server
- player.ready
- player.orders
- player.combat_decisions 