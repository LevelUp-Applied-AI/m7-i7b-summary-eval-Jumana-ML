python -m venv .venv

# Activate and install dependencies
# Works for Git Bash on Windows
echo "Activating virtual environment..."

source .venv/Scripts/activate

echo "Installing requirements..."

pip install -r requirements.txt
pip install transformers torch pandas openpyxl
python -m spacy download xx_ent_wiki_sm

echo "--------------------------------"
echo "Setup complete!"