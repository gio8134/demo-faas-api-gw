LISTA_FAAS = [
    {
        "nome-faas": "demo-faas-sheepcounter",
        "url-faas":
            "http://demo-faas-sheepcounter.default.svc.cluster.local/"
    }
]


def get_lista_faas():
    return LISTA_FAAS

def get_fass_url_from_faas_name(faas_name):
    for f in LISTA_FAAS:

        if f.get("nome-faas") == faas_name:
            return f.get("url-faas")

    return ""
    
    