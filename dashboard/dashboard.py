import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import OrderedDict
sns.set(style='dark')

st.title('Air Quality')

task1, task2 = st.tabs(["Task 1", "Task 2"])
all_df = pd.read_csv("main_data.csv")
aotizhongxin = all_df.loc[all_df["station"] == "Aotizhongxin"]
changping = all_df.loc[all_df["station"] == "Changping"]
dingling = all_df.loc[all_df["station"] == "Dingling"]
dongsi = all_df.loc[all_df["station"] == "Dongsi"]
guanyuan = all_df.loc[all_df["station"] == "Guanyuan"]
gucheng = all_df.loc[all_df["station"] == "Gucheng"]
huairou = all_df.loc[all_df["station"] == "Huairou"]
nongzhanguan = all_df.loc[all_df["station"] == "Nongzhanguan"]
shunyi = all_df.loc[all_df["station"] == "Shunyi"]
tiantan = all_df.loc[all_df["station"] == "Tiantan"]
wanliu = all_df.loc[all_df["station"] == "Wanliu"]
wanshouxigong = all_df.loc[all_df["station"] == "Wanshouxigong"]

def perbandingan_setiap_tahun_barchart(data, ax):
    bars = ax.bar(
        list(data.keys()),
        list(data.values()),
        color ='maroon', 
        width = 0.4
    )

    for i, bar in enumerate(bars):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), str(round(list(kadar_year.values())[i], 2)), ha='center', va='bottom', fontsize=20)

    ax.set_xlabel("Tahun", fontsize=30)
    ax.set_ylabel("Rata-rata kadar senyawa CO", fontsize=35)
    ax.set_ylim(1100, 1700)
    ax.set_title("Bar chart", loc="center", fontsize=50)
    ax.tick_params(axis='y', labelsize=35)
    ax.tick_params(axis='x', labelsize=30)

def perbandingan_setiap_tahun_linechart(data, ax):
    ax.plot(list(data.keys()), list(data.values()), color ='maroon', marker='o')

    for i, value in enumerate(list(data.values())):
        ax.text(list(data.keys())[i], value, str(round(value, 2)), ha='center', va='bottom', rotation=45)

    ax.set_xlabel("Tahun", fontsize=30)
    ax.set_xticks(list(data.keys()), list(data.keys()), rotation=45, ha='center')
    ax.set_ylabel("Rata-rata kadar senyawa CO", fontsize=35)
    ax.set_ylim(1100, 1700)
    ax.set_title("Line chart", loc="center", fontsize=50)
    ax.tick_params(axis='y', labelsize=35)
    ax.tick_params(axis='x', labelsize=30)
    ax.grid(True)

def perbandingan_kenaikan_tiap_bulan_linechart(data, ax):
    year_months, values = data
    ax.plot(year_months, values, marker='o', color='maroon')

    ax.set_xlabel("Bulan - Tahun", fontsize=30)
    ax.set_xticklabels(year_months, rotation=90, ha='center')
    ax.set_ylabel("Nilai", fontsize=35)
    ax.tick_params(axis='y', labelsize=35)
    ax.tick_params(axis='x', labelsize=30)
    ax.set_title("Line chart", loc="center", fontsize=50)

def perbandingan_kenaikan_tiap_bulan_tahun_linechart(data, ax):
    all_year = []
    all_color = ["maroon", "chocolate", "green", "navy", "indigo"]
    all_month = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1: thn_2013 = st.checkbox('2013', value=True)
    with col2: thn_2014 = st.checkbox('2014', value=True)
    with col3: thn_2015 = st.checkbox('2015', value=True)
    with col4: thn_2016 = st.checkbox('2016', value=True)
    with col5: thn_2017 = st.checkbox('2017', value=True)

    if thn_2013: all_year.append(2013)
    if thn_2014: all_year.append(2014)
    if thn_2015: all_year.append(2015)
    if thn_2016: all_year.append(2016)
    if thn_2017: all_year.append(2017)

    for i in range(len(all_year)):
        year = all_year[i]
        color = all_color[i]
        data = dict_data[year]

        year_months = []
        values = []
        for month, value in data.items():
            year_months.append(f'{all_month[month-1]}')
            values.append(value)

        ax.plot(year_months, values, marker='o', color=color, label=year, linewidth=2, markersize=12)

    ax.set_xlabel("Bulan", fontsize=30)
    ax.set_ylabel("Nilai", fontsize=35)
    ax.set_title("Line chart", loc="center", fontsize=50)
    ax.tick_params(axis='y', labelsize=35)
    ax.tick_params(axis='x', labelsize=30)
    ax.legend(loc="upper left", fontsize='xx-large')
    
def get_data_year(df):
    year = df.groupby('year')
    year_co = year['CO'].mean()
    kadar_year = {}
    for year, value in year_co.items():
        kadar_year[year] = value

    return kadar_year

def get_data_year_month_values(df):
    year_month = df.groupby(['year', 'month'])
    mean_year_month = year_month['CO'].mean()
    mean_year_month = mean_year_month.reset_index()

    dict_data = {}
    for year, month, value in mean_year_month.values:
        dict_data[(int(year), int(month))] = value
        
    all_month = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    year_months = []
    values = []
    for key, value in dict_data.items():
        year, month = key
        year_months.append(f'{all_month[month-1]} {year}')
        values.append(value)

    return year_months, values

