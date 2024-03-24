# QBMin

This uses docker to automate deploying either rqiner or qubic.li miner on your Qubic rigs.

Let's assume we have a simple setup:

1. A main computer where you want to control rigs from.
2. A number of rigs accessible from the network.

Note: This was built using python 3.11, I have no idea if it's compatible with earlier python versions. It depends on no external dependencies, only Python standard library.

# How-to?

## 1. Pick a main computer to control the rigs from.

## 2. Install linux and docker on your rigs and on the "control" computer.

https://docs.docker.com/engine/install/

## 3. Install an SSH server on your rigs.

Example:

```
sudo apt-get install openssh-server
```

## 4. Add automatic SSH login from your control computer to the rigs.

Example:

```
ssh-copy-id user@righostname
```

## 5. On the main computer, create docker contexts for each rig.

```
docker context create a_unique_name_for_rig --docker host=ssh://my_user@my_rig_hostname
```

Note: You'll already have a `default` docker context corresponding to the main computer.

If you forget the name of the docker context, use `docker context ls` to list docker contexts.

## 6. Configure config.json to your liking.

Copy `config.json.example` to a new file called `config.json`. Edit it to fit your needs.

It needs to be valid JSON and follow this format.

Example: (Remove the `# ...` comments!)

```
{
  "rigs": [
    # Example rig qith rqiner:
    {
      "context": "default",    # This is the name of the docker context setup on step 5 for this rig.
      "thread_count": "24",    # How many threads to run miner with.
      "label": "debrah-5900X", # A label to identify this rig.
      "miner": "rqiner",       # Either `qli` or `rqiner`.
      "miner_url": "https://github.com/Qubic-Solutions/rqiner-builds/releases/download/v0.3.14/rqiner-x86-znver3", # Which miner to download on this rig. See https://github.com/Qubic-Solutions/rqiner-builds/releases/ for the full list of available rqiner.
      "token": "YWLETVKDAQEHXDDUMGBHCFZBWYQCVWTLOZLWTNFHBEJPBWULIVFNGOMAERRK" # The Wallet ID you want to send QUs to if you're using
    },
    # Example rig qith qubic.li miner:
    {
      "context": "debbie" ,    # This is the name of the docker context setup on step 5 for this rig.
      "thread_count": "32",    # How many threads to run miner with.
      "label": "debrah-7950X", # A label to identify this rig.
      "miner": "qli",          # Either `qli` or `rqiner`.
      "miner_url": "https://dl.qubic.li/downloads/qli-Client-1.8.10-Linux-x64.tar.gz", # Which miner to download on the rig. See https://github.com/qubic-li/client/ for available qubic.li miner versions.
      "token": "ey..."         # Your qubic.li access token.
    }
  ]
}
```

# Usage

## Deploy miners on all rigs.

```
./deploy.py deploy
```

## Stop miners on all rigs.

```
./deploy.py stop
```

## Show aggregated logs.

```
./deploy.py logs
```
