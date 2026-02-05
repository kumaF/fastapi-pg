from collections.abc import Mapping
from time import perf_counter_ns
from typing import Any

from sqlalchemy import event
from sqlalchemy.engine import Connection
from sqlalchemy.engine.interfaces import ExecutionContext

from app.core.cache import set_cache
from app.core.request import get_request_id
from app.db.base import async_engine


@event.listens_for(async_engine.sync_engine, 'before_cursor_execute')
def before_cursor_execute(
    conn: Connection,
    cursor: Any,
    statement: str,
    parameters: Mapping[str, Any] | tuple[Any, ...],
    context: ExecutionContext,
    executemany: bool,
) -> None:
    """Record the start time of a SQL query execution.

    This listener runs immediately before the database cursor executes
    a SQL statement. The timestamp is stored on the SQLAlchemy execution
    context so it can be used later to calculate query duration.

    Args:
        conn: The SQLAlchemy connection being used.
        cursor: The DBAPI cursor executing the statement.
        statement: The SQL statement to be executed.
        parameters: Parameters passed to the SQL statement.
        context: SQLAlchemy execution context for the statement.
        executemany: Whether the statement is executed with executemany().
    """
    _ = conn, cursor, statement, parameters, executemany
    context._query_start_time = perf_counter_ns()


@event.listens_for(async_engine.sync_engine, 'after_cursor_execute')
def after_cursor_execute(
    conn: Connection,
    cursor: Any,
    statement: str,
    parameters: Mapping[str, Any] | tuple[Any, ...],
    context: ExecutionContext,
    executemany: bool,
) -> None:
    """Compute and store the duration of a SQL query execution.

    This listener runs immediately after the database cursor finishes
    executing a SQL statement. It calculates the elapsed time using the
    timestamp recorded in `before_cursor_execute` and stores the result
    in a request-scoped cache.

    Args:
        conn: The SQLAlchemy connection being used.
        cursor: The DBAPI cursor that executed the statement.
        statement: The executed SQL statement.
        parameters: Parameters passed to the SQL statement.
        context: SQLAlchemy execution context for the statement.
        executemany: Whether the statement was executed with executemany().
    """
    _ = conn, cursor, statement, parameters, executemany
    end_time: int = perf_counter_ns()
    duration_ns: int = end_time - context._query_start_time
    set_cache(get_request_id(), duration_ns)
