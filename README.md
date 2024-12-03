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


## Cara menjalankan
1. Nyalakan docker
```sh
cd docker
docker-compose up -d
```

2. Config Kafka
```sh
docker exec -it kafka bash
kafka-topics.sh --create --topic product_reviews --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
```