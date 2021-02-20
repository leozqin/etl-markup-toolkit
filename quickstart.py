from etl_markup_toolkit.etl_process import ETLProcess
from json import dumps
from sys import argv

if __name__ == "__main__":

    cfg_path = argv[1]
    params_path = argv[2]

    process = ETLProcess(cfg_path=cfg_path, params_path=params_path)

    process.execute()

    report = process.get_report()
    print(dumps(report))