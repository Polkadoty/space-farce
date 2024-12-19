package server

import (
	"github.com/Polkadoty/Space-Farce/internal/config"
	"github.com/Polkadoty/Space-Farce/internal/game"
	"github.com/Polkadoty/Space-Farce/internal/handlers"
	"github.com/gin-gonic/gin"
)

type Server struct {
	router *gin.Engine
	cfg    *config.Config
	games  *game.Manager
}

func New(cfg *config.Config) (*Server, error) {
	s := &Server{
		router: gin.Default(),
		cfg:    cfg,
		games:  game.NewManager(),
	}

	s.setupRoutes()
	return s, nil
}

func (s *Server) setupRoutes() {
	api := s.router.Group("/api/v1")

	// Auth routes
	auth := api.Group("/auth")
	{
		auth.POST("/login", handlers.Login)
		auth.POST("/register", handlers.Register)
		auth.POST("/refresh", handlers.RefreshToken)
	}

	// Game routes
	games := api.Group("/games")
	games.Use(handlers.AuthMiddleware(s.cfg.JWTSecret))
	{
		games.GET("", handlers.ListGames(s.games))
		games.POST("/create", handlers.CreateGame(s.games))
		games.GET("/:id", handlers.GetGame(s.games))
		games.POST("/:id/join", handlers.JoinGame(s.games))
		games.GET("/:id/ws", handlers.GameWebSocket(s.games))
	}
}

func (s *Server) Run() error {
	return s.router.Run(s.cfg.Port)
}
