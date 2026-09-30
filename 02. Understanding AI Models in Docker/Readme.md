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


<br/>


```shell
// ERROR! Cuda Error!
$ docker model list
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
$ sudo apt update
$ sudo apt install nvidia-driver-610-open -y
$ sudo reboot
```

<br/>

```shell
$ nvidia-smi
Wed Sep 30 21:53:38 2026       
+-----------------------------------------------------------------------------------------+
| NVIDIA-SMI 610.57.04              KMD Version: 610.57.04     CUDA UMD Version: 13.3     |
+-----------------------------------------+------------------------+----------------------+
| GPU  Name                 Persistence-M | Bus-Id          Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |           Memory-Usage | GPU-Util  Compute M. |
|                                         |                        |               MIG M. |
|=========================================+========================+======================|
|   0  NVIDIA GeForce GTX 1650        Off |   00000000:01:00.0  On |                  N/A |
|  0%   51C    P0            N/A  /   75W |     580MiB /   4096MiB |     39%      Default |
|                                         |                        |                  N/A |
+-----------------------------------------+------------------------+----------------------+
```

<br/>

```
$ docker model list
MODEL NAME           PARAMETERS  QUANTIZATION    ARCHITECTURE  MODEL ID      CREATED        CONTEXT  SIZE        
smollm2:360M-Q4_K_M  361.82 M    IQ2_XXS/Q4_K_M  llama         354bf30d0aa3  18 months ago           256.35 MiB  
```
