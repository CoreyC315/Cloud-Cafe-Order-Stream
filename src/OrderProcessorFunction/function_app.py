import azure.functions as func
import logging
import json
import uuid
import os
import pyodbc # For SQL Database connection
import datetime # Added for datetime objects
from azure.identity import DefaultAzureCredential # For Managed Identity

# Initialize the FunctionApp instance
app = func.FunctionApp()

@app.queue_trigger(arg_name="azqueue", queue_name="ordersqueue", connection="AzureWebJobsStorage")
def OrderProcessor(azqueue: func.QueueMessage):
    logging.info('Python queue trigger function processed a message: %s', azqueue.get_body().decode('utf-8'))

    try:
        # 1. Deserialize the incoming order message from the queue
        incoming_order_str = azqueue.get_body().decode('utf-8')
        incoming_order = json.loads(incoming_order_str)

        # Ensure required fields exist, handle gracefully if not
        item_name = incoming_order.get("ItemName")
        quantity = incoming_order.get("Quantity")
        customer_name = incoming_order.get("CustomerName", None) # Optional

        if not item_name or quantity is None:
            logging.error("Missing ItemName or Quantity in the order message: %s", incoming_order_str)
            return

        # 2. Process the order: Assign ID, set status
        order_id = str(uuid.uuid4()) # Generate a unique ID
        order_date = datetime.datetime.utcnow() # Current UTC time for database
        status = "Pending" # Initial status
        processed_by_function_id = "PythonOrderProcessor" # Placeholder, or you can enhance this

        logging.info(f"Processing OrderId: {order_id} - Item: {item_name}")

        # 3. Save to Azure SQL Database
        save_order_to_database(
            order_id, item_name, quantity, customer_name,
            order_date, status, processed_by_function_id
        )

        logging.info(f"Order {order_id} for {item_name} saved successfully to SQL DB.")

    except json.JSONDecodeError as e:
        logging.error(f"JSON decoding error: {e}. Raw message: {azqueue.get_body().decode('utf-8')}")
    except pyodbc.Error as e:
        sqlstate = e.args[0]
        logging.error(f"Database error ({sqlstate}): {e}")
        raise # Re-raise to indicate failure and allow retry policies
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise

def save_order_to_database(order_id, item_name, quantity, customer_name, order_date, status, processed_by_function_id):
    # Retrieve SQL connection details from environment variables (local.settings.json or Azure App Settings)
    sql_server = os.environ.get("SQL_SERVER_NAME")
    sql_database = os.environ.get("SQL_DATABASE_NAME")

    # Connection string for pyodbc
    # Ensure this driver name matches your ODBC Driver installation (e.g., "ODBC Driver 18 for SQL Server")
    connection_string_template = (
        f"Driver={{ODBC Driver 18 for SQL Server}};"
        f"Server=tcp:{sql_server},1433;"
        f"Database={sql_database};"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
        "Connection Timeout=30;"
    )

    conn = None
    try:
        if os.environ.get("AZURE_FUNCTIONS_ENVIRONMENT") == "Development":
            logging.warning("Using SQL admin credentials for local database connection. Switch to Managed Identity for Azure deployment.")
            sql_user = os.environ.get("SQL_ADMIN_USER")
            sql_password = os.environ.get("SQL_ADMIN_PASSWORD")
            conn_str = f"{connection_string_template}UID={sql_user};PWD={sql_password};"
            conn = pyodbc.connect(conn_str)
        else:
            logging.info("Attempting to connect to SQL DB using Managed Identity.")
            credential = DefaultAzureCredential()
            token = credential.get_token("https://database.windows.net/.default").token
            conn_str = f"{connection_string_template}Authentication=ActiveDirectoryAccessToken;"
            conn = pyodbc.connect(conn_str, attrs_before={1256: token})

        cursor = conn.cursor()

        sql_insert = """
        INSERT INTO Orders (OrderId, ItemName, Quantity, CustomerName, OrderDate, Status, ProcessedByFunctionId)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        cursor.execute(
            sql_insert,
            order_id, item_name, quantity, customer_name,
            order_date, status, processed_by_function_id
        )
        conn.commit()
        cursor.close()

    except pyodbc.Error as e:
        sqlstate = e.args[0]
        logging.error(f"Failed to save order to database. SQLSTATE: {sqlstate}, Error: {e}")
        if conn:
            conn.rollback()
        raise
    finally:
        if conn:
            conn.close()
            logging.info("Database connection closed.")