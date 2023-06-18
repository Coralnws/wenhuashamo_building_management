# Docker with Python 3.9
FROM python:3.9

# Add these three line to change the source for pip to use in China Mainland
RUN pip install -U pip
RUN pip config set global.index.url http://mirrors.aliyun.com/pypi/simple
RUN pip config set install.trusted-host mirrors.aliyun.com

# Allows docker to cache installed dependencies between builds
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Mounts the application code to the image
COPY . code
WORKDIR /code

# Set environment variables
ENV DJANGO_SETTINGS_MODULE=backend.settings
ENV PYTHONUNBUFFERED=1

# Expose port 8000
EXPOSE 8000

# Start the development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]