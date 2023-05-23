#  Copyright 2022 The FeatHub Authors
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from datetime import timedelta

from feathub.feathub_client import FeathubClient
from feathub.feature_tables.sinks.file_system_sink import FileSystemSink
from feathub.feature_tables.sinks.kafka_sink import KafkaSink
from feathub.feature_tables.sinks.print_sink import PrintSink
from feathub.feature_tables.sources.kafka_source import KafkaSource
from feathub.feature_views.feature import Feature
from feathub.feature_views.derived_feature_view import DerivedFeatureView
from feathub.feature_views.transforms.over_window_transform import (
    OverWindowTransform,
)

from feathub.common import types
from feathub.feature_tables.sources.file_system_source import FileSystemSource
from feathub.table.schema import Schema

if __name__ == "__main__":
    client = FeathubClient(
        props={
            "processor": {
                "type": "flink",
                "flink": {
                    "master": "localhost:8081",
                    "native.table.exec.source.idle-timeout": "1000",
                },
            },
            "online_store": {
                "types": ["memory"],
                "memory": {},
            },
            "registry": {
                "type": "local",
                "local": {
                    "namespace": "default",
                },
            },
            "feature_service": {
                "type": "local",
                "local": {},
            },
        }
    )

    user_behavior_events_schema = (
        Schema.new_builder()
        .column("user_id", types.String)
        .column("item_id", types.String)
        .column("action_type", types.String)
        .column("timestamp", types.Int64)
        .build()
    )

    user_behavior_events_source = KafkaSource(
        name="user_behavior_events",
        bootstrap_server="kafka:9092",
        topic="user_behavior_events",
        key_format=None,
        value_format="json",
        schema=user_behavior_events_schema,
        consumer_group="feathub",
        timestamp_field="timestamp",
        timestamp_format="epoch",
        startup_mode="earliest-offset",
    )

    item_attributes_schema = (
        Schema.new_builder()
        .column("item_id", types.String)
        .column("brand", types.String)
        .column("category", types.String)
        .column("timestamp", types.Int64)
        .build()
    )

    item_attributes_source = FileSystemSource(
        name="item_attributes",
        path="/tmp/data/item_attributes.csv",
        data_format="csv",
        schema=item_attributes_schema,
        timestamp_field="timestamp",
        timestamp_format="epoch",
        keys=["item_id"],
    )

    enriched_user_behavior_events = DerivedFeatureView(
        name="enriched_user_behavior_events",
        source=user_behavior_events_source,
        features=["item_attributes.brand"],
        keep_source_fields=True,
    )

    client.build_features([item_attributes_source, enriched_user_behavior_events])

    enriched_events_sink = KafkaSink(
        bootstrap_server="kafka:9092",
        topic="enriched_user_behavior_events",
        key_format=None,
        value_format="json",
    )

    result_table = client.get_features(enriched_user_behavior_events)

    result_table_df = result_table.to_pandas(force_bounded=True)

    print(result_table_df)

    job = client.materialize_features(
        enriched_user_behavior_events, enriched_events_sink, allow_overwrite=True
    )
    try:
        job.wait()
    finally:
        job.cancel()
