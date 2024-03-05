import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import seaborn as sns

path = os.getcwd()
hour_dataset = pd.read_csv(path + '/data/hour.csv')

dataset_2011 = hour_dataset[hour_dataset['yr'] == 0]
dataset_2012 = hour_dataset[hour_dataset['yr'] == 1]
dataset_both = hour_dataset

dataset_list = {'2011': dataset_2011, '2012': dataset_2012, '2011 & 2012': dataset_both}
title_list = {'2011': ' 2011', '2012': ' 2012', '2011 & 2012': ' 2011 dan 2012'}
color_list = {'2011': 'b', '2012': 'g', '2011 & 2012': 'y'}
years = ['2011', '2012', '2011 & 2012']


def weather_plot(year):
    grouped_by_weather = dataset_list[year].groupby('weathersit')['cnt'].mean().reset_index()
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.bar(grouped_by_weather['weathersit'], grouped_by_weather['cnt'])
    plt.xlabel('Kondisi Cuaca')
    plt.xticks([1, 2, 3, 4])
    plt.ylabel('Rata-rata Jumlah Sewa Sepeda')
    plt.yticks(np.arange(0, 300, 50))
    plt.title('Pengaruh Cuaca Terhadap Jumlah Sewa Sepeda di Tahun' + title_list[year])
    st.pyplot(fig)


def day_type_plot(year):
    grouped_by_day_type = dataset_list[year].groupby(['workingday', 'weekday'])['cnt'].mean().reset_index()
    fig, ax = plt.subplots(figsize=(10, 10))
    bar = sns.barplot(data=grouped_by_day_type, x='weekday', y='cnt', hue='workingday')

    weekday_type = {0: 'Akhir Pekan / Hari Libur', 1: 'Hari Kerja'}
    new_labels = [weekday_type[value] for value in grouped_by_day_type['workingday'].unique()]
    new_handles = bar.get_legend_handles_labels()[0]

    plt.legend(title='Jenis Hari', labels=new_labels, handles=new_handles)
    plt.xlabel('Hari')
    plt.xticks([0, 1, 2, 3, 4, 5, 6], ['Minggu', 'Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu'])
    plt.ylabel('Rata-rata Jumlah Sewa Sepeda')
    plt.yticks(np.arange(0, 350, 25))
    plt.title('Pengaruh Jenis Hari Terhadap Jumlah Sewa Sepeda di Tahun' + title_list[year])
    st.pyplot(fig)


def season_plot(year):
    grouped_by_season = dataset_list[year].groupby('season')['cnt'].mean().reset_index()
    fig, ax = plt.subplots(figsize=(10, 10))
    plt.pie(grouped_by_season['cnt'], labels=['Musim Semi', 'Musim Panas', 'Musim Gugur', 'Musim Dingin'],
            autopct='%1.1f%%', startangle=90, counterclock=False, colors=['#66b3ff', '#99ff99', '#ffcc99', '#c2c2f0'])
    plt.title('Pengaruh Musim Terhadap Rata-Rata Sewa Sepeda di Tahun' + title_list[year])
    st.pyplot(fig)


