Installation
================================================================

Installing Using Helm Package Manager
--------------------------------------

0. Make sure the Kubernetes cluster is accessible from the machine where you will be deploying this solution

  .. code-block:: shell

    >kubectl get nodes
    NAME         STATUS   ROLES    AGE   VERSION
    masternode   Ready    master   25d   v1.13.3
    node1        Ready    <none>   25d   v1.13.3
    node2        Ready    <none>   25d   v1.13.3

1. Download source code from github

  .. code-block:: shell

    git clone https://github.com/NetApp/devops-at-scale

2. Go to the "devops-at-scale" directory

  .. code-block:: shell

    cd ./devops-at-scale

3. Enter storage details and installation options by modifying values.yaml


  .. code-block:: shell

    cat values.yaml
    global:
      # "LoadBalancer" or "NodePort"
      ServiceType: NodePort
      NameSpace: default
      scm:
        # "gitlab" or "bitbucket"
        type: "gitlab"
      registry:
        # "artifactory" or "docker-registry"
        type: "artifactory"
      persistence:
        ontap:
          # ontap data lif IP address
          dataIP: ""

5. Install helm chart using following command :

  .. code-block:: shell

        helm install –-name <helm_release_name> .

  .. note:: If helm is not already installed , visit https://helm.sh/ for installation instructions
  
6. Wait for pods to reach the "Running" state:

  .. code-block:: shell

    >kubectl get pods -n <namespace> | grep <helm_release_name>

    NAME                                              READY     STATUS    RESTARTS   AGE

    devops-at-scale-couchdb-58f48c5b8d-vw9mb           1/1       Running   0          3m

    devops-at-scale-docker-registry-7969844c9f-phshp   1/1       Running   0          3m

    devops-at-scale-gitlab-6c6dc79b77-j4dww            1/1       Running   0          3m

    devops-at-scale-jenkins-74d87d6fd5-th29g           1/1       Running   0          3m

    devops-at-scale-webservice-5bbcdbf88c-rjrp4        1/1       Running   0          3m

  .. note:: It may take up to 10 minutes for all the pods to come up.

7. After the pods are ready, retrieve the webservice URL:

  .. code-block:: shell

    >kubectl get svc -n <namespace>

        NAME                                       TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)                                  AGE

    devops-at-scale-couchdb                     NodePort    10.108.249.65    <none>        5984:14339/TCP                           5m

    devops-at-scale-docker-registry             NodePort    10.97.110.240    <none>        5000:24646/TCP                           5m

    devops-at-scale-gitlab                      NodePort    10.102.216.157   <none>        80:30593/TCP,22:8639/TCP,443:18600/TCP   5m

    devops-at-scale-jenkins                     NodePort    10.99.97.28      <none>        8080:12899/TCP                           5m

    devops-at-scale-jenkins-agent               ClusterIP   10.100.249.190   <none>        50000/TCP                                5m

    devops-at-scale-webservice                  NodePort    10.101.38.243    <none>        5000:12054/TCP


    export NODE_IP=$(kubectl get nodes -o jsonpath="{.items[0].status.addresses[0].address}")
    export SERVICE_PORT=$(kubectl get -o jsonpath="{.spec.ports[0].nodePort}" services <helm_release_name>-webservice -n development)
    export SERVICE_URL=$NODE_IP:$SERVICE_PORT

  .. note:: Take note of the port of web service. After exporting the $NODE_IP, $SERVICE_PORT and $SERVICE_URL variables. The web service will be available at $SERVICE_URL. [In the above example, <helm_release_name> is 'devops-at-scale']


