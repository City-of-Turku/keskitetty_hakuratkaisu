# Kubernetes scripts

These scripts have been used during development project to test the search application (both frontend and backend components) on a Kubernetes cluster, and kept here just for future reference and as an example.

More general info at https://cloud.google.com/kubernetes-engine/docs/tutorials/hello-app

Init tools

```
gcloud init
gcloud install kubectl
```

Set active project id
```
gcloud config set project turku-keskitetty-hakuratkaisu
```

Create artifact registry repository:
```
gcloud artifacts repositories create keha --repository-format docker --location=europe-north1
```

Authenticate to artifact registery for docker cli:
```
gcloud auth configure-docker europe-north1-docker.pkg.dev
```

Tag and push an images to artifact registry:
```
docker tag search_backend europe-north1-docker.pkg.dev/turku-keskitetty-hakuratkaisu/keha/search_backend:latest

docker tag scrapy europe-north1-docker.pkg.dev/turku-keskitetty-hakuratkaisu/keha/scrapy:latest

docker push europe-north1-docker.pkg.dev/turku-keskitetty-hakuratkaisu/keha/search_backend

docker push europe-north1-docker.pkg.dev/turku-keskitetty-hakuratkaisu/keha/scrapy
```

Connect to GKE cluster:
```
gcloud container clusters get-credentials cluster-keha --zone europe-north1-a
```

See cluster status, e.g.:
```
kubectl top node
kubectl top pod

kubectl get persistentvolumes
kubectl get persistentvolumeclaims
kubectl get nodes
kubectl get pods
kubectl get all

kubectl describe pod xxxxx
kubectl logs -f xxxxx
```

Push configuration(s) to create cluster resources:
```
kubectl apply -f <yaml file or directory>
```

Run scheduled job immediately (e.g. crawler):
```
kubectl create job --from=cronjob.batch/crawler crawler-manual
```
