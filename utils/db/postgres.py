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
        telegram_id BIGINT NOT NULL,
        game_on BOOLEAN DEFAULT FALSE              
        );
        """
        await self.execute(sql, execute=True)

    async def add_user(self, full_name, telegram_id):
        sql = "INSERT INTO users (full_name, telegram_id) VALUES($1, $2)"
        return await self.execute(sql, full_name, telegram_id, fetchrow=True)

    async def select_all_users(self):
        sql = "SELECT * FROM Users"
        return await self.execute(sql, fetch=True)

    async def select_user(self, telegram_id):
        sql = f"SELECT * FROM Users WHERE telegram_id='{telegram_id}'"
        return await self.execute(sql, fetchrow=True)

    async def select_user_random(self, telegram_id):
        sql = (f"SELECT * FROM Users WHERE game_on IS FALSE AND telegram_id != '{telegram_id}' "
               f"ORDER BY RANDOM() LIMIT 1")
        return await self.execute(sql, fetchrow=True)

    async def edit_status_users(self, game_on, telegram_id):
        sql = f"UPDATE Users SET game_on='{game_on}' WHERE telegram_id='{telegram_id}'"
        return await self.execute(sql, execute=True)

    async def stop_game_users(self, telegram_id):
        sql = f"UPDATE Users SET game_on=False WHERE telegram_id='{telegram_id}'"
        return await self.execute(sql, execute=True)

    async def count_users(self):
        sql = "SELECT COUNT(*) FROM Users"
        return await self.execute(sql, fetchval=True)

    async def delete_users(self):
        await self.execute("DELETE FROM Users WHERE TRUE", execute=True)

    async def drop_users(self):
        await self.execute("DROP TABLE Users", execute=True)

    # ===================== TABLE | RESULTS =================
    async def create_table_results(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Results (
        id SERIAL PRIMARY KEY,                
        telegram_id BIGINT NOT NULL,        
        book_id INT NULL,        
        result INT DEFAULT 0        
        );
        """
        await self.execute(sql, execute=True)

    async def add_gamer(self, telegram_id, book_id):
        sql = "INSERT INTO Results (telegram_id, book_id) VALUES($1, $2)"
        return await self.execute(sql, telegram_id, book_id, fetchrow=True)

    async def update_results(self, results, telegram_id, book_id):
        sql = (f"UPDATE Results SET result=result + '{results}' WHERE telegram_id='{telegram_id}' AND "
               f"book_id='{book_id}'")
        return await self.execute(sql, execute=True)

    async def delete_user_results(self, telegram_id):
        await self.execute(f"DELETE FROM Results WHERE telegram_id='{telegram_id}' "
                           f"AND result=0", execute=True)

    async def drop_table_results(self):
        await self.execute("DROP TABLE Results", execute=True)

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
    async def create_table_questions(self, table_name: str):
        sql = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
        id SERIAL PRIMARY KEY,
        question VARCHAR(2500),
        a_correct VARCHAR(255),
        b VARCHAR(255),
        c VARCHAR(255),
        d VARCHAR(255)                 
        );
        """
        await self.execute(sql, execute=True)

    async def add_question(self, table_name, question, a_correct, b, c, d):
        sql = f"INSERT INTO {table_name} (question, a_correct, b, c, d) VALUES($1, $2, $3, $4, $5) returning id"
        return await self.execute(sql, question, a_correct, b, c, d, fetchrow=True)

    async def select_all_questions(self, table_name):
        sql = f"SELECT * FROM {table_name} ORDER BY RANDOM() LIMIT 1"
        return await self.execute(sql, fetch=True)

    async def delete_table(self, table_name):
        await self.execute(f"DELETE FROM {table_name}", execute=True)

    async def drop_table(self, table_name):
        await self.execute(f"DROP TABLE {table_name}", execute=True)

    # ===================== TABLE | TEMPORARY ANSWERS =================
    async def create_table_temporary_answers(self):
        sql = """
        CREATE TABLE IF NOT EXISTS temporary (
            id SERIAL PRIMARY KEY,
            telegram_id BIGINT NULL,            
            battle_id INT NULL,
            question_number INT NULL,
            answer TEXT DEFAULT '❌',
            game_status TEXT DEFAULT 'OFF'                         
        );
        """
        await self.execute(sql, execute=True)

    async def add_answer(self, telegram_id):
        sql = f"INSERT INTO temporary (telegram_id) VALUES($1) returning id"
        return await self.execute(sql, telegram_id, fetchrow=True)

    async def add_answer_(self, telegram_id, battle_id, question_number, answer, game_status):
        sql = (f"INSERT INTO temporary (telegram_id, battle_id, question_number, answer, game_status) "
               f"VALUES($1, $2, $3, $4, $5)")
        return await self.execute(
            sql, telegram_id, battle_id, question_number, answer, game_status, fetchrow=True
        )

    async def add_answer_second(self, second_player, battle_id, question_number, answer, game_status):
        sql = (f"INSERT INTO temporary (second_player, battle_id, question_number, answer, game_status) "
               f"VALUES($1, $2, $3, $4, $5)")
        return await self.execute(
            sql, second_player, battle_id, question_number, answer, game_status, fetchrow=True
        )

    async def select_player(self, telegram_id):
        sql = (f"SELECT answer FROM temporary WHERE telegram_id='{telegram_id}' AND question_number IS NOT NULL "
               f"ORDER BY question_number")
        return await self.execute(sql, fetch=True)

    async def select_second_player(self, second_player):
        sql = (f"SELECT answer FROM temporary WHERE second_player='{second_player}' AND question_number IS NOT NULL "
               f"ORDER BY question_number")
        return await self.execute(sql, fetch=True)

    async def update_all_game_status(self, game_status, telegram_id, battle_id):
        sql = (f"UPDATE temporary SET game_status='{game_status}' WHERE telegram_id='{telegram_id}' AND "
               f"battle_id='{battle_id}'")
        return await self.execute(sql, execute=True)

    async def get_battle_first(self, battle_id):
        sql = f"SELECT * FROM temporary WHERE battle_id='{battle_id}' AND first_player IS NOT NULL"
        return await self.execute(sql, fetch=True)

    async def get_battle(self, battle_id, telegram_id):
        sql = (f"SELECT * FROM temporary WHERE battle_id = '{battle_id}' AND telegram_id != '{telegram_id}' AND "
               f"telegram_id IS NOT NULL")
        return await self.execute(sql, fetch=True)

    async def count_answers(self, telegram_id, answer):
        sql = f"SELECT COUNT(answer) FROM Temporary WHERE telegram_id='{telegram_id}' AND answer='{answer}'"
        return await self.execute(sql, fetchval=True)

    async def clean_temporary_table(self, battle_id):
        await self.execute(f"DELETE FROM temporary WHERE battle_id='{battle_id}'", execute=True)

    async def delete_answers_user(self, telegram_id):
        await self.execute(f"DELETE FROM temporary WHERE telegram_id='{telegram_id}'", execute=True)

    async def drop_table_temporary(self):
        await self.execute(f"DROP TABLE temporary", execute=True)
