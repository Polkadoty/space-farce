package game

type MessageType string

const (
	// Server -> Client messages
	MsgStateUpdate  MessageType = "game.state_update"
	MsgTurnStart    MessageType = "game.turn_start"
	MsgCombatResult MessageType = "game.combat_result"
	MsgPlayerJoined MessageType = "game.player_joined"
	MsgPlayerLeft   MessageType = "game.player_left"

	// Client -> Server messages
	MsgPlayerReady     MessageType = "player.ready"
	MsgPlayerOrders    MessageType = "player.orders"
	MsgCombatDecisions MessageType = "player.combat_decisions"
)

type Message struct {
	Type    MessageType `json:"type"`
	Payload interface{} `json:"payload"`
}

type StateUpdate struct {
	GameID      string                 `json:"game_id"`
	Turn        int                    `json:"turn"`
	Phase       string                 `json:"phase"`
	PlayerState map[string]PlayerState `json:"player_state"`
}

type PlayerState struct {
	Ready      bool      `json:"ready"`
	Systems    []int     `json:"systems"`
	KnownSpace []int     `json:"known_space"`
	Resources  int       `json:"resources"`
	TechLevels TechLevel `json:"tech_levels"`
}

type TechLevel struct {
	Weapons      int `json:"weapons"`
	Propulsion   int `json:"propulsion"`
	Shields      int `json:"shields"`
	Construction int `json:"construction"`
}
