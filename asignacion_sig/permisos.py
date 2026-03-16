# -*- coding: utf-8 -*-
"""
Módulo de Gestión de Permisos PostgreSQL
=========================================

Este módulo proporciona funciones para gestionar permisos de usuarios en bases de datos PostgreSQL.
Incluye operaciones de lectura, asignación y revocación de permisos en tablas y esquemas.

Autor: Servinformación
Versión: 1.0.0
Fecha: 2026-03-09

Funciones principales:
    - obtenerUsuariosYPermisos: Obtiene usuarios con permisos explícitos
    - obtenerPermisosDetallados: Obtiene permisos específicos de un usuario
    - obtenerTablasBaseDatos: Obtiene todas las tablas de la BD
    - revocarPermisosUsuarios: Revoca permisos a usuarios específicos
    - concederPermisos: Genera script SQL para asignar permisos (heredado)

Notas de Seguridad:
    - Todas las consultas usan información_schema para permisos explícitos
    - Los nombres de usuarios y esquemas se entrecomillan para evitar inyección SQL
    - Se validan conexiones antes de ejecutar operaciones
    - No se modifican datos, solo permisos
"""

import psycopg2
from psycopg2 import Error as PostgreSQLError
from datetime import datetime


def obtenerUsuariosYPermisos(host, bd, usuario, contrasena):
    """
    Obtiene lista de usuarios que tienen permisos EXPLÍCITOS en tablas.
    
    Solo retorna usuarios con permisos directamente otorgados (SELECT, INSERT, UPDATE, DELETE),
    excluyendo permisos heredados de roles.
    
    Args:
        host (str): Dirección IP o nombre del servidor PostgreSQL
        bd (str): Nombre de la base de datos
        usuario (str): Usuario administrador para conectarse
        contrasena (str): Contraseña del usuario administrador
    
    Returns:
        list: Lista de tuplas (usuario, permisos_string)
              Ejemplo: [('user1', 'Permisos: SELECT, INSERT'), ('user2', 'Permisos: SELECT')]
    
    Raises:
        Exception: Si hay error en la conexión o consulta SQL
    
    Ejemplo:
        >>> usuarios = obtenerUsuariosYPermisos('localhost', 'mibd', 'admin', 'pass')
        >>> for usuario, permisos in usuarios:
        ...     print(f"{usuario}: {permisos}")
    """
    usuarios_permisos = []
    
    try:
        # Usar context manager para garantizar cierre de conexión
        with psycopg2.connect(
            host=host, 
            database=bd, 
            user=usuario, 
            password=contrasena, 
            port='5432'
        ) as conn:
            with conn.cursor() as cursor:
                # Consulta para obtener SOLO permisos explícitamente otorgados en tablas
                # Usa information_schema.role_table_grants que muestra solo permisos directos
                query = """
                SELECT DISTINCT
                    grantee as usuario,
                    string_agg(DISTINCT privilege_type, ', ' ORDER BY privilege_type) as permisos_tablas
                FROM information_schema.role_table_grants
                WHERE table_schema NOT IN ('pg_catalog', 'information_schema', 'pg_toast')
                    AND grantee NOT IN ('pg_database_owner', 'postgres')
                    AND privilege_type IN ('SELECT', 'INSERT', 'UPDATE', 'DELETE')
                GROUP BY grantee
                ORDER BY grantee;
                """
                
                cursor.execute(query)
                resultados = cursor.fetchall()
                
                # Procesar resultados
                for row in resultados:
                    usuario = row[0]
                    permisos_tablas = row[1] if row[1] else 'Sin permisos'
                    permisos_str = f"Permisos: {permisos_tablas}"
                    usuarios_permisos.append((usuario, permisos_str))
        
        return usuarios_permisos
    
    except PostgreSQLError as e:
        raise Exception(f"Error de PostgreSQL al obtener usuarios: {str(e)}")
    except Exception as e:
        raise Exception(f"Error al obtener usuarios: {str(e)}")


