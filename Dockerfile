FROM debian:bookworm-slim

ARG RQMINER_URL
ARG THREAD_COUNT
ARG LABEL
ARG PUBLIC_ID

ENV THREAD_COUNT=$THREAD_COUNT
ENV LABEL=$LABEL
ENV PUBLIC_ID=$PUBLIC_ID

RUN apt-get update
RUN apt-get install -y libicu-dev procps wget
RUN adduser qb
USER qb
WORKDIR /miner
RUN wget $RQMINER_URL -O ./rqminer
RUN chmod +x rqminer
ENTRYPOINT ./rqminer --threads $THREAD_COUNT --id $PUBLIC_ID --label $LABEL
