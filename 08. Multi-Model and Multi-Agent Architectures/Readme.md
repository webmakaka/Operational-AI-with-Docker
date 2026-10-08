# Chapter 08: Multi-Model and Multi-Agent Architectures


### Firecrawl API key

https://firecrawl.dev/


In this section, we're going to build a research assistant that can actually search the web, analyze results, and write coherent reports. The multi-agent research assistant will be composed of four specialized services: a coordinator, searcher, analyzer, and writer. We will begin by understanding why breaking the system into multiple agents provides scalability, cost efficiency, and easier debugging compared to a monolithic approach. Then, we will define the overall architecture, where agents communicate through Redis and HTTP APIs, and implement the full project structure using Docker Compose. Each agent is built as an independent Flask service with its own responsibility: the coordinator plans research queries, the searcher retrieves web data using the Firecrawl API, the analyzer extracts structured insights from results, and the writer generates a polished research report. We will configure different models for each role, containerize the agents with Dockerfiles, and orchestrate everything with Compose. Finally, we will test the full pipeline and trace the end-to-end execution flow to understand how the agents collaborate to produce a final answer.
