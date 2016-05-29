DROP TABLE IF EXISTS `Sessions`;
CREATE TABLE `Sessions` (
    `session_id` VARCHAR(128) UNIQUE NOT NULL,
    `atime` TIMESTAMP NOT NULL default CURRENT_TIMESTAMP,
    `data` TEXT
);

DROP TABLE IF EXISTS `APsFeatures`;
CREATE TABLE `APsFeatures`
(
    `bssid` CHAR(17),
    `ssid` VARCHAR(30),
    `security` VARCHAR(50),
    `signals` SMALLINT,
    `longtitude` DOUBLE,
    `latitude` DOUBLE,
    `macAdress` VARCHAR(30),
    `timeString` VARCHAR(30),
    PRIMARY KEY(`bssid`)
);
CREATE TABLE `APAcessRecord`
(
    `bssid` CHAR(17),
	`macAdress` VARCHAR(30),
	`startTime` VARCHAR(30),
	`endTime` VARCHAR(30),
	`latitude` DOUBLE,
	`longtitude` DOUBLE,
	PRIMARY KEY(`startTime`)
)
CREATE TABLE `TraceRouteRecord`
(
    `bssid` CHAR(17),
	`macAdress` VARCHAR(30),
	`content` VARCHAR(1000)
)