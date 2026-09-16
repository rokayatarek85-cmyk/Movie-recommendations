import json
import pandas as pd
import streamlit as st

st.title("🎬 Movie Recommendation System")
st.write("ارفع ملف `movies_dataset.csv` الخام وسيقوم التطبيق بتنظيفه ومعالجته.")

uploaded_file = st.file_uploader("Upload movies_dataset.csv", type=['csv'])

if uploaded_file is not None:
  data = pd.read_csv(uploaded_file)
  st.write("📊 البيانات قبل التنظيف:")
  st.dataframe(data.head())

  if st.button("⚙️ بدء التنظيف (Clean Data)"):
    with st.spinner("جاري معالجة البيانات..."):
      genres = []
      for i in data['genres']:
        genres.append(i)

      for i in range(len(genres)):
        try:
          genres[i] = json.loads(str(genres[i]).replace("'", '"'))
        except:
          genres[i] = []

      for i in range(len(genres)):
        for j in range(len(genres[i])):
          try:
            genres[i][j] = genres[i][j]['name']
          except:
            pass

      all_genres = set([genre for sublist in genres for genre in sublist])
      for genre in all_genres:
        data[genre] = [1 if genre in g else 0 for g in genres]

      if 'genres' in data.columns:
        data = data.drop('genres', axis=1)

      if 'vote_average' in data.columns:
        data['vote_average'] = data['vote_average'].fillna(
            data['vote_average'].mean()
        )

      st.success("✅ تم تنظيف البيانات بنجاح!")
      st.dataframe(data.head())

      csv = data.to_csv(index=False).encode('utf-8')
      st.download_button(
          label="📥 تحميل ملف Cleaned_Data.csv",
          data=csv,
          file_name='Cleaned_Data.csv',
          mime='text/csv',
      )
