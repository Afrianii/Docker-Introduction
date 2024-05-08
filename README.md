# PostgreSQL Docker

1. Create folder postgresql
2. Create docker-compose.yml
3. docker-compose.yml Code:
```
version: '14'
services:
  src_db:
    image: postgres:15
    container_name: src_db
    environment:
      - .env
    volumes:
      - /var/lib/postgresql/data
    ports:
      - "5436:5432"
  tgt_db:
    image: postgres:15
    container_name: tgt_db
    environment:
      - .env
    volumes:
      - /var/lib/postgresql/data
    ports: 
    - "5433:5432"
```
4. Create `.env` file with this code:
```
SOURCE_DB_HOST=source_db
SOURCE_DB_NAME=sourcedb
SOURCE_DB_USER=source_postgres
SOURCE_DB_PASS=source_password

TARGET_DB_HOST=source_db  
TARGET_DB_NAME=targetdb
TARGET_DB_USER=target_postgres
TARGET_DB_PASS=target_password
```
5. Go to postgresql directory 
6. jalankan docker dengan command `docker compose up`
7. Membuat koneksi dengan postgresql menggunakan extension mysql di VSCode

Sumber data yang digunakan : https://www.kaggle.com/datasets/juanmerinobermejo/smartphones-price-dataset
