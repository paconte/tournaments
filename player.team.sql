PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE "player_team" (
    "id" integer NOT NULL PRIMARY KEY,
    "name" varchar(30) NOT NULL,
    "division" varchar(3) NOT NULL
);
INSERT INTO "player_team" VALUES(1,'Touch Berlin Red','MXO');
INSERT INTO "player_team" VALUES(2,'Den Haag','MXO');
INSERT INTO "player_team" VALUES(3,'Touch Berlin Black','MXO');
INSERT INTO "player_team" VALUES(4,'Bandits','MXO');
INSERT INTO "player_team" VALUES(5,'Frankfurt','MXO');
INSERT INTO "player_team" VALUES(6,'Hot Custard','MXO');
INSERT INTO "player_team" VALUES(7,'Oxford Touch','MXO');
INSERT INTO "player_team" VALUES(8,'Nottingham Hoods','MXO');
INSERT INTO "player_team" VALUES(9,'Phoenix Touch','MXO');
INSERT INTO "player_team" VALUES(10,'Bareback Riders','MXO');
INSERT INTO "player_team" VALUES(11,'Wigan Touch Warriors','MXO');
INSERT INTO "player_team" VALUES(12,'CSSC Phantoms','MXO');
INSERT INTO "player_team" VALUES(13,'Tumeke Sports','MXO');
INSERT INTO "player_team" VALUES(14,'London Scorpions','MXO');
INSERT INTO "player_team" VALUES(15,'Galaxy Knights	','MXO');
INSERT INTO "player_team" VALUES(16,'Thames Valley Vikings','MXO');
INSERT INTO "player_team" VALUES(17,'Manchester Chargers','MXO');
INSERT INTO "player_team" VALUES(18,'Cambridge Hornets','MXO');
INSERT INTO "player_team" VALUES(19,'Durka Touch','MXO');
INSERT INTO "player_team" VALUES(20,'Bristol Fijians','MXO');
INSERT INTO "player_team" VALUES(21,'London Galaxy','MXO');
COMMIT;
