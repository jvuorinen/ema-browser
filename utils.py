import pandas as pd
from matplotlib.colors import LinearSegmentedColormap


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

    data = {}
    for s, n in zip(sheets, dataset_names):
        df = pd.read_excel(XLS_FILE, sheet_name=s)
        data[n] = parse_dataset(df)
    return data


def get_table(data, chosen: dict):
    final = []

    for p, start in chosen.items():
        idx = data[p]["dates"].index(start)
        for d, step in zip(data[p]["data"][idx], data[p]["steps"]):
            rec = d, p, step
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


def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4))


def get_color_map(hex_a, hex_b, hex_c):
    colors = [hex_to_rgb(hex_a), hex_to_rgb(hex_b), hex_to_rgb(hex_c)]
    positions = [0.0, 0.5, 1.0]

    cmap = LinearSegmentedColormap.from_list('custom_cmap', list(zip(positions, colors)), N=256)
    return cmap


if __name__ == "__main__":
    data = read_data_from_xls()

    chosen = {}

    table = get_table(data, [x[1]["dates"][0] for x in data]).reset_index()

    table.style.highlight_max(subset="process")
   