def get_data_month_values(df):
    dict_data = {}

    dict_data[2013] = {}
    dict_data[2013][1] = None
    dict_data[2013][2] = None

    year_month = df.groupby(['year', 'month'])
    mean_year_month = year_month['CO'].mean()
    mean_year_month = mean_year_month.reset_index()

    for year, month, value in mean_year_month.values:
        try:
            data = dict_data[int(year)]
        except:
            data = {}
        
        data[int(month)] = value
        dict_data[int(year)] = data

    dict_data[2017][3] = None
    dict_data[2017][4] = None
    dict_data[2017][5] = None
    dict_data[2017][6] = None
    dict_data[2017][7] = None
    dict_data[2017][8] = None
    dict_data[2017][9] = None
    dict_data[2017][10] = None
    dict_data[2017][11] = None
    dict_data[2017][12] = None

    return dict_data

def senyawa_kadar_visualisasi(senyawa, ax):
    stasiun = ["Aotizhongxin", "Changping", "Dingling", "Dongsi", "Guanyuan", "Gucheng",
            "Huairou", "Nongzhanguan", "Shunyi", "Tiantan", "Wanliu", "Wanshouxigong"]
    
    all_data = [aotizhongxin, changping, dingling, dongsi, guanyuan, gucheng,
            huairou, nongzhanguan, shunyi, tiantan, wanliu, wanshouxigong]
    
    stasiun_kadar = {}
    for i in range(len(all_data)):
        stasiun_kadar[stasiun[i]] = all_data[i][senyawa].mean()

    sorted_stasiun_kadar = OrderedDict(sorted(stasiun_kadar.items(), key=lambda x: x[1]))

    ax.bar(list(sorted_stasiun_kadar.keys()), list(sorted_stasiun_kadar.values()), color ='maroon', width = 0.4)
    ax.set_xlabel("Tempat Stasion", fontsize=30)
    ax.set_xticklabels(list(sorted_stasiun_kadar.keys()), rotation=45, ha='right')
    ax.set_ylabel("Rata-rata Kadar Senyawa", fontsize=35)
    ax.tick_params(axis='y', labelsize=35)
    ax.tick_params(axis='x', labelsize=30)
    ax.set_title(f'Kadar Senyawa {senyawa} pada setiap stasiun', fontsize=35)

def all_senyawa_kadar_visualisasi(df, ax, station):
    all_senyawa = ["PM2.5", "PM10", "SO2", "NO2", "CO", "O3"]
    kadar = df[all_senyawa].mean()
    
    kadar_senyawa = {}
    for i in range(len(all_senyawa)):
        senyawa = all_senyawa[i]
        kadar_senyawa[senyawa] = kadar[senyawa].mean()

    ax.bar(list(kadar_senyawa.keys()), list(kadar_senyawa.values()), color ='maroon', width = 0.4)
    ax.set_xlabel("Senyawa", fontsize=30)
    ax.set_ylabel("Rata-rata Kadar Senyawa", fontsize=35)
    ax.set_title(f'Kadar senyawa pada {station} station', fontsize=35)
    ax.tick_params(axis='y', labelsize=35)
    ax.tick_params(axis='x', labelsize=30)

def get_data_station(station):
    if (station == 'Aotizhongxin'): return aotizhongxin
    elif (station == 'Changping'): return changping
    elif (station == 'Dingling'): return dingling
    elif (station == 'Dongsi'): return dongsi
    elif (station == 'Guanyuan'): return guanyuan
    elif (station == 'Gucheng'): return gucheng
    elif (station == 'Huairou'): return huairou
    elif (station == 'Nongzhanguan'): return nongzhanguan
    elif (station == 'Shunyi'): return shunyi
    elif (station == 'Tiantan'): return tiantan
    elif (station == 'Wanliu'): return wanliu
    elif (station == 'Wanshouxigong'): return wanshouxigong
    else: return all_df

with task1:
    st.header("Bagaimana kondisi kadar senyawa pada udara di setiap station?")
    
    st.subheader("Memvisualisasikan kondisi kadar senyawa setiap stasiun")
    # Select Box
    station = st.selectbox(
        label="What's your favorite movie genre",
        options=('Semua', 'Aotizhongxin', 'Changping', 'Dingling', 'Dongsi', 
                 'Guanyuan', 'Gucheng', 'Huairou', 'Nongzhanguan', 'Shunyi', 
                 'Tiantan', 'Wanliu', 'Wanshouxigong')
    )

    data = get_data_station(station)
    fig, ax = plt.subplots( figsize=(35, 15))
    all_senyawa_kadar_visualisasi(data, ax, station)
    st.pyplot(fig)

    st.subheader("Memvisualisasikan kondisi kadar senyawa pada stasiun untuk setiap senyawa")
    # Multiselect
    all_senyawa = st.multiselect(
        label="Pilih senyawa yang ingin dilihat kondisi kadarnya...",
        options=("PM2.5", "PM10", "SO2", "NO2", "CO", "O3")
    )

    for senyawa in all_senyawa:
        fig, ax = plt.subplots( figsize=(35, 15))
        senyawa_kadar_visualisasi(senyawa, ax)
        st.pyplot(fig)

with task2:
    st.header("Bagaimana kondisi kadar Karbon monoksida (CO) untuk setiap tahun?")
    
    st.subheader("Perbandingan setiap tahun - Rata-rata kadar senyawa CO setiap tahun")
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))
    
    kadar_year = get_data_year(all_df)
    perbandingan_setiap_tahun_barchart(kadar_year, ax[0])
    perbandingan_setiap_tahun_linechart(kadar_year, ax[1])

    st.pyplot(fig)

    st.subheader("Perbandingan kenaikan tiap bulan")
    fig, ax = plt.subplots(figsize=(35, 15))

    data = get_data_year_month_values(all_df)
    perbandingan_kenaikan_tiap_bulan_linechart(data, ax)

    st.pyplot(fig)

    st.markdown("Per tahun")
    fig, ax = plt.subplots(figsize=(35, 15))
    
    dict_data = get_data_month_values(all_df)

    perbandingan_kenaikan_tiap_bulan_tahun_linechart(data, ax)

    st.pyplot(fig)
