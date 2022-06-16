FROM python:3.9-slim-buster

WORKDIR /usr/src/app

COPY . .

RUN pip install --no-cache-dir --upgrade -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN rm requirements.txt

CMD [ "python3", "bot.py" ]