from django.db import DEFAULT_DB_ALIAS, connections
from django.db.migrations import RunSQL


def quote_ident(ident):
    return f'"{ident}"'


def col(model_field) -> str:
    if hasattr(model_field, "field"):
        return quote_ident(model_field.field.column)

    if hasattr(model_field, "descriptor"):
        return quote_ident(model_field.descriptor.field.column)

    raise ValueError()


def table(model) -> str:
    return quote_ident(model._meta.db_table)  # pylint: disable=protected-access


def value(literal) -> str:
    literal = str(literal).replace("'", "''")
    return f"'{literal}'"


class MaterializedViewMixin:
    class Meta:
        managed = False

    @classmethod
    def get_migrate_create_sql(cls):
        return cls.get_create_sql(), cls.get_remove_sql()

    @classmethod
    def get_migrate_update_sql(cls):
        return cls.get_recreate_sql(), RunSQL.noop

    @classmethod
    def get_create_sql(cls):
        raise NotImplementedError()

    @classmethod
    def get_recreate_sql(cls):
        return cls.get_remove_sql() + cls.get_create_sql()

    @classmethod
    def get_remove_sql(cls):
        return f"""
            DROP MATERIALIZED VIEW {table(cls)};
        """

    @classmethod
    def refresh(cls, concurrently=False, using=DEFAULT_DB_ALIAS):
        sql = f"""
            REFRESH MATERIALIZED VIEW {"CONCURRENTLY" if concurrently else ""} {table(cls)};
        """

        with connections[using].cursor() as cursor:
            cursor.execute(sql)