def obtenerPermisosDetallados(host, bd, usuario, contrasena, usuario_objetivo):
    """
    Obtiene los permisos EXPLÍCITOS de un usuario en tablas específicas.
    
    Retorna información detallada sobre qué permisos tiene un usuario en cada tabla
    y esquema de la base de datos.
    
    Args:
        host (str): Dirección IP o nombre del servidor PostgreSQL
        bd (str): Nombre de la base de datos
        usuario (str): Usuario administrador para conectarse
        contrasena (str): Contraseña del usuario administrador
        usuario_objetivo (str): Usuario del cual se desean obtener los permisos
    
    Returns:
        dict: Diccionario con estructura:
              {
                  'SELECT': bool,
                  'INSERT': bool,
                  'UPDATE': bool,
                  'DELETE': bool,
                  'tablas': list de tuplas (esquema, tabla, select, insert, update, delete)
              }
    
    Raises:
        Exception: Si hay error en la conexión o consulta SQL
    
    Ejemplo:
        >>> permisos = obtenerPermisosDetallados('localhost', 'mibd', 'admin', 'pass', 'user1')
        >>> print(f"SELECT: {permisos['SELECT']}")
        >>> for tabla in permisos['tablas']:
        ...     print(tabla)
    """
    try:
        with psycopg2.connect(
            host=host, 
            database=bd, 
            user=usuario, 
            password=contrasena, 
            port='5432'
        ) as conn:
            with conn.cursor() as cursor:
                # Consulta para obtener resumen de permisos del usuario (usando parámetros)
                query = """
                SELECT 
                    CASE WHEN COUNT(CASE WHEN privilege_type = 'SELECT' THEN 1 END) > 0 THEN true ELSE false END as tiene_select,
                    CASE WHEN COUNT(CASE WHEN privilege_type = 'INSERT' THEN 1 END) > 0 THEN true ELSE false END as tiene_insert,
                    CASE WHEN COUNT(CASE WHEN privilege_type = 'UPDATE' THEN 1 END) > 0 THEN true ELSE false END as tiene_update,
                    CASE WHEN COUNT(CASE WHEN privilege_type = 'DELETE' THEN 1 END) > 0 THEN true ELSE false END as tiene_delete
                FROM information_schema.role_table_grants
                WHERE grantee = %s
                    AND table_schema NOT IN ('pg_catalog', 'information_schema', 'pg_toast')
                    AND privilege_type IN ('SELECT', 'INSERT', 'UPDATE', 'DELETE');
                """
                
                cursor.execute(query, (usuario_objetivo,))
                resultado = cursor.fetchone()
                
                # Consulta para obtener detalles por tabla (usando parámetros)
                detalles_query = """
                SELECT 
                    table_schema,
                    table_name,
                    BOOL_OR(CASE WHEN privilege_type = 'SELECT' THEN true ELSE false END) as tiene_select,
                    BOOL_OR(CASE WHEN privilege_type = 'INSERT' THEN true ELSE false END) as tiene_insert,
                    BOOL_OR(CASE WHEN privilege_type = 'UPDATE' THEN true ELSE false END) as tiene_update,
                    BOOL_OR(CASE WHEN privilege_type = 'DELETE' THEN true ELSE false END) as tiene_delete
                FROM information_schema.role_table_grants
                WHERE grantee = %s
                    AND table_schema NOT IN ('pg_catalog', 'information_schema', 'pg_toast')
                    AND privilege_type IN ('SELECT', 'INSERT', 'UPDATE', 'DELETE')
                GROUP BY table_schema, table_name
                ORDER BY table_schema, table_name;
                """
                
                cursor.execute(detalles_query, (usuario_objetivo,))
                detalles_resultados = cursor.fetchall()
        
        # Validar resultado
        if resultado is None or len(resultado) == 0:
            return {
                'SELECT': False,
                'INSERT': False,
                'UPDATE': False,
                'DELETE': False,
                'tablas': []
            }
        
        return {
            'SELECT': bool(resultado[0]) if resultado[0] is not None else False,
            'INSERT': bool(resultado[1]) if resultado[1] is not None else False,
            'UPDATE': bool(resultado[2]) if resultado[2] is not None else False,
            'DELETE': bool(resultado[3]) if resultado[3] is not None else False,
            'tablas': detalles_resultados if detalles_resultados else []
        }
    
    except PostgreSQLError as e:
        raise Exception(f"Error de PostgreSQL al obtener permisos detallados: {str(e)}")
    except Exception as e:
        raise Exception(f"Error al obtener permisos detallados: {str(e)}")


