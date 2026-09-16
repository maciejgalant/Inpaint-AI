# First push to GitHub

Repository URL:

https://github.com/maciejgalant/Inpaint-AI

## If the GitHub repository is empty

Open a terminal in this repository folder and run:

```bash
git init
git branch -M main
git add .
git commit -m "Fix silent exception handling flagged by QGIS plugin validation"
git remote add origin https://github.com/maciejgalant/Inpaint-AI.git
git push -u origin main
```

## If the GitHub repository already contains an initial README/license

Clone it first, then copy this prepared repository content into the cloned directory:

```bash
git clone https://github.com/maciejgalant/Inpaint-AI.git
cd Inpaint-AI
# copy the prepared files into this directory
git add .
git commit -m "Fix silent exception handling flagged by QGIS plugin validation"
git push
```

Do not commit OpenAI API keys, QGIS authentication databases or local `.env` files.

After the source is pushed and validated, create tag `v1.0.0-rc1` and attach the exact tested `InpaintAI.zip` from the release package.
