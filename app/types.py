from typing import Literal


class ColumnID(str):
    pass


class ColumnName(str):
    pass


class ColumnType(str):
    def __init__(
        self,
        _type: Literal[
            # Numeric
            "TINYINT",
            "SMALLINT",
            "MEDIUMINT",
            "INT",
            "INTEGER",
            "BIGINT",
            "DECIMAL",
            "NUMERIC",
            "FLOAT",
            "DOUBLE",
            "REAL",
            "BIT",
            # String
            "CHAR",
            "VARCHAR",
            "TEXT",
            "TINYTEXT",
            "MEDIUMTEXT",
            "LONGTEXT",
            "ENUM",
            "SET",
            # Date & Time
            "DATE",
            "DATETIME",
            "TIMESTAMP",
            "TIME",
            "YEAR",
            # JSON & Binary
            "JSON",
            "BLOB",
            "TINYBLOB",
            "MEDIUMBLOB",
            "LONGBLOB",
            # Spatial / GIS
            "GEOMETRY",
            "POINT",
            "LINESTRING",
            "POLYGON",
        ],
    ) -> None:
        super().__init__()

        self._type = _type