def obtenerTablasBaseDatos(host, bd, usuario, contrasena):
    """
    Obtiene todas las tablas BASE de la base de datos.
    
    Retorna solo tablas reales (no vistas ni objetos del sistema), excluyendo
    esquemas del sistema de PostgreSQL.
    
    Args:
        host (str): Dirección IP o nombre del servidor PostgreSQL
        bd (str): Nombre de la base de datos
        usuario (str): Usuario administrador para conectarse
        contrasena (str): Contraseña del usuario administrador
    
    Returns:
        list: Lista de tuplas (esquema, tabla)
              Ejemplo: [('public', 'usuarios'), ('public', 'productos')]
    
    Raises:
        Exception: Si hay error en la conexión o consulta SQL
    
    Ejemplo:
        >>> tablas = obtenerTablasBaseDatos('localhost', 'mibd', 'admin', 'pass')
        >>> print(f"Total de tablas: {len(tablas)}")
    """
    try:
        with psycopg2.connect(
            host=host, 
            database=bd, 
            user=usuario, 
            password=contrasena, 
            port='5432'
        ) as conn:
            with conn.cursor() as cursor:
                # Consulta para obtener solo tablas BASE (no vistas)
                query = """
                SELECT table_schema, table_name
                FROM information_schema.tables
                WHERE table_schema NOT IN ('pg_catalog', 'information_schema', 'pg_toast')
                AND table_type = 'BASE TABLE'
                ORDER BY table_schema, table_name
                """
                
                cursor.execute(query)
                tablas = cursor.fetchall()
        
        return tablas
    
    except PostgreSQLError as e:
        raise Exception(f"Error de PostgreSQL al obtener tablas: {str(e)}")
    except Exception as e:
        raise Exception(f"Error al obtener tablas: {str(e)}")


def revocarPermisosUsuarios(host, bd, usuario, contrasena, usuarios_a_revocar):
    """
    Revoca TODOS los permisos a usuarios específicos en esquemas y tablas.
    
    Ejecuta comandos REVOKE para eliminar todos los permisos de un usuario
    en todas las tablas y esquemas de la base de datos.
    
    Args:
        host (str): Dirección IP o nombre del servidor PostgreSQL
        bd (str): Nombre de la base de datos
        usuario (str): Usuario administrador para conectarse
        contrasena (str): Contraseña del usuario administrador
        usuarios_a_revocar (list): Lista de nombres de usuarios a los que revocar permisos
    
    Returns:
        bool: True si la operación fue exitosa
    
    Raises:
        Exception: Si hay error en la conexión o ejecución de comandos SQL
    
    Ejemplo:
        >>> revocarPermisosUsuarios('localhost', 'mibd', 'admin', 'pass', ['user1', 'user2'])
        True
    
    Notas:
        - Los nombres de usuarios se entrecomillan para evitar inyección SQL
        - Se ignoran errores de permisos ya revocados
        - Se revoca conexión a la base de datos al final
    """
    try:
        with psycopg2.connect(
            host=host, 
            database=bd, 
            user=usuario, 
            password=contrasena, 
            port='5432'
        ) as conn:
            with conn.cursor() as cursor:
                for user in usuarios_a_revocar:
                    # Revocar permisos en esquemas
                    revoke_query = """
                    SELECT 'REVOKE ALL ON SCHEMA "' || schema_name || '" FROM "' || %s || '";' as cmd
                    FROM information_schema.schemata
                    WHERE schema_name NOT IN ('pg_catalog', 'information_schema', 'pg_toast')
                    """
                    
                    cursor.execute(revoke_query, (user,))
                    revoke_commands = cursor.fetchall()
                    
                    # Ejecutar comandos de revocación
                    for cmd_tuple in revoke_commands:
                        if cmd_tuple and cmd_tuple[0]:
                            try:
                                cursor.execute(cmd_tuple[0])
                            except PostgreSQLError:
                                # Ignorar errores si el permiso ya fue revocado
                                pass
                    
                    # Revocar permisos en tablas
                    revoke_tables_query = """
                    SELECT 'REVOKE ALL ON TABLE "' || table_schema || '"."' || table_name || '" FROM "' || %s || '";' as cmd
                    FROM information_schema.tables
                    WHERE table_schema NOT IN ('pg_catalog', 'information_schema', 'pg_toast')
                    """
                    
                    cursor.execute(revoke_tables_query, (user,))
                    revoke_table_commands = cursor.fetchall()
                    
                    # Ejecutar comandos de revocación en tablas
                    for cmd_tuple in revoke_table_commands:
                        if cmd_tuple and cmd_tuple[0]:
                            try:
                                cursor.execute(cmd_tuple[0])
                            except PostgreSQLError:
                                pass
                    
                    # Revocar conexión a la BD
                    try:
                        revoke_connect_query = 'REVOKE CONNECT ON DATABASE "' + bd + '" FROM "' + user + '";'
                        cursor.execute(revoke_connect_query)
                    except PostgreSQLError:
                        pass
                
                conn.commit()
        
        return True
    
    except PostgreSQLError as e:
        raise Exception(f"Error de PostgreSQL al revocar permisos: {str(e)}")
    except Exception as e:
        raise Exception(f"Error al revocar permisos: {str(e)}")


