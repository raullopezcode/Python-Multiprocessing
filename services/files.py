import csv
from config.Factory import ConfigFactory

def get_files_info():
    files = {
        'breast': 'datasets/breast.csv',
    }

    info = []
    for name, path in files.items():
        with open(path, 'r') as f:
            config = ConfigFactory.from_name(name)
            reader = csv.reader(f)
            columns = len(next(reader))
            f.seek(0)
            rows = sum(1 for _ in reader)
            
            info.append({
                'id': name,
                'name': config['name'],
                'columns': columns,
                'rows': rows,
            })

    return info