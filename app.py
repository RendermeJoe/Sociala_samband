import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
from supabase import create_client

st.set_page_config(page_title="Socialsamband", layout="wide")

supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_ANON_KEY"]
)

share_id = st.query_params.get("map")

if share_id:
    res = supabase.table("maps").select("id,title").eq("share_id", share_id).single().execute()
    st.sidebar.write("Laddar karta:", res.data)
else:
    st.sidebar.info("Ingen map i URL. Lägg till ?map=<share_id>")


# --- Inmatning ---
st.sidebar.header("Skriv in ditt namn och välj vilka du har ett socialt samband med!")

st.sidebar.header("Lägg till samband")
name = st.sidebar.text_input("Du")
relation = st.sidebar.selectbox(
    "Är...",
    ["vän", "släkt", "bekant", "i förhållande"]
)
target = st.sidebar.text_input("Med...")
add = st.sidebar.button("Lägg till")
st.sidebar.subheader("Lathund färgkodning:")
st.sidebar.write("Vän = Blå")
st.sidebar.write("Släkt = Grön")
st.sidebar.write("Bekant = Orange")
st.sidebar.write("I förhållande = Röd")
# --- Data i session ---
if "G" not in st.session_state:
    st.session_state.G = nx.Graph()

G = st.session_state.G
if add and name and target and name != target:
    G.add_nodes_from([name, target])
    G.add_edge(name, target, relation=relation)

# --- Rita ---
pos = nx.spring_layout(G, seed=42)
fig, ax = plt.subplots()
ax.set_facecolor("white")  # vit bakgrund

# Färger på kanter (samband)
edge_colors = []
for u, v, data in G.edges(data=True):
    rel = data.get("relation", "vän")
    if rel == "vän":
        edge_colors.append("blue")
    elif rel == "släkt":
        edge_colors.append("green")
    elif rel == "bekant":
        edge_colors.append("orange")
    elif rel == "i förhållande":
        edge_colors.append("red")
    else:
        edge_colors.append("gray")

# Dynamisk bubbelstorlek så texten alltid får plats
def bubble_size_for_label(label, base= 1500, mul=150):
    return base + len(label) * mul

node_sizes = [bubble_size_for_label(node) for node in G.nodes()]

# --- Bubblorna (noderna) ---
nx.draw_networkx_nodes(
    G,
    pos,
    node_color="white",    # vit insida
    node_size=node_sizes,  # storlek beroende på namnets längd
    edgecolors="black",    # svart kant runt cirkeln
    linewidths=2,          # tjocklek på kanten
)

# --- Samband ---
nx.draw_networkx_edges(
    G,
    pos,
    width=2.5,             # TJOCKARE samband
    edge_color=edge_colors # färg per relation
)

# --- Text i bubblorna ---
nx.draw_networkx_labels(
    G,
    pos,
    font_color="black",    # svart text
    font_size=12,
)

plt.axis("off")
st.pyplot(fig)
