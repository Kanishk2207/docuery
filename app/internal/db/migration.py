import os
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

async def run_migrations(db: AsyncSession, script_path: str):
    """
    Execute SQL migration scripts.
    """
    if not os.path.isfile(script_path):
        raise FileNotFoundError(f"Migration script {script_path} does not exist.")

    with open(script_path, 'r') as f:
        sql_commands = f.read()

    # Split SQL commands on ';' for individual execution if multiple commands
    commands = [cmd.strip() for cmd in sql_commands.split(';') if cmd.strip()]
    
    async with db.begin():
        for command in commands:
            await db.execute(text(command))
