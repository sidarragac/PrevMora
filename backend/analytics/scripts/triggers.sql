-- Script completo para crear triggers de auto-actualización de updated_at
-- Ejecutar en Azure Data Studio o SQL Server Management Studio

-- 1. Trigger para tabla credit
CREATE TRIGGER tr_credit_updated_at
ON credit
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;
    UPDATE credit 
    SET updated_at = GETDATE()
    FROM credit c
    INNER JOIN inserted i ON c.id = i.id;
END;
GO

-- 2. Trigger para tabla installment
CREATE TRIGGER tr_installment_updated_at
ON installment
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;
    UPDATE installment 
    SET updated_at = GETDATE()
    FROM installment c
    INNER JOIN inserted i ON c.id = i.id;
END;
GO

-- 3. Trigger para tabla portfolio
CREATE TRIGGER tr_portfolio_updated_at
ON portfolio
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;
    UPDATE portfolio 
    SET updated_at = GETDATE()
    FROM portfolio c
    INNER JOIN inserted i ON c.id = i.id;
END;
GO

-- 4. Trigger para tabla alert
CREATE TRIGGER tr_alert_updated_at
ON alert
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;
    UPDATE alert 
    SET updated_at = GETDATE()
    FROM alert c
    INNER JOIN inserted i ON c.id = i.id;
END;
GO

-- 5. Trigger para tabla reconciliation
CREATE TRIGGER tr_reconciliation_updated_at
ON reconciliation
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;
    UPDATE reconciliation 
    SET updated_at = GETDATE()
    FROM reconciliation c
    INNER JOIN inserted i ON c.id = i.id;
END;
GO

-- Verificar que los triggers se crearon correctamente
SELECT 
    t.name AS trigger_name,
    OBJECT_NAME(t.parent_id) AS table_name,
    t.is_disabled
FROM sys.triggers t
WHERE t.name LIKE 'tr_%_updated_at'
ORDER BY table_name;