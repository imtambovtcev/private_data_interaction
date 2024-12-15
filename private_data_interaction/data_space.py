import json

import numpy as np
import pandas as pd


class DataSpace:
    def __init__(self, min_bin_population=10):
        self.data = {}
        self.metadata = {}
        self.min_bin_population = min_bin_population

    def create_user_space(self, df_name_list, shuffle=False):
        space = DataSpace(min_bin_population=self.min_bin_population)
        for df_name in df_name_list:
            space.data[df_name] = self.data[df_name].copy()
            space.metadata[df_name] = self.metadata[df_name].copy()
            if shuffle:
                for column in space.data[df_name].columns:
                    space.data[df_name][column] = np.random.permutation(
                        space.data[df_name][column].values)
        return space

    ### df_methods ###

    def copy_df(self, df_name, new_df_name):
        if new_df_name in self.data:
            return 'A dataframe with that name already exists, aborting.'

        self.data[new_df_name] = self.data[df_name].copy()
        # Deep copy metadata dictionary to avoid references
        self.metadata[new_df_name] = {
            'columns': {col_name: col_meta.copy() for col_name, col_meta in self.metadata[df_name]['columns'].items()}
        }

        return 'Operation successful.'

    def drop_df(self, df_name):
        del self.data[df_name]
        del self.metadata[df_name]
        return 'Operation successful.'

    def drop_column(self, df_name, column):
        self.data[df_name].drop(column, axis=1, inplace=True)
        # Remove the column from the metadata dictionary
        if column in self.metadata[df_name]['columns']:
            del self.metadata[df_name]['columns'][column]
        return 'Operation successful.'

    def filter_df(self, df_name, column, value):
        df = self.data[df_name][self.data[df_name][column] == value]
        if len(df) < self.min_bin_population:
            return 'Operation would result in a dataframe with less than the minimum bin population, aborting.'
        else:
            self.data[df_name] = df
            return 'Operation successful.'

    def merge_df(self, left_df_name, right_df_name, on, new_df_name, how='inner'):
        # Check if the new dataframe name is already used
        if new_df_name in self.data:
            return 'A dataframe with that name already exists, aborting.'

        # Check that both dataframes exist
        if left_df_name not in self.data or right_df_name not in self.data:
            return 'One or both of the specified dataframes do not exist, aborting.'

        # Perform the merge operation
        merged_df = self.data[left_df_name].merge(
            self.data[right_df_name], on=on, how=how)

        # Check the size of the merged dataframe
        if len(merged_df) < self.min_bin_population:
            return 'Operation would result in a dataframe with less than the minimum bin population, aborting.'

        # Combine metadata from both dataframes
        left_metadata_cols = self.metadata[left_df_name]['columns']
        right_metadata_cols = self.metadata[right_df_name]['columns']

        combined_metadata = {}
        for col_name in merged_df.columns:
            if col_name in left_metadata_cols:
                combined_metadata[col_name] = left_metadata_cols[col_name]
            elif col_name in right_metadata_cols:
                combined_metadata[col_name] = right_metadata_cols[col_name]
            else:
                # If the column doesn't appear in either metadata,
                # create a default metadata entry for it.
                combined_metadata[col_name] = {
                    "type": "unknown",
                    "description": "No metadata found."
                }

        # Store the merged data and metadata
        self.data[new_df_name] = merged_df
        self.metadata[new_df_name] = {
            'columns': combined_metadata
        }

        return 'Operation successful.'

    def rename_column(self, df_name, old_column, new_column):
        if new_column in self.data[df_name].columns:
            return 'A column with that name already exists, aborting.'

        self.data[df_name].rename(
            columns={old_column: new_column}, inplace=True)

        # Update the metadata dictionary keys
        if old_column in self.metadata[df_name]['columns']:
            col_data = self.metadata[df_name]['columns'].pop(old_column)
            self.metadata[df_name]['columns'][new_column] = col_data

        return 'Operation successful.'

    ######

    def add_data_from_data_and_metadata_files(self, df_name, data_file, metadata_file):
        with open(metadata_file) as f:
            metadata = json.load(f)
            self.metadata[df_name] = metadata

        df = pd.read_csv(data_file)
        self.data[df_name] = df

    @property
    def sources(self):
        return list(self.data.keys())

    def columns(self, source):
        if source not in self.data:
            return None

        return self.data[source].columns

    def _distribution_of(self, df, column, bin_ranges=None):
        if column not in df.columns:
            return None

        valid_data = df[column].dropna()

        if bin_ranges is None:
            bin_ranges = np.histogram_bin_edges(valid_data, bins='auto')

        distribution_counts, bin_edges = np.histogram(
            valid_data, bins=bin_ranges)

        distribution_df = pd.DataFrame({
            'Bin Range': [f"{bin_edges[i]} - {bin_edges[i + 1]}" for i in range(len(bin_edges) - 1)],
            'Count': distribution_counts
        })

        distribution_df.loc[distribution_df['Count']
                            < self.min_bin_population, 'Count'] = 0

        return distribution_df

    def request_distribution_of(self, source, column, bin_ranges=None):
        if source not in self.data:
            return None

        df = self.data[source]
        distribution_df = self._distribution_of(df, column, bin_ranges)
        return distribution_df.to_json()

    def request_metadata(self, source):
        if source not in self.metadata:
            return None

        return self.metadata[source]

    def _column_metadata(self, source, column):
        if source not in self.metadata:
            return None

        return self.metadata[source]['columns'].get(column, None)

    def request_column_metadata(self, source, column):
        return self._column_metadata(source, column)

    def request_is_column_standard_unique_identifier(self, source, column):
        metadata = self._column_metadata(source, column)
        return metadata.get('is_standard_unique_identifier', False) if metadata else False

    def request_length_of_df(self, source):
        return len(self.data[source])

    def info(self):
        for source in self.sources:
            print(f"Source: {source}")
            print(f"Columns: {self.columns(source)}")
            print(f"Length: {self.request_length_of_df(source)}")
            print(f"Metadata: {self.request_metadata(source)}")
            print()
