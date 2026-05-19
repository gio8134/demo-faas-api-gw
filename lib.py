import subprocess
import yaml
from kubernetes import client, config
from kubernetes.client.rest import ApiException

CONFIGMAP_NAME = "faas-packages-list"
NAMESPACE = "default"

def load_lista_faas(
    configmap_name: str = CONFIGMAP_NAME,
    namespace: str = NAMESPACE
) -> list[dict]:
    # Carica automaticamente le credenziali del cluster
    config.load_incluster_config()
    v1 = client.CoreV1Api()
    try:
        # Legge la ConfigMap
        configmap = v1.read_namespaced_config_map(
            name=configmap_name,
            namespace=namespace
        )
        # Recupera contenuto campo "packages"
        packages_raw = (
            configmap.data.get("packages", "")
            if configmap.data else ""
        )
        # Parsing YAML -> lista dict
        packages = yaml.safe_load(packages_raw) or []
        lista_faas = []
        for pkg in packages:
            # Validazione minima
            if not isinstance(pkg, dict):
                continue
            lista_faas.append({
                "faas-name": pkg.get("faas-name", ""),
                "faas-url": pkg.get("faas-url", ""),
                "faas-namespace": pkg.get("faas-namespace", "")
            })
        return lista_faas
    except ApiException as e:
        raise RuntimeError(
            f"Errore Kubernetes API ({e.status}): {e.reason}"
        ) from e


def get_lista_faas():
    return load_lista_faas()

def get_fass_url_from_faas_name(faas_name):
    lista_faas = load_lista_faas()
    for f in lista_faas:
        if f.get("faas-name") == faas_name:
            return f.get("faas-url")
    return ""    