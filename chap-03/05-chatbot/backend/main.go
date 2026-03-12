package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
)

// ChatRequest is the payload the frontend sends to the backend.
type ChatRequest struct {
	Message string `json:"message"`
}

// ChatResponse is what the backend returns to the frontend.
type ChatResponse struct {
	Reply string `json:"reply"`
}

// dmrRequest matches the OpenAI chat completions request format.
type dmrRequest struct {
	Model    string        `json:"model"`
	Messages []dmrMessage  `json:"messages"`
}

type dmrMessage struct {
	Role    string `json:"role"`
	Content string `json:"content"`
}

// dmrResponse matches the OpenAI chat completions response format.
type dmrResponse struct {
	Choices []struct {
		Message dmrMessage `json:"message"`
	} `json:"choices"`
}

func chatHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Access-Control-Allow-Origin", "*")
	w.Header().Set("Access-Control-Allow-Headers", "Content-Type")
	if r.Method == http.MethodOptions {
		w.WriteHeader(http.StatusOK)
		return
	}

	var req ChatRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, "invalid request", http.StatusBadRequest)
		return
	}

	// LLM_URL and LLM_MODEL are injected by Docker Compose from the models: binding.
	llmURL := os.Getenv("LLM_URL")
	llmModel := os.Getenv("LLM_MODEL")
	if llmURL == "" {
		llmURL = "http://model-runner.docker.internal/engines/v1"
	}
	if llmModel == "" {
		llmModel = "ai/smollm2"
	}

	payload := dmrRequest{
		Model: llmModel,
		Messages: []dmrMessage{
			{Role: "user", Content: req.Message},
		},
	}

	body, _ := json.Marshal(payload)
	resp, err := http.Post(
		llmURL+"/chat/completions",
		"application/json",
		bytes.NewReader(body),
	)
	if err != nil {
		http.Error(w, fmt.Sprintf("model runner error: %v", err), http.StatusBadGateway)
		return
	}
	defer resp.Body.Close()

	respBody, _ := io.ReadAll(resp.Body)
	var dmrResp dmrResponse
	if err := json.Unmarshal(respBody, &dmrResp); err != nil || len(dmrResp.Choices) == 0 {
		http.Error(w, "unexpected response from model runner", http.StatusBadGateway)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(ChatResponse{Reply: dmrResp.Choices[0].Message.Content})
}

func healthHandler(w http.ResponseWriter, r *http.Request) {
	w.WriteHeader(http.StatusOK)
	w.Write([]byte("ok"))
}

func main() {
	http.HandleFunc("/chat", chatHandler)
	http.HandleFunc("/health", healthHandler)
	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}
	log.Printf("Go backend listening on :%s", port)
	log.Fatal(http.ListenAndServe(":"+port, nil))
}
