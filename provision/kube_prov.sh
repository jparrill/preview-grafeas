#!/bin/bash

function validations() {
  email='image.signer@example.com'
}

function create_certs() {
  gpg2 --quick-generate-key --yes ${email}
  gpg2 -u ${email} --armor --clearsign --output=signature.gpg image-digest.txt
  gpg2 --output - --verify signature.gpg
  export GPG_KEY_ID=`gpg2 --list-keys --keyid-format short | grep ${email} | grep rsa2 | cut -f2 -d/ | cut -f1 -d\ `
  export GPG_SIGNATURE=$(cat signature.gpg | base64)
  gpg2 --armor --export ${email} > ${GPG_KEY_ID}.pub
}

function load_data() {
  kubectl apply -f ../kubernetes/grafeas.yaml
  echo "Waking up pods..."
  sleep 15
  kubectl get pods --all-namespaces -o wide
  kubectl port-forward $(kubectl get pods -l app=grafeas -o jsonpath='{.items[0].metadata.name}') 8080:8080
}

function minikube_start() {
  curl -Lo minikube https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64 && chmod +x minikube && sudo mv minikube /usr/local/bin/
  curl -Lo kubectl https://storage.googleapis.com/kubernetes-release/release/v1.8.0/bin/linux/amd64/kubectl && chmod +x kubectl && sudo mv kubectl /usr/local/bin/
  minikube start
}

