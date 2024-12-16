# Final Project Big Data dan Data Lakehouse
## Anggota Kelompok
| Nrp | Anggota Kelompok |
| --- | --- |
| 5027221031 | Gavriel Pramuda Kurniaadi |
| 5027221049 | Arsyad Rizantha M.S. |
| 5027221050 | Jody Hezekiah T.S. |
| 5027221059 | M. Ida Bagus Rafi Habibie |

## Overview
Implementasi Data Lakehouse pada Tokopedia

## Dataset
https://www.kaggle.com/datasets/farhan999/tokopedia-product-reviews/data

## Arsitektur
![arsi](img/image.png)

## Cara menjalankan
### Tahap Awal
run docker
```bash
docker-compose up -d
```

kafka
```bash
docker exec -it kafka kafka-topics.sh --create --topic product-review --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
docker exec -it kafka kafka-topics.sh --create --topic product-input --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
```

### Login Minio
```txt
minio/minio123
```

### Tahap 1 (preset)
```bash
cd preset
python3 producer.py
python3 consumer.py
python3 train.py
```
atau bash start.sh dan liat pada minio untuk memastikan apakah sudah selesai

### Tahap 2 (main)
```bash
cd main
python3 api/app.py 
python3 kafka/consumer.py
```

web
```bash
cd main/web
python3 -m http.server 8080
```