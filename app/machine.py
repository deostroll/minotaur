import psutil
import platform
import csv
from consts import utility as util
import os.path


def _process_dict(_dict):
    new_dict = {}
    for key, value in _dict.items():
        new_dict[key] = _convert(value)
    return new_dict

def _process_iter(_iter):
    return [ _convert(x) for x in _iter]

def _convert(item):
    if type(item) == dict:
        return _process_dict(item)
    elif type(item) in [list, tuple]:
        return _process_iter(item)
    elif hasattr(item, '_asdict'):
        return _convert(item._asdict())
    else:
        return item
    

def _get_psutil_param(param):
    if param == 'networks':
        ifaces = psutil.net_if_addrs()
        return _convert(ifaces)
    elif param == 'cpu_cores':
        return psutil.cpu_count(logical=False)
    elif param == 'storage':
        return _convert(psutil.disk_partitions())
    elif param == 'memory':
        return _convert(psutil.virtual_memory())
    else:
        return None


def get_machine_info():
    filename = 'params.csv'
    dirname = os.path.dirname(__file__)

    info = {}
    with open(os.path.join(dirname, filename)) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            if len(row) == 0:
                return

            key, utility = row

            if utility == util.PSUTIL:
                info[key] = _get_psutil_param(key)
            else:
                info[key] = _convert(platform.uname())

    return info
if __name__ == '__main__':
    info = get_machine_info()
    # from pprint import pprint as pp
    # pp(info)
    import json
    print(json.dumps(info, indent=2))