package handlers

import (
	"encoding/json"
	"log"
	"os"
	"path/filepath"

	"github.com/gin-gonic/gin"
)

func GetGalaxy() gin.HandlerFunc {
	return func(c *gin.Context) {
		log.Printf("Method: %s, Path: %s", c.Request.Method, c.Request.URL.Path)
		log.Printf("Headers: %v", c.Request.Header)

		// Read the JSON file
		jsonPath := filepath.Join("data", "galaxy_data.json")
		data, err := os.ReadFile(jsonPath)
		if err != nil {
			log.Printf("Error reading galaxy data: %v", err)
			c.JSON(500, gin.H{"error": "Failed to read galaxy data"})
			return
		}

		// Parse JSON to ensure it's valid
		var galaxy map[string]interface{}
		if err := json.Unmarshal(data, &galaxy); err != nil {
			log.Printf("Error parsing galaxy data: %v", err)
			c.JSON(500, gin.H{"error": "Failed to parse galaxy data"})
			return
		}

		log.Printf("Successfully sending galaxy data")
		c.JSON(200, galaxy)
	}
}
