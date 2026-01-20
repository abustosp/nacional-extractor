# Extractor Nacional Sistema

Extractor dockerizado para `Nacional_Sistema_1.7.0_update.exe`. Usa 7-Zip dentro del contenedor para listar o extraer el contenido sin instalar herramientas en el sistema.

## Requisitos
- Docker
- (Opcional) Docker Compose

## Uso rapido

Construir imagen:
```bash
docker build -t extractor .
```

Listar contenido:
```bash
docker run --rm -u "$(id -u):$(id -g)" -v "$PWD":/data extractor --listar Nacional_Sistema_1.7.0_update.exe
```

Extraer contenido:
```bash
docker run --rm -u "$(id -u):$(id -g)" -v "$PWD":/data extractor Nacional_Sistema_1.7.0_update.exe -o Nacional_Sistema_1.7.0_update_extracted
```

## Uso con Docker Compose

```bash
export UID=$(id -u) GID=$(id -g)
docker compose run --rm extractor --listar Nacional_Sistema_1.7.0_update.exe
docker compose run --rm extractor Nacional_Sistema_1.7.0_update.exe -o Nacional_Sistema_1.7.0_update_extracted
```

## Parametros
- `archivo`: ruta al `.exe`/`.rar`/`.cab` (default: `Nacional_Sistema_1.7.0_update.exe`)
- `-o`, `--output`: carpeta destino (default: nombre del archivo sin extension)
- `--listar`: solo listar contenido sin extraer

## Notas
- El instalador es NSIS; 7-Zip lo maneja sin problemas.
- Los archivos extraidos se escriben en el volumen montado, con tu UID/GID para evitar permisos de root.
