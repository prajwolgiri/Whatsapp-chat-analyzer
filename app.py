import streamlit as st
import data_preprocessing,functions_list
import matplotlib.pyplot as plt


st.sidebar.title("Whatsapp Chat Analyzer")
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = data_preprocessing.preprocess(data)

    st.dataframe(df)

    # for fetching unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")
    selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)

    if st.sidebar.button("Show analysis"):

        num_messages, words,  num_of_media_messages, num_links = functions_list.fetch_stats(selected_user, df)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.header("Total messages")
            st.title(num_messages)

        with col2:
            st.header("Total words")
            st.title(words)

        with col3:
            st.header("Number of Media Shared")
            st.title(num_of_media_messages)
        with col4:
            st.header("Number of Links Shared")
            st.title(num_links)

        # finding busiest person in gp
        if selected_user == 'Overall':
            st.title('Most Active Users')
            x, new_df = functions_list.most_active_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values,)
                plt.xticks(rotation='vertical')

                st.pyplot(fig)

            with col2:
                st.header("User active in %")
                st.dataframe(new_df)


            #For wordcloud
            st.title('WordCloud')
            df_wc = functions_list.create_wordcloud(selected_user, df)
            fig,ax = plt.subplots()
            ax.imshow(df_wc)
            st.pyplot(fig)

            

