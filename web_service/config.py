import os


class BaseConfig:
    """Base configuration"""
    DEBUG = True
    TESTING = False
    DEV = True
    # The below ontap variables are only used once when configuring devops@scale for the first time
    # Therafter , this information is retrieved from couchdb
    # TODO: Should the DevOps Admin be able to set all the configuration document parameters through ENV variables?

    # ONTAP
    ONTAP_SVM_NAME = os.getenv('ONTAP_SVM_NAME', 'ci_dev')
    ONTAP_AGGR_NAME = os.getenv('ONTAP_AGGR_NAME', 'olb03_sat1')
    ONTAP_DATA_IP = os.getenv('ONTAP_DATA_IP', '10.193.8.78')

    # default username, password for couchdb
    DATABASE_USER = os.getenv('DATABASE_USER', 'admin')
    DATABASE_PASS = os.getenv('DATABASE_PASS', 'admin')
    DATABASE_NAME = os.getenv('DATABASE_NAME', 'devops-at-scale')

    # The following values are set during Helm deployment

    # SCM
    SCM_SERVICE_NAME = os.getenv('SCM_SERVICE_NAME')
    SCM_PVC_NAME = os.getenv('SCM_PVC_NAME')
    SCM_TYPE = os.getenv('SCM_TYPE')

    # Jenkins
    JENKINS_SERVICE_NAME = os.getenv('JENKINS_SERVICE_NAME')
    JENKINS_PVC_NAME = os.getenv('JENKINS_PVC_NAME')

    # Database CouchDB
    DATABASE_SERVICE_NAME = os.getenv('DATABASE_SERVICE_NAME')
    DATABASE_PVC_NAME = os.getenv('DATABASE_PVC_NAME')

    # Artifactory
    REGISTRY_SERVICE_NAME = os.getenv('REGISTRY_SERVICE_NAME')
    REGISTRY_PVC_NAME = os.getenv('REGISTRY_PVC_NAME')
    REGISTRY_TYPE = os.getenv('REGISTRY_TYPE')

    # Webservice
    WEB_SERVICE_NAME = os.getenv('WEB_SERVICE_NAME')
    WEB_PVC_NAME = os.getenv('WEB_PVC_NAME')

    # Kube specs
    KUBE_NAMESPACE = os.getenv('KUBE_NAMESPACE')
    STORAGE_CLASS = os.getenv('STORAGE_CLASS')
    SERVICE_TYPE = os.getenv('SERVICE_TYPE')


class TestingConfig(BaseConfig):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    DATABASE_NAME = 'test_devops_at_scale'
    DATABASE_URL = 'test_devops_at_scale'
    DATABASE_PASS = 'test_devops_at_scale'


class DevConfig(BaseConfig):
    """Testing configuration"""
    DEBUG = True
    DEV = True
    DATABASE_NAME = 'devops_at_scale'


class ProductionConfig(BaseConfig):
    """Production configuration"""
    DEBUG = False
