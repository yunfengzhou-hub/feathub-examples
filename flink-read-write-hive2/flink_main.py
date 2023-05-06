from datetime import datetime

from feathub.processors.flink.flink_jar_utils import add_jar_to_t_env
from feathub.processors.flink.table_builder.hive_utils import _get_hive_connector_jars
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment, DataTypes
from pyflink.table.catalog import HiveCatalog

env = StreamExecutionEnvironment.get_execution_environment()
t_env = StreamTableEnvironment.create(env)

add_jar_to_t_env(t_env, *_get_hive_connector_jars())

hive_catalog = HiveCatalog(
    catalog_name="myhive",
    hive_conf_dir=".",
)

t_env.register_catalog("myhive", hive_catalog)

row_data = [
    (1, 2, datetime(2022, 1, 1, 0, 0, 0).strftime("%Y-%m-%d %H:%M:%S")),
    (2, 3, datetime(2022, 1, 1, 0, 0, 1).strftime("%Y-%m-%d %H:%M:%S")),
    (3, 4, datetime(2022, 1, 1, 0, 0, 2).strftime("%Y-%m-%d %H:%M:%S")),
]
table = t_env.from_elements(
    row_data,
    DataTypes.ROW(
        [
            DataTypes.FIELD("id", DataTypes.BIGINT()),
            DataTypes.FIELD("val", DataTypes.BIGINT()),
            DataTypes.FIELD("ts", DataTypes.STRING()),
        ]
    ),
)

table.execute_insert("myhive.`default`.mytable");

