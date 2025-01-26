## video-to-mp3-service

> Docker images - https://hub.docker.com/repository/docker/kaustubhdeokar/fastapi-mysql-auth/general
- fast api - app
- mysql db
- jwt token authentication   

Rest calls - calls.json


rabbit mq configuration 
- if we configure to publish the message on an empty exchange and routing key = 'x' it will be published to the queue named 'x' 
- we can configure to have multiple consumers for the same channel if we anticipate high amount of traffic for a certain channel.

Docker and kubernetes

> kubernetes worker node/ data plane
- (kube-proxy, kubelet & docker container runtime) form the kubernetes worker node/ data plane
  - docker - container runtime is Docker Shim or container d. it communicates with the docker engine and manages the execution of the container.
  - in docker as the containerd takes care of the container, kubernetes pod is controlled by kubelet.
  - as docker has docker-bridge for networking, kubernetes has kube-proxy.

> kubernetes control plane/master node.
- server api - heart of the kubernetes, takes all the incoming requests.
- Scheduler - scheules request send by server-api.
- etcd - key:value store, stores the state of the cluster information.
- controller manager - 
  - there are controllers in k8s, for example some controller taking care of replica set. So all such controllers are managed by controller manager.

#### manifests folder/
- The files in your manifests folder are Kubernetes resource definitions. They define how various components of your application should be deployed and managed within a Kubernetes cluster. Here's a breakdown of what each type of file does and what you get from them:

- Configmap
  - A ConfigMap is used to store non-confidential configuration data in key-value pairs. It allows you to decouple configuration artifacts from image content to keep containerized applications portable.
- Secret
  - A Secret is used to store and manage sensitive information, such as passwords, OAuth tokens, and SSH keys. Secrets are base64 encoded and can be mounted as files or exposed as environment variables in a pod.
- Deployment
  - Describe the desired state of the deployment, deployment controller changes actual state to the desired state.
- Service
  - A Service is an abstraction that defines a logical set of pods and a policy by which to access them. Services enable network access to a set of pods.