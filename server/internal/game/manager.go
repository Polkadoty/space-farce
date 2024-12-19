package game

import (
	"sync"

	"github.com/google/uuid"
)

type Manager struct {
	games map[string]*Game
	mu    sync.RWMutex
}

func NewManager() *Manager {
	return &Manager{
		games: make(map[string]*Game),
	}
}

func (m *Manager) CreateGame(seed int64, maxPlayers, galaxySize int) (*Game, error) {
	m.mu.Lock()
	defer m.mu.Unlock()

	id := uuid.New().String()
	game := NewGame(id, seed, maxPlayers, galaxySize)
	m.games[id] = game

	return game, nil
}

func (m *Manager) GetGame(id string) (*Game, bool) {
	m.mu.RLock()
	defer m.mu.RUnlock()

	game, exists := m.games[id]
	return game, exists
}

func (m *Manager) ListGames() []*Game {
	m.mu.RLock()
	defer m.mu.RUnlock()

	games := make([]*Game, 0, len(m.games))
	for _, game := range m.games {
		games = append(games, game)
	}
	return games
}
