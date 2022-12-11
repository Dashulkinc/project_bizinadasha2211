import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
st.markdown('# Main project page')

df = pd.read_csv('brain_stroke.csv')
d = df.head()

main, data, concl = st.tabs(['Dataset analysis', 'Data cleanup and transformation', 'Conclusion'])
with main:
    st.header('Issues')
    st.subheader('Hypothesis')
    st.write('In this data analysis project I am considering causes of brain stroke. After analyzing the data, I will highlight the key reasons for this illness and give conclusions on some plots')
    st.write('I assume that older people addicted to cigarettes with a high body mass index and heart diseses are more prone to stroke than others')
    st.subheader('Dataset')
    st.dataframe(d)
    st.write('I will use only 5 columns for my project: age, heart disease, avg glucose level, bmi, smoking status and sroke. So lets delete others')
    df.pop('gender')
    df.pop('hypertension')
    df.pop('ever_married')
    df.pop('work_type')
    df.pop('Residence_type')
    st.subheader('Changed dataset')
    st.dataframe(df)
    st.subheader('Statistic')
    stat = df.describe()
    st.dataframe(stat)
    st.subheader('Charts')
    tab1, tab2, tab3, tab4 = st.tabs(['age', 'smoking status', 'bmi', 'heart diseases'])

    with tab1:
        st.caption('Use boxplot to determine which age group most often has a strok')
        fig, ax = plt.subplots()
        sns.boxplot(x='stroke', y='age', data=df).set_title('Аge groups regarding stroke')
        st.pyplot(fig)
        st.write('It is noticable that only people over the age of 30 had a stroke, at the same time, older people are most affected')
    with tab2:
        option = st.selectbox('', (['General information', 'Detailed overview']))
        if option == 'General information':
            st.caption('Use barchart to see the number of people in different smoking status')
            fig, ax = plt.subplots()
            num1 = df['smoking_status'].value_counts()
            smok = num1.index
            value1 = num1.values
            bar_ch = pd.DataFrame({'smoking_status': smok, 'Num of people': value1})
            bar_ch.plot.bar(x='smoking_status', y='Num of people', figsize=(6, 4), rot=45, ax=ax).set_title('The number of people in differnt smoking status')
            plt.xlabel('smoking status')
            plt.show()
            st.pyplot(fig)
            st.write('From this histogram it can be seen that there are fewer people who smoke or have smoked before')
        else:
            st.caption('Use two graphics to show the dependence of smoking and stroke for two age groups (1 group - people over 60, 2 group - people under 60)')
            fig, ax = plt.subplots()
            old = df[df['age'] >= 60]
            old.groupby(['smoking_status', 'stroke']).size().unstack().fillna(0).plot(kind='barh', stacked=False, ax=ax)
            plt.xlabel('num of people')
            plt.ylabel('smoking status')
            plt.title('The dependence of smoking and stroke for people over 60')
            st.pyplot(fig)
            fig, ax = plt.subplots()
            old = df[df['age'] < 60]
            old.groupby(['smoking_status', 'stroke']).size().unstack().fillna(0).plot(kind='barh', stacked=False, ax=ax)
            plt.xlabel('num of people')
            plt.ylabel('smoking status')
            plt.title('The dependence of smoking and stroke for people under 60')
            st.pyplot(fig)
            st.write('This two graphic shows that there are almost no cases when smokers under the age of 60 have experienced a stroke, unlike the elderly')

    with tab3:
        options = st.selectbox('', (['Correlation between age and bmi', 'Particular overview']))
        if options == 'Correlation between age and bmi':
            st.caption('Look at means between ages and figure out people who have high bmi')
            fig, ax = plt.subplots()
            ag = df['age'].unique()
            means = {}
            for i in ag:
                agsplit = df[df['age'] == i]
                means[i] = agsplit['bmi'].mean()
            ind = means.keys()
            val = means.values()
            plt.title('Correlation between age and bmi')
            plt.xlabel('age')
            plt.ylabel('bmi')
            plt.bar(ind, val, label='Data', color="g")
            plt.axhline(df['bmi'].mean(), color="red", label='Mean', linestyle='--')
            plt.legend()
            plt.show()
            st.pyplot(fig)
            st.write('From this graphic one can see that in general all people over 30 have bmi higher then average')
        else:
            st.caption('Use histograms to determine if people in different age groups with high bmi had strokes')
            fig, ax = plt.subplots()
            oldp = df[df['age'] >= 60]
            oldps = oldp[oldp['stroke'] == 1]
            plt.hist(x='bmi', bins=25, data=oldps)
            plt.xlabel('bmi')
            plt.ylabel('number of people')
            oldp = df[df['age'] < 60]
            oldps = oldp[oldp['stroke'] == 1]
            plt.hist(x='bmi', bins=25, data=oldps)
            plt.title('The correlation between bmi and stroke in two age groups')
            st.pyplot(fig)
            st.write('This histograms show that very few people with high body mass index (>30) had a stroke regardless age')

    with tab4:
        optionss = st.selectbox('', (['general information', 'detailed overview']))
        if optionss == 'general information':
            st.caption('Use pie-chart to indicate the part of people which is with heart diseases')
            fig, ax = plt.subplots()
            num1 = df['heart_disease'].value_counts()
            value1 = num1.values
            plt.pie(value1, labels=num1.index, autopct='%1.1f%%', startangle=180)
            plt.title('The percentage of people regarding heart diseases')
            plt.legend()
            plt.show()
            st.pyplot(fig)
            st.write('This graph shows that 5,5% of people are with heart diseases')
        else:
            st.caption('Use two boxplots to indicate the correlation between heart diseases and stroke for people in different ages')
            fig, ax = plt.subplots()
            old = df[df['age'] >= 60]
            sns.boxplot(x='heart_disease', y='age', hue='stroke', data=old).set_title('the correlation between heart diseases and stroke for people over 60')
            plt.xlabel('heart disease')
            st.pyplot(fig)

            fig, ax = plt.subplots()
            old = df[df['age'] < 60]
            sns.boxplot(x='heart_disease', y='age', hue='stroke', data=old).set_title('the correlation between heart diseases and stroke for people under 60')
            plt.xlabel('heart disease')
            st.pyplot(fig)
            st.write('These two graphs help one to see that people under 60 with heart diseases amost do not have strokes, but at the same time elderly people are equally likely to have a stroke despite heart disease')

