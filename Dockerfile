# # # FROM public.ecr.aws/lambda/python:3.11

# # # RUN npm install -g npm install -g gcc-c++
# # # RUN npm install java-1.8.0-openjdk-devel -g

# # # COPY requirements.txt ${LAMBDA_TASK_ROOT}
# # # COPY lambda_function.py ${LAMBDA_TASK_ROOT}
# # # RUN pip install -r requirements.txt 
# # # CMD ["lambda_function.handler"]

# # FROM public.ecr.aws/lambda/python:3.11

# # # Install system dependencies
# # RUN yum update -y && \
# #     yum install -y gcc gcc-c++ 
# # Run yum install java-1.8.0-openjdk-devel && \
# #     yum clean all

# # # Copy application files
# # COPY requirements.txt ${LAMBDA_TASK_ROOT}
# # COPY lambda_function.py ${LAMBDA_TASK_ROOT}

# # # Install Python dependencies
# # RUN pip install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

# # # Lambda handler
# # CMD ["lambda_function.handler"]


# FROM public.ecr.aws/lambda/python:3.11

# # Install system dependencies
# RUN yum update -y && \
#     yum install -y gcc gcc-c++ java-1.8.0-openjdk-devel && \
#     yum clean all

# # Copy application files
# COPY requirements.txt ${LAMBDA_TASK_ROOT}
# COPY lambda_function.py ${LAMBDA_TASK_ROOT}

# # Install Python dependencies
# RUN pip install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

# # Lambda handler
# CMD ["lambda_function.handler"] 
FROM python:3.11-slim-bookworm

# Install system build tools and Java for compiling/running submitted code
RUN set -eux; \
    echo 'Acquire::Retries "5"; Acquire::http::Timeout "30"; Acquire::https::Timeout "30";' > /etc/apt/apt.conf.d/99network-retries; \
    apt-get update; \
    apt-get install -y --no-install-recommends --fix-missing \
    g++ \
    openjdk-17-jdk-headless \
    ca-certificates; \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy application files
COPY requirements.txt ./
COPY lambda_function.py ./
COPY app.py ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port and run via gunicorn for production
EXPOSE 8000
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8000", "--workers", "2"]