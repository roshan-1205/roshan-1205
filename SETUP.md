# ROSHAN × AKATSUKI — Setup

## Upload in one go
1. Open **https://github.com/roshan-1205/roshan-1205** (your profile README repository).
2. Extract the ZIP locally. **Upload the contents of the extracted folder**, not the outer ZIP or an extra nested folder.
3. Preserve every relative path, including `.github/workflows/refresh-profile.yml` and `scripts/update_activity.py`.
4. Commit the changes on the repository's default branch.
5. Go to **Settings → Actions → General → Workflow permissions** and enable **Read and write permissions** if your repository's policy permits it.
6. Go to **Actions → Refresh Akatsuki Profile → Run workflow** and inspect the result.
7. Revisit your profile after the workflow completes. On later days, the workflow refreshes automatically.

## Animated visuals
- `hero.svg`, `ninja-way.svg`, `jutsu-stack.svg`, `ninja-id.svg`, `mission-header.svg`, `village-banner.svg`, and `connect.svg` use SVG/CSS animation: floating character, rotating rings, glows, and scan effects.
- `assets/akatsuki-crows-loop.gif` is a **real 45-frame looping animation** containing moving crows and a red moon. It continues to move even if the viewer's GitHub client does not support every SVG animation.
- Display headings are **vector outlines** rather than live fonts; this keeps typography consistent and avoids SVG overflow on different systems.
- Viewers who have reduced-motion settings may see static SVGs.

## Commit tracker: real data only
- `activity-tracker.svg` is initially a custom **waiting-for-sync** placeholder with no fake counts.
- `scripts/update_activity.py` uses GitHub GraphQL's `totalCommitContributions`, `totalContributions`, and daily contribution calendar to compute real statistics.
- The displayed streak is a **contribution-day streak** (not necessarily consecutive days containing commits).
- The first successful run refreshes numbers and the calendar. The schedule is daily, and GitHub may start scheduled jobs later than the precise cron time.
- The workflow token may not expose certain private contributions: GitHub's API determines the totals.
- On failed tracker requests, no mock data is written; the workflow reports the error and the previously generated SVG is preserved.
- If the third-party 3D skyline action fails, the tracker can still be published; the skyline retains its placeholder.

## Files used by the running README
```
README.md
hero.svg
ninja-way.svg
jutsu-stack.svg
ninja-id.svg
mission-header.svg
activity-tracker.svg
village-banner.svg
connect.svg
assets/
  activity-template.svg
  akatsuki-crows-loop.gif
  akatsuki-portrait.png
  variant-1.jpg ... variant-7.jpg
scripts/
  update_activity.py
.github/workflows/
  refresh-profile.yml
profile-3d-contrib/
  profile-night-view.svg
```

## Validation
Generated SVGs were parsed as XML and rendered to PNG; the tracker was tested with **temporary synthetic data for layout validation only**. This package includes **no simulated tracker stats**. Its real-data workflow can only be tested end-to-end after it runs on GitHub.

## Important
No account modification is performed by this ZIP download. Push it manually to your own repository. This is Itachi/Akatsuki-*inspired* original profile composition, rather than a pixel-identical copy of a third-party README.
