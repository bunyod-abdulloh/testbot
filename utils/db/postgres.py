import datetime
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
        result INT DEFAULT 0,        
        time_result INTERVAL NULL,
        created_at DATE DEFAULT CURRENT_DATE        
        );
        """
        await self.execute(sql, execute=True)

    async def add_gamer(self, telegram_id, book_id):
        sql = "INSERT INTO Results (telegram_id, book_id) VALUES($1, $2)"
        return await self.execute(sql, telegram_id, book_id, fetchrow=True)

    async def add_gamer_(self, telegram_id, book_id, result, timer):
        sql = "INSERT INTO Results (telegram_id, book_id, result, time_result) VALUES($1, $2, $3, $4)"
        return await self.execute(sql, telegram_id, book_id, result, timer, fetchrow=True)

    async def select_user_in_results(self, telegram_id, book_id):
        sql = f"SELECT result FROM Results WHERE telegram_id='{telegram_id}' AND book_id='{book_id}'"
        return await self.execute(sql, fetchrow=True)

    async def select_in_results(self):
        sql = f"SELECT * FROM Results"
        return await self.execute(sql, fetchrow=True)

    async def select_battle_id_results(self, telegram_id, book_id, battle_id):
        sql = (f"SELECT * FROM Results WHERE telegram_id='{telegram_id}' AND book_id='{book_id}' "
               f"AND battle_id='{battle_id}'")
        return await self.execute(sql, fetchrow=True)

    async def update_results(self, results, telegram_id, book_id, time_result):
        sql = (f"UPDATE Results SET result=result + '{results}', time_result='{time_result}'"
               f"WHERE telegram_id='{telegram_id}' AND book_id='{book_id}'")
        return await self.execute(sql, execute=True)

    async def get_rating_by_id(self, book_name):
        sql = (f"SELECT telegram_id SUM(result) AS total_result FROM Results WHERE book_id = '{book_name}' "
               f"GROUP BY user ORDER BY total_result DESC")
        return await self.execute(sql, fetchrow=True)

    async def get_rating_by_result(self, book_id):
        sql = (f"SELECT telegram_id, result, time_result FROM Results WHERE book_id = '{book_id}' "
               f"ORDER BY result DESC, time_result ASC")
        return await self.execute(sql, fetch=True)

    async def get_rating_book(self, book_id):
        sql = (f"SELECT telegram_id, result, time_result FROM Results WHERE book_id='{book_id}' AND result!=0 "
               f"ORDER BY result DESC")
        return await self.execute(sql, fetch=True)

    async def get_rating_all(self):
        sql = f"SELECT telegram_id, result FROM Results WHERE result!=0 ORDER BY result DESC, time_result ASC"
        return await self.execute(sql, fetch=True)

    async def delete_from_results(self, telegram_id):
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
        game_status TEXT DEFAULT 'OFF',
        start_time TIMESTAMP NULL,
        end_time TIMESTAMP NULL                                 
        );
        """
        await self.execute(sql, execute=True)

    async def add_battle_to_temporary(self, telegram_id):
        sql = f"INSERT INTO temporary (telegram_id) VALUES('{telegram_id}') returning id"
        return await self.execute(sql, fetchrow=True)

    async def start_time_to_temporary(self, telegram_id: int, battle_id: int,
                                      game_status: str, start_time: datetime.datetime):
        sql = "INSERT INTO temporary (telegram_id, battle_id, game_status, start_time) VALUES($1, $2, $3, $4)"
        return await self.execute(sql, telegram_id, battle_id, game_status, start_time, fetchrow=True)

    async def add_answer_to_temporary(self, telegram_id: int, battle_id: int, question_number: int, answer: str,
                                      game_status: str):
        sql = ("INSERT INTO temporary (telegram_id, battle_id, question_number, answer, game_status) "
               "VALUES($1, $2, $3, $4, $5)")
        return await self.execute(
            sql, telegram_id, battle_id, question_number, answer, game_status, fetchrow=True
        )

    async def end_answer_to_temporary(self, telegram_id: int, battle_id: int, game_status,
                                      end_time: datetime.datetime):
        sql = "INSERT INTO temporary (telegram_id, battle_id, game_status, end_time) VALUES($1, $2, $3, $4)"
        return await self.execute(sql, telegram_id, battle_id, game_status, end_time, fetchrow=True)

    async def select_start_time(self, telegram_id, battle_id):
        sql = (f"SELECT start_time FROM temporary WHERE telegram_id='{telegram_id}' AND battle_id='{battle_id}'"
               f"AND start_time IS NOT NULL")
        return await self.execute(sql, fetch=True)

    async def select_end_time(self, telegram_id, battle_id):
        sql = (f"SELECT end_time FROM temporary WHERE telegram_id='{telegram_id}' AND battle_id='{battle_id}' "
               f"AND end_time IS NOT NULL")
        return await self.execute(sql, fetch=True)

    async def select_user_from_temporary(self, battle_id, telegram_id):
        sql = (f"SELECT * FROM temporary WHERE battle_id='{battle_id}' AND telegram_id='{telegram_id} "
               f"AND time_result IS NOT NULL")
        return await self.execute(sql, fetch=True)

    async def update_all_game_status(self, game_status, telegram_id, battle_id):
        sql = (f"UPDATE temporary SET game_status='{game_status}' WHERE telegram_id='{telegram_id}' AND "
               f"battle_id='{battle_id}'")
        return await self.execute(sql, execute=True)

    async def get_battle_temporary(self, battle_id, telegram_id):
        sql = (f"SELECT * FROM temporary WHERE battle_id = '{battle_id}' AND telegram_id != '{telegram_id}' AND "
               f"telegram_id IS NOT NULL")
        return await self.execute(sql, fetch=True)

    async def count_answers(self, telegram_id, answer):
        sql = (f"SELECT COUNT(answer) FROM Temporary WHERE telegram_id='{telegram_id}' AND answer='{answer}' "
               f"AND question_number IS NOT NULL")
        return await self.execute(sql, fetchval=True)

    async def clean_temporary_table(self, battle_id):
        await self.execute(f"DELETE FROM temporary WHERE battle_id='{battle_id}'", execute=True)

    async def delete_from_temporary(self, telegram_id):
        await self.execute(f"DELETE FROM temporary WHERE telegram_id='{telegram_id}'", execute=True)

    async def drop_table_temporary(self):
        await self.execute(f"DROP TABLE temporary", execute=True)

    # ===================== TABLE | COUNTER =================

    async def create_table_counter(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Counter (        
        telegram_id BIGINT NULL,            
        battle_id INT NULL,
        counter INT DEFAULT 0                                 
        );
        """
        await self.execute(sql, execute=True)

    async def add_to_counter(self, telegram_id, battle_id, counter):
        sql = (f"INSERT INTO Counter (telegram_id, battle_id, counter) "
               f"VALUES('{telegram_id}', '{battle_id}', '{counter}')")
        return await self.execute(sql, fetchrow=True)

    async def update_counter(self, counter, telegram_id, battle_id):
        sql = (f"UPDATE Counter SET counter=counter + '{counter}' WHERE telegram_id='{telegram_id}' AND "
               f"battle_id='{battle_id}'")
        return await self.execute(sql, execute=True)

    async def select_user_counter(self, telegram_id, battle_id):
        sql = f"SELECT * FROM Counter WHERE telegram_id='{telegram_id}' AND battle_id='{battle_id}'"
        return await self.execute(sql, fetchrow=True)

    async def delete_from_counter(self, telegram_id):
        await self.execute(f"DELETE FROM Counter WHERE telegram_id='{telegram_id}'", execute=True)

    async def drop_table_counter(self):
        await self.execute(f"DROP TABLE Counter", execute=True)
