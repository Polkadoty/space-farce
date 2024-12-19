package config

type Config struct {
    Port        string
    JWTSecret   string
    Environment string
}

func Load() *Config {
    // TODO: Load from environment variables
    return &Config{
        Port:        ":8080",
        JWTSecret:   "your-secret-key",
        Environment: "development",
    }
} 