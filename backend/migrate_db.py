"""
Migration Script: Fix user_id column type in todos table

This script:
1. Drops existing todos table (old schema with UUID user_id)
2. Recreates it with new schema (string user_id to match Better Auth)
3. Preserves user and other Better Auth tables

Run this after deploying the model changes.
"""

import logging
from app.models.database import engine, drop_db
from app.models.user import User
from app.models.todo import Todo
from sqlmodel import SQLModel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def migrate():
    """Execute the migration"""
    try:
        logger.info("=" * 60)
        logger.info("DATABASE MIGRATION: Fix user_id type in todos table")
        logger.info("=" * 60)
        
        # Drop only the todos table (not user table from Better Auth)
        logger.info("1. Dropping existing todos table...")
        Todo.__table__.drop(engine, checkfirst=True)
        logger.info("   ✓ todos table dropped")
        
        # Recreate with new schema
        logger.info("2. Creating todos table with new schema...")
        Todo.__table__.create(engine, checkfirst=True)
        logger.info("   ✓ todos table created with string user_id")
        
        logger.info("=" * 60)
        logger.info("✓ Migration completed successfully!")
        logger.info("=" * 60)
        logger.info("\nChanges:")
        logger.info("- user_id column: UUID → VARCHAR (to match Better Auth)")
        logger.info("- Foreign key: users.id → user.id")
        logger.info("\nThe todos table is now ready for new data.")
        
    except Exception as e:
        logger.error("=" * 60)
        logger.error("✗ Migration failed!")
        logger.error("=" * 60)
        logger.error(f"Error: {e}")
        raise

if __name__ == "__main__":
    migrate()
