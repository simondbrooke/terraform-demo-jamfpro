package main

import (
	"context"
	"encoding/json"
	"fmt"
	"os"

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
	workspaceName := os.Getenv("TF_WORKSPACE")
	organization := os.Getenv("TF_CLOUD_ORGANIZATION")

	if token == "" {
		fmt.Fprintf(os.Stderr, "Error: TF_API_TOKEN environment variable is not set\n")
		os.Exit(1)
	}

	if runID == "" {
		fmt.Fprintf(os.Stderr, "Error: TF_RUN_ID environment variable is not set\n")
		os.Exit(1)
	}

	if workspaceName == "" {
		fmt.Fprintf(os.Stderr, "Error: TF_WORKSPACE environment variable is not set\n")
		os.Exit(1)
	}

	if organization == "" {
		fmt.Fprintf(os.Stderr, "Error: TF_CLOUD_ORGANIZATION environment variable is not set\n")
		os.Exit(1)
	}

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

	if run.Apply == nil {
		fmt.Fprintf(os.Stderr, "Error: No apply data available for this run\n")
		os.Exit(1)
	}

	apply, err := client.Applies.Read(context.Background(), run.Apply.ID)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error reading apply: %s\n", err)
		os.Exit(1)
	}

	result := ApplyResult{
		Status:             string(apply.Status),
		ResourcesAdded:     apply.ResourceAdditions,
		ResourcesChanged:   apply.ResourceChanges,
		ResourcesDestroyed: apply.ResourceDestructions,
		RunURL:             fmt.Sprintf("https://app.terraform.io/app/%s/workspaces/%s/runs/%s", organization, workspaceName, runID),
	}

	jsonResult, err := json.Marshal(result)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error marshalling result: %s\n", err)
		os.Exit(1)
	}

	fmt.Println(string(jsonResult))
}
