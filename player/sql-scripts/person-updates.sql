-- update paco
BEGIN;
UPDATE player_player SET person_id = 1 WHERE id in (1239, 2642, 2449);
DELETE FROM player_person WHERE id in (1095, 2108)
COMMIT;

-- update josue manuel quintana diaz
BEGIN;
UPDATE player_player SET person_id = 1698 WHERE id=2700;
DELETE FROM player_person WHERE id = 2262;
COMMIT;

-- update ben powell to benjamin powell
BEGIN;
UPDATE player_player SET person_id = 630 WHERE id in (81, 233, 2123);
DELETE FROM player_person WHERE id = 85;
COMMIT;

-- update jörg schloßmacher
BEGIN;
UPDATE player_player SET person_id = 2228 WHERE id in (SELECT id FROM player_player WHERE person_id in (1604, 1694, 2228, 1091));
DELETE FROM player_person WHERE id in (1604, 1694, 1091);
COMMIT;
