import streamlit as st
import json
import html
from streamlit.components.v1 import html as st_html

st.set_page_config(page_title="ChemVerse | Chemistry Learning Lab", page_icon="🧪", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');
html, body, [class*="css"] {font-family:'DM Sans',sans-serif;}
.stApp {background:linear-gradient(135deg,#071426 0%,#102b46 55%,#123d4b 100%);color:#eef7ff;}
h1,h2,h3 {font-family:'Space Grotesk',sans-serif;color:#f4fbff;}
p,li,label {color:#d7e8f3;}
.hero {padding:28px;border:1px solid #32617a;border-radius:22px;background:linear-gradient(120deg,#123653,#12616a);margin-bottom:20px;}
.hero h1 {font-size:2.7rem;margin:0;color:#fff;}
.hero p {color:#d0f2f1;font-size:1.05rem;margin-bottom:0;}
.panel {background:#102940;border:1px solid #2a526a;border-radius:16px;padding:17px;margin:10px 0;}
.panel h3 {color:#75e5d3;margin-top:0;}
div[data-testid="stMetric"] {background:#102940;border:1px solid #2a526a;padding:12px;border-radius:14px;}
.stButton>button {border-radius:10px;font-weight:700;}
.small {color:#b8d0df;font-size:.88rem;}
</style>
""", unsafe_allow_html=True)

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

MOLECULES = {
    "Water": {"formula":"H₂O","atoms":"2 hydrogen + 1 oxygen","shape":"Bent","bond":"Polar covalent","use":"Essential for life; used as a solvent.","facts":"A water molecule has two O–H covalent bonds and a bent shape."},
    "Carbon dioxide": {"formula":"CO₂","atoms":"1 carbon + 2 oxygen","shape":"Linear","bond":"Covalent","use":"Used in carbonated drinks and fire extinguishers.","facts":"Carbon dioxide has two C=O double bonds and a linear shape."},
    "Methane": {"formula":"CH₄","atoms":"1 carbon + 4 hydrogen","shape":"Tetrahedral","bond":"Covalent","use":"A major component of natural gas.","facts":"One carbon atom forms four single covalent bonds with hydrogen."},
    "Ammonia": {"formula":"NH₃","atoms":"1 nitrogen + 3 hydrogen","shape":"Trigonal pyramidal","bond":"Polar covalent","use":"Used to manufacture fertilizers.","facts":"Nitrogen has one lone pair, giving ammonia a pyramidal shape."},
    "Oxygen": {"formula":"O₂","atoms":"2 oxygen","shape":"Linear","bond":"Double covalent","use":"Needed for aerobic respiration.","facts":"Two oxygen atoms share two pairs of electrons."},
    "Hydrogen": {"formula":"H₂","atoms":"2 hydrogen","shape":"Linear","bond":"Single covalent","use":"Used in chemical manufacture and fuel research.","facts":"Two hydrogen atoms share one pair of electrons."},
    "Sodium chloride": {"formula":"NaCl","atoms":"Sodium and chlorine ions","shape":"Ionic crystal lattice","bond":"Ionic","use":"Common table salt.","facts":"Sodium transfers an electron to chlorine, forming Na⁺ and Cl⁻ ions."},
    "Glucose": {"formula":"C₆H₁₂O₆","atoms":"6 carbon + 12 hydrogen + 6 oxygen","shape":"Ring form common in solution","bond":"Covalent","use":"An important energy source in living cells.","facts":"Glucose is a simple sugar and a monosaccharide."},
    "Ozone": {"formula":"O₃","atoms":"3 oxygen","shape":"Bent","bond":"Covalent","use":"The ozone layer absorbs much of the Sun's harmful UV radiation.","facts":"Ozone is a form of oxygen containing three oxygen atoms."}
}

THEORY = {
"Introduction to Chemistry":("Chemistry is the branch of science that studies matter, its composition, structure, properties and the changes it undergoes.","Example: Water is made from hydrogen and oxygen."),
"Structure of an Atom":("An atom is the smallest unit of an element that retains its chemical identity. It contains a nucleus with protons and neutrons. Electrons occupy regions around the nucleus.","Example: A neutral carbon-12 atom has 6 protons, 6 neutrons and 6 electrons."),
"Atomic Number and Mass Number":("Atomic number is the number of protons in an atom. Mass number is the total number of protons and neutrons in its nucleus.","Example: Carbon-12 has atomic number 6 and mass number 12."),
"Periodic Table":("The periodic table arranges elements in increasing order of atomic number. Horizontal rows are periods and vertical columns are groups.","Example: Sodium and potassium are in Group 1."),
"Chemical Bonding":("Chemical bonds are attractive forces that hold atoms or ions together. Common types are ionic, covalent and metallic bonds.","Example: Sodium chloride is ionic; water has covalent bonds."),
"Physical and Chemical Changes":("A physical change changes the form or state of a substance without changing its chemical identity. A chemical change produces new substances.","Example: Melting ice is physical; rusting iron is chemical."),
"Acids and Bases":("In the Brønsted–Lowry model, an acid donates a proton and a base accepts a proton. pH is commonly used to describe aqueous acidity.","Example: Lemon juice is acidic."),
"Chemical Reactions":("A chemical reaction rearranges atoms to form new substances. A balanced equation has the same number of each type of atom on both sides.","Example: 2H₂ + O₂ → 2H₂O.")
}

QUIZ = [
("What is the chemical symbol for oxygen?",["O","Ox","Og","Oy"],"O","O is the chemical symbol for oxygen."),
("How many protons does carbon have?",["4","6","8","12"],"6","Carbon's atomic number is 6."),
("What is the formula of water?",["CO₂","H₂O","NaCl","NH₃"],"H₂O","Water contains two hydrogen atoms and one oxygen atom."),
("Which bond involves sharing electron pairs?",["Ionic","Covalent","Metallic","Hydrogen"],"Covalent","Covalent bonds involve sharing electron pairs."),
("What is the pH of neutral water at 25 °C?",["0","5","7","14"],"7","Pure water is neutral at about pH 7 at 25 °C.")
]

def molecule_animation(name, formula):
    safe_name, safe_formula = html.escape(name), html.escape(formula)
    page = f"""
    <div style="background:#0b2035;border:1px solid #315b73;border-radius:16px;padding:18px;color:white;text-align:center;font-family:Arial">
      <div style="font-size:13px;color:#9ec6d8">MOLECULAR MOTION PREVIEW</div>
      <div style="font-size:25px;font-weight:bold;margin:8px">{safe_name} · {safe_formula}</div>
      <div style="height:180px;display:flex;align-items:center;justify-content:center;gap:12px;overflow:hidden">
        <div class="atom a">H</div><div class="bond"></div><div class="atom b">O</div><div class="bond"></div><div class="atom c">H</div>
      </div>
      <div style="color:#b8d4e2;font-size:13px">Illustrative animation preview (not to scale)</div>
      <style>
      .atom{width:64px;height:64px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:bold;font-size:20px;box-shadow:0 0 22px #4fd6d0;animation:bob 1.6s ease-in-out infinite alternate}
      .a,.c{background:#e7f4ff;color:#14324a}.b{background:#e76b69;color:white;animation-delay:.4s}
      .bond{height:7px;width:34px;background:#80d9d0;border-radius:8px}
      @keyframes bob{from{transform:translateY(-12px) scale(.96)}to{transform:translateY(12px) scale(1.05)}}
      </style>
    </div>"""
    st_html(page, height=300, scrolling=False)

with st.sidebar:
    st.markdown("## 🧪 ChemVerse")
    st.caption("Your interactive chemistry learning lab")
    page = st.radio("EXPLORE",["Home","Getting Started","Theory Library","Periodic Table","Molecule Explorer","Molecular Animation","Animation Videos","Quiz","Assignments","Compare Molecules","About"])

if page == "Home":
    st.markdown('<div class="hero"><h1>🧪 ChemVerse</h1><p>Discover. Visualize. Understand. Explore.</p><p>Your interactive Chemistry Learning Lab.</p></div>',unsafe_allow_html=True)
    st.subheader("Welcome!")
    st.write("Learn about atoms, elements, molecules and chemical bonds through simple notes, a searchable periodic table, molecular models and practice activities.")
    c1,c2,c3 = st.columns(3)
    for col,icon,title,desc in [(c1,"⚛️","118 Elements","Explore element names, symbols and atomic numbers."),(c2,"🧬","Molecule Explorer","Learn formulas, shapes, bonds and uses."),(c3,"🎞️","Animated Preview","Watch a simple moving molecular illustration.")]:
        with col: st.markdown(f'<div class="panel"><h3>{icon} {title}</h3>{desc}</div>',unsafe_allow_html=True)
    c1,c2,c3 = st.columns(3)
    for col,icon,title,desc in [(c1,"📚","Theory Library","Read beginner-friendly chemistry notes."),(c2,"📝","Assignments & Quiz","Practise questions and download your work."),(c3,"📊","Compare","Compare common molecules side by side.")]:
        with col: st.markdown(f'<div class="panel"><h3>{icon} {title}</h3>{desc}</div>',unsafe_allow_html=True)
    st.success("Choose any section from the left menu to begin.")

elif page == "Getting Started":
    st.title("👋 Getting Started")
    st.write("ChemVerse is a student learning application that brings chemistry theory and interactive practice into one place.")
    st.subheader("How to use ChemVerse")
    steps = ["Choose a topic from the left navigation menu.","Open Theory Library to learn basic concepts.","Search for an element in Periodic Table.","Choose a molecule in Molecule Explorer to see its formula and properties.","Open Molecular Animation to watch an illustrative moving model.","Complete the Quiz and Assignments to test your understanding."]
    for i,s in enumerate(steps,1): st.markdown(f"**{i}.** {s}")
    st.info("The molecular animation is an educational illustration. It is not a scientific simulation or a downloadable MP4 video.")

elif page == "Theory Library":
    st.title("📚 Theory Library")
    topic = st.selectbox("Select a chemistry topic",list(THEORY))
    body,example = THEORY[topic]
    st.subheader(topic)
    st.write(body)
    st.success(example)

elif page == "Periodic Table":
    st.title("⚛️ Periodic Table Explorer")
    query = st.text_input("Search by element name or symbol",placeholder="Try Oxygen, Fe or Au")
    filtered = [x for x in ELEMENTS if not query or query.lower() in x[2].lower() or query.lower()==x[1].lower()]
    st.caption(f"Showing {len(filtered)} of 118 elements")
    st.dataframe([{"Atomic number":n,"Symbol":sym,"Element":name} for n,sym,name in filtered],use_container_width=True,hide_index=True)
    choice = st.selectbox("Select an element", [f"{n}. {sym} — {name}" for n,sym,name in ELEMENTS])
    n,sym,name = next(x for x in ELEMENTS if choice.startswith(str(x[0])+"."))
    a,b,c = st.columns(3)
    a.metric("Atomic number",n); b.metric("Protons",n); c.metric("Electrons in neutral atom",n)
    st.info("The number of neutrons depends on the isotope. Element properties such as melting and boiling points should be checked against a reliable reference.")

elif page == "Molecule Explorer":
    st.title("🧬 Molecule Explorer")
    name = st.selectbox("Choose a molecule or compound",list(MOLECULES))
    data = MOLECULES[name]
    st.markdown(f'<div class="hero"><h1>{html.escape(name)}</h1><p>Formula: {html.escape(data["formula"])}</p></div>',unsafe_allow_html=True)
    a,b,c = st.columns(3)
    a.metric("Formula",data["formula"]); b.metric("Shape",data["shape"]); c.metric("Bond type",data["bond"])
    st.subheader("Molecular composition")
    st.write(data["atoms"])
    st.subheader("Key information")
    st.write(data["facts"])
    st.subheader("Common use")
    st.write(data["use"])
    st.caption("This page provides introductory learning information. For advanced experimental values, consult a chemistry reference database.")

elif page == "Molecular Animation":
    st.title("🎞️ Molecular Animation Preview")
    name = st.selectbox("Select a preview",["Water","Hydrogen","Oxygen"])
    formulas = {"Water":"H₂O","Hydrogen":"H₂","Oxygen":"O₂"}
    st.write("Press play in the embedded preview if your browser shows the animation controls. The moving atoms below illustrate molecular motion.")
    molecule_animation(name,formulas[name])
    st.subheader("What does the model show?")
    st.write("Atoms are represented by spheres and bonds by connecting lines. The model is simplified and is not drawn to exact scale.")
    st.info("This is a browser-based animation preview, not an exported MP4 or a full video editor.")

elif page == "Animation Videos":
    st.title("🎬 Chemistry Animation Videos")
    st.write("Choose a topic and watch an educational chemistry animation inside ChemVerse.")
    video_library = {
        "Water molecule formation": {
            "url": "https://www.youtube.com/watch?v=2jG4C1BUekE",
            "description": "See two hydrogen atoms attach to an oxygen atom to form a water molecule (H₂O).",
            "source": "NASA Video"
        },
        "Ionic and covalent bonding": {
            "url": "https://www.youtube.com/watch?v=Bpm3tIIyupk",
            "description": "An animated explanation of how ionic and covalent bonds form.",
            "source": "EarthPen"
        },
        "Chemical bonding explained": {
            "url": "https://www.youtube.com/watch?v=KDVahhH8mcU",
            "description": "Learn about electron transfer in ionic bonding and electron sharing in covalent bonding.",
            "source": "Najam Academy"
        },
        "Electrolysis of water": {
            "url": "https://www.youtube.com/watch?v=GmSZNFwcbs0",
            "description": "Watch an animation showing how water can be separated into hydrogen and oxygen during electrolysis.",
            "source": "American Chemical Society animation"
        },
        "Ethanol evaporation": {
            "url": "https://www.youtube.com/watch?v=jKGeDlqJOgU",
            "description": "Visualise ethanol molecules leaving the liquid and entering the gas phase.",
            "source": "American Chemical Society animation"
        },
        "Sugar dissolving and changing": {
            "url": "https://www.youtube.com/watch?v=UHhQzeXxSNQ",
            "description": "See the difference between sugar dissolving (a physical change) and later chemical changes during caramelisation.",
            "source": "American Chemical Society animation"
        }
    }
    chosen_video = st.selectbox("Select an animation video", list(video_library))
    selected_video = video_library[chosen_video]
    st.subheader(chosen_video)
    st.video(selected_video["url"])
    st.write(selected_video["description"])
    st.caption("Video source: " + selected_video["source"] + ". Videos are hosted by their publishers on YouTube and require an internet connection.")
    st.info("If a video does not play inside the app, open it on YouTube using the video player menu or try the link in your browser.")
    with st.expander("Show all video topics"):
        for title, details in video_library.items():
            st.markdown(f"**{title}** — {details['description']}")

elif page == "Quiz":
    st.title("🧠 Chemistry Quiz")
    st.write("Choose one answer for each question, then submit to see your score.")
    answers = {}
    for i,(question,options,correct,explanation) in enumerate(QUIZ):
        answers[i] = st.radio(f"{i+1}. {question}",options,key=f"quiz_{i}")
    if st.button("Submit quiz",type="primary"):
        score = sum(answers[i] == item[2] for i,item in enumerate(QUIZ))
        st.session_state["quiz_score"] = score
        st.session_state["quiz_submitted"] = True
    if st.session_state.get("quiz_submitted"):
        score = st.session_state["quiz_score"]
        st.success(f"Your score: {score} / {len(QUIZ)}")
        for i,item in enumerate(QUIZ):
            st.write(f"**Q{i+1}:** {'Correct' if answers[i]==item[2] else 'Correct answer: '+item[2]} — {item[3]}")
        if st.button("Try quiz again"):
            st.session_state["quiz_submitted"] = False
            st.rerun()

elif page == "Assignments":
    st.title("📝 Practice Assignments")
    tasks = {
      "Assignment 1 – Atomic Structure":["Define an atom.","Name the three main subatomic particles.","State the charge of each particle.","Explain atomic number and mass number with one example."],
      "Assignment 2 – Chemical Bonding":["What is a chemical bond?","Explain ionic bonding using sodium chloride.","Explain covalent bonding using water.","Write two differences between ionic and covalent compounds."],
      "Assignment 3 – Molecules and Properties":["Define a molecule and a compound.","Write the formulas of water, carbon dioxide and methane.","Explain two physical properties and two chemical properties.","Describe one use of each compound."]
    }
    selected = st.selectbox("Choose an assignment",list(tasks))
    st.subheader(selected)
    questions = tasks[selected]
    for i,q in enumerate(questions,1):
        st.markdown(f"**{i}. {q}**")
    st.divider()
    st.subheader("Write your answers")
    answer = st.text_area("Your answers",height=260,placeholder="Type your answers here. You can number them 1, 2, 3 and 4.")
    content = selected + "\n\nQUESTIONS\n" + "\n".join(f"{i}. {q}" for i,q in enumerate(questions,1)) + "\n\nMY ANSWERS\n" + answer
    st.download_button("⬇️ Download assignment",content,file_name="chemverse_assignment.txt",mime="text/plain")
    st.caption("Your questions are displayed above. Write your answers and download a copy to keep.")

elif page == "Compare Molecules":
    st.title("📊 Compare Molecules")
    left,right = st.columns(2)
    with left: one = st.selectbox("First molecule",list(MOLECULES),index=0)
    with right: two = st.selectbox("Second molecule",list(MOLECULES),index=1)
    st.dataframe([
      {"Property": "Formula",one:MOLECULES[one]["formula"],two:MOLECULES[two]["formula"]},
      {"Property": "Shape",one:MOLECULES[one]["shape"],two:MOLECULES[two]["shape"]},
      {"Property": "Bond type",one:MOLECULES[one]["bond"],two:MOLECULES[two]["bond"]},
      {"Property": "Composition",one:MOLECULES[one]["atoms"],two:MOLECULES[two]["atoms"]},
      {"Property": "Common use",one:MOLECULES[one]["use"],two:MOLECULES[two]["use"]}
    ],use_container_width=True,hide_index=True)

elif page == "About":
    st.title("ℹ️ About ChemVerse")
    st.write("ChemVerse is an educational Chemistry application created as a student project.")
    st.markdown("**Main objectives**")
    st.write("- Make chemistry topics easier to understand.\n- Help students explore elements and molecules.\n- Provide visual learning and practice questions.\n- Encourage independent learning.")
    st.caption("Educational content is introductory. Always follow your lecturer's notes and trusted chemistry references.")

st.divider()
st.markdown('<p class="small">ChemVerse • Chemistry Learning Lab • Educational student project</p>',unsafe_allow_html=True)
