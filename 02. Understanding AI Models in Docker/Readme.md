# Understanding AI Models in Docker

```shell
$ docker model pull smollm2:360M-Q4_K_M
```


```shell
$ docker model tag smollm2:360M-Q4_K_M registry.example.com/myteam/smollm2:360M-Q4_K_M
```


```shell
$ docker model push registry.example.com/myteam/smollm2:360M-Q4_K_M
```

<br/>


```shell
// Pull (cached locally)
$ docker model pull smollm2:360M-Q4_K_M

// List locally available models
$ docker model list

// Run interactively (CLI)
$ docker model run smollm2:360M-Q4_K_M

// Inspect logs (CLI)
$ docker model logs

// Remove a model
$ docker model rm smollm2:360M-Q4_K_M

// Purge cached model data (be careful)
$ docker model purge
```
