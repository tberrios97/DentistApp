# Modulo de Computo

## Build and Up
```
docker-compose build && docker-compose up
```

## Test image
```
curl -X POST -F image=@spirals.png 'http://localhost:5000/moco/mod1/predict'

curl -X POST -F image=@waves.png 'http://localhost:5000/moco/mod2/predict'
```