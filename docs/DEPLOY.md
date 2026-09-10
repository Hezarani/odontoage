# Deploying OdontoAge — GitHub · PyPI · Zenodo · Pages

A one-time checklist to publish OdontoAge and make it citable. It is written to be followed
by someone who does **not** live in a terminal: most steps are clicks on a website, and the
few commands are given in full, to copy and paste one line at a time.

> **Two things are permanent, so do them last and only once you're happy:**
> publishing to **PyPI** (version `0.1.0` can never be re-uploaded — a later fix ships as
> `0.1.1`) and minting a **Zenodo DOI**. Everything else is editable.

---

## Before you start — decide the GitHub account

The project is written for the GitHub user **`Hezarani`** (repo `Hezarani/odontoage`); the
web app, citation file, and links all use that name. If you publish under a **different**
GitHub username, tell me and I'll update every link in one pass first — otherwise the demo
URL and badges will point at the wrong place.

You'll also need, when the time comes:
- a **GitHub** account (free), and
- a **PyPI** account (free) — https://pypi.org/account/register/.

---

## 1 · Put the code on GitHub

**The simplest, all-in-the-browser way (recommended if git isn't set up on your machine):**

1. Go to **https://github.com/new**. Repository name: **`odontoage`**. Visibility:
   **Public**. Do **not** tick "Add a README". Click **Create repository**.
2. On the new empty repo page, click **"uploading an existing file"**.
3. Open your file manager at `DentGit/odontoage`, select **everything inside** it, and drag
   it onto the browser page. (Your source PDFs in `download/` are ignored automatically and
   must not be uploaded.) Wait for the list to fill in, then click **Commit changes**.

**Or, from a terminal** (the repo is already prepared locally with a first commit — see the
note I'll leave you; you only need to connect it and push):
```bash
cd DentGit/odontoage
git remote add origin https://github.com/Hezarani/odontoage.git
git push -u origin main
```
If the push asks for a password, use a **Personal Access Token** (GitHub → Settings →
Developer settings → Tokens), not your login password. If it's rejected with **GH007**
("email is private"), run this once and push again:
```bash
git config user.email "Hezarani@users.noreply.github.com"
git commit --amend --reset-author --no-edit
```

---

## 2 · Turn on the live demo (GitHub Pages)

Repo → **Settings → Pages** → *Build and deployment* → Source: **Deploy from a branch** →
Branch **main**, folder **/docs** → **Save**. About a minute later the demo is live at:
```
https://hezarani.github.io/odontoage/
```
(The `docs/.nojekyll` file is already included so the styling loads correctly.)

---

## 3 · Publish to PyPI so anyone can `pip install odontoage`

**Recommended — automatic, no passwords (Trusted Publishing).** The repo already contains
the workflow `.github/workflows/publish.yml`. You authorise it once:

1. Sign in to PyPI → **Account settings → Publishing → Add a pending publisher**.
2. Fill in exactly:
   - **PyPI project name:** `odontoage`
   - **Owner:** your GitHub username (e.g. `Hezarani`)
   - **Repository name:** `odontoage`
   - **Workflow name:** `publish.yml`
   - **Environment name:** `pypi`
3. Save. From now on, **publishing a GitHub Release (Step 4) also publishes to PyPI
   automatically** — GitHub builds the package and PyPI accepts it over a secure one-time
   handshake, with no token stored anywhere.

**Alternative — manual upload from your machine.** Ready-built files are in the `dist/`
folder (`odontoage-0.1.0.tar.gz` and `odontoage-0.1.0-py3-none-any.whl`, already validated):
```bash
cd DentGit/odontoage
python3 -m pip install --upgrade twine
python3 -m twine upload dist/*        # username: __token__   password: your PyPI API token
```
Create the API token at https://pypi.org/manage/account/token/. Verify afterwards at
https://pypi.org/project/odontoage/.

---

## 4 · Mint a citable DOI (Zenodo) — the part that "brings citations"

1. Go to **https://zenodo.org**, click **Log in → GitHub**, and authorise Zenodo.
2. Zenodo → **Settings → GitHub**. Find **`Hezarani/odontoage`** in the list and flip its
   switch **ON**. (If it's not listed, click *Sync now*.)
3. Back on GitHub: repo → **Releases → Draft a new release**. Tag: **`v0.1.0`**; title:
   **`OdontoAge v0.1.0`**; description: a sentence or two. Click **Publish release**.
4. That single release does three things at once: Zenodo archives the repo and mints a
   permanent **DOI**; (if you set up Step 3-recommended) the package publishes to **PyPI**;
   and Pages redeploys.
5. Copy the DOI Zenodo shows you, then tell me — I'll drop it into the README badge,
   `CITATION.cff`, and `.zenodo.json` and you re-commit (or I'll prepare the change for you).

---

## 5 · Ten minutes of polish that drives discovery

- Repo **About** (gear icon, top-right of the repo): add the description and set the website
  to `https://hezarani.github.io/odontoage/`.
- **Topics:** `forensic-odontology`, `dental-age-estimation`, `cameriere`, `demirjian`,
  `willems`, `kvaal`, `forensic`, `dentistry`, `python`.
- **Social preview** (Settings → General → Social preview): upload
  `assets/social-preview.png`.

---

## 6 · Later — a peer-reviewed software paper (JOSS)

With an OSI licence, tests, docs, and a few months of public history, OdontoAge is a good
candidate for a short **JOSS** paper (`paper.md` and `paper.bib` are already included) — a
peer-reviewed, Crossref-DOI citation. Submit at https://joss.theoj.org when you're ready.

---

### Releasing a fix later
Bump the version in `pyproject.toml` and `odontoage/__init__.py` (e.g. to `0.1.1`), commit
and push, then **Draft a new release** with tag `v0.1.1`. Trusted Publishing ships it to
PyPI and Zenodo mints a new version DOI automatically.
