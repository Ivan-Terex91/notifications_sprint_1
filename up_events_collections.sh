#!/bin/bash

# Создаем БД
docker exec -it mongo bash -c 'echo "use notificationsDb" | mongo';
sleep 5;
# Создаем коллекцию
docker exec -it mongo bash -c 'echo "db.createCollection(\"ugcDb.administration_notificationCollection\")" | mongo';
docker exec -it mongo bash -c 'echo "db.createCollection(\"ugcDb.registration_notificationCollection\")" | mongo';
docker exec -it mongo bash -c 'echo "db.createCollection(\"ugcDb.rating_review_notificationCollection\")" | mongo';
docker exec -it mongo bash -c 'echo "db.createCollection(\"ugcDb.scheduler_bookmarks_notificationCollection\")" | mongo';
sleep 5;
echo 'MongoDB for notifications service ready to work';