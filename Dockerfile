FROM python:3.12-slim

# 这个/app是容器内的路径，不是这里本地的app目录，也就是说容器拥有自己单独的文件系统视图
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt ./

# RUN在构建镜像时执行
RUN python -m pip install --no-cache-dir -r requirements.txt

COPY app ./app

EXPOSE 8000

# CMD指定启动容器时默认执行的命令
CMD ["python", "-m", "uvicorn", "app.api_server:app", "--host", "0.0.0.0", "--port", "8000"]