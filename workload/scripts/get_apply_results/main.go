package main

import (
	"context"
	"encoding/json"
	"fmt"
	"os"
	"strings"

	tfe "github.com/hashicorp/go-tfe"
)

type ApplyResult struct {
	Status             string `json:"status"`
	ResourcesAdded     int    `json:"resources_added"`
	ResourcesChanged   int    `json:"resources_changed"`
	ResourcesDestroyed int    `json:"resources_destroyed"`
	RunURL             string `json:"run_url"`
}

func main() {
	token := os.Getenv("TF_API_TOKEN")
	runID := os.Getenv("TF_RUN_ID")

	config := &tfe.Config{
		Token: token,
	}

	client, err := tfe.NewClient(config)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error creating client: %s\n", err)
		os.Exit(1)
	}

	run, err := client.Runs.Read(context.Background(), runID)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error reading run: %s\n", err)
		os.Exit(1)
	}

	apply, err := client.Applies.Read(context.Background(), run.Apply.ID)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error reading apply: %s\n", err)
		os.Exit(1)
	}

	logs, err := client.Applies.Logs(context.Background(), apply.ID)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error reading apply logs: %s\n", err)
		os.Exit(1)
	}

	result := ApplyResult{
		Status: string(run.Status),
		RunURL: run.HTTPURL,
	}

	logContent, err := logs.Read(context.Background())
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error reading log content: %s\n", err)
		os.Exit(1)
	}

	// Extract resource changes from logs
	for _, line := range strings.Split(string(logContent), "\n") {
		if strings.Contains(line, "Apply complete!") {
			fmt.Sscanf(line, "Apply complete! Resources: %d added, %d changed, %d destroyed.",
				&result.ResourcesAdded, &result.ResourcesChanged, &result.ResourcesDestroyed)
			break
		}
	}

	jsonResult, err := json.Marshal(result)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error marshalling result: %s\n", err)
		os.Exit(1)
	}

	fmt.Println(string(jsonResult))
}
