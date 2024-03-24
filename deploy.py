#!/bin/env python3

from asyncio.subprocess import PIPE, STDOUT
from signal import SIGINT, SIGTERM
from threading import Thread
from typing import TypeAlias, TypedDict, List
import asyncio
import json
import subprocess
import sys

CONFIG_FILE = "config.json"
LOG_TAIL_N = "10"
READLINE_TIMEOUT = 0.1

class Rig(TypedDict):
    context: str
    thread_count: str
    label: str
    rqminer_url: str
    public_id: str
    
Rigs: TypeAlias = List[Rig]
Procs: TypeAlias = List[asyncio.subprocess.Process]


async def deploy_one(
    context: str,
    rq_miner_url: str,
    thread_count: str,
    label: str,
    public_id: str,
    procs: Procs
) -> None:
    await subprocess_capture(
        "docker",
        f"--context={context}",
        "build",
        "--progress=plain",
        f"--build-arg=RQMINER_URL={rq_miner_url}",
        f"--build-arg=THREAD_COUNT={thread_count}",
        f"--build-arg=LABEL={label}",
        f"--build-arg=PUBLIC_ID={PUBLIC_ID}",
        ".",
        "-t",
        "miner",
        rig_name=context,
        procs=procs,
    )
    await subprocess_capture(
        "docker",
        f"--context={context}",
        "run",
        "--rm",
        "-d",
        "--name=miner",
        "miner",
        rig_name=context,
        procs=procs,
    )


async def deploy(rigs: Rigs, procs: Procs) -> None:
    async with asyncio.TaskGroup() as tg:
        for conf in rigs:
            tg.create_task(
                deploy_one(
                    conf["context"],
                    conf["rqminer_url"],
                    conf["thread_count"],
                    conf["label"],
                    conf["public_id"],
                    procs=procs,
                )
            )


async def stop_one(context, procs: Procs) -> Thread:
    await subprocess_capture(
        "docker",
        f"--context={context}",
        "stop",
        "miner",
        rig_name=context,
        procs=procs,
    )


async def stop(rigs: Rigs, procs: Procs) -> None:
    async with asyncio.TaskGroup() as tg:
        for conf in rigs:
            tg.create_task(stop_one(conf["context"], procs=procs))


async def log_one(context: str, procs: Procs) -> None:
    await subprocess_capture(
        "docker",
        f"--context={context}",
        "logs",
        "-n",
        LOG_TAIL_N,
        "--follow",
        "miner",
        rig_name=context,
        procs=procs,
    )


async def logs(rigs: Rigs, procs: Procs) -> None:
    async with asyncio.TaskGroup() as tg:
        for conf in rigs:
            tg.create_task(log_one(conf["context"], procs=procs))


async def subprocess_capture(*command: List[str], rig_name: str, procs: Procs) -> None:
    proc = await asyncio.create_subprocess_exec(*command, stdout=PIPE, stderr=STDOUT)
    procs.append(proc)

    command_str = " ".join(command)
    prefix = f"PID: {proc.pid}, {rig_name}> "
    print(f"{prefix}{command_str}")

    while True:
        try:
            line = (await asyncio.wait_for(proc.stdout.readline(), READLINE_TIMEOUT)).decode("utf8")
        except asyncio.TimeoutError:
            continue
        else:
            if not line:
                break

            print(f"{prefix}{line}", end="")


def get_rigs(config_file: str) -> Rigs:
    return json.loads(open(config_file).read())["rigs"]


def print_usage() -> None:
    print(
        "Usage: deploy.py COMMAND [CONFIGFILE]\n"
        "\n"
        "Commands:\n"
        "  deploy:  Deploy miners.\n"
        "  stop:    Stop miners.\n"
        "  logs:    Show miner logs.\n"
        "\n"
        "CONFIGFILE defaults to \"config.json\""
    )


async def main() -> None:
    config_file = CONFIG_FILE if len(sys.argv) == 2 else sys.argv[2]
    rigs = get_rigs(config_file)
    loop = asyncio.get_running_loop()

    procs = []

    def killer():
        for proc in procs:
            print(f"Killing subprocess {proc}...")
            proc.kill()

    for signal in [SIGINT, SIGTERM]:
        loop.add_signal_handler(signal, killer)

    if sys.argv[1] == "deploy":
        await deploy(rigs, procs)

    if sys.argv[1] == "stop":
        await stop(rigs, procs)

    if sys.argv[1] == "logs":
        await logs(rigs, procs)


if __name__ == "__main__":
    if len(sys.argv) not in (2, 3):
        print_usage()
        sys.exit(1)

    asyncio.run(main())
