import json
from pathlib import Path
from scripts.streamlit.data_preprocessing import convert2onelvl
import streamlit as st


#  start
#  from root:
#  PYTHONPATH="./" streamlit run scripts/streamlit/streamlit_run.py


BASE_DIR = Path(__file__).parent.parent.parent.absolute()
STREAMLIT_DIR = BASE_DIR / 'scripts' / 'streamlit'
JSON_PATH = STREAMLIT_DIR / 'udc_teacode_utf_onelvl.json'

MASK = {
    "002": 5,
    "124.1": 100,
    "22": 90,
    "511-33": 150,
    "51-8": 180,
    "517.383": 200,
    "517.387": 210,
}

if not JSON_PATH.exists():
    if (STREAMLIT_DIR / 'udc_teacode_utf.json').exists():
        with open(STREAMLIT_DIR / 'udc_teacode_utf.json', "r") as fp:
            d_graph = json.load(fp)
        onelvl = convert2onelvl(d_graph)
        with open(JSON_PATH, 'w', encoding='utf-8') as fp:
            json.dump(onelvl, fp, ensure_ascii=False)
    else:
        raise RuntimeError('File udc_teacode_utf.json not found.')


def load_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data


def update_mask():
    if st.session_state.target_node != 'root':
        new_mask = dict()
        for k, v in MASK.items():
            if st.session_state.target_node == k[:len(st.session_state.target_node)]:
                new_mask.update({k: v})
            else:
                new_mask.update({k: 0})
        st.session_state.mask = new_mask
    else:
        st.session_state.mask = MASK
    return


def up_the_tree():
    st.session_state.target_node = st.session_state.child_parent[st.session_state.target_node]
    update_mask()
    return


def to_root():
    st.session_state.target_node = 'root'
    update_mask()
    return


def set_target_node(target_node):
    st.session_state.target_node = target_node
    update_mask()
    return


def check_data():
    if 'data' not in st.session_state:
        st.session_state.data = load_data(file_path=JSON_PATH)

    if 'child_parent' not in st.session_state:
        st.session_state.child_parent = {k: v["parent"] for k, v in st.session_state.data.items()}

    if 'target_node' not in st.session_state:
        st.session_state.target_node = 'root'

    if 'mask' not in st.session_state:
        st.session_state.mask = MASK

    return


def find_children():
    children_keys = st.session_state.data[st.session_state.target_node]['children']
    if children_keys:
        children_nodes = [
            {'udc': st.session_state.data[child]['udc'], 'name': st.session_state.data[child]['name']}
            for child in children_keys
        ]
    else:
        children_nodes = list()
    return children_nodes


if __name__ == "__main__":
    # uploading data at the first launch
    check_data()

    # find children
    children_nodes = find_children()

    # adding a navigation and description container if not at the root
    if st.session_state.target_node != 'root':

        logits_value = 0
        for k, v in st.session_state.mask.items():
            if (st.session_state.data[st.session_state.target_node]["udc"] in
                    k[:len(st.session_state.data[st.session_state.target_node]["udc"])]):
                logits_value = v

        with st.container():
            st.button('в начало', on_click=to_root)
            st.button('вверх', on_click=up_the_tree)
            st.write(f'Код УДК: {st.session_state.data[st.session_state.target_node]["udc"]} // '
                     f'Название: {st.session_state.data[st.session_state.target_node]["name"]} // '
                     f'LOGITS VALUE: {logits_value}')
            st.write('Потомки:')

    # add button children
    with st.container():
        for node in children_nodes:

            logits_value = None
            type_button = 'secondary'
            for k, v in st.session_state.mask.items():
                if node["udc"] in k[:len(node["udc"])]:
                    logits_value = v
                    type_button = 'primary'

            st.button(
                f'{node["udc"]} -- {node["name"]} -- LOGITS VALUE: {logits_value}',
                on_click=set_target_node,
                args=[node['udc']],
                type=type_button
            )
        if not children_nodes:
            st.write('отсутствуют')