with data:
    st.header('Data cleanup')
    st.write('No NaN fields detected')
    st.write('All data types are correct')
    st.header('Data transformation')
    st.write('I create two new columns: the first one is "weight" and the second one is "diabetes status"')
    st.write("The first column will tell about a person's weight: underweight/healthy/overweight/obesity.")
    st.write("The second column will tell about a person's average glucose level: hypoglycemia/normal/monitoring glycemia/diabetes")


    def weight(bmi):
        if bmi < 18.5:
            return 'underweight'
        elif 18.5 <= bmi < 25:
            return 'healthy'
        elif 25 <= bmi < 30:
            return 'overweight'
        else:
            return 'obesity'


    def agl(avg_glucose_level):
        if avg_glucose_level < 70:
            return 'hypoglycemia'
        elif 70 <= avg_glucose_level < 100:
            return 'normal'
        elif 100 <= avg_glucose_level < 125:
            return 'monitoring glycemia'
        else:
            return 'diabetes'


    df['weight'] = df['bmi'].apply(weight)
    df['diabetes status'] = df['avg_glucose_level'].apply(agl)
    new = df.head()
    st.dataframe(new)

with concl:
    st.header('Conclusion')
    st.write('The hypothesis put at the beginning of the dataset analysis has been checked. Indeed, the most common age group that experienced a brain stroke were people over 60')
    st.write('1. Smoking turned out to be one of the factors of stroke in the elderly, while people from another age group almost never experienced a stroke when smoking')
    st.write('2. Very few people under the age of 60 have heart problems, moreover, they have almost no effect on the occurrence of stroke. Speaking of the elderly, it can be concluded that indeed people with diseases are more prone to stroke in old age, although the probability of this is 50%')
    st.write('3. Graphs show that almost all people over the age of 30 are overweight and regardless age people with high bmi are not likely to have a stroke')
    st.write('The above points show that the hypothesis has been partially refuted. Indeed, older people addicted to cigarettes and suffering from heart disease are more prone to stroke than others, but high bmi is not an indicator that distinguishes these two age groups or even inpact on strokes')
    st.balloons()
