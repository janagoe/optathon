import os
import json
import pandas as pd


class Generator:

    def __init__(self, tasks, batch_size=None):
        self.batch_size = batch_size

        customer_instances = tasks * 2

        if customer_instances not in [200, 400, 600, 800, 1000]:
            raise Exception("Not possible")

        folder = 'homberger_{}_customer_instances'.format(customer_instances)
        self.path = os.path.join(
            os.getcwd(), 'generator', 'homberger', folder)

        for filename in os.listdir(self.path):
            filepath = os.path.join(self.path, filename)

            df = self.load_dataframe(filepath)
            obj, number_of_tasks = self.create_object(df)

            output_filename = self.get_output_filename(
                filename.split('.')[0], number_of_tasks)

            output_filepath = os.path.join(
                os.getcwd(), 'datasets', 'batches', output_filename)

            self.write_json(obj, output_filepath)

    def load_dataframe(self, filepath: str):
        with open(filepath, 'r') as file:
            file_content = file.read()

        sections = file_content.strip().split('\n\n')
        data = {}

        for section in sections:
            lines = section.strip().split('\n')
            header = lines[0].strip()

            if len(lines) <= 3:
                continue

            data_lines = [line.split() for line in lines[1:]]

            columns = ['CUST NO.', 'XCOORD.', 'YCOORD.', 'DEMAND',
                       'READY TIME', 'DUE DATE', 'SERVICE TIME']

            df = pd.DataFrame(data_lines[2:], columns=columns)

            df['CUST NO.'] = df['CUST NO.'].astype(int)
            df['XCOORD.'] = df['XCOORD.'].astype(int)
            df['YCOORD.'] = df['YCOORD.'].astype(int)
            df['READY TIME'] = df['READY TIME'].astype(int)
            df['DUE DATE'] = df['DUE DATE'].astype(int)

            del df['DEMAND']
            del df['SERVICE TIME']

            df['DIFF'] = df['DUE DATE'] - df['READY TIME']

            df.sort_values('READY TIME', inplace=True)

            return df

    def create_object(self, df: pd.DataFrame):
        obj = dict()
        obj['batches'] = []

        tasks = []

        task_id = 0
        batch_id = 0
        for i in range(0, len(df)-1, 2):
            r1 = df.iloc[i]
            r2 = df.iloc[i+1]

            task = {
                'id': task_id,
                'earliest_start': int(r1['READY TIME']),
                'latest_finish': int(max(r1['DUE DATE'], r2['DUE DATE'])),
                'start_location': (int(r1['XCOORD.']), int(r1['YCOORD.'])),
                'end_location':  (int(r2['XCOORD.']), int(r2['YCOORD.']))
            }

            task_id += 1
            tasks.append(task)

            if self.batch_size is not None and len(tasks) >= self.batch_size:
                obj['batches'].append({
                    'id': batch_id,
                    'tasks': tasks
                })

                batch_id += 1
                tasks = []

        if len(tasks) > 0:
            obj['batches'].append({
                'id': batch_id,
                'tasks': tasks
            })

            batch_id += 1
            tasks = []

        return obj, task_id

    def write_json(self, obj: dict, output_path: str):
        try:
            if os.path.exists(output_path):
                os.remove(output_path)  # Remove the file if it already exists

            with open(output_path, 'w') as json_file:
                json.dump(obj, json_file, indent=4)
        except TypeError as e:
            raise TypeError(
                "Error: The object cannot be serialized into JSON.") from e
        except OSError as e:
            raise OSError(
                f"Error: Unable to write the JSON file at {output_path}.") from e

    def get_output_filename(self, filename, number_of_tasks):
        return "tasks_{}_batchsize_{}_{}.json".format(number_of_tasks, self.batch_size, filename)
