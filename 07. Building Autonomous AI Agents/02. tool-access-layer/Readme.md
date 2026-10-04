## Tool Access Layer

https://hub.docker.com/r/docker/mcp-gateway/tags

<br/>

```shell
$ docker mcp secret ls
secrets engine is not available: unavailable: dial unix /home/marley/.cache/docker-secrets-engine/engine.sock: connect: no such file or directory
```

<br/>

```shell
$ cp mcp-secrets.env.template mcp-secrets.env
```

<br/>

```shell
$ docker compose up --build
```

## Result:

The gateway launches each MCP server as an isolated Docker container with security constraints. The --security-opt no-new-privileges flag prevents privilege escalation. 

```
- github-official: time=2025-12-27T13:37:26.229Z level=INFO msg="starting server" 
  version=v0.26.3
- github-official: GitHub MCP Server running on stdio
- github-official: time=2025-12-27T13:37:26.241Z level=INFO msg="session initialized"
  > github-official: (40 tools) (2 prompts) (5 resourceTemplates)
  
  > firecrawl: (6 tools)
  
> 46 tools listed in 6.29s
> Initialized in 16.93s
> Start stdio server
```

## Test the gateway with a simple tool call:


### List available tools

```shell
$ read -rsp 'Gateway token: ' TOKEN; echo

$ curl -sS -D /tmp/mcp-headers -o /tmp/mcp-init \
  -X POST http://localhost:8811/mcp \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"curl","version":"1.0"}}}'

$ SESSION_ID=$(awk 'tolower($1)=="mcp-session-id:" {gsub("\r","",$2); print $2}' /tmp/mcp-headers)
$ printf 'Session: %s\n' "$SESSION_ID"
$ cat /tmp/mcp-init
```

```shell
$ curl -sS -X POST http://localhost:8811/mcp \
  -H "Authorization: Bearer $TOKEN" \
  -H "Mcp-Session-Id: $SESSION_ID" \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","method":"notifications/initialized"}'

$ curl -sS -X POST http://localhost:8811/mcp \
  -H "Authorization: Bearer $TOKEN" \
  -H "Mcp-Session-Id: $SESSION_ID" \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}' \
  | sed -n 's/^data: //p' \
  | jq -r '.result.tools[].name'
```

<br/>

```
add_comment_to_pending_review
add_issue_comment
add_reply_to_pull_request_comment
assign_copilot_to_issue
create_branch
create_or_update_file
create_pull_request
create_repository
delete_file
fork_repository
get_commit
get_file_contents
get_label
get_latest_release
get_me
get_release_by_tag
get_tag
get_team_members
get_teams
issue_read
issue_write
list_branches
list_commits
list_issue_fields
list_issue_types
list_issues
list_pull_requests
list_releases
list_repository_collaborators
list_tags
merge_pull_request
pull_request_read
pull_request_review_write
push_files
request_copilot_review
search_code
search_commits
search_issues
search_pull_requests
search_repositories
search_users
sub_issue_write
ui_get
update_issue_comment
update_pull_request
update_pull_request_branch
```


<br/>

### Search GitHub repositories (read-only, safe to test)

```shell
$ curl -X POST http://localhost:8811/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "search_repositories",
    "arguments": {
      "query": "docker language:go stars:>1000"
    }
  }'
```
