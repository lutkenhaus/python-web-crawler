import pandas as pd


def save_new_spreadsheet(dataframe, filename):
    df = pd.DataFrame(data=dataframe)
    df.to_excel("./dados/" + filename + ".xlsx", index=False)


def read_spreadsheet_as_a_list(filename):
    df = pd.read_excel("./dados/" + filename + ".xlsx", header=None)
    list = df.values.tolist()
    return list


def append_to_existing_spreadsheet(lista, filename):

    dataframe = pd.DataFrame(data=lista)
    df_existing_data = pd.read_excel(filename)
    df_merged = df_existing_data.append(dataframe, ignore_index=True)
    df_merged.to_excel(filename, index=False)
    print("operação finalizada!")
