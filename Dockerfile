FROM python:3.9-buster

RUN groupadd -g 1000 user && \
    useradd -m -d /home/user -s /bin/bash -c "User for service" \
    -u 1000 -g 1000 user
COPY requirements.txt /requirements.txt
RUN python -m pip install -r requirements.txt

USER user
COPY ./ /home/user/
WORKDIR /home/user

EXPOSE 3520
CMD ["bash", "start.sh"]