from typing import List, Dict

from psycopg2 import sql
from psycopg2.extras import RealDictCursor

import database_common


@database_common.connection_handler
def get_mentors(cursor: RealDictCursor) -> list:
    query = """
        SELECT first_name, last_name, city
        FROM mentor
        ORDER BY first_name"""
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_applicants(cursor: RealDictCursor) -> list:
    query = """
        SELECT first_name || ' ' || last_name, phone_number
        FROM applicant
        ORDER BY first_name"""
    cursor.execute(query)
    return cursor.fetchall()

@database_common.connection_handler
def get_full_applicants(cursor: RealDictCursor) -> list:
    query = """
        SELECT  first_name, last_name, phone_number, email, application_code
        FROM applicant
        ORDER BY first_name"""
    cursor.execute(query)
    return cursor.fetchall()

@database_common.connection_handler
def update_phone(cursor: RealDictCursor, code, phone):
    command = """
            UPDATE applicant
            SET phone_number = %(phone)s
            WHERE application_code = %(code)s;
    """
    param = {'code': code, 'phone': phone}
    cursor.execute(command, param)

@database_common.connection_handler
def get_applicants_by_name(cursor: RealDictCursor, name: str) -> list:
    query = """
        SELECT first_name || ' ' || last_name, phone_number
        FROM applicant
        WHERE first_name LIKE %(name)s OR last_name LIKE %(name)s
        ESCAPE '='
        """

    # https://stackoverflow.com/questions/2106207/escape-sql-like-value-for-postgres-with-psycopg2

    cursor.execute(query, dict(name= '%' + name + '%'))
    return cursor.fetchall()

@database_common.connection_handler
def get_applicant_by_code(cursor: RealDictCursor, code: int):
    query = """
            SELECT  first_name, last_name, phone_number, email, application_code
            FROM applicant
            WHERE application_code = %(code)s
            """
    param = {'code': code}
    cursor.execute(query, param)
    return cursor.fetchone()


@database_common.connection_handler
def get_applicant_data_by_email_ending(cursor: RealDictCursor, email_end: str) -> list:
    query = """
        SELECT first_name || ' ' || last_name, phone_number
        FROM applicant
        WHERE email LIKE %(email_end)s
        ESCAPE '='
        ORDER BY first_name;"""
    cursor.execute(query, {'email_end': '%' + email_end})
    return cursor.fetchall()


@database_common.connection_handler
def get_mentors_by_last_name(cursor: RealDictCursor, last_name: str) -> list:
    query = """
        SELECT first_name, last_name, city
        FROM mentor
        WHERE last_name = %(last_name)s
        ORDER BY first_name"""
    cursor.execute(query, {'last_name': last_name})
    return cursor.fetchall()


@database_common.connection_handler
def get_mentors_by_first_name(cursor: RealDictCursor, first_name: str) -> list:
    query = """
        SELECT first_name, last_name, city
        FROM mentor
        WHERE first_name = %(first_name)s
        ORDER BY first_name"""
    cursor.execute(query, {'first_name': first_name})
    return cursor.fetchall()


@database_common.connection_handler
def get_mentors_by_city(cursor: RealDictCursor, city_name: str):
    query = """
            SELECT first_name, last_name, city
            FROM mentor
            WHERE city = %(city_name)s
            ORDER BY first_name"""
    cursor.execute(query, {'city_name': city_name})
    return cursor.fetchall()

@database_common.connection_handler
def delete_applicant(cursor:RealDictCursor, code: int):
    command = """
            DELETE
            FROM applicant 
            WHERE email = %(code)s
    """
    param = {'code': code}
    cursor.execute(command,param)

@database_common.connection_handler
def delete_by_domain(cursor:RealDictCursor, domain: str):
    command = """
                DELETE
                FROM applicant 
                WHERE email LIKE %(email_end)s
                ESCAPE '='
        """

    param = {'email_end': '%' + domain}
    cursor.execute(command, param)

@database_common.connection_handler
def add_applicant(cursor:RealDictCursor, applicant):
    command = """
            INSERT INTO applicant (first_name, last_name, phone_number, email, application_code)
            VALUES (%(first_name)s, %(last_name)s, %(phone_number)s, %(email)s, %(application_code)s);"""
    param = {'first_name': applicant.get('first_name'),
               'last_name': applicant.get('last_name'),
               'phone_number': applicant.get('phone_number'),
               'email': applicant.get('email'),
               'application_code': applicant.get('application_code')}
    cursor.execute(command, param )
