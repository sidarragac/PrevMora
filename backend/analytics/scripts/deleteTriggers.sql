DECLARE @sql NVARCHAR(MAX) = N'';

SELECT @sql = @sql + 'DROP TRIGGER [' + name + '];' + CHAR(13)
FROM sysobjects
WHERE type = 'TR';  -- TR = Trigger

EXEC sp_executesql @sql;