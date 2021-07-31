#!/bin/bash

# Создаем БД
docker exec -it mongo bash -c 'echo "use ugcDb" | mongo';
sleep 5;
# Создаем коллекцию
docker exec -it mongo bash -c 'echo "db.createCollection(\"ugcDb.movie_ratingCollection\")" | mongo';
docker exec -it mongo bash -c 'echo "db.createCollection(\"ugcDb.movie_reviewCollection\")" | mongo';
docker exec -it mongo bash -c 'echo "db.createCollection(\"ugcDb.movie_bookmarkCollection\")" | mongo';
sleep 5;
echo 'MongoDB ready to work';