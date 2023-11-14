import pandas as pd


XLS_FILE = "ema_data.xlsx"


def parse_dataset(df):
    key_col = df.columns[0]
    tmp = df.dropna().astype(str).set_index(key_col)

    dates = list(tmp.index)
    steps = list(tmp.columns)
    data = list(tmp.to_records())
    return {"dates": dates, "steps": steps, "data": data}


def read_data_from_xls():
    meta = pd.read_excel(XLS_FILE, sheet_name="meta")
    
    sheets = list(meta.sheet)
    dataset_names = list(meta.dataset)

    data = []
    for s, n in zip(sheets, dataset_names):
        df = pd.read_excel(XLS_FILE, sheet_name=s)
        data.append((n, parse_dataset(df)))
    return data


def get_table(data, dates):
    final = []
    for date, row in zip(dates, data):
        idx = row[1]["dates"].index(date)
        for d, st in zip(row[1]["data"][idx], row[1]["steps"]):
            rec = (d, row[0], st)
            final.append(rec)
    df = pd.DataFrame(final)
    df.columns = ["date", "process", "step"]
    return df.set_index("date").sort_index()


def save_xls_file(bytes_data):
    with open(XLS_FILE, 'wb') as file:
        file.write(bytes_data)


def read_xls_file():
    with open(XLS_FILE, 'rb') as file:
        file_data = file.read()
    return file_data


if __name__ == "__main__":
    data = read_data_from_xls()

    table = get_table(data, [x[1]["dates"][0] for x in data]).reset_index()

    table.style.highlight_max(subset="process")