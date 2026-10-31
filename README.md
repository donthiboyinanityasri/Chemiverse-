# ChemVerse – Chemistry Learning App

A mobile-friendly Streamlit starter project for an interactive Chemistry learning platform.

## Features in this starter
- Home page and getting-started guide
- Introductory Chemistry theory
- List/search for all 118 element names and symbols
- PubChem compound lookup for available identifiers/properties
- PubChem 2D structure image and interactive 3Dmol.js viewer when 3D data exists
- Molecular display styles and viewer background selection
- Animation storyboards
- Video planning workspace (not full MP4 rendering yet)
- Quiz, practice assignments, molecule comparison and downloadable text reports

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy on Streamlit Community Cloud
1. Push these files to a GitHub repository.
2. Visit https://share.streamlit.io/
3. Sign in with GitHub and choose **Create app**.
4. Select your repository, branch `main`, and file path `app.py`.
5. Deploy.

## Important science/data notes
- Compound records are fetched from PubChem PUG REST when available.
- PubChem may return computed properties; consult the compound record for definitions and source references.
- Melting point, freezing point, boiling point and chemical properties are not available for every compound record. Missing values must not be interpreted as zero.
- The periodic table list includes all 118 element names and symbols. It does not yet include a complete curated dataset of every element's physical constants.
- 3D conformers may not be available for every compound.
- The 3D viewer loads 3Dmol.js from its public CDN. Internet access is required.
- The Video Studio currently creates a script/storyboard text file; full MP4 rendering, music mixing and timeline editing are planned for a later version.

## Academic use
Use this as a learning prototype. Verify scientific values with trusted sources and cite them in your assignment.


## Fast submission checklist
- Upload `app.py`, `requirements.txt`, `README.md`, and `.gitignore` to GitHub.
- Deploy the repository from Streamlit Community Cloud using `app.py` as the main file.
- Test the app on your phone before presenting.
