# -*- coding: utf-8 -*-
import json

import elasticsearch
import elasticsearch_dsl
from elasticsearch_dsl.aggs import A
from elasticsearch_dsl.query import Q

from codetoname.features import firstname


def first_words(index='codetoname', language='python'):
    es = elasticsearch.Elasticsearch()

    # update first name
    s = elasticsearch_dsl.Search(using=es, index=index, doc_type=language)\
        .query('bool', filter=Q('exists', field='feature') & Q('missing', field='first_name'))
    for hit in s.scan():
        data = hit.to_dict()
        feature = json.loads(data['feature'])
        data['first_name'] = firstname(feature['name'], language)
        es.index(index=index, doc_type=language, id=hit.meta.id, body=data)
    es.indices.refresh(index=index)

    # aggregation
    s = elasticsearch_dsl.Search(using=es, index=index, doc_type=language)\
        .query('bool', filter=Q('exists', field='feature'))
    a = A('terms', field='first_name')
    s.aggs.bucket('first_name_terms', a)
    response = s.execute()

    words = []
    for item in response.aggregations.first_name_terms.buckets:
        percentage = item.doc_count / float(response.hits.total) * 100
        words.append({'word': item.key, 'percentage': percentage})
    return words
