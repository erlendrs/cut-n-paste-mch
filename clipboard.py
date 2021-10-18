import streamlit as st
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
from io import StringIO
import pandas as pd

st.title("Klipp & lim inn tekst")

def main():
    try:
        copy_button = Button(label="Slå sammen Mch koder")
        copy_button.js_on_event("button_click", CustomJS(code="""
            navigator.clipboard.readText().then(text => document.dispatchEvent(new CustomEvent("GET_TEXT", {detail: text})))
           """))
        result = streamlit_bokeh_events(
            copy_button,
            events="GET_TEXT",
            key="get_text",
            refresh_on_update=False,
            override_height=75,
            debounce_time=0)

        if result:
            if "GET_TEXT" in result:
                df = pd.read_csv(StringIO(result.get("GET_TEXT")),names=['Mch Code'])
                #txt = df['Mch Code']#';'.join(set(df['Mch Code'].apply(str)))
                #txt = df.values.tolist()
                values = ['Mch Code', 'Dokumentnummer']
                df = df[df['Mch Code'].isin(values) == False]
                merged_text = ';'.join(set(df['Mch Code'].apply(str)))
                st.success(merged_text)
                #st.text(txt)
                st.table(df)
                
    except KeyError as missing_column:
        st.error(f'Følgende obligatorisk kolonne mangler: {missing_column}')

if __name__ == "__main__":
    main()
