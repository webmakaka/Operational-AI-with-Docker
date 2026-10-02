## Chapter 6: Protocol-based AI Integration with MCP

https://github.com/docker/mcp-gateway

https://registry.modelcontextprotocol.io/

<br/>

### Installation and setup

```
$ mkdir -p ~/.docker/cli-plugins/

$ curl -fsSL https://github.com/docker/mcp-gateway/releases/download/v0.44.1/docker-mcp-linux-amd64.tar.gz | tar -xz -C ~/.docker/cli-plugins/
```

<br/>

```shell
$ docker mcp --version
v0.44.1
```

<br/>


```shell
$ sudo apt-get install -y docker-secrets-engine docker-secrets-engine-plugins
```

<br/>

```shell
// FAIL!
$ docker mcp secret ls
secrets engine is not available: unavailable: dial unix /home/marley/.cache/docker-secrets-engine/engine.sock: connect: no such file or directory
```


<br/>

### Enable MCP toolkit

```shell
// Actually not needed
// $ docker mcp catalog create my-local-catalog:latest --from-community-registry registry.modelcontextprotocol.io
Fetched 24721 servers from registry.modelcontextprotocol.io
  Total in registry: 38462
  Imported:          24721
    OCI (stdio):     828
    Remote:          23893
  Skipped:           13741
    npm:             8739
    pypi:            3592
    mcpb:            673
    no packages:     468
    nuget:           120
    oci:             99
    cargo:           50
Catalog my-local-catalog:latest created
```

<br/>

```shell
// $ docker mcp catalog rm my-local-catalog:latest
```


<br/>

```shell
$ docker mcp catalog pull mcp/docker-mcp-catalog:latest
$ docker mcp catalog show mcp/docker-mcp-catalog
```


<br/>

```shell
$ docker mcp catalog ls
Reference | Digest | Title
mcp/docker-mcp-catalog:latest	| a72d41e7a13b4ec8bb5756d6bef1dbd620045a114b7aa1e1993a678d8be77f9c	| Docker MCP Catalog
```

<br/>

```shell
$ docker mcp catalog show mcp/docker-mcp-catalog
```

<br/>

### Enable your first MCP server

<br/>

```shell
$ docker mcp profile create --name dev_tools
```

<br/>

```shell
$ docker mcp profile server add dev_tools --server catalog://mcp/docker-mcp-catalog/github-official
Added 1 server(s) to profile dev_tools
```

<br/>

```shell
$ docker mcp profile server ls --filter profile=dev_tools
PROFILE   | TYPE  | IDENTIFIER     
dev_tools | image | github-official
```

<br/>

### [SKIP] Managing secrets securely

```shell
$ echo your_github_pat_here > token.txt
$ cat token.txt | docker mcp secret set github.personal_access_token
$ rm token.txt
```

<br/>

```shell
$ docker mcp secret ls
```

<br/>

### Adding filesystem MCP server

```shell
$ docker mcp profile server add dev_tools --server catalog://mcp/docker-mcp-catalog/filesystem
```

<br/>

```shell
$ docker mcp profile server ls --filter profile=dev_tools
PROFILE   | TYPE  | IDENTIFIER     
dev_tools | image | filesystem     
dev_tools | image | github-official
```

<br/>

#### Configuring filesystem paths

<br/>

```shell
$ docker mcp profile config dev_tools --set filesystem.paths='["/home/marley/Documents", "/home/marley/Pictures"]'
```

<br/>

```shell
$ docker mcp profile config dev_tools --get-all
filesystem.paths=[/home/marley/Documents /home/marley/Pictures]
```

<br/>

### Adding Firecrawl MCP server

```shell
$ docker mcp profile server add dev_tools --server catalog://mcp/docker-mcp-catalog/firecrawl
```

<br/>

```shell
$ echo "fc-your_api_key_here" > firecrawl_key.txt
$ cat firecrawl_key.txt | docker mcp secret set firecrawl.api_key
$ rm firecrawl_key.txt
```

<br/>

```shell
$ docker mcp secret ls
```

<br/>

```shell
$ docker mcp profile server ls --filter profile=dev_tools
```

<br/>

### [TODO] Connecting AI clients

### [TODO] Running the local MCP gateway for development

<br/>

## 

 - [Running the local MCP Gateway for development](https://github.com/ajeetraina/Operational-AI-with-Docker/tree/main/chap-06/local-mcp-gateway)
 - [Demonstrating Docker Compose with secrets](https://github.com/ajeetraina/Operational-AI-with-Docker/tree/main/chap-06/local-mcp-gateway-secrets)
 - [Run a PostgreSQL database and connect it to the MCP Gateway
](https://github.com/ajeetraina/Operational-AI-with-Docker/tree/main/chap-06/local-mcp-gateway-database)
 

