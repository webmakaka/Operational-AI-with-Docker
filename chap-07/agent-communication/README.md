## Designing agent communication patterns


```
docker compose up --build
```

### Watch the writer publishing events every 5 seconds:


```
writer-1  | 📤 Writer Agent Starting...
writer-1  |    Publishing patches to 'patches' channel
writer-1  | 
writer-1  | 📤 Publishing: patch-001
writer-1  |    Size: 110 bytes
writer-1  | 📤 Publishing: patch-002
writer-1  |    Size: 120 bytes
```

### And the reader picks them up immediately:

```
reader-1  | 👂 Reader Agent Starting...
reader-1  |    Listening for patches on 'patches' channel
reader-1  | 
reader-1  | ✅ Subscribed successfully!
reader-1  | 
reader-1  | 📨 Received: patch-001
reader-1  |    Location: /data/patch-001.diff
reader-1  |    Size: 110 bytes
reader-1  |    Processing patch...
reader-1  | 
reader-1  | 📨 Received: patch-002
reader-1  |    Location: /data/patch-002.diff
reader-1  |    Size: 120 bytes
reader-1  |    Processing patch...
```


What happens when you scale readers? Stop the system with Ctrl+C, then restart with three readers:


```
docker compose up --build --scale reader=3
```

Now watch—all three readers receive the same events:

```
writer-1  |    Size: 120 bytes
reader-1  | 📨 Received: patch-002
reader-2  | 📨 Received: patch-002
reader-3  | 📨 Received: patch-002
reader-1  |    Location: /data/patch-002.diff
reader-2  |    Location: /data/patch-002.diff
reader-3  |    Location: /data/patch-002.diff
reader-1  |    Size: 120 bytes
reader-2  |    Size: 120 bytes
reader-3  |    Size: 120 bytes
```


