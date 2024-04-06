from typing import Union

import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool

from data import config


class Database:
    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME,
        )

    async def execute(
        self,
        command,
        *args,
        fetch: bool = False,
        fetchval: bool = False,
        fetchrow: bool = False,
        execute: bool = False,
    ):
        
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    # ===================== TABLE | USERS =================

    async def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users (
        id SERIAL PRIMARY KEY,
        full_name VARCHAR(255) NOT NULL,
        username varchar(255) NULL,
        telegram_id BIGINT NOT NULL UNIQUE,
        game_on BOOLEAN DEFAULT FALSE
        );
        """
        await self.execute(sql, execute=True)

    async def add_user(self, full_name, username, telegram_id):
        sql = "INSERT INTO users (full_name, username, telegram_id) VALUES($1, $2, $3) returning *"
        return await self.execute(sql, full_name, username, telegram_id, fetchrow=True)

    async def select_all_users(self):
        sql = "SELECT * FROM Users"
        return await self.execute(sql, fetch=True)

    async def select_user(self, telegram_id):
        sql = f"SELECT * FROM Users WHERE telegram_id='{telegram_id}'"
        return await self.execute(sql, fetchrow=True)

    async def select_user_random(self):
        sql = "SELECT * FROM Users WHERE game_on IS FALSE ORDER BY RANDOM() LIMIT 1"
        return await self.execute(sql, fetchrow=True)

    async def update_gaming_status(self, status, telegram_id):
        sql = f"UPDATE Users SET game_on='{status}' WHERE telegram_id='{telegram_id}'"
        return await self.execute(sql, execute=True)

    async def count_users(self):
        sql = "SELECT COUNT(*) FROM Users"
        return await self.execute(sql, fetchval=True)

    async def update_user_username(self, username, telegram_id):
        sql = "UPDATE Users SET username=$1 WHERE telegram_id=$2"
        return await self.execute(sql, username, telegram_id, execute=True)

    async def delete_users(self):
        await self.execute("DELETE FROM Users WHERE TRUE", execute=True)

    async def drop_users(self):
        await self.execute("DROP TABLE Users", execute=True)

    # ===================== TABLE | TABLES =================
    async def create_table_tables(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Tables (
        id SERIAL PRIMARY KEY,
        table_name VARCHAR(255) NULL                 
        );
        """
        await self.execute(sql, execute=True)

    async def add_table(self, table_name):
        sql = f"INSERT INTO Tables (table_name) VALUES($1) returning id"
        return await self.execute(sql, table_name, fetchrow=True)

    async def select_all_tables(self):
        sql = f"SELECT * FROM Tables"
        return await self.execute(sql, fetch=True)

    async def select_book_by_id(self, id_):
        sql = f"SELECT * FROM Tables WHERE id=$1"
        return await self.execute(sql, id_, fetchrow=True)

    async def delete_book_by_id(self, id_):
        await self.execute(f"DELETE FROM Tables WHERE table_name=$1", id_, execute=True)

    async def drop_table_tables(self):
        await self.execute(f"DROP TABLE Tables", execute=True)

    # ===================== TABLE | QUESTIONS =================
    async def create_table_questions(self, table_number: str):
        sql = f"""
        CREATE TABLE IF NOT EXISTS {table_number} (
        id SERIAL PRIMARY KEY,
        question VARCHAR(2500),
        a_correct VARCHAR(255),
        b VARCHAR(255),
        c VARCHAR(255),
        d VARCHAR(255)                 
        );
        """
        await self.execute(sql, execute=True)

    async def add_question(self, table_number, question, a_correct, b, c, d):
        sql = f"INSERT INTO {table_number} (question, a_correct, b, c, d) VALUES($1, $2, $3, $4, $5) returning id"
        return await self.execute(sql, question, a_correct, b, c, d, fetchrow=True)

    async def select_all_questions(self, table_number):
        sql = f"SELECT * FROM {table_number}"
        return await self.execute(sql, fetchrow=True)

    async def delete_table(self, table_number):
        await self.execute(f"DELETE FROM {table_number}", execute=True)

    async def drop_table(self, table_number):
        await self.execute(f"DROP TABLE {table_number}", execute=True)
