from elasticsearch import Elasticsearch

es = Elasticsearch(
    hosts=["https://localhost:9200"],
    basic_auth=("elastic", "changeme"),
    verify_certs=False 
)