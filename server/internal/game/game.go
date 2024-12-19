package game

import (
	"errors"
	"sync"
	"time"

	"github.com/gorilla/websocket"
)

var (
	ErrGameFull         = errors.New("game is full")
	ErrConnectionClosed = errors.New("connection closed")
)

type GameState int

const (
	StateWaiting GameState = iota
	StatePlaying
	StateFinished
)

type Game struct {
	ID         string
	Seed       int64
	MaxPlayers int
	State      GameState
	Players    map[string]*Player
	Created    time.Time
	GalaxySize int

	connections map[string]*Connection
	mu          sync.RWMutex
}

func NewGame(id string, seed int64, maxPlayers, galaxySize int) *Game {
	return &Game{
		ID:          id,
		Seed:        seed,
		MaxPlayers:  maxPlayers,
		GalaxySize:  galaxySize,
		State:       StateWaiting,
		Players:     make(map[string]*Player),
		connections: make(map[string]*Connection),
		Created:     time.Now(),
	}
}

func (g *Game) AddPlayer(player *Player) error {
	g.mu.Lock()
	defer g.mu.Unlock()

	if len(g.Players) >= g.MaxPlayers {
		return ErrGameFull
	}

	g.Players[player.ID] = player
	g.broadcastMessage(MsgPlayerJoined, player)
	return nil
}

func (g *Game) RegisterConnection(player *Player, conn *Connection) {
	g.mu.Lock()
	defer g.mu.Unlock()

	g.connections[player.ID] = conn
}

func (g *Game) UnregisterPlayer(player *Player) {
	g.mu.Lock()
	defer g.mu.Unlock()

	delete(g.connections, player.ID)
	delete(g.Players, player.ID)
	g.broadcastMessage(MsgPlayerLeft, player)
}

func (g *Game) HandlePlayerReady(player *Player) {
	g.mu.Lock()
	defer g.mu.Unlock()

	player.Ready = true

	// Check if all players are ready
	allReady := true
	for _, p := range g.Players {
		if !p.Ready {
			allReady = false
			break
		}
	}

	if allReady {
		g.State = StatePlaying
		g.broadcastMessage(MsgTurnStart, nil)
	}
}

func (g *Game) broadcastMessage(msgType MessageType, payload interface{}) {
	for _, conn := range g.connections {
		conn.SendMessage(msgType, payload)
	}
}

func (g *Game) NewConnection(player *Player, conn *websocket.Conn) *Connection {
	return NewConnection(g, player, conn)
}

func (g *Game) NewPlayer(id, name string) *Player {
	return NewPlayer(id, name)
}
