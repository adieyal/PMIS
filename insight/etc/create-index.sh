#!/usr/bin/env bash

curl -XDELETE http://localhost:9200/pmis

curl -XPOST -d'{
  "settings": {
    "analysis": {
      "analyzer":{
        "default":{
          "type":"custom",
          "tokenizer":"standard",
          "filter":[ "standard", "lowercase", "stop", "kstem", "ngram" ] 
        }
      },
      "filter":{
        "ngram":{
          "type":"edgeNGram",
          "min_gram":3,
          "max_gram":15
        }
      }
    }
  },
  "mappings": {
    "project": {
      "properties" : {
        "id": {
          "type": "string",
          "index": "no"
        },
        "cluster": {
          "type": "string",
          "index": "no"
        },
        "cluster_id": {
          "type": "string",
          "index": "no"
        },
        "title" : {
          "type" :    "string"
        },
        "description" : {
          "type" :    "string"
        },
        "url": {
          "type": "string",
          "index": "no"
        },
        "programme_id": {
          "type": "string",
          "index": "no"
        },
        "programme": {
          "type": "string",
          "index": "no"
        }
      }
    },
    "programme" : {
      "properties" : {
        "id": {
          "type": "string",
          "index": "no"
        },
        "cluster": {
          "type": "string",
          "index": "no"
        },
        "cluster_id": {
          "type": "string",
          "index": "no"
        },
        "title" : {
          "type" :    "string"
        },
        "description" : {
          "type" :    "string"
        }
      }
    }
  }
}' http://localhost:9200/pmis


