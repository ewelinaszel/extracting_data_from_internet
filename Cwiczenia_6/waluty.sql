BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "CurrenciesTypes" (
	"Id"	INTEGER NOT NULL UNIQUE,
	"CurrencyName"	TEXT UNIQUE,
	"CurrencyCode"	TEXT UNIQUE,
	PRIMARY KEY("Id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "Rates" (
	"Id"	INTEGER NOT NULL UNIQUE,
	"EffectiveDate"	DATE,
	"Mid"	REAL,
	"CurrencyType"	INTEGER,
	PRIMARY KEY("Id" AUTOINCREMENT),
	FOREIGN KEY("CurrencyType") REFERENCES "CurrenciesTypes"("Id")
);
INSERT INTO "CurrenciesTypes" VALUES (1,'euro','EUR');
INSERT INTO "CurrenciesTypes" VALUES (2,'funt szterling','GBP');
INSERT INTO "CurrenciesTypes" VALUES (3,'dolar amerykański','USD');
INSERT INTO "CurrenciesTypes" VALUES (4,'frank szwajcarski','CHF');
INSERT INTO "CurrenciesTypes" VALUES (5,'jen (Japonia)','JPY');
INSERT INTO "Rates" VALUES (1,'2024-03-19',4.3201,1);
INSERT INTO "Rates" VALUES (2,'2024-03-20',4.3242,1);
INSERT INTO "Rates" VALUES (3,'2024-03-21',4.3031,1);
INSERT INTO "Rates" VALUES (4,'2024-03-22',4.3186,1);
INSERT INTO "Rates" VALUES (5,'2024-03-25',4.3091,1);
INSERT INTO "Rates" VALUES (6,'2024-03-26',4.3093,1);
INSERT INTO "Rates" VALUES (7,'2024-03-27',4.3153,1);
INSERT INTO "Rates" VALUES (8,'2024-03-28',4.3191,1);
INSERT INTO "Rates" VALUES (9,'2024-03-29',4.3009,1);
INSERT INTO "Rates" VALUES (10,'2024-04-02',4.2934,1);
INSERT INTO "Rates" VALUES (11,'2024-04-03',4.2923,1);
INSERT INTO "Rates" VALUES (12,'2024-04-04',4.2921,1);
INSERT INTO "Rates" VALUES (13,'2024-04-05',4.2883,1);
INSERT INTO "Rates" VALUES (14,'2024-04-08',4.2805,1);
INSERT INTO "Rates" VALUES (15,'2024-04-09',4.2588,1);
INSERT INTO "Rates" VALUES (16,'2024-04-10',4.2641,1);
INSERT INTO "Rates" VALUES (17,'2024-04-11',4.2649,1);
INSERT INTO "Rates" VALUES (18,'2024-04-12',4.2666,1);
INSERT INTO "Rates" VALUES (19,'2024-04-15',4.2851,1);
INSERT INTO "Rates" VALUES (20,'2024-04-16',4.3197,1);
INSERT INTO "Rates" VALUES (21,'2024-04-17',4.3353,1);
INSERT INTO "Rates" VALUES (22,'2024-04-18',4.3309,1);
INSERT INTO "Rates" VALUES (23,'2024-04-19',4.3316,1);
INSERT INTO "Rates" VALUES (24,'2024-04-22',4.3203,1);
INSERT INTO "Rates" VALUES (25,'2024-04-23',4.3335,1);
INSERT INTO "Rates" VALUES (26,'2024-03-19',5.0516,2);
INSERT INTO "Rates" VALUES (27,'2024-03-20',5.0635,2);
INSERT INTO "Rates" VALUES (28,'2024-03-21',5.0367,2);
INSERT INTO "Rates" VALUES (29,'2024-03-22',5.0257,2);
INSERT INTO "Rates" VALUES (30,'2024-03-25',5.0246,2);
INSERT INTO "Rates" VALUES (31,'2024-03-26',5.0243,2);
INSERT INTO "Rates" VALUES (32,'2024-03-27',5.0327,2);
INSERT INTO "Rates" VALUES (33,'2024-03-28',5.0474,2);
INSERT INTO "Rates" VALUES (34,'2024-03-29',5.03,2);
INSERT INTO "Rates" VALUES (35,'2024-04-02',5.0256,2);
INSERT INTO "Rates" VALUES (36,'2024-04-03',5.0117,2);
INSERT INTO "Rates" VALUES (37,'2024-04-04',5.0042,2);
INSERT INTO "Rates" VALUES (38,'2024-04-05',5.0003,2);
INSERT INTO "Rates" VALUES (39,'2024-04-08',4.9915,2);
INSERT INTO "Rates" VALUES (40,'2024-04-09',4.966,2);
INSERT INTO "Rates" VALUES (41,'2024-04-10',4.9843,2);
INSERT INTO "Rates" VALUES (42,'2024-04-11',4.9835,2);
INSERT INTO "Rates" VALUES (43,'2024-04-12',5.0007,2);
INSERT INTO "Rates" VALUES (44,'2024-04-15',5.0192,2);
INSERT INTO "Rates" VALUES (45,'2024-04-16',5.0609,2);
INSERT INTO "Rates" VALUES (46,'2024-04-17',5.0812,2);
INSERT INTO "Rates" VALUES (47,'2024-04-18',5.0589,2);
INSERT INTO "Rates" VALUES (48,'2024-04-19',5.0615,2);
INSERT INTO "Rates" VALUES (49,'2024-04-22',5.0131,2);
INSERT INTO "Rates" VALUES (50,'2024-04-23',5.0238,2);
INSERT INTO "Rates" VALUES (51,'2024-03-19',3.9866,3);
INSERT INTO "Rates" VALUES (52,'2024-03-20',3.9895,3);
INSERT INTO "Rates" VALUES (53,'2024-03-21',3.9431,3);
INSERT INTO "Rates" VALUES (54,'2024-03-22',3.9928,3);
INSERT INTO "Rates" VALUES (55,'2024-03-25',3.9833,3);
INSERT INTO "Rates" VALUES (56,'2024-03-26',3.9704,3);
INSERT INTO "Rates" VALUES (57,'2024-03-27',3.9857,3);
INSERT INTO "Rates" VALUES (58,'2024-03-28',4.0081,3);
INSERT INTO "Rates" VALUES (59,'2024-03-29',3.9886,3);
INSERT INTO "Rates" VALUES (60,'2024-04-02',4.0009,3);
INSERT INTO "Rates" VALUES (61,'2024-04-03',3.9843,3);
INSERT INTO "Rates" VALUES (62,'2024-04-04',3.9515,3);
INSERT INTO "Rates" VALUES (63,'2024-04-05',3.9571,3);
INSERT INTO "Rates" VALUES (64,'2024-04-08',3.9546,3);
INSERT INTO "Rates" VALUES (65,'2024-04-09',3.9223,3);
INSERT INTO "Rates" VALUES (66,'2024-04-10',3.9264,3);
INSERT INTO "Rates" VALUES (67,'2024-04-11',3.9707,3);
INSERT INTO "Rates" VALUES (68,'2024-04-12',3.9983,3);
INSERT INTO "Rates" VALUES (69,'2024-04-15',4.0209,3);
INSERT INTO "Rates" VALUES (70,'2024-04-16',4.0687,3);
INSERT INTO "Rates" VALUES (71,'2024-04-17',4.0741,3);
INSERT INTO "Rates" VALUES (72,'2024-04-18',4.0559,3);
INSERT INTO "Rates" VALUES (73,'2024-04-19',4.0688,3);
INSERT INTO "Rates" VALUES (74,'2024-04-22',4.054,3);
INSERT INTO "Rates" VALUES (75,'2024-04-23',4.061,3);
INSERT INTO "Rates" VALUES (76,'2024-03-19',4.4886,4);
INSERT INTO "Rates" VALUES (77,'2024-03-20',4.4771,4);
INSERT INTO "Rates" VALUES (78,'2024-03-21',4.4069,4);
INSERT INTO "Rates" VALUES (79,'2024-03-22',4.4337,4);
INSERT INTO "Rates" VALUES (80,'2024-03-25',4.4371,4);
INSERT INTO "Rates" VALUES (81,'2024-03-26',4.4047,4);
INSERT INTO "Rates" VALUES (82,'2024-03-27',4.4018,4);
INSERT INTO "Rates" VALUES (83,'2024-03-28',4.4228,4);
INSERT INTO "Rates" VALUES (84,'2024-03-29',4.425,4);
INSERT INTO "Rates" VALUES (85,'2024-04-02',4.4037,4);
INSERT INTO "Rates" VALUES (86,'2024-04-03',4.3875,4);
INSERT INTO "Rates" VALUES (87,'2024-04-04',4.3621,4);
INSERT INTO "Rates" VALUES (88,'2024-04-05',4.3796,4);
INSERT INTO "Rates" VALUES (89,'2024-04-08',4.3667,4);
INSERT INTO "Rates" VALUES (90,'2024-04-09',4.3366,4);
INSERT INTO "Rates" VALUES (91,'2024-04-10',4.3447,4);
INSERT INTO "Rates" VALUES (92,'2024-04-11',4.3451,4);
INSERT INTO "Rates" VALUES (93,'2024-04-12',4.3805,4);
INSERT INTO "Rates" VALUES (94,'2024-04-15',4.4047,4);
INSERT INTO "Rates" VALUES (95,'2024-04-16',4.4554,4);
INSERT INTO "Rates" VALUES (96,'2024-04-17',4.4777,4);
INSERT INTO "Rates" VALUES (97,'2024-04-18',4.4637,4);
INSERT INTO "Rates" VALUES (98,'2024-04-19',4.4787,4);
INSERT INTO "Rates" VALUES (99,'2024-04-22',4.4505,4);
INSERT INTO "Rates" VALUES (100,'2024-04-23',4.4535,4);
INSERT INTO "Rates" VALUES (101,'2024-03-19',0.026455,5);
INSERT INTO "Rates" VALUES (102,'2024-03-20',0.026301,5);
INSERT INTO "Rates" VALUES (103,'2024-03-21',0.026098,5);
INSERT INTO "Rates" VALUES (104,'2024-03-22',0.026334,5);
INSERT INTO "Rates" VALUES (105,'2024-03-25',0.026309,5);
INSERT INTO "Rates" VALUES (106,'2024-03-26',0.026247,5);
INSERT INTO "Rates" VALUES (107,'2024-03-27',0.026347,5);
INSERT INTO "Rates" VALUES (108,'2024-03-28',0.026472,5);
INSERT INTO "Rates" VALUES (109,'2024-03-29',0.026366,5);
INSERT INTO "Rates" VALUES (110,'2024-04-02',0.026384,5);
INSERT INTO "Rates" VALUES (111,'2024-04-03',0.026262,5);
INSERT INTO "Rates" VALUES (112,'2024-04-04',0.026045,5);
INSERT INTO "Rates" VALUES (113,'2024-04-05',0.026133,5);
INSERT INTO "Rates" VALUES (114,'2024-04-08',0.026035,5);
INSERT INTO "Rates" VALUES (115,'2024-04-09',0.025823,5);
INSERT INTO "Rates" VALUES (116,'2024-04-10',0.025856,5);
INSERT INTO "Rates" VALUES (117,'2024-04-11',0.025911,5);
INSERT INTO "Rates" VALUES (118,'2024-04-12',0.02608,5);
INSERT INTO "Rates" VALUES (119,'2024-04-15',0.026134,5);
INSERT INTO "Rates" VALUES (120,'2024-04-16',0.026335,5);
INSERT INTO "Rates" VALUES (121,'2024-04-17',0.026359,5);
INSERT INTO "Rates" VALUES (122,'2024-04-18',0.026274,5);
INSERT INTO "Rates" VALUES (123,'2024-04-19',0.02635,5);
INSERT INTO "Rates" VALUES (124,'2024-04-22',0.026202,5);
INSERT INTO "Rates" VALUES (125,'2024-04-23',0.026226,5);
INSERT INTO "Rates" VALUES (126,'2024-04-24',4.3177,1);
INSERT INTO "Rates" VALUES (127,'2024-04-24',5.022,2);
INSERT INTO "Rates" VALUES (128,'2024-04-24',4.0417,3);
INSERT INTO "Rates" VALUES (129,'2024-04-24',4.4202,4);
INSERT INTO "Rates" VALUES (130,'2024-04-24',0.026091,5);
COMMIT;