PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE "player_tournament_teams" (
    "id" integer NOT NULL PRIMARY KEY,
    "tournament_id" integer NOT NULL,
    "team_id" integer NOT NULL REFERENCES "player_team" ("id"),
    UNIQUE ("tournament_id", "team_id")
);
INSERT INTO "player_tournament_teams" VALUES(1,1,1);
INSERT INTO "player_tournament_teams" VALUES(2,1,2);
INSERT INTO "player_tournament_teams" VALUES(3,1,3);
INSERT INTO "player_tournament_teams" VALUES(4,1,4);
INSERT INTO "player_tournament_teams" VALUES(5,1,5);
INSERT INTO "player_tournament_teams" VALUES(24,3,6);
INSERT INTO "player_tournament_teams" VALUES(25,3,7);
INSERT INTO "player_tournament_teams" VALUES(26,3,8);
INSERT INTO "player_tournament_teams" VALUES(27,3,9);
INSERT INTO "player_tournament_teams" VALUES(28,3,10);
INSERT INTO "player_tournament_teams" VALUES(29,3,11);
INSERT INTO "player_tournament_teams" VALUES(30,3,12);
INSERT INTO "player_tournament_teams" VALUES(31,3,13);
INSERT INTO "player_tournament_teams" VALUES(32,3,14);
INSERT INTO "player_tournament_teams" VALUES(33,3,15);
INSERT INTO "player_tournament_teams" VALUES(34,3,16);
INSERT INTO "player_tournament_teams" VALUES(35,3,17);
INSERT INTO "player_tournament_teams" VALUES(36,3,18);
INSERT INTO "player_tournament_teams" VALUES(37,3,19);
INSERT INTO "player_tournament_teams" VALUES(38,3,20);
INSERT INTO "player_tournament_teams" VALUES(39,3,21);
INSERT INTO "player_tournament_teams" VALUES(40,2,6);
INSERT INTO "player_tournament_teams" VALUES(41,2,7);
INSERT INTO "player_tournament_teams" VALUES(42,2,8);
INSERT INTO "player_tournament_teams" VALUES(43,2,9);
INSERT INTO "player_tournament_teams" VALUES(44,2,10);
INSERT INTO "player_tournament_teams" VALUES(45,2,11);
INSERT INTO "player_tournament_teams" VALUES(46,2,12);
INSERT INTO "player_tournament_teams" VALUES(47,2,13);
INSERT INTO "player_tournament_teams" VALUES(48,2,14);
INSERT INTO "player_tournament_teams" VALUES(49,2,15);
INSERT INTO "player_tournament_teams" VALUES(50,2,16);
INSERT INTO "player_tournament_teams" VALUES(51,2,17);
INSERT INTO "player_tournament_teams" VALUES(52,2,18);
INSERT INTO "player_tournament_teams" VALUES(53,2,19);
INSERT INTO "player_tournament_teams" VALUES(54,2,20);
INSERT INTO "player_tournament_teams" VALUES(55,2,21);
CREATE INDEX "player_tournament_teams_4b799490" ON "player_tournament_teams" ("tournament_id");
CREATE INDEX "player_tournament_teams_95e8aaa1" ON "player_tournament_teams" ("team_id");
COMMIT;
