import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px

# # ================== CUSTOM CSS ==================
st.markdown("""
<style>

/* Main background */
.stApp {background: linear-gradient(165deg,#0f0f0f,#121212,#159a44)}

/* Sidebar */
section[data-testid="stSidebar"] {background: rgba(0,0,0,0.6);
}

/* Cards */
   .metric-card {
        background-color: #121212;
        padding: 5px;
        border-radius: 10px;
        text-align: center;
        transition: 0.3s;
        box-shadow: 0px 0px 5px rgba(0,255,200,0.4);}

/* Cards */
   .card {
        padding: 5px;
        text-align: center;}

/* Cards */
   .o-card {
        background-color: #121212;
        padding: 5px;
        border-radius: 10px;
        text-align: center;
        transition: 0.3s;
        box-shadow: 0px 0px 5px rgba(0,255,200,0.4);}

/* Text input box */
div[data-baseweb="input"] > div {
    background-color: #1e1e2f;
    border-radius: 10px;
    border: 2px solid #4CAF50;
    padding: 5px;
}


/* Selectbox container */
div[data-baseweb="select"] > div {
    background-color: #1e1e2f;
    border-radius: 10px;
    border: 2px solid #4CAF50;
}

/* Buttons */
.stButton>button {
    background: linear-gradient(45deg, #00c6ff, #0072ff);
    color: white;
    border-radius: 10px;
    border: none;
    transition: 0.3s;
}
.stButton>button:hover {transform: scale(1.05);background: linear-gradient(45deg, #43e97b, #38f9d7);}

/* Tables */
.stDataFrame {
    border-radius: 10px;
    overflow: hidden;
}

/* Expander */
details {
    background: rgba(255,255,255,0.05);
    border-radius: 10px;
    padding: 10px;
}

/* Scrollbar */
::-webkit-scrollbar {
    width: 8px;
}
::-webkit-scrollbar-thumb {
    background: #00ffe1;
    border-radius: 10px;
}

/* Hover animation */
.element-container:hover {
    transform: translateY(-2px);
    transition: 0.2s;
}

</style>
""", unsafe_allow_html=True)

# ================== DATA ==================
with st.spinner("Loading data..."):
    df = pd.read_csv(r'C:\Users\nikil\Downloads\PY demo/SPOTIFY.csv')

df["release_date"] = pd.to_datetime(df["release_date"])

# ------------Cleaning-------------------

Duration = df["duration"].mean().astype(int)
df["duration"] = df["duration"].fillna(Duration)
df["language"] = df["language"].fillna("English")
df["collaboration"] = df["collaboration"].fillna("MD")

df["popularity"] = df["popularity"].astype(int)
df["duration"] = df["duration"].astype(int)

# ================== CONFIG ==================
st.set_page_config(page_title="SPOTIFY ANALYTICS", layout="wide", page_icon="🎶")

# Sidebar
st.sidebar.image("img_1.png", width=190)
st.sidebar.write("")
with st.sidebar:
    selected = option_menu(
        " Main Menu",
        ["DataSet", "Overview", "Music Analytics","Data Assistant","Search Engine"],
        icons=["table", "bar-chart", "music-note","robot","search"],
        menu_icon="headphones",
        default_index=0,
        styles={
            "container": {"padding": "5px"},
            "icon": {"color": "#00ffe1", "font-size": "20px"},
            "nav-link": {"color": "white", "font-size": "16px"},
            "nav-link-selected": {"background-color": "#006400"}
        }
    )

st.sidebar.divider()
st.sidebar.write("Scan the QR code to download the Spotify app!")
st.sidebar.image("QR.png",width=140)

