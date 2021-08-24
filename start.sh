alembic upgrade head
python dataset_creator/run.py


# docker run --rm --env-file file.env -p 3520:3520 --name dataset_creator -d -v /home/nortlite/proj/prep/test:/home/user/db --net=host dataset_creator