FROM public.ecr.aws/lambda/python:3.12

RUN dnf install -y git
RUN cd /opt && \
    git clone https://github.com/awslabs/git-secrets.git && \
    cp /opt/git-secrets/git-secrets $( git --exec-path )/

# git-secrets wants a repo to run in so prepare one
RUN mkdir -p /var/run/scan && \
    cd /var/run/scan && \
    git init && \
    git secrets --register-aws

# Copy the function code to the LAMBDA_TASK_ROOT directory
# This environment variable is provided by the lambda base image
COPY index.py ${LAMBDA_TASK_ROOT}

# Set the CMD to the function handler
CMD [ "index.lambda_handler" ]