# ================== DATASET ==================
if selected == "DataSet":
    st.title("🎶 Music Analytics Dashboard ")
    st.divider()
    col1,col2,col3 = st.columns([1,2,1],vertical_alignment="center")
    with col1:
        st.markdown(f"""
           <div class="metric-card">
               <h3>📊 Total Rows</h3>
               <h1>{df.shape[0]}</h1>
           </div>
           """, unsafe_allow_html=True)
    with col3:
         st.markdown(f"""
                   <div class="metric-card">
                       <h3>📊 Total Columns</h3>
                       <h1>{df.shape[1]}</h1>
                   </div>
                   """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
                           <div class="card">
                               <h1>📄 Dataset View</h1>
                           </div>
                           """, unsafe_allow_html=True)
    st.write("")

    with st.expander("DATA INFORMATION"):
        col1,col2 = st.columns([4,6])

        with col1.container(border=True):
            st.write("### Data info")
            st.dataframe(df.dtypes.to_frame(name="dtypes"))
        with col2.container(border=True):
            st.write(df.describe())
    st.divider()
    st.header("🧾 Column Selection")
    Column_data = st.multiselect("Filter Columns", df.columns)

    view, dwn = st.columns([9, 1])
    with view:
        expand = st.expander("📂 Show Filter Columns Data")
        filter_df = pd.DataFrame(df[Column_data])
        expand.write(filter_df)
    with dwn:
        csv = filter_df.to_csv(index=False).encode("utf-8")
        st.download_button("Get Data", csv, "Filtered_Data.csv", "text/csv")
    st.write("")
    search_val = st.text_input("🔍 Smart Data Search", icon="🔍",placeholder="Search")

    if search_val:
        filter_df = filter_df[
            filter_df.astype(str).apply(
                lambda row: row.str.contains(search_val, case=False).any(), axis=1
            )]
    expand = st.expander("Filtered Data")
    data = pd.DataFrame(filter_df)
    expand.write(data)
    st.write("")

    st.header("🔓 Unlock Dataset ")
    csv = filter_df.to_csv(index=False).encode("utf-8")
    button = st.download_button("Download Filter Data", csv, "Filtered_Data.csv", "text/csv")
    if button:
        st.success("Dataset Downloaded Successfully...")

    st.markdown("---")
    st.markdown(
            "<center>Developed by <b>Nikil Patel</b> | Data Analytics Project</center>",
            unsafe_allow_html=True)

# ================== OVERVIEW ==================
if selected == "Overview":
    st.title("📊 Overview Of Data")
    st.write(" ")
    st.markdown("***")
    c1, c2, c3,c4 = st.columns(4)
    with c1:
        st.markdown(f"""<div class="o-card"><h3>🎵 Songs</h3>
                       <h1>{len(df)}</h1></div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="o-card"><h3>🎤 Artists</h3>
                       <h1>{df['artist'].nunique()}</h1></div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class="o-card"><h3>⭐ Avg Popularity</h3>
                       <h1>{ round(df['popularity'].mean(), 2)}</h1></div>""", unsafe_allow_html=True)
    with c4:
        st.markdown(f"""<div class="o-card"><h3>⏱ Avg Duration </h3>
                       <h1>{round(df['duration'].mean(),2)}</h1></div>""", unsafe_allow_html=True)
    st.write(" ")
    st.write(" ")
    c6, col2, c7 = st.columns([1, 2, 1], vertical_alignment="center")

    with c6:
        st.markdown(f"""<div class="o-card"><h3>📡Total Stream</h3>
                               <h1>{df["stream"].sum()}</h1></div>""", unsafe_allow_html=True)
    with c7:
        st.markdown(f"""<div class="o-card"><h3>📖 Unique Album</h3>
                                       <h1>{df["album"].nunique()}</h1></div>""", unsafe_allow_html=True)
    st.write("")
    with st.container(border=True):
        st.header("Genre wise unit Performance metrics")

        Gen_matrix = df.groupby("genre").agg(
            Total_popularity=("popularity", "sum"),
            Avg_duration=("duration", "mean"),
            Count=("song_id", "count"),
            Total_Stream=("stream", "sum"),
        )
        st.dataframe(
            Gen_matrix.style.highlight_max(axis=0, color="#2bfb6b").highlight_min(axis=0, color="#fb352b").format({
                "Total_popularity": "{:,.0f}",
                "Avg_duration": "{:,.0f} /min",
            }).background_gradient(subset=["Total_Stream"], cmap="RdYlBu_r"))
    st.write("")

    c1, c2 = st.columns(2)

    with c1.container(border=True):
        st.header("Explicit Content Analysis")
        pivot_data = df.pivot_table(
            index="label",
            columns="explicit_content",
            aggfunc="size",
            fill_value=0)
        st.dataframe(pivot_data)

    with c2.container(border=True):
        st.header("Label count metrics")
        label = df["label"].value_counts().to_frame(name="Count")
        st.dataframe(label.style.background_gradient(subset=["Count"], cmap="RdYlBu_r"))

    st.write("")
    st.markdown("***")
    with st.container():
        g1, s1 = st.columns([7, 3])
        with g1:
            language = st.selectbox("Label Distribution", df['label'].unique())
            filter_df = df[df["label"].isin([language])]
            total_stream = filter_df["stream"].sum()
        with s1:
            st.markdown(f"""<div class="o-card"><h3>📡Total Stream</h3>
                                           <h1>{total_stream}</h1></div>""", unsafe_allow_html=True)
    st.write("")
    st.divider()
    with st.expander("Song Title"):
        select = st.selectbox("select language", options=df['language'].unique())
        filter_data = df[df["language"].isin([select])]
        title = filter_data["song_title"]
        total = len(title)
        st.success(f"Total Song title is {total}")
        st.dataframe(title)
    st.markdown("---")
    st.markdown(
            "<center>Developed by <b>Nikil Patel</b> | Data Analytics Project</center>",
            unsafe_allow_html=True)

# ================== MUSIC ANALYTICS ==================

if selected == "Music Analytics":
    st.title("🎵 Music Analytics")
    st.markdown("***")
    f1, f2 = st.columns(2)
    with f1.container(border=True):
        st.subheader("🎤 Top Artists")
        fig1 = px.bar(df['artist'].value_counts().head(5),
                      color_discrete_sequence=px.colors.sequential.Tealgrn)
        st.plotly_chart(fig1, use_container_width=True)

    with f2.container(border=True):
        st.subheader("⭐ Top 5 Artists by it's Popularity")
        data = df.groupby("artist")["popularity"].sum().sort_values(ascending=False).head(5).reset_index()
        fig2 = px.bar(data, x="artist", y="popularity", color="artist",
                      color_discrete_sequence=px.colors.sequential.Tealgrn)
        st.plotly_chart(fig2, use_container_width=True)

    with st.container(border=True):
        st.subheader("⏱ Duration vs Popularity")
        fig3 = px.scatter(df, x='duration', y='popularity',
                          color='genre', hover_data=['artist'],
                          color_discrete_sequence=px.colors.sequential.Tealgrn)
        st.plotly_chart(fig3, use_container_width=True)

    f4,f5 = st.columns(2)
    with f4.container(border=True):
        st.subheader("🎚️ Hierarchical Distribution of Data")
        fig4 = px.sunburst(df, path=["language", "genre"],
                           values="popularity",
                           # color="popularity",
                           color_discrete_sequence=px.colors.sequential.Tealgrn)
        fig4.update_layout(height=500)
        st.plotly_chart(fig4, use_container_width=True)

    with f5.container(border=True):
        st.subheader("🔝 Top 10 Songs")
        TOP = df.groupby("song_title")["popularity"].sum().sort_values(ascending=False).head(10).reset_index()
        fig5 = px.bar(TOP, x="song_title", y="popularity", color="song_title",
                      barmode="stack",color_discrete_sequence=px.colors.sequential.Tealgrn)
        st.plotly_chart(fig5, use_container_width=True)


    st.subheader("Revenue Distribution")
    fig6 = px.treemap(df, path=["label", "genre"],
                      values="popularity",
                      color="genre",
                      color_discrete_sequence=px.colors.sequential.Tealgrn)
    fig6.update_layout(margin=dict(t=20, l=0, r=0, b=0), width=800)
    st.plotly_chart(fig6)

    f7,f8 = st.columns(2)
    with f7.container(border=True):
        st.subheader("🌍 Language Distribution")
        profit_product = df.groupby("language").size().reset_index(name="count")
        fig7 = px.pie(profit_product,
                         values="count",
                         names="language",
                         color_discrete_sequence=px.colors.sequential.Tealgrn,
                         hole=0.5)
        st.plotly_chart(fig7, use_container_width=True)

    with f8.container(border=True):
        st.subheader("🌍 Label Distribution")
        label_pop = df.groupby("label")["popularity"].sum()
        fig8 = px.pie(df, values="popularity",
                      color_discrete_sequence=px.colors.sequential.Tealgrn,names="label")
        st.plotly_chart(fig8, use_container_width=True)

    with st.container(border=True):
        st.header("Language 🆚 Avg Popularity")
        data1 = df.groupby("language")["popularity"].sum().reset_index()
        fig9 = px.bar(data1,x="popularity",y="language", color="language",
                      color_discrete_sequence=px.colors.sequential.Tealgrn,
                      orientation="h")
        st.plotly_chart(fig9, use_container_width=True)

    with st.container(border=True):
        st.subheader("📅 Time Trends")

        df["release_date"] = pd.to_datetime(df["release_date"], errors='coerce')
        df["year"] = df["release_date"].dt.year

        songs_per_year = df.groupby("year").size().reset_index(name="count")

        fig11 = px.line(songs_per_year, x="year", y="count",color_discrete_sequence=px.colors.sequential.Tealgrn,
                        title="Songs Released Over Time")
        st.plotly_chart(fig11, use_container_width=True)

    st.markdown("---")
    st.markdown(
        "<center>Developed by <b>Nikil Patel</b> | Data Analytics Project</center>",
        unsafe_allow_html=True)

# ================== DATA ASSISTANT ==================
if selected == "Data Assistant":
    st.title("🤖 Data Assistant")
    st.divider()

    st.write("Ask Question about the dataset and get visual analytics")
    user_question = st.text_input("Ask Me Question",placeholder="Ask Your Question About the Dataset")

    if user_question:
        q = user_question.lower()

        # total song
        if "total song" in q:
            total = len(df["song_id"])
            st.success(f"Total Song in Dataset {total}")

        # total genre
        elif "genre" in q:
            genre = df["genre"].value_counts()
            st.success(f"Most genre : {genre.idxmax()}")

            fig = px.pie(names=genre.index, values=genre.values, title="genre  Distribution")
            st.plotly_chart(fig)

        # revenue popularity
        elif "popularity" in q:
            popularity = df.groupby("genre")["popularity"].sum().reset_index()
            st.success(f"Total popularity: {df["popularity"].sum()}")

            fig = px.bar(popularity, x="genre",
                         y="popularity",
                         color="genre",
                         title="Total Popularity by Genre", )
            st.plotly_chart(fig)

        elif "total producer" in q:
            total = len(df["producer"])
            st.success(f"Total producer in Dataset {total}")

        # artist
        elif "duration" in q:
            fig = px.scatter(df, y="popularity",
                             x="duration",
                             color="label",
                             title="Popularity vs Duration")
            st.plotly_chart(fig)

        else:
            st.warning("🤔 Question not recognized ,\n\n Try :, total song, genre, popularity, "
                       "total producer, duration etc")
            st.divider()

    st.markdown("---")
    st.markdown(
        "<center>Developed by <b>Nikil Patel</b> | Data Analytics Project</center>",
        unsafe_allow_html=True)

# ================== SEARCH ==================
if selected == "Search Engine":

    # Title
    st.markdown("<h1 style='text-align: center;'>🔍 Smart Search Engine</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>Search Song Name on Spotify</p>",
                unsafe_allow_html=True)
    st.write("---")

    # Input box with better label
    query = st.text_input("✨ What kind of song are you listen today?")

    # Action
    if query:
        search_url = f"https://open.spotify.com/search/{query}"

        st.success(f"Showing results for: **{query}**")

        st.write("👉 Click below to open search results:")

        # Center button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.link_button("🚀 Open in Spotify", search_url, use_container_width=True)

    st.markdown("---")
    st.markdown(
        "<center>Developed by <b>Nikil Patel</b> | Data Analytics Project</center>",
        unsafe_allow_html=True)