8. Using a Web Browser, open the "devops-at-scale-webservice" URL (http://<$SERVICE_URL>) to visit the DevOps-At-Scale Frontend Management Console

  .. figure:: images/index.png
      :width: 100%
      :alt: Create CI Pipeline

  .. note:: GitLab service can be accessed using credentials 'root:root_devopsatscale' initially
  .. note:: All other services can be accessed using credentials 'admin:admin' initially
  .. note:: Default user for web-service is created with username 'admin'

Customized deployment
--------------------------------------

**Customizing Kubernetes NameSpace**

  By default, the Kubernetes deployment is run in 'default' namespace.
  This can be customized by setting the 'NameSpace' field in devops-at-scale/values.yaml

  Below example deploys in 'production' namespace'

  .. code-block:: shell

    cat values.yaml
    global:
      # "LoadBalancer" or "NodePort"
      ServiceType: NodePort
      NameSpace: production

**Customizing Storage Class**

There are 6 Kubernetes services deployed as part of this master helm chart.
By default, all PVCs assigned to the services use the default storage class set in the Kubernetes cluster.
This can be customized, by setting the desired storage class in the appropriate service's values.yaml

Below example specifies how to use 'gold' storage class for the Artifactory service.
The value is set in devops-at-scale/charts/artifactory/values.yaml

  .. code-block:: shell

    replicaCount: 1
    image: docker.bintray.io/jfrog/artifactory-oss:latest
    imagePullPolicy: Always
    persistence:
      volumeSize: "10000M"
    # Assigns PVCs to default storage class when not specified
    StorageClass: "gold"

**Customizing Volume access mode from Kubernetes PVC**

By default, all the 6 Kubernetes service PVCs are assigned to the 'ReadWriteOnce' access mode in the PVC spec.
The default value 'ReadWriteOnce' supports both NFS and iSCSI volume backends, and is sufficient for most PVCs.
However for Jenkins service, this can be customized to 'ReadWriteMany' to allow parallel Jenkins build agents (if there is a need to parallelize the build).


Below example specifies how to use 'ReadWriteMany' access mode for Jenkins PVC
The value is set in devops-at-scale/charts/jenkins/templates/jenkins-pvc.yaml

  .. code-block:: shell

    spec:
      # use 'ReadWriteMany' if there is a need to parallelize the builds (multiple Jenkins agents running parallel)
      accessModes:
      - "ReadWriteMany"
      resources:
        requests:
          storage: "{{ .Values.persistence.volumeSize }}"


Customized Deployment
--------------------------------------

**Jenkins repository running behind a forward proxy**

Refer to devops-at-scale/charts/jenkins/README.md for more customization options to the Jenkins deployment
The master pod uses an Init Container to install plugins etc. If you are behind a corporate proxy it may be useful to set `Master.InitContainerEnv` to add environment variables such as `http_proxy`, so that these can be downloaded.

Additionally, you may want to add env vars for the Jenkins container, and the JVM (`Master.JavaOpts`).

  .. code-block:: shell

    Master:
      InitContainerEnv:
        - name: http_proxy
          value: "http://192.168.64.1:3128"
        - name: https_proxy
          value: "https://192.168.64.1:3128"
        - name: no_proxy
          value: ""
      ContainerEnv:
        - name: http_proxy
          value: "http://192.168.64.1:3128"
        - name: https_proxy
          value: "https://192.168.64.1:3128"
      JavaOpts: >-
        -Dhttp.proxyHost=192.168.64.1
        -Dhttp.proxyPort=3128
        -Dhttps.proxyHost=192.168.64.1
        -Dhttps.proxyPort=3128


Additional Configuration
--------------------------------------

**Create Initial Bitbucket Account**


    An initial account has to be created on Bitbucket before starting to use it.

    To create an account on Bitbucket, visit the following URL and sign up.

    Please note that the account credentials for the account should be root (username) and root_devopsatscale (password)

    .. code :: shell

        http://<<$NODE_IP>>:<<Bitbucket_service_port>>


    .. figure:: images/bitbucket.png
        :width: 100%
        :alt: Bitbucket

**Create Initial GitLab User (Optional)**


    An initial account has to be created on Gitlab before starting to use it.
    To create an account on Gitlab, visit the following URL and sign up.

    .. code :: shell

        http://<<$NODE_IP>>:<<Gitlab_service_port>>


    .. figure:: images/gitlab.png
        :width: 100%
        :alt: GitLab
