PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE "player_tournament" (
    "id" integer NOT NULL PRIMARY KEY,
    "name" varchar(50) NOT NULL,
    "country" varchar(30) NOT NULL,
    "city" varchar(30) NOT NULL,
    "address" varchar(100),
    "date" date,
    "division" varchar(3) NOT NULL
);
INSERT INTO "player_tournament" VALUES(1,'Capital Cup','Germany','Berlin','Columbia Damm 111','2014-05-10','MXO');
INSERT INTO "player_tournament" VALUES(2,'XBlades NTS 3 2014','England','Manchester','',NULL,'MXO');
INSERT INTO "player_tournament" VALUES(3,'XBlades NTS 4 2014','England','Oxford','',NULL,'MXO');
COMMIT;
