import streamlit as st
import requests
import pandas as pd
import json
import html
from urllib.parse import quote
from streamlit.components.v1 import html as st_html

st.set_page_config(page_title="ChemVerse | Chemistry Learning Lab", page_icon="🧪", layout="wide")

# ---------- Theme ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');
html, body, [class*="css"] {font-family:'DM Sans',sans-serif;}
.stApp {background:linear-gradient(135deg,#081426 0%,#0d2038 55%,#102d43 100%); color:#eef7ff;}
h1,h2,h3 {font-family:'Space Grotesk',sans-serif;}
.hero {padding:28px;border:1px solid #28506b;border-radius:22px;background:linear-gradient(120deg,#102d48,#124e62);margin-bottom:18px;}
.hero h1 {font-size:2.65rem;margin:0;color:#f5fbff;}
.hero p {color:#c4e8f2;font-size:1.05rem;margin-bottom:0;}
.tile {background:#10263c;border:1px solid #244760;border-radius:16px;padding:17px;min-height:118px;}
.tile h3 {color:#6de2d0;margin:0 0 7px 0;}
.tile p {color:#d4e4f0;margin:0;font-size:.93rem;}
.small-note {color:#b9cfdf;font-size:.85rem;}
div[data-testid="stMetric"] {background:#10263c;border:1px solid #244760;padding:12px;border-radius:14px;}
</style>
""", unsafe_allow_html=True)

# ---------- Reference data ----------
ELEMENTS = [
(1,"H","Hydrogen"),(2,"He","Helium"),(3,"Li","Lithium"),(4,"Be","Beryllium"),(5,"B","Boron"),(6,"C","Carbon"),(7,"N","Nitrogen"),(8,"O","Oxygen"),(9,"F","Fluorine"),(10,"Ne","Neon"),
(11,"Na","Sodium"),(12,"Mg","Magnesium"),(13,"Al","Aluminium"),(14,"Si","Silicon"),(15,"P","Phosphorus"),(16,"S","Sulfur"),(17,"Cl","Chlorine"),(18,"Ar","Argon"),(19,"K","Potassium"),(20,"Ca","Calcium"),
(21,"Sc","Scandium"),(22,"Ti","Titanium"),(23,"V","Vanadium"),(24,"Cr","Chromium"),(25,"Mn","Manganese"),(26,"Fe","Iron"),(27,"Co","Cobalt"),(28,"Ni","Nickel"),(29,"Cu","Copper"),(30,"Zn","Zinc"),
(31,"Ga","Gallium"),(32,"Ge","Germanium"),(33,"As","Arsenic"),(34,"Se","Selenium"),(35,"Br","Bromine"),(36,"Kr","Krypton"),(37,"Rb","Rubidium"),(38,"Sr","Strontium"),(39,"Y","Yttrium"),(40,"Zr","Zirconium"),
(41,"Nb","Niobium"),(42,"Mo","Molybdenum"),(43,"Tc","Technetium"),(44,"Ru","Ruthenium"),(45,"Rh","Rhodium"),(46,"Pd","Palladium"),(47,"Ag","Silver"),(48,"Cd","Cadmium"),(49,"In","Indium"),(50,"Sn","Tin"),
(51,"Sb","Antimony"),(52,"Te","Tellurium"),(53,"I","Iodine"),(54,"Xe","Xenon"),(55,"Cs","Caesium"),(56,"Ba","Barium"),(57,"La","Lanthanum"),(58,"Ce","Cerium"),(59,"Pr","Praseodymium"),(60,"Nd","Neodymium"),
(61,"Pm","Promethium"),(62,"Sm","Samarium"),(63,"Eu","Europium"),(64,"Gd","Gadolinium"),(65,"Tb","Terbium"),(66,"Dy","Dysprosium"),(67,"Ho","Holmium"),(68,"Er","Erbium"),(69,"Tm","Thulium"),(70,"Yb","Ytterbium"),
(71,"Lu","Lutetium"),(72,"Hf","Hafnium"),(73,"Ta","Tantalum"),(74,"W","Tungsten"),(75,"Re","Rhenium"),(76,"Os","Osmium"),(77,"Ir","Iridium"),(78,"Pt","Platinum"),(79,"Au","Gold"),(80,"Hg","Mercury"),
(81,"Tl","Thallium"),(82,"Pb","Lead"),(83,"Bi","Bismuth"),(84,"Po","Polonium"),(85,"At","Astatine"),(86,"Rn","Radon"),(87,"Fr","Francium"),(88,"Ra","Radium"),(89,"Ac","Actinium"),(90,"Th","Thorium"),
(91,"Pa","Protactinium"),(92,"U","Uranium"),(93,"Np","Neptunium"),(94,"Pu","Plutonium"),(95,"Am","Americium"),(96,"Cm","Curium"),(97,"Bk","Berkelium"),(98,"Cf","Californium"),(99,"Es","Einsteinium"),(100,"Fm","Fermium"),
(101,"Md","Mendelevium"),(102,"No","Nobelium"),(103,"Lr","Lawrencium"),(104,"Rf","Rutherfordium"),(105,"Db","Dubnium"),(106,"Sg","Seaborgium"),(107,"Bh","Bohrium"),(108,"Hs","Hassium"),(109,"Mt","Meitnerium"),(110,"Ds","Darmstadtium"),
(111,"Rg","Roentgenium"),(112,"Cn","Copernicium"),(113,"Nh","Nihonium"),(114,"Fl","Flerovium"),(115,"Mc","Moscovium"),(116,"Lv","Livermorium"),(117,"Ts","Tennessine"),(118,"Og","Oganesson")
]
COMMON_MOLECULES = ["Water", "Carbon dioxide", "Methane", "Ammonia", "Ethanol", "Glucose", "Benzene", "Acetic acid", "Sodium chloride", "Sulfuric acid", "Ozone", "Caffeine"]

QUIZ = [
("What is the chemical symbol for oxygen?", ["O","Ox","Og","Oy"], "O", "The symbol O represents oxygen."),
("How many protons are in a carbon atom?", ["4","6","8","12"], "6", "Carbon's atomic number is 6, so it has 6 protons."),
("What is the formula of water?", ["CO₂","H₂O","NaCl","NH₃"], "H₂O", "A water molecule contains two hydrogen atoms and one oxygen atom."),
("Which bond involves sharing electron pairs?", ["Ionic","Covalent","Metallic","Hydrogen"], "Covalent", "Covalent bonds form when atoms share electron pairs."),
("What is the pH of a neutral solution at 25 °C?", ["0","5","7","14"], "7", "At 25 °C, a neutral aqueous solution has pH 7.")
]

def pubchem_get(url, timeout=18):
    try:
        r = requests.get(url, timeout=timeout, headers={"User-Agent":"ChemVerseStudentProject/1.0"})
        if r.status_code == 200:
            return r
        return None
    except requests.RequestException:
        return None

@st.cache_data(ttl=3600, show_spinner=False)
def fetch_compound(name):
    safe = quote(name.strip(), safe="")
    prop_url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{safe}/property/MolecularFormula,MolecularWeight,IUPACName,CanonicalSMILES,IsomericSMILES,XLogP,TPSA,HBondDonorCount,HBondAcceptorCount/JSON"
    r = pubchem_get(prop_url)
    if not r:
        return None
    try:
        props = r.json()["PropertyTable"]["Properties"][0]
    except (ValueError, KeyError, IndexError):
        return None
    cid = props.get("CID")
    sdf = None
    png_url = None
    if cid:
        sr = pubchem_get(f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/SDF?record_type=3d")
        if sr:
            sdf = sr.text
        png_url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/PNG"
    return {"props":props, "cid":cid, "sdf":sdf, "png_url":png_url}

def show_3d(sdf, style, bg, atom_colors):
    safe_sdf = json.dumps(sdf)
    style_js = {
        "Ball and stick": "viewer.setStyle({}, {stick:{radius:0.18}, sphere:{scale:0.28}});",
        "Stick": "viewer.setStyle({}, {stick:{radius:0.22}});",
        "Space filling": "viewer.setStyle({}, {sphere:{scale:0.85}});",
        "Wireframe": "viewer.setStyle({}, {line:{linewidth:2}});"
    }[style]
    html_doc = f"""
    <div id="cv3d" style="width:100%;height:430px;position:relative;border-radius:14px;overflow:hidden;">
    <div style="position:absolute;z-index:2;top:8px;left:10px;color:#9fb6c9;font:12px Arial;">Drag to rotate • Pinch or scroll to zoom</div></div>
    <script src="https://3Dmol.org/build/3Dmol-min.js"></script>
    <script>
    const sdf = {safe_sdf};
    const elementColors = {json.dumps(atom_colors)};
    const viewer = $3Dmol.createViewer("cv3d", {{backgroundColor:"{bg}"}});
    viewer.addModel(sdf, "sdf");
    {style_js}
    viewer.zoomTo();
    viewer.render();
    viewer.zoom(0.85, 1000);
    </script>
    """
    st_html(html_doc, height=445, scrolling=False)

# ---------- Sidebar navigation ----------
with st.sidebar:
    st.markdown("## 🧪 ChemVerse")
    st.caption("Your interactive chemistry world")
    page = st.radio("NAVIGATION", [
        "Home", "Getting Started", "Theory Library", "Periodic Table",
        "Molecule Explorer", "2D & 3D Lab", "Animation Studio",
        "Video Studio", "Quiz", "Assignments", "Compare Molecules", "Reports"
    ])
    st.divider()
    st.caption("Student project • Data references shown on each page")

# ---------- Pages ----------
if page == "Home":
    st.markdown('<div class="hero"><h1>🧪 ChemVerse</h1><p>Discover. Visualize. Understand. Explore.</p><p>Turn chemistry concepts into an interactive learning experience.</p></div>', unsafe_allow_html=True)
    st.subheader("Welcome to your Chemistry Learning Lab")
    st.write("ChemVerse is a student learning platform designed to explain elements, atoms, molecules and compounds using simple notes, molecular structures, interactive models and practice activities.")
    cols = st.columns(3)
    tiles = [("⚛️","Explore elements","Browse the 118 elements in the periodic table."),("🧬","Understand molecules","Search compounds and view their molecular information."),("🔬","Visualize in 3D","Rotate, zoom and change molecular display styles.")]
    for c,(icon,title,desc) in zip(cols,tiles):
        with c: st.markdown(f'<div class="tile"><h3>{icon} {title}</h3><p>{desc}</p></div>',unsafe_allow_html=True)
    st.write("")
    cols = st.columns(3)
    tiles2 = [("🎞️","Learn with visuals","Explore animation ideas and video learning."),("📝","Test yourself","Take quizzes and practise chemistry questions."),("📊","Compare & report","Compare molecular data and download a study report.")]
    for c,(icon,title,desc) in zip(cols,tiles2):
        with c: st.markdown(f'<div class="tile"><h3>{icon} {title}</h3><p>{desc}</p></div>',unsafe_allow_html=True)
    st.info("Start with **Getting Started**, then visit the Periodic Table or Molecule Explorer.")
    st.caption("Learning resource: PubChem (National Library of Medicine) is used to retrieve compound records when available.")

elif page == "Getting Started":
    st.title("👋 Welcome to ChemVerse")
    st.subheader("What is ChemVerse?")
    st.write("ChemVerse is an interactive Chemistry learning application. It brings basic theory, element information, molecular structures, visualization, quizzes and assignments together in one place.")
    st.subheader("How to use the application")
    for n,t in enumerate([
        "Choose a section from the navigation menu on the left.",
        "Read a topic in Theory Library or select an element in Periodic Table.",
        "Search a molecule by its common name in Molecule Explorer.",
        "Open 2D & 3D Lab to view the structure. Drag to rotate and use pinch or scroll to zoom.",
        "Try the quiz and complete the practice assignment.",
        "Use Compare Molecules to compare available data and Reports to download a study summary."
    ],1): st.write(f"**{n}.** {t}")
    st.subheader("Main features")
    st.write("- Chemistry notes for beginners\n- Periodic table containing 118 element names and symbols\n- Compound lookup using PubChem\n- 2D structure image and interactive 3D model when available\n- Visualization styles and background colour choices\n- Quizzes, assignments and comparison tools\n- Downloadable study report")
    st.warning("Some advanced features, such as exporting a fully edited MP4 video with music, are planned for a later version. This starter version provides an animation storyboard and video planning workspace.")

elif page == "Theory Library":
    st.title("📚 Theory Library")
    topics = {
        "Introduction to Chemistry":"Chemistry is the branch of science that studies matter, its composition, structure, properties and the changes it undergoes. Matter is anything that has mass and occupies space.",
        "Structure of an Atom":"An atom is the smallest unit of an element that retains its chemical identity. It contains a nucleus with protons and neutrons, while electrons occupy regions around the nucleus.",
        "Atomic Number and Mass Number":"Atomic number is the number of protons in the nucleus. Mass number is the total number of protons and neutrons in a particular atom.",
        "Periodic Table":"The periodic table arranges elements by increasing atomic number. Rows are called periods and columns are called groups. Elements in a group often show related chemical behaviour.",
        "Chemical Bonding":"Chemical bonds are attractive forces that hold atoms or ions together. Common types include ionic, covalent and metallic bonding.",
        "Acids and Bases":"An acid donates hydrogen ions in the Brønsted–Lowry model. A base accepts hydrogen ions. The pH scale is commonly used to describe acidity or basicity in aqueous solutions.",
        "Physical and Chemical Changes":"A physical change alters a substance's form or state without changing its chemical identity. A chemical change produces one or more new substances.",
        "Organic Chemistry":"Organic chemistry mainly studies carbon-containing compounds, including hydrocarbons and many compounds found in living systems.",
        "Chemical Reactions":"A chemical reaction rearranges atoms to form new substances. A balanced chemical equation has the same number of each type of atom on both sides."
    }
    topic = st.selectbox("Choose a topic", list(topics.keys()))
    st.subheader(topic)
    st.write(topics[topic])
    examples = {
        "Introduction to Chemistry":"Example: Water is made from hydrogen and oxygen.",
        "Structure of an Atom":"Example: A neutral carbon-12 atom has 6 protons, 6 neutrons and 6 electrons.",
        "Atomic Number and Mass Number":"Example: Carbon-12 has atomic number 6 and mass number 12.",
        "Periodic Table":"Example: Sodium (Na) and potassium (K) are in Group 1.",
        "Chemical Bonding":"Example: Sodium chloride contains ionic bonding; water contains covalent bonds.",
        "Acids and Bases":"Example: Lemon juice is acidic; soap solutions are often basic.",
        "Physical and Chemical Changes":"Example: Ice melting is physical; iron rusting is chemical.",
        "Organic Chemistry":"Example: Methane (CH₄) is the simplest alkane.",
        "Chemical Reactions":"Example: 2H₂ + O₂ → 2H₂O."
    }
    st.success(examples[topic])
    st.caption("Use a chemistry textbook or your lecturer's notes to extend these introductory explanations.")

elif page == "Periodic Table":
    st.title("⚛️ Periodic Table Explorer")
    st.write("Search the element list by name or symbol. This starter includes all 118 element names and symbols.")
    q = st.text_input("Search element", placeholder="Try Oxygen, Fe or Au")
    df = pd.DataFrame(ELEMENTS, columns=["Atomic number","Symbol","Element"])
    if q:
        df = df[df.apply(lambda row: q.lower() in str(row["Element"]).lower() or q.lower() == str(row["Symbol"]).lower(), axis=1)]
    st.dataframe(df, use_container_width=True, hide_index=True)
    choice = st.selectbox("Select an element", [f"{n}. {sym} — {name}" for n,sym,name in ELEMENTS])
    n,sym,name = next(x for x in ELEMENTS if choice.startswith(str(x[0])+"."))
    st.markdown(f"### {name} ({sym})")
    c1,c2,c3 = st.columns(3)
    c1.metric("Atomic number", n)
    c2.metric("Protons", n)
    c3.metric("Electrons in neutral atom", n)
    st.info("Neutron number depends on the isotope. Atomic mass, electron configuration, melting point and boiling point should be checked against a trusted element reference for the specific isotope or standard conditions.")
    st.markdown(f"[Open {name} in PubChem](https://pubchem.ncbi.nlm.nih.gov/#query={quote(name)})")

elif page in ["Molecule Explorer","2D & 3D Lab"]:
    st.title("🧬 Molecule Explorer" if page=="Molecule Explorer" else "🔬 2D & 3D Molecular Lab")
    st.write("Search by a common chemical name. Compound information and structures are retrieved from PubChem when a matching record is available.")
    default = "Water"
    molecule = st.text_input("Enter molecule or compound name", value=default, placeholder="e.g. Water, caffeine, ethanol")
    if st.button("Explore molecule", type="primary"):
        st.session_state["cv_molecule"] = molecule
    molecule = st.session_state.get("cv_molecule", molecule)
    if molecule:
        with st.spinner("Searching PubChem for the compound..."):
            result = fetch_compound(molecule)
        if not result:
            st.error("No matching compound record was found, or the data service is temporarily unavailable. Check the spelling and try another name.")
        else:
            p = result["props"]
            st.subheader(p.get("IUPACName", molecule))
            a,b,c = st.columns(3)
            a.metric("PubChem CID", result["cid"] if result["cid"] else "—")
            b.metric("Molecular formula", p.get("MolecularFormula","—"))
            b.metric("Molecular weight", f'{p.get("MolecularWeight","—")} g/mol')
            c.metric("XLogP", p.get("XLogP","—"))
            st.markdown("#### Molecular information")
            rows = [
                ("IUPAC name",p.get("IUPACName","Not available")),
                ("Molecular formula",p.get("MolecularFormula","Not available")),
                ("Molecular weight (g/mol)",p.get("MolecularWeight","Not available")),
                ("Canonical SMILES",p.get("ConnectivitySMILES",p.get("CanonicalSMILES","Not available"))),
                ("Isomeric SMILES",p.get("SMILES",p.get("IsomericSMILES","Not available"))),
                ("Topological polar surface area",p.get("TPSA","Not available")),
                ("Hydrogen bond donors",p.get("HBondDonorCount","Not available")),
                ("Hydrogen bond acceptors",p.get("HBondAcceptorCount","Not available")),
                ("XLogP (computed)",p.get("XLogP","Not available"))
            ]
            st.dataframe(pd.DataFrame(rows,columns=["Property","Value"]),use_container_width=True,hide_index=True)
            st.markdown("#### 2D structure")
            if result["png_url"]:
                st.image(result["png_url"], caption="2D structure image provided by PubChem", width=360)
            else:
                st.caption("2D image is not available for this record.")
            st.markdown("#### Interactive 3D structure")
            if result["sdf"]:
                style = st.selectbox("Molecular display style",["Ball and stick","Stick","Space filling","Wireframe"])
                bg = st.selectbox("Viewer background",["#071525","#FFFFFF","#17202A","#EAF4F4"])
                st.caption("The atom colours in this starter use the viewer's standard element colour scheme. More detailed per-atom colour editing is a planned enhancement.")
                show_3d(result["sdf"],style,bg,{})
            else:
                st.warning("A 3D conformer is not available from PubChem for this compound. Try another molecule.")
            st.markdown(f"[View full PubChem record](https://pubchem.ncbi.nlm.nih.gov/compound/{result['cid']})")
            st.caption("Source: PubChem PUG REST. Retrieved fields may be computed or experimental; check the source record for definitions and references.")
            st.info("Melting point, freezing point, boiling point and other experimental physical/chemical properties are not included in every PubChem compound record. Do not assume a missing value is zero; consult the linked record and cited literature.")

elif page == "Animation Studio":
    st.title("🎞️ Chemistry Animation Studio")
    st.write("Choose a concept and explore a simple step-by-step animation storyboard. This is a learning aid, not a laboratory simulation.")
    concept = st.selectbox("Choose an animation",["Formation of water","Ionic bond in sodium chloride","Covalent bond in hydrogen","Carbon dioxide molecule"])
    storyboards = {
        "Formation of water":[("1","Two hydrogen atoms and one oxygen atom are shown."),("2","The atoms approach one another."),("3","Covalent bonds form as electrons are shared."),("4","A water molecule, H₂O, is displayed.")],
        "Ionic bond in sodium chloride":[("1","A sodium atom and a chlorine atom are shown."),("2","Sodium transfers one electron to chlorine."),("3","Sodium becomes Na⁺ and chlorine becomes Cl⁻."),("4","Oppositely charged ions attract and form an ionic lattice.")],
        "Covalent bond in hydrogen":[("1","Two hydrogen atoms each have one electron."),("2","Their electron clouds overlap."),("3","The atoms share a pair of electrons."),("4","A hydrogen molecule, H₂, is formed.")],
        "Carbon dioxide molecule":[("1","One carbon atom and two oxygen atoms are shown."),("2","The oxygen atoms arrange on either side of carbon."),("3","Two carbon–oxygen double bonds are represented."),("4","The linear CO₂ molecule is displayed.")]
    }
    for step,desc in storyboards[concept]:
        st.markdown(f'<div class="tile" style="margin:8px 0;min-height:0"><h3>Frame {step}</h3><p>{desc}</p></div>',unsafe_allow_html=True)
    st.caption("Future upgrade: animated 3D atoms, narration, subtitles and exportable video clips.")

elif page == "Video Studio":
    st.title("🎬 Video Studio – Planning Workspace")
    st.write("Plan a short chemistry teaching video. Full MP4 rendering, timeline editing and music mixing are not enabled in this first version.")
    title = st.text_input("Video title", "How a Water Molecule Forms")
    audience = st.selectbox("Audience",["Beginner students","School students","College students"])
    script = st.text_area("Narration / script", "A water molecule contains two hydrogen atoms and one oxygen atom. These atoms are joined by covalent bonds.")
    captions = st.text_area("Captions", "H₂O = two hydrogen atoms + one oxygen atom")
    music_note = st.text_input("Background music note (optional)", "Soft instrumental background")
    if st.button("Create video plan"):
        plan = f"CHEMVERSE VIDEO PLAN\nTitle: {title}\nAudience: {audience}\n\nNARRATION\n{script}\n\nCAPTIONS\n{captions}\n\nMUSIC DIRECTION\n{music_note}\n"
        st.download_button("Download video plan",plan,file_name="chemverse_video_plan.txt",mime="text/plain")
        st.success("Your video plan is ready to download.")

elif page == "Quiz":
    st.title("📝 Chemistry Knowledge Quiz")
    st.write("Choose one answer for each question, then submit.")
    answers = {}
    with st.form("chem_quiz"):
        for i,(question,options,correct,explain) in enumerate(QUIZ):
            answers[i] = st.radio(f"{i+1}. {question}",options,key=f"quiz_{i}")
        submitted = st.form_submit_button("Submit quiz")
    if submitted:
        score = sum(answers[i] == item[2] for i,item in enumerate(QUIZ))
        st.success(f"Your score: {score} / {len(QUIZ)}")
        for i,item in enumerate(QUIZ):
            st.write(("✅ " if answers[i]==item[2] else "❌ ")+item[0])
            st.caption(item[3])

elif page == "Assignments":
    st.title("📄 Practice Assignments")
    tasks = {
        "Assignment 1 – Atomic structure":"1. Define an atom.\n2. Name the three main subatomic particles.\n3. State the charge of each particle.\n4. Explain atomic number and mass number with one example.",
        "Assignment 2 – Chemical bonding":"1. What is a chemical bond?\n2. Explain ionic bonding using sodium chloride.\n3. Explain covalent bonding using water.\n4. Write two differences between ionic and covalent compounds.",
        "Assignment 3 – Molecules and properties":"1. Define a molecule and a compound.\n2. Write the formulas of water, carbon dioxide and methane.\n3. Explain two physical properties and two chemical properties.\n4. Describe one use of each compound."
    }
    selected = st.selectbox("Choose an assignment",list(tasks.keys()))
    st.text_area("Assignment questions",tasks[selected],height=190)
    answer = st.text_area("Write your answer here",height=220,placeholder="Type your answer...")
    st.download_button("Download my answers",f"{selected}\n\n{tasks[selected]}\n\nMY ANSWERS\n{answer}",file_name="chemverse_assignment.txt",mime="text/plain")

elif page == "Compare Molecules":
    st.title("📊 Compare Molecules")
    st.write("Compare basic molecular data retrieved from PubChem.")
    names = st.text_input("Enter two compound names separated by a comma","Water, Ethanol")
    if st.button("Compare",type="primary"):
        parts = [x.strip() for x in names.split(",") if x.strip()][:2]
        if len(parts)!=2:
            st.warning("Please enter exactly two compound names, separated by a comma.")
        else:
            records=[]
            for nm in parts:
                res=fetch_compound(nm)
                if res:
                    p=res["props"]
                    records.append({"Compound":nm,"Formula":p.get("MolecularFormula","—"),"Molecular weight (g/mol)":p.get("MolecularWeight","—"),"XLogP":p.get("XLogP","—"),"TPSA":p.get("TPSA","—")})
                else:
                    st.warning(f"Could not retrieve {nm}.")
            if records: st.dataframe(pd.DataFrame(records),use_container_width=True,hide_index=True)
            st.caption("A missing value means the selected record did not return that property.")

elif page == "Reports":
    st.title("📥 Study Reports")
    st.write("Create a simple study report for your project submission.")
    student = st.text_input("Student name (optional)")
    course = st.text_input("Course / class (optional)","Chemistry")
    topic = st.text_input("Report topic","Introduction to molecules")
    summary = st.text_area("Your learning summary","I learned how atoms combine to form molecules and how molecular structures can be represented in 2D and 3D.")
    report = f"CHEMVERSE – CHEMISTRY STUDY REPORT\n\nStudent: {student or 'Not provided'}\nCourse: {course}\nTopic: {topic}\n\nSUMMARY\n{summary}\n\nApplication: ChemVerse\nData reference: PubChem (where used)\n"
    st.download_button("Download report (.txt)",report,file_name="chemverse_study_report.txt",mime="text/plain")
    st.caption("This report is a study summary, not a certified laboratory or scientific report.")

st.divider()
st.caption("ChemVerse • Educational student project • Verify scientific values with authoritative references before academic submission.")
