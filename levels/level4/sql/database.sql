USE master;
CREATE LOGIN webapp WITH PASSWORD = 'hd92ghfiuqwba*b378fg';

USE azure_trainer_db;

CREATE USER webapp FOR LOGIN webapp WITH DEFAULT_SCHEMA = dbo;
EXEC sp_addrolemember 'db_datareader', 'webapp'

ALTER ROLE db_datareader ADD MEMBER webapp