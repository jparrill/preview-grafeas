# Grafeas

## Overview

Grafeas defines metadata API spec for computing components (e.g., VM images, container images, jar files, scripts) that can assist with aggregations over your metadata. Grafeas uses two API concepts, a note and an occurrence. This division allows 3rd party metadata providers to create and manage metadata on behalf of many customers. Additionally, the division also allows implementation of access control settings that allow fine grain access control.

In grafeas we have two elements, I will use an analogy to make it simple:

- **Notes**: It's the definition of a object that you are looking for EG 'CVE-2017-14159' 
- **Occurrences**: It's the existence of the note on a Docker Container, RPM, Etc... 

## Where we start?

This repository contains an ansible playbook that create a couple of containers, one of the to compile the data _(build time)_ and the other one to expose the API. 

### Requirements

- Fedora/Centos:
  - docker
  - python
  - ansible

### Provision

Execute this command for:

- Minikube
```
curl -Lo minikube https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64 && chmod +x minikube && sudo mv minikube /usr/local/bin/
curl -Lo kubectl https://storage.googleapis.com/kubernetes-release/release/v1.8.0/bin/linux/amd64/kubectl && chmod +x kubectl && sudo mv kubectl /usr/local/bin/
minikube start
kublectl apply -f kubernetes/grafeas.yaml
```

- Minishift
```
curl -Lo /tmp/minishift-1.12.0-linux-amd64.tgz https://github.com/minishift/minishift/releases/download/v1.12.0/minishift-1.12.0-linux-amd64.tgz && tar xvzf /tmp/minishift-1.12.0-linux-amd64.tgz -C /tmp && chmod +x /tmp/minishift-1.12.0-linux-amd64/minishift && sudo mv /tmp/minishift-1.12.0-linux-amd64/minishift /usr/local/bin
minishift start
oc login -u system:admin
oc new-project testgrafeas
oc create -f kubernetes/grafeas.yaml
```

Now just make a port-forward on a shell:

```
kubectl port-forward $(kubectl get pods -l app=grafeas -o jsonpath='{.items[0].metadata.name}') 8080:8080
```

### Installing the client

I will give a try to the Python one, just follow this steps:

```
virtualenv -p python .virtualenv
source .virtualenv/bin/activate
git clone https://github.com/Grafeas/client-python.git
cd client-python/v1alpha1
```

Add this line to setup.py:

```
      ...
      include_package_data=True,
+     zip_safe=False,
      long_description="""\
      ...
```

Save and install the client in the venv:

```
python setup.py install
```

Modify this file to point to the correct server:

- .virtualenv/lib/python2.7/site-packages/swagger_client-1.0.0-py2.7.egg/swagger_client/configuration.py
```
...
...
    def __init__(self):
        """
        Constructor
        """
        # Default Base url
        self.host = "http://<host>:10000"
...
...
```

Ok, we are now ready to start testing Grafeas. In this repository you have a client.py that could help you to understand how the client works ;).

### grafctl.py

This script will help you to understand how grafeas python-client works, the code is simple. Just modify as your needs to test the server.

- Create Note into Grafeas server (mock for now)
```
python grafctl.py -v push_note -n 'note_02' -p 'myproject'
```

- Get already created Note
```
python grafctl.py -v get_note -n 'note_02' -p 'myproject'
```

- Get already created Ocurrence
```
python grafctl.py -v get_occurrence -o 'occurence_02' -p 'myproject'
```

- List all Notes from a Project
```
python grafctl.py -v list_notes -p 'myproject'
```

- List Ocurrences associated to a Note in a Project
```
python grafctl.py -v list_occurrences -p 'myproject' -n 'note_02'
```

Enjoy!

## References

- [Grafeas Website](https://grafeas.io)
- [Grafeas GH](https://github.com/Grafeas/Grafeas)
- [Grafeas Blog - 01](https://cloudplatform.googleblog.com/2017/10/introducing-grafeas-open-source-api-.html)
- [Grafeas Blog - 02](https://www.infoworld.com/article/3230462/security/what-is-grafeas-better-auditing-for-containers.html)
- [Kubecon Presentation](https://schd.ws/hosted_files/kccncna17/c6/KubeCon%202017_%20Grafeas%20BoF%202017-12-06.pdf)
- [Kubecon Grafeas Meetup](https://schd.ws/hosted_files/kccncna17/6a/KubeCon%202017_%20Grafeas%20Meet-Up%20%282017-12-08%29.pdf)
- [Grafeas Python Client](https://github.com/Grafeas/client-python)
- [Grafeas Tutorial](https://github.com/kelseyhightower/grafeas-tutorial)

## Demo

- [Grafeas with Minishift on Asciinema](https://asciinema.org/a/Xn7NdEYTrYnJmrRcyiQv4zO6t)

# Kritis

## To be continue...

## References

- [Kritis GH](https://github.com/Grafeas/Grafeas/blob/master/case-studies/binary-authorization.md)
