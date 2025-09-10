"""
Script to completely recreate the database with the new structure
This script will:
1. Drop all existing tables and constraints
2. Create new tables with the updated schema
"""

import os
import sys

from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker

# Add the parent directory to sys.path to import models
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.abspath(os.path.join(script_dir, "../..")))

from credit_management.app.config.settings import settings
from credit_management.app.models import (
    Alert,
    Client,
    Credit,
    Installment,
    Manager,
    Portfolio,
    Reconciliation,
)
from credit_management.app.models.base import Base


def recreate_database():
    """Completely recreate the database with new structure"""

    # Create engine with the configured database
    engine = create_engine(settings.DATABASE_URL.replace("+aioodbc", "+pyodbc"))

    print("🗑️ Starting database recreation...")
    print("=" * 50)

    with engine.connect() as connection:
        transaction = connection.begin()

        try:
            # Step 1: Drop all foreign key constraints
            print("1️⃣ Dropping foreign key constraints...")
            drop_fk_sql = """
            DECLARE @sql NVARCHAR(MAX) = N'';
            SELECT @sql += 'ALTER TABLE [' + s.name + '].[' + t.name + '] DROP CONSTRAINT [' + f.name + '];' + CHAR(13)
            FROM sys.foreign_keys f
            JOIN sys.tables t ON f.parent_object_id = t.object_id
            JOIN sys.schemas s ON t.schema_id = s.schema_id;
            EXEC sp_executesql @sql;
            """

            try:
                connection.execute(text(drop_fk_sql))
                print("✅ Foreign key constraints dropped successfully")
            except Exception as e:
                print(f"⚠️ Warning dropping FK constraints: {e}")

            # Step 2: Drop all tables
            print("2️⃣ Dropping all existing tables...")
            drop_tables_sql = """
            DECLARE @sql NVARCHAR(MAX) = N'';
            SELECT @sql += 'DROP TABLE [' + s.name + '].[' + t.name + '];' + CHAR(13)
            FROM sys.tables t
            JOIN sys.schemas s ON t.schema_id = s.schema_id
            WHERE s.name = 'dbo';
            EXEC sp_executesql @sql;
            """

            try:
                connection.execute(text(drop_tables_sql))
                print("✅ All tables dropped successfully")
            except Exception as e:
                print(f"⚠️ Warning dropping tables: {e}")

            # Step 3: Create all tables with new structure
            print("3️⃣ Creating tables with new structure...")

            # Table creation order (respecting foreign key dependencies)
            table_order = [
                "client",
                "manager",
                "credit",
                "installment",
                "portfolio",
                "alert",
                "reconciliation",
            ]

            created_tables = []

            for table_name in table_order:
                if table_name in Base.metadata.tables:
                    table = Base.metadata.tables[table_name]
                    try:
                        table.create(connection, checkfirst=False)
                        created_tables.append(table_name)
                        print(f"   ✅ Created table: {table_name}")
                    except Exception as table_error:
                        print(f"   ❌ Error creating table {table_name}: {table_error}")
                        continue

            # Commit all changes
            transaction.commit()

            print("=" * 50)
            print("🎉 Database recreation completed successfully!")
            print(f"📊 Created {len(created_tables)} tables:")
            for table in created_tables:
                print(f"   • {table}")

            # Step 4: Verify tables
            print("\n🔍 Verifying created tables...")
            inspector = inspect(engine)
            actual_tables = inspector.get_table_names()

            print(f"📋 Tables in database: {len(actual_tables)}")
            for table in sorted(actual_tables):
                print(f"   • {table}")

                # Show columns for each table
                columns = inspector.get_columns(table)
                print(f"     Columns: {len(columns)}")
                for col in columns:
                    nullable = "NULL" if col["nullable"] else "NOT NULL"
                    print(f"       - {col['name']}: {col['type']} {nullable}")

                # Show foreign keys
                fks = inspector.get_foreign_keys(table)
                if fks:
                    print(f"     Foreign Keys: {len(fks)}")
                    for fk in fks:
                        print(
                            f"       - {fk['constrained_columns']} -> {fk['referred_table']}.{fk['referred_columns']}"
                        )
                print()

        except Exception as e:
            transaction.rollback()
            print(f"❌ Database recreation failed: {e}")
            raise

        finally:
            connection.close()


if __name__ == "__main__":
    recreate_database()