def registrarLogGestion(host, usuario_admin, contrasena, tipo_gestion, bd_objetivo, usuario_gestionado, permisos, usuario_gestion=None):
    """
    Registra una acción de gestión de permisos en la tabla log_usuarios de 00_LogGestionUsuarios.
    
    Conecta a la base de datos 00_LogGestionUsuarios e inserta un registro con los detalles
    de la acción realizada (asignación, actualización o revocación de permisos).
    
    Args:
        host (str): Dirección IP o nombre del servidor PostgreSQL
        usuario_admin (str): Usuario administrador para conectarse
        contrasena (str): Contraseña del usuario administrador
        tipo_gestion (str): Tipo de acción: 'ASIGNACION PERMISOS', 'ACTUALIZACION PERMISOS', 'QUITAR PERMISOS'
        bd_objetivo (str): Nombre de la base de datos sobre la cual se realizó la acción
        usuario_gestionado (str): Usuario al cual se le asignaron/actualizaron/quitaron permisos
        permisos (str): Permisos asignados/actualizados/quitados (separados por comas)
        usuario_gestion (str, optional): Usuario que ejecutó la acción (por defecto es usuario_admin)
    
    Returns:
        bool: True si el registro se insertó exitosamente
    
    Raises:
        Exception: Si hay error en la conexión o inserción
    
    Ejemplo:
        >>> registrarLogGestion(
        ...     'localhost', 'admin', 'password',
        ...     'ASIGNACION PERMISOS', 'mibd', 'user1', 'SELECT,INSERT',
        ...     usuario_gestion='admin'
        ... )
        True
    
    Notas:
        - La fecha y hora se obtienen del sistema
        - El ID se genera automáticamente en la base de datos (SERIAL)
        - Si la base de datos 00_LogGestionUsuarios no existe, se lanza una excepción
        - Se usa context manager para garantizar cierre de conexión
    """
    try:
        # Usar usuario_admin como usuario_gestion si no se proporciona
        if usuario_gestion is None:
            usuario_gestion = usuario_admin
        
        # Obtener fecha y hora actual
        ahora = datetime.now()
        fecha = ahora.strftime('%Y-%m-%d')
        hora = ahora.strftime('%H:%M:%S')
        
        # Conectar a la base de datos 00_LogGestionUsuarios
        with psycopg2.connect(
            host=host,
            database='00_LogGestionUsuarios',
            user=usuario_admin,
            password=contrasena,
            port='5432'
        ) as conn:
            with conn.cursor() as cursor:
                # Insertar registro en la tabla log_usuarios
                insert_query = """
                INSERT INTO log_usuarios (fecha, hora, usuario_gestion, bd, tipo_gestion, usuario_gestionado, permisos)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                
                cursor.execute(insert_query, (
                    fecha,
                    hora,
                    usuario_gestion,
                    bd_objetivo,
                    tipo_gestion,
                    usuario_gestionado,
                    permisos
                ))
                
                conn.commit()
        
        return True
    
    except psycopg2.Error as e:
        # Si la base de datos no existe o hay error de conexión
        if '00_LogGestionUsuarios' in str(e) or 'does not exist' in str(e):
            raise Exception(f"Base de datos 00_LogGestionUsuarios no encontrada: {str(e)}")
        else:
            raise Exception(f"Error de PostgreSQL al registrar log: {str(e)}")
    except Exception as e:
        raise Exception(f"Error al registrar log de gestión: {str(e)}")


def concederPermisos(profesionales, usuarios, bd):
    """
    FUNCIÓN HEREDADA - Genera script SQL para asignar permisos.
    
    Esta función está deprecada. Se recomienda usar las funciones individuales
    de asignación de permisos en validaciones_dialog.py
    
    Args:
        profesionales (str): Usuarios profesionales separados por comas
        usuarios (str): Usuarios digitalizadores separados por comas
        bd (str): Nombre de la base de datos
    
    Returns:
        str: Script SQL con comandos GRANT
    
    Nota:
        Esta función genera un script SQL completo pero no lo ejecuta.
        Se mantiene por compatibilidad con código anterior.
    """
    query = """
    --QUITAR PERMISOS
    DO $
    DECLARE
        r RECORD;
        s RECORD;
    BEGIN
        -- Revocar permisos en todos los esquemas
        FOR s IN
            SELECT nspname
            FROM pg_namespace
            WHERE nspname NOT IN ('pg_catalog', 'information_schema')
        LOOP
            FOR r IN
                SELECT rolname
                FROM pg_roles
                WHERE has_schema_privilege(rolname, s.nspname, 'USAGE')
            LOOP
                EXECUTE format('REVOKE CONNECT ON DATABASE %I FROM %I;', current_database(), r.rolname);
                EXECUTE format('REVOKE ALL ON SCHEMA %I FROM %I;', s.nspname, r.rolname);
                EXECUTE format('REVOKE ALL ON ALL TABLES IN SCHEMA %I FROM %I;', s.nspname, r.rolname);
                EXECUTE format('REVOKE ALL ON ALL SEQUENCES IN SCHEMA %I FROM %I;', s.nspname, r.rolname);
                EXECUTE format('REVOKE ALL ON ALL FUNCTIONS IN SCHEMA %I FROM %I;', s.nspname, r.rolname);
            END LOOP;
        END LOOP;
    END $;
    
    /*DAR PERMISOS A PROFESIONAL SIG*/
    
    DO
    $
    DECLARE
        schema_name text;
    BEGIN
        FOR schema_name IN
            SELECT nspname
            FROM pg_catalog.pg_namespace
            WHERE nspname NOT IN ('pg_catalog', 'information_schema')
        LOOP
            -- Otorgar permisos completos en cada esquema para el usuario_A
            EXECUTE format('GRANT USAGE ON SCHEMA %I TO {profesionales}', schema_name);
            EXECUTE format('GRANT INSERT, UPDATE, DELETE, SELECT ON ALL TABLES IN SCHEMA %I TO {profesionales}', schema_name);
            EXECUTE format('GRANT USAGE, SELECT, UPDATE ON ALL SEQUENCES IN SCHEMA %I TO {profesionales}', schema_name);
            EXECUTE format('GRANT TRUNCATE, REFERENCES ON ALL TABLES IN SCHEMA %I TO {profesionales}', schema_name);
            EXECUTE format('GRANT ALL ON ALL SEQUENCES IN SCHEMA %I TO {profesionales}', schema_name);
            EXECUTE format('GRANT ALL ON ALL FUNCTIONS IN SCHEMA %I TO {profesionales}', schema_name);
            EXECUTE format('GRANT CREATE ON SCHEMA %I TO {profesionales}', schema_name);
            EXECUTE format('GRANT USAGE ON SCHEMA %I TO {profesionales}', schema_name);
        END LOOP;

        -- Permiso de creación y eliminación de tablas en la base de datos para usuario_A
        GRANT CREATE, TEMPORARY, CONNECT ON DATABASE "{bd}" TO {profesionales};
    END
    $;

    /*DAR PERMISOS A DIGITALIZADORES*/

    GRANT CONNECT ON DATABASE "{bd}" TO latam_alex_camelo, {usuarios};
    
    DO
    $
    DECLARE
        schema_record RECORD;
        schemas CURSOR FOR 
            SELECT schema_name 
            FROM information_schema.schemata 
            WHERE schema_name NOT IN ('information_schema', 'pg_catalog', 'pg_toast') 
            AND schema_name NOT LIKE 'pg_temp%';
    BEGIN
        FOR schema_record IN schemas LOOP
            EXECUTE format('GRANT USAGE ON SCHEMA %I TO latam_alex_camelo, {usuarios};', schema_record.schema_name);
            EXECUTE format('GRANT DELETE, SELECT, UPDATE, INSERT ON ALL TABLES IN SCHEMA %I TO latam_alex_camelo, {usuarios};', schema_record.schema_name);
            EXECUTE format('GRANT ALL ON ALL SEQUENCES IN SCHEMA %I TO latam_alex_camelo, {usuarios};', schema_record.schema_name);
            EXECUTE format('GRANT ALL ON ALL FUNCTIONS IN SCHEMA %I TO latam_alex_camelo, {usuarios};', schema_record.schema_name);
        END LOOP;
    END;
    $;

    """.format(bd=bd, profesionales=profesionales, usuarios=usuarios)

    return query
