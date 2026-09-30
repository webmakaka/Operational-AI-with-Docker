# Understanding AI Models in Docker

https://github.com/docker/model-runner

<br/>

```shell
$ sudo apt-get install docker-model-plugin
```

<br/>

```shell
$ docker model version
Client:
 Version:    v1.2.6
 OS/Arch:    linux/amd64

Server:
 Version:    (not reachable)
 Engine:     Docker Engine
```


<br/>

```shell
$ docker model pull smollm2:360M-Q4_K_M
```

<br/>

```shell
$ docker model tag smollm2:360M-Q4_K_M registry.example.com/myteam/smollm2:360M-Q4_K_M
```

<br/>


```shell
$ docker model push registry.example.com/myteam/smollm2:360M-Q4_K_M
```


<br/>

```shell
$ nvidia-smi
```

<br/>

```
// required
cuda>=13.3
```

<br/>

```
Driver Version: 595.91.07
CUDA Version: 13.2
```

<br/>


```shell
$ sudo apt update
$ apt policy nvidia-driver-*
$ ubuntu-drivers devices
```

<br/>


```shell
// $ sudo apt update
// $ sudo apt install nvidia-driver-610-open -y
// $ sudo reboot
```

<br/>


```shell
$ sudo ubuntu-drivers install
$ sudo reboot
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
