PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE "player_gameround" (
    "id" integer NOT NULL PRIMARY KEY,
    "round" varchar(1) NOT NULL,
    "number_teams" integer unsigned NOT NULL,
    "category" varchar(1) NOT NULL
);
INSERT INTO "player_gameround" VALUES(1,'Pool A',4,'Gold');
INSERT INTO "player_gameround" VALUES(2,'Pool B',4,'Gold');
INSERT INTO "player_gameround" VALUES(3,'Pool C',4,'Gold');
INSERT INTO "player_gameround" VALUES(4,'Pool D',4,'Gold');
INSERT INTO "player_gameround" VALUES(5,'1/4',2,'Gold');
INSERT INTO "player_gameround" VALUES(6,'Semifinal',2,'Gold');
INSERT INTO "player_gameround" VALUES(7,'Final',2,'Gold');
INSERT INTO "player_gameround" VALUES(8,'Semifinal',2,'Silver');
INSERT INTO "player_gameround" VALUES(9,'Final',2,'Silver');
INSERT INTO "player_gameround" VALUES(10,'1/4',2,'Bronze');
INSERT INTO "player_gameround" VALUES(11,'Semifinal',2,'Bronze');
INSERT INTO "player_gameround" VALUES(12,'Final',2,'Bronze');
INSERT INTO "player_gameround" VALUES(13,'Semifinal',2,'Wood');
INSERT INTO "player_gameround" VALUES(14,'Final',2,'Wood');
COMMIT;
