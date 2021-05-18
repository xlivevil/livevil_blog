from haystack.backends.elasticsearch5_backend import Elasticsearch5SearchBackend
from haystack.backends.elasticsearch5_backend import Elasticsearch5SearchEngine


class Elasticsearch5IkSearchBackend(Elasticsearch5SearchBackend):
    def __init__(self, *args, **kwargs):
        self.DEFAULT_SETTINGS['settings']['analysis']['analyzer']['ik_analyzer'] = {
            "type": "custom",
            "tokenizer": "ik_max_word",
        }
        super(Elasticsearch5IkSearchBackend, self).__init__(*args, **kwargs)


class Elasticsearch5IkSearchEngine(Elasticsearch5SearchEngine):
    backend = Elasticsearch5IkSearchBackend
