package game

type Player struct {
	ID         string `json:"id"`
	Name       string `json:"name"`
	Ready      bool   `json:"ready"`
	Systems    []int  `json:"systems"`
	KnownSpace []int  `json:"known_space"`
}

func NewPlayer(id, name string) *Player {
	return &Player{
		ID:         id,
		Name:       name,
		Ready:      false,
		Systems:    make([]int, 0),
		KnownSpace: make([]int, 0),
	}
}
