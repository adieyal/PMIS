SERVER=http://localhost:9200

# Delete index first
curl -XDELETE $SERVER/pmis

curl -XPOST $SERVER/pmis

# Setup analyzer for autocomplete
curl -XPOST $SERVER/pmis/_close

curl -XPUT $SERVER/pmis/_settings -d'{
    "analysis": {
        "analyzer": {
            "autocomplete": {
                "type": "custom",
                "tokenizer": "standard",
                "filter":[ "standard", "lowercase", "stop", "kstem", "ngram" ]
            }
        },
        "filter": {
            "ngram": {
                "type": "ngram",
                "min_gram": 2,
                "max_gram": 15
            }
        }
    }
}'

# Setup mappings for project type
curl -XPUT $SERVER/pmis/_mapping/project -d'{
    "properties": {
        "cluster": {
            "type": "string",
            "analyzer": "autocomplete"
        },
        "programme": {
            "type": "string",
            "analyzer": "autocomplete"
        },
        "title": {
            "type": "string",
            "analyzer": "autocomplete"
        },

        "manager": {
            "type": "string",
            "analyzer": "autocomplete"
        },
        "municipality": {
            "type": "string",
            "analyzer": "autocomplete"
        },
        "comments": {
            "type": "string",
            "analyzer": "autocomplete"
        }
    }
}'

# Setup mappings for programme type
curl -XPUT $SERVER/pmis/_mapping/programme -d'{
    "properties": {
        "cluster": {
            "type": "string",
            "analyzer": "autocomplete"
        },
        "title": {
            "type": "string",
            "analyzer": "autocomplete"
        }
    }
}'

curl -XPOST $SERVER/pmis/_open