def trend_plot(year):
    grouped_by_trend = dataset_list[year].groupby('mnth')['cnt'].mean().reset_index()
    fig, ax = plt.subplots(figsize=(10, 10))
    sns.lineplot(data=grouped_by_trend, x='mnth', y='cnt', marker='o', color=color_list[year])
    plt.xlabel('Bulan')
    plt.xticks(range(1, 13), ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    plt.ylabel('Rata-rata Sewa Sepeda')
    plt.yticks(np.arange(0, 350, 25))
    plt.title('Rata-rata Sewa Sepeda Setiap Bulan di Tahun' + title_list[year])
    st.pyplot(fig)
    

def hour_plot(year):
    grouped_by_hour = dataset_list[year].groupby('hr')['cnt'].mean().reset_index()
    fig, ax = plt.subplots(figsize=(10, 10))
    sns.lineplot(data=grouped_by_hour, x='hr', y='cnt', marker='o', color=color_list[year])
    plt.xlabel('Jam')
    plt.xticks(range(0, 24))
    plt.ylabel('Rata-rata Sewa Sepeda')
    plt.yticks(np.arange(0, 700, 100))
    plt.title('Rata-rata Sewa Sepeda Setiap Jam di Tahun' + title_list[year])
    st.pyplot(fig)


st.set_page_config(layout="wide")

st.title("Proyek Analisis Data: Bike Sharing Dataset")

with st.container():
    st.header("Data Diri")
    st.write(
        """
        - **Nama**: Martinus Angger Budi Wicaksono
        - **Email**: anggerbudi9@gmail.com
        - **ID Dicoding**: martinus_angger
        """
    )

with st.container():
    st.header("Isi Dataset yang Digunakan")
    st.write("*Menampilkan 10 data pertama dari dataset*")
    st.dataframe(hour_dataset.head(10))

with st.container():
    st.header("5 Pertanyaan Bisnis")
    questions = [
        "1. Bagaimana pengaruh cuaca terhadap jumlah sewa sepeda?",
        "2. Bagaimana pengaruh jenis hari (holiday, weekday, workingday) terhadap jumlah tertinggi sewa sepeda?",
        "3. Bagaimana pengaruh musim terhadap jumlah sewa sepeda?",
        "4. Pada bulan apa jumlah sewa sepeda berada pada titik tertinggi?",
        "5. Pada jam berapa jumlah sewa sepeda berada pada titik tertinggi?"
    ]
    st.write("\n".join(questions))

st.write("\n")

with st.container():
    st.markdown("<h1 style='text-align: center;'> Visualisasi Data Sewa Sepeda</h1>",
                unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        with st.container():
            st.header("Pengaruh Cuaca")
            tab1, tab2, tab3 = st.tabs(['2011', '2012', '2011 & 2012'])
            with tab1:
                weather_plot('2011')
            with tab2:
                weather_plot('2012')
            with tab3:
                weather_plot('2011 & 2012')
            with st.expander("Keterangan Cuaca"):
                st.write(
                    """
                    - **Cuaca 1**: Cerah, Sedikit Berawan, Sebagian Berawan
                    - **Cuaca 2**: Kabut, Berawan
                    - **Cuaca 3**: Ringan Hujan, Hujan Badai Petir
                    - **Cuaca 4**: Hujan Lebat, Salju Lebat, Petir, Kabut
                    """
                )
            st.subheader("Kesimpulan Pengaruh Cuaca")
            st.write(
                """
                Pada tahun 2011 dan 2012, rata-rata jumlah sewa sepeda tertinggi terjadi pada kondisi cuaca 1 (cerah) dan rata-rata jumlah sewa sepeda terendah terjadi pada kondisi cuaca 4 (cuaca sangat buruk).
                """
            )

    with col2:
        with st.container():
            st.header("Pengaruh Jenis Hari")
            tab1, tab2, tab3 = st.tabs(['2011', '2012', '2011 & 2012'])
            with tab1:
                day_type_plot('2011')
            with tab2:
                day_type_plot('2012')
            with tab3:
                day_type_plot('2011 & 2012')
            with st.expander("Keterangan Jenis Hari"):
                st.write(
                    """
                    - **Akhir Pekan**: Sabtu dan Minggu
                    - **Hari Libur**: Sabtu, Minggu dan Hari libur lainnya
                    - **Hari Kerja**: Senin sampai Jumat
                    """
                )
            st.subheader("Kesimpulan Pengaruh Jenis Hari")
            st.write(
                """
                - Pada tahun 2011 :.
                    - Rata-rata jumlah sewa sepeda tertinggi pada hari kerja terjadi pada hari Senin. Sedangkan rata-rata tertinggi pada akhir pekan / hari libur terjadi pada hari Minggu.
                    - Rata-rata jumlah sewa sepeda terendah pada hari kerja terjadi pada hari Rabu. Sedangkan rata-rata terendah pada akhir pekan / hari libur terjadi pada hari Kamis.
                - Pada tahun 2012 :
                    - Rata-rata jumlah sewa sepeda tertinggi pada hari kerja terjadi pada hari Kamis. Sedangkan rata-rata tertinggi pada akhir pekan / hari libur terjadi pada hari Rabu.
                    - Rata-rata jumlah sewa sepeda terendah pada hari kerja terjadi pada hari Senin. Sedangkan rata-rata terendah pada akhir pekan / hari libur terjadi pada hari Selasa.
                - Pada tahun 2011 dan 2012 (digabung):
                    - Rata-rata jumlah sewa sepeda tertinggi pada hari kerja terjadi pada hari Kamis. Sedangkan rata-rata tertinggi pada akhir pekan / hari libur terjadi pada hari Rabu.
                    - Rata-rata jumlah sewa sepeda terendah pada hari kerja terjadi pada hari Senin. Sedangkan rata-rata terendah pada akhir pekan / hari libur terjadi pada hari Selasa.
                """
            )

    with col3:
        with st.container():
            st.header("Pengaruh Musim")
            tab1, tab2, tab3 = st.tabs(['2011', '2012', '2011 & 2012'])
            with tab1:
                season_plot('2011')
            with tab2:
                season_plot('2012')
            with tab3:
                season_plot('2011 & 2012')
            st.write("\n")
            with st.expander("Keterangan Musim"):
                st.write(
                    """
                    - **Musim Semi**: Maret, April, Mei
                    - **Musim Panas**: Juni, Juli, Agustus
                    - **Musim Gugur**: September, Oktober, November
                    - **Musim Dingin**: Desember, Januari, Februari
                    """
                )
            st.subheader("Kesimpulan Pengaruh Musim")
            st.write(
                """
                - Pada tahun 2011, 2012, dan kedua tahun Peringkat rata-rata sewa sepeda berdasarkan musim adalah sebagai berikut:
                    - Musim Gugur
                    - Musim Panas
                    - Musim Dingin
                    - Musim Semi
                """
            )

    blan_col1, col4, col5, blank_col2 = st.columns([1, 2, 2, 1])
    with col4:
        with st.container():
            st.header("Trend Sewa Tiap Bulan")
            tab1, tab2, tab3, tab4 = st.tabs(['2011', '2012', '2011 & 2012', 'Komparasi'])
            with tab1:
                trend_plot('2011')
            with tab2:
                trend_plot('2012')
            with tab3:
                trend_plot('2011 & 2012')
            with tab4:
                grouped_by_trend_2011 = dataset_2011.groupby('mnth')['cnt'].mean().reset_index()
                grouped_by_trend_2012 = dataset_2012.groupby('mnth')['cnt'].mean().reset_index()
                fig, ax = plt.subplots(figsize=(10, 10))
                sns.lineplot(data=grouped_by_trend_2011, x='mnth', y='cnt', marker='o', label='2011', color='b')
                sns.lineplot(data=grouped_by_trend_2012, x='mnth', y='cnt', marker='o', label='2012', color='g')
                plt.xlabel('Bulan')
                plt.xticks(range(1, 13),
                           ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
                plt.ylabel('Rata-rata Sewa Sepeda')
                plt.title('Rata-rata Sewa Sepeda Setiap Bulan (2011 vs 2012)')
                plt.legend()
                st.pyplot(fig)
            st.subheader("Kesimpulan Trend Tiap Bulan")
            st.write(
                """
                - Pada tahun 2011, rata-rata jumlah sewa sepeda berada pada titik tertinggi pada bulan Juni dan berada pada titik terendah pada bulan Januari.
                - Pada tahun 2012, rata-rata jumlah sewa sepeda berada pada titik tertinggi pada bulan September dan berada pada titik terendah pada bulan Januari.
                - Pada kedua tahun (digabung), rata-rata jumlah sewa sepeda berada pada titik tertinggi pada bulan September dan berada pada titik terendah pada bulan Januari.
                """
            )

    with col5:
        with st.container():
            st.header("Trend Sewa Tiap Jam")
            tab1, tab2, tab3, tab4 = st.tabs(['2011', '2012', '2011 & 2012', 'Komparasi'])
            with tab1:
                hour_plot('2011')
            with tab2:
                hour_plot('2012')
            with tab3:
                hour_plot('2011 & 2012')
            with tab4:
                grouped_by_hour_2011 = dataset_2011.groupby('hr')['cnt'].mean().reset_index()
                grouped_by_hour_2012 = dataset_2012.groupby('hr')['cnt'].mean().reset_index()
                fig, ax = plt.subplots(figsize=(10, 10))
                sns.lineplot(data=grouped_by_hour_2011, x='hr', y='cnt', marker='o', label='2011', color='b')
                sns.lineplot(data=grouped_by_hour_2012, x='hr', y='cnt', marker='o', label='2012', color='g')
                plt.xlabel('Bulan')
                plt.xticks(range(0, 24))
                plt.ylabel('Rata-rata Sewa Sepeda')
                plt.yticks(np.arange(0, 700, 100))
                plt.title('Rata-rata Sewa Sepeda Setiap Jam (2011 vs 2012)')
                plt.legend()
                st.pyplot(fig)
            st.subheader("Kesimpulan Trend Tiap Jam")
            st.write(
                """
                - Pada plot 2011, 2012, dan gabungan, rata-rata jumlah sewa sepeda berada pada titik tertinggi pada jam 5 sore (17.00) lalu diikuti jam 8 pagi (08.00) dan berada pada titik terendah pada jam 4 pagi (04.00).
                """
            )
