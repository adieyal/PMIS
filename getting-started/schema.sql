BEGIN;
CREATE TABLE "entry_cluster" (
    "id" integer NOT NULL PRIMARY KEY,
    "name" varchar(128) NOT NULL
)
;
CREATE TABLE "entry_programme" (
    "id" integer NOT NULL PRIMARY KEY,
    "name" varchar(128) NOT NULL,
    "cluster_id" integer NOT NULL REFERENCES "entry_cluster" ("id")
)
;
CREATE TABLE "entry_implementingagent" (
    "id" integer NOT NULL PRIMARY KEY,
    "name" varchar(128) NOT NULL
)
;

COMMIT;
