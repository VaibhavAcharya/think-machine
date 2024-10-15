import subprocess
import requests


class Tools:
    @staticmethod
    def execute_command(command: str):
        """Executes the command in the shell and returns the output.

        Args:
            command (str): The command to execute.

        Returns:
            str: The output of the command or an error message
        """

        try:
            result = subprocess.run(
                command, shell=True, capture_output=True, text=True, timeout=None
            )

            return result.stdout
        except subprocess.TimeoutExpired:
            return "Command execution timed out"
        except Exception as e:
            return f"Command execution failed: {str(e)}"

    @staticmethod
    def execute_code(code: str):
        """Executes the python code in the shell and returns the output.

        Args:
            code (str): The code to execute. This should print() the result or process for the output.

        Returns:
            str: The output of the code or an error message
        """

        try:
            result = subprocess.run(
                ["python", "-c", code], capture_output=True, text=True, timeout=None
            )

            return result.stdout
        except subprocess.TimeoutExpired:
            return "Code execution timed out"
        except Exception as e:
            return f"Code execution failed: {str(e)}"

    @staticmethod
    def query_postgres_database(connection_string: str, query: str):
        """Executes SELECT queries on postgres database.

        Args:
            connection_string (str): The connection string for the database.
            query (str): The query to execute.

        Returns:
            str: The output of the query or an error message
        """

        try:
            query_tokens = query.split()

            # lower case all tokens
            query_tokens = [token.lower() for token in query_tokens]

            # check for insert, update, delete, etc queries and throw
            if (
                "insert" in query_tokens
                or "update" in query_tokens
                or "delete" in query_tokens
                or "alter" in query_tokens
                or "create" in query_tokens
                or "drop" in query_tokens
                or "truncate" in query_tokens
                or "grant" in query_tokens
                or "revoke" in query_tokens
            ):
                return f"Query execution failed: only SELECT queries are allowed"

            # execute query
            response = requests.post(
                "http://database-proxy.intelcave.com/api/query",
                json={"connectionString": connection_string, "query": query},
                timeout=60,
            )
            response.raise_for_status()

            result = response.json()

            return result
        except subprocess.TimeoutExpired:
            return "Query execution timed out"
        except Exception as e:
            return f"Query execution failed: {str(e)}"
