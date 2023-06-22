import streamlit as st
import pyodbc

# Establecer la cadena de conexión a la base de datos
connection_string = ''

# Obtener el código del procedimiento almacenado "GSOCWAddWithoutSage"
def get_procedure_code(procedure_name):
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()

    # Ejecutar una consulta para obtener el código del procedimiento almacenado
    cursor.execute(f"EXEC sp_helptext '{procedure_name}'")
    code_rows = cursor.fetchall()
    
    # Unir las filas del código en una sola cadena
    code = '\n'.join([row[0] for row in code_rows])

    cursor.close()
    conn.close()

    return code

# Función para mostrar el código del procedimiento almacenado en un textarea
def show_procedure_code(procedure_name):
    code = get_procedure_code(procedure_name)
    st.subheader(f"Código del procedimiento almacenado: {procedure_name}")
    st.text_area("Código del procedimiento almacenado", value=code)

# Mostrar la lista de tablas y procedimientos almacenados en una tabla
def show_table_procedure_list():
    st.header("Tablas y Procedimientos almacenados en la base de datos")

    # Obtener la lista de tablas y procedimientos almacenados
    tables = get_table_list()
    procedures = get_procedure_list()

    # Crear una lista combinada de tablas y procedimientos
    combined_list = tables + procedures

    # Mostrar la lista en una tabla
    selected_item = st.table(combined_list)


# Obtener la lista de tablas en la base de datos
def get_table_list():
    conn = pyodbc.connect(connection_string)
    tables = conn.cursor().tables(tableType='TABLE')
    table_list = [table.table_name for table in tables]
    conn.close()
    return table_list

# Obtener la lista de procedimientos almacenados en la base de datos
def get_procedure_list():
    conn = pyodbc.connect(connection_string)
    procedures = conn.cursor().procedures()
    procedure_list = [procedure.procedure_name.split(';')[0] for procedure in procedures]
    conn.close()
    return procedure_list

st.write(get_procedure_code("GSOCWAddWithoutSage"))
# Llamar a la función para mostrar la lista de tablas y procedimientos almacenados
show_table_procedure_list()
