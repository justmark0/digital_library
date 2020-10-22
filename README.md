# Digital library

A site which provides links and materials to study

## Usage
1. Build containers:
```bash
$ docker-compose build
```

2. Run containers:
```bash
$ docker-compose up -d
```
3. Initialize database:
 ```bash
$  docker-compose exec web python3 main.py create_db
```

Now you can open http://127.0.0.1:5000

To stop:
```bash
$ docker-compose down -v
```