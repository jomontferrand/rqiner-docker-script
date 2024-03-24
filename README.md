# QBMin

This uses docker to automate deploying rqiner on your Qubic rigs.

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

It needs to be valid JSON and follow this format.

Examlpe: (Remove the `# ...` comments!)

```
{
  "rigs": [
    {
      "context": "default",    # This is the name of the docker context setup on step 5 for this rig.
      "thread_count": "24",    # How many threads to run rqminer with.
      "label": "debrah-5900X", # A label to identify this rig.
      "rqminer_url": "https://github.com/Qubic-Solutions/rqiner-builds/releases/download/v0.3.14/rqiner-x86-znver3", # Which miner to download on this rig. See https://github.com/Qubic-Solutions/rqiner-builds/releases/tag/v0.3.14 for the full list.
      "public_id": "YWLETVKDAQEHXDDUMGBHCFZBWYQCVWTLOZLWTNFHBEJPBWULIVFNGOMAERRK" # The Wallet ID you want to send QUs to.
    },
    {
      "context": "default",
      "thread_count": "32",
      "label": "debrah-7950X",
      "rqminer_url": "https://github.com/Qubic-Solutions/rqiner-builds/releases/download/v0.3.14/rqiner-x86-znver4",
      "public_id": "YWLETVKDAQEHXDDUMGBHCFZBWYQCVWTLOZLWTNFHBEJPBWULIVFNGOMAERRK"
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
