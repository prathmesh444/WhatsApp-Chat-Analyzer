import nltk
import streamlit as st
import plotly.express as px
import helper
import preprosser
from nltk.corpus import stopwords
nltk.download('stopwords')
excl = stopwords.words("hinglish")
st.sidebar.title("Whatsapp CHAT Analyzer")
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue().decode("utf-8")
    # st.write(bytes_data)
    df = preprosser.proprocess(bytes_data)
    user_list = df.user.unique().tolist()
    user_list.remove("group notification")
    user_list.sort()
    user_list.insert(0, "Overall")

    curr_user = st.sidebar.selectbox("Select user", user_list)
    if st.sidebar.button("Show Stats"):
        msg_size, word_size, media_size, links = helper.basic_stats(curr_user, df)
        st.title("Top Statistics")
        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.header("Total Messages")
            st.title(msg_size)
        with c2:
            st.header("Total Words")
            st.title(word_size)
        with c3:
            st.header("Media Shared")
            st.title(media_size)
        with c4:
            st.header("Links Shared")
            st.title(str(len(links)))

        with st.expander(f"Total Links"):
            st.write(links)

        if curr_user == "Overall":
            st.title("Most Busy Users")
            A = helper.most_busy_users(df)
            col1, col2 = st.columns([0.6, 0.4])
            with col1:
                fig1 = px.bar(x=A.index, y=A.values, color=A.index)
                st.plotly_chart(fig1, use_container_width=True)
            with col2:
                B = helper.busy_percentage(df)
                st.dataframe(B)

        # Yearly Timeline
        st.title("Yearly Timeline")
        years_timeline = helper.yearly_timeline(df, curr_user)
        fig2 = px.line(years_timeline, x="year", y="message", color_discrete_sequence=['yellow'], markers=True)
        st.plotly_chart(fig2, use_container_width=True)

        # Monthly Timeline
        st.title("Monthly Timeline")
        months_timeline = helper.monthly_timeline(df, curr_user)
        fig3 = px.line(months_timeline, x="timeline", y="message", color_discrete_sequence=['blue'])
        st.plotly_chart(fig3, use_container_width=True)

        # Daily Timeline
        st.title('Daily Timeline')
        days_timeline = helper.daily_timeline(df, curr_user)
        fig4 = px.line(days_timeline, x='timeline', y='message', color_discrete_sequence=['green'])
        st.plotly_chart(fig4, use_container_width=True)

        # Hourly Timeline
        st.title('Hourly Timeline')
        hourly = helper.hour_timeline(df, curr_user)
        fig5 = px.area(hourly, x='hour', y='message', color_discrete_sequence=["red"])
        fig5.update_xaxes(autotypenumbers='strict')
        st.plotly_chart(fig5, use_container_width=True)

        # Activity Map
        st.title("Activity Map")
        col3, col4 = st.columns(2)
        month, week = helper.activity_map(df, curr_user)
        with col3:
            st.title("Most Buzy Day")
            fig6 = px.bar(week, x='day', y='message', color='day')
            st.plotly_chart(fig6, use_container_width=True)
        with col4:
            st.title("Most Buzy Month")
            fig7 = px.bar(month, x="message", y="month", color="month", orientation='h')
            st.plotly_chart(fig7, use_container_width=True)

        # Word Cloud code
        st.title("Word Cloud")
        wordCloud = helper.word_cloud(df, curr_user, excl)
        st.image(wordCloud.to_array())

        # most common words
        st.title("Most Common Words")
        common_words = helper.most_common_words(df, curr_user, excl)
        fig8 = px.bar(common_words, x="Percent", y="Common Words", color="Common Words", orientation='h')
        st.plotly_chart(fig8, use_container_width=True)

        # show top emojis
        st.title("Most Common Emojis")
        emojis = helper.get_emojis(df, curr_user)
        fig8 = px.pie(emojis, names="emoji", values='count')
        fig8.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig8, use_container_width=True)
