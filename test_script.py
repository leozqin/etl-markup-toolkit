from etl_markup_toolkit.etl_process import ETLProcess
from json import dumps

if __name__ == "__main__":

    cfg_path = "tests/configs/main.yml"
    params_path = "tests/configs/params.yml"

    process = ETLProcess(cfg_path=cfg_path, params_path=params_path)

    process.execute()

    report = process.get_report()
    print(dumps(report))