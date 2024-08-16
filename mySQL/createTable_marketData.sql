CREATE TABLE `aiqt`.`market_data` (
    `instType` VARCHAR(255) NOT NULL COMMENT '产品类型',
    `instId` VARCHAR(255) NOT NULL COMMENT '产品ID',
    `last` DECIMAL(10, 2) NOT NULL COMMENT '最新成交价',
    `lastSz` DECIMAL(10, 2) NOT NULL COMMENT '最新成交的数量',
    `askPx` DECIMAL(10, 2) NOT NULL COMMENT '卖一价',
    `askSz` DECIMAL(10, 2) NOT NULL COMMENT '卖一价对应的数量',
    `bidPx` DECIMAL(10, 2) NOT NULL COMMENT '买一价',
    `bidSz` DECIMAL(10, 2) NOT NULL COMMENT '买一价对应的数量',
    `open24h` DECIMAL(10, 2) NOT NULL COMMENT '24小时开盘价',
    `high24h` DECIMAL(10, 2) NOT NULL COMMENT '24小时最高价',
    `low24h` DECIMAL(10, 2) NOT NULL COMMENT '24小时最低价',
    `volCcy24h` DECIMAL(10, 2) NOT NULL COMMENT '24小时成交量，以币为单位',
    `vol24h` DECIMAL(10, 2) NOT NULL COMMENT '24小时成交量，以张为单位',
    `sodUtc0` DECIMAL(10, 2) NOT NULL COMMENT 'UTC+0 时开盘价',
    `sodUtc8` DECIMAL(10, 2) NOT NULL COMMENT 'UTC+8 时开盘价',
    `ts` BIGINT NOT NULL COMMENT 'ticker数据产生时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
