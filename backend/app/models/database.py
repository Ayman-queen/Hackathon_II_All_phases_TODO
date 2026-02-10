# Task T-210/T-223: Database connection configuration and session management
# Task T-223: Neon PostgreSQL serverless support
from sqlmodel import create_engine, SQLModel, Session
from sqlalchemy.pool import NullPool
from sqlalchemy import text, inspect
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)


def get_database_url() -> str:
    """
    Task T-223: Get database URL with correct driver for psycopg3

    Converts postgresql:// to postgresql+psycopg:// for psycopg3 driver.
    """
    url = settings.DATABASE_URL
    # If using postgresql:// scheme, convert to use psycopg (psycopg3) driver
    if url.startswith("postgresql://"):
        url = url.replace("postgresql://", "postgresql+psycopg://", 1)
    elif url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql+psycopg://", 1)
    return url


# Get the database URL with correct driver
database_url = get_database_url()

# Task T-223: Create engine optimized for serverless environments
# For Vercel/Neon Serverless PostgreSQL:
# - Use NullPool: No persistent connections (each request gets fresh connection)
# - pool_pre_ping: Verify connections are alive (detect stale connections)
# - pool_recycle: Prevent connection timeout issues
# - No pool_size/overflow: NullPool doesn't use these
engine = create_engine(
    database_url,
    echo=False,  # Set to True for SQL logging (development only)
    poolclass=NullPool,  # No pooling - ideal for serverless (new connection per request)
    pool_pre_ping=True,  # Verify connections before use (detect stale connections)
    pool_recycle=300,  # Recycle connections after 5 mins (Neon timeout)
)

def get_db():
    """
    Task T-210: Dependency for getting database session in FastAPI routes

    Usage in FastAPI route:
        @app.get("/todos")
        async def get_todos(db: Session = Depends(get_db)):
            todos = db.query(Todo).filter(Todo.user_id == current_user.id).all()
            return todos

    FastAPI automatically closes the session after the request completes.
    """
    with Session(engine) as session:
        yield session


def _migrate_todo_user_id_column():
    """
    CRITICAL FIX (2026-01-01): Migrate todos.user_id from UUID to VARCHAR
    
    Better Auth stores user_id as string UUIDs, but the old schema had
    todos.user_id as UUID type, causing type mismatch errors:
    "operator does not exist: uuid = character varying"
    
    This migration:
    1. Checks if todos table exists and user_id is UUID type
    2. Drops the old todos table
    3. Recreates it with correct string user_id type
    """
    try:
        with engine.connect() as conn:
            # Check if todos table exists
            inspector = inspect(engine)
            tables = inspector.get_table_names()
            
            if "todos" not in tables:
                logger.info("✓ todos table doesn't exist yet (first run)")
                return
            
            # Check the type of user_id column
            columns = inspector.get_columns("todos")
            user_id_col = next((c for c in columns if c["name"] == "user_id"), None)
            
            if not user_id_col:
                logger.warning("⚠ todos.user_id column not found - table may be corrupted")
                return
            
            col_type = str(user_id_col["type"])
            logger.info(f"Current todos.user_id type: {col_type}")
            
            # If it's UUID, we need to migrate
            if "uuid" in col_type.lower() or "UUID" in col_type:
                logger.warning("⚠ Found old UUID type for user_id - migrating to VARCHAR...")
                
                # Drop and recreate the todos table
                conn.execute(text("DROP TABLE IF EXISTS todos CASCADE"))
                conn.commit()
                logger.info("  ✓ Dropped old todos table")
                
                # Create new table from model
                from app.models.todo import Todo
                Todo.__table__.create(engine, checkfirst=True)
                logger.info("  ✓ Created new todos table with VARCHAR user_id")
                
            else:
                logger.info(f"✓ todos.user_id is already correct type: {col_type}")
                
    except Exception as e:
        logger.error(f"⚠ Migration check failed: {e}")
        logger.error("  This may cause type mismatch errors")
        # Don't raise - let the app continue, migration can be run manually


def init_db():
    """
    Task T-210/T-223: Initialize database tables (create_all)

    Call this once on application startup:
        @app.on_event("startup")
        def on_startup():
            init_db()

    Creates all tables defined in SQLModel models (User, Todo).
    Safe to call multiple times (idempotent - only creates missing tables).

    CRITICAL FIX (2026-01-01): Also performs migration of todos.user_id
    from UUID to VARCHAR to match Better Auth schema.

    In production, use Alembic for migrations instead of create_all.

    Raises:
        Exception: If database connection fails or table creation fails
    """
    try:
        logger.info("=" * 70)
        logger.info("Initializing database tables...")
        logger.info("=" * 70)
        
        # First, check and migrate todos.user_id if needed
        logger.info("Checking for schema migrations...")
        _migrate_todo_user_id_column()
        
        # Create any missing tables
        logger.info("Creating missing tables from models...")
        SQLModel.metadata.create_all(engine)
        logger.info("✓ Database tables initialized successfully")
        logger.info("=" * 70)
        
    except Exception as e:
        logger.error("=" * 70)
        logger.error("✗ Failed to initialize database")
        logger.error("=" * 70)
        logger.error(f"Error: {e}")
        logger.error(f"Database URL: {settings.DATABASE_URL}")
        logger.error("Make sure PostgreSQL is running and DATABASE_URL is correct")
        raise  # Re-raise to prevent app startup with no database


def drop_db():
    """
    Task T-210: Drop all database tables (DESTRUCTIVE - development only)

    WARNING: This deletes all tables and data. Only use for testing/cleanup.
    """
    SQLModel.metadata.drop_all(engine)
