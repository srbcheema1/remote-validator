# Remote-Validator

A network interface to run vcf-validator as a service. To allow users to validate their own remote files, or even a dynamically generated VCF stream.

## Setting up environment

You can set up a virtual environment to install the dependencies:
```
    python3 -m venv env
    source ./env/bin/activate
    pip insall -r reqirements.txt
```

## compiling proto files
server and client needs compiled proto files to run:
```
    make compile
```

to validate the file:

    1. start the server
    2. run client with input the vcf stream from stdin you may use < operator

```
    ./client.py < vcf-file
```

