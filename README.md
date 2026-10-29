# My Opportunity Desk — daily auto-updating personal dashboard

This is a mobile-friendly static website plus a scheduled feed updater. The site reads `data.json`; GitHub Actions runs the Python updater every day at approximately 8:00 AM India time and commits refreshed items. GitHub Pages serves the website.

## Important limitation (please read)
The updater discovers leads through Google News RSS search feeds. This is **not** an official government API and does **not** prove a vacancy is open or that you are eligible. Open the source and verify the original official notification before applying. Some RSS links may lead to media coverage rather than the original notice. The official portal shortcuts remain on the dashboard. This starter intentionally does not invent age limits, fees, deadlines, or eligibility.

## One-time setup (phone or computer)
1. Sign in or create a GitHub account at https://github.com/.
2. Create a new **public** repository, for example `my-opportunity-desk`.
3. Upload the contents of this folder to the repository, keeping the `.github/workflows/daily-update.yml` path. If using GitHub's web uploader, make sure the `.github` folder is included; easiest is to upload the ZIP's extracted contents from a computer or use GitHub Desktop.
4. Open **Settings → Pages**. Under Build and deployment, select **Deploy from a branch**, choose `main` and `/ (root)`, then Save.
5. Open **Actions** and enable workflows if GitHub asks. Open **Update opportunity feed** and click **Run workflow** once to test. The daily schedule then runs at 02:30 UTC (08:00 IST), though GitHub may delay scheduled runs.
6. After the workflow completes, open the Pages URL shown under Settings → Pages. It can take a few minutes for first publication.

## Files
- `index.html` — dashboard UI
- `data.json` — feed the dashboard displays
- `scripts/update_feed.py` — RSS collection and de-duplication
- `.github/workflows/daily-update.yml` — daily schedule and commit

## Troubleshooting
- If the site shows no items, run the workflow manually under Actions and inspect its log.
- GitHub Pages does not run the updater itself; GitHub Actions does.
- If scheduled updates stop, check Actions for failures and repository workflow permissions. Under Settings → Actions → General, allow workflows to read and write repository contents if needed.
- Keep the repository public only if you are comfortable with the source code being public. No personal account number or secret is needed for this starter.
