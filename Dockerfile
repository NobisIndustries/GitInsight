FROM node:current-alpine3.12 as frontend_builder
COPY frontend /workspace/frontend
WORKDIR /workspace/frontend
RUN npm install
RUN npm run build


FROM continuumio/miniconda as app_base
RUN apt-get update -y; apt-get upgrade -y; apt-get install -y tzdata git-all;
# Docker does not adopt the time zone of its host
ENV TZ Europe/Berlin

COPY backend/conda_env.yml /app_setup/env.yml
RUN conda env create -f /app_setup/env.yml; conda clean --all
ENV CONDA_DIR=/opt/conda/envs/GitInsight/bin


FROM app_base as app_full

COPY backend /app/backend
COPY version.txt /app/
COPY --from=frontend_builder /workspace/frontend/dist /app/frontend/dist
EXPOSE 80

ENTRYPOINT $CONDA_DIR/python /app/backend/main.py
