## Current Setup
- FastAPI serves Jinja templates from templates and static assets from static.
- The root index.html and style.css are standalone and not currently used by the FastAPI routes.

## Goal
- Make /Users/advaith/Soccer Automation/index.html the main entry point and /Users/advaith/Soccer Automation/style.css the primary stylesheet.
- Introduce React with minimal overhead (CDN-based), no Node toolchain required initially.

## Approach
- Switch the “/” route to serve the root index.html so it becomes the app shell.
- Enhance index.html with a React mount point and CDN scripts for React/ReactDOM.
- Keep styling in style.css; optionally copy any template CSS from static/style.css later if needed.

## Changes (Files)
- index.html: add <div id="app"></div>, load style.css, include React and ReactDOM via CDN, add a small inline or external module script to bootstrap React.
- style.css: retain existing rules; optionally add utility classes for cards and layout used by React components.
- web route: update FastAPI route for “/” to return FileResponse("index.html"). Keep /static mounted for any additional assets.

## React Initialization
- Render a simple React component (e.g., Card) into #app to validate setup.
- Organize future code in static/js/main.js and static/js/components/* if preferred; initially can use a single script for simplicity.

## Data Fetching (Optional)
- If API endpoints exist (e.g., /api/*), add fetch calls in React to display dynamic data.
- Keep SSR templates available under separate routes while SPA grows.

## Verification
- Start Uvicorn and visit / to confirm index.html renders.
- Verify React mounts successfully and CSS applies to components.

## Future Upgrade (Optional)
- If desired, migrate to Vite: create a /frontend React app, build to /static/dist, and update index.html to load built assets. Keep FastAPI for API and static serving.

## Code References
- FastAPI web app and static mounting: [web.py](file:///Users/advaith/Soccer%20Automation/src/interfaces/web.py)
- Templates currently used: [index.html](file:///Users/advaith/Soccer%20Automation/templates/index.html), [base.html](file:///Users/advaith/Soccer%20Automation/templates/base.html)
- Root files to become primary: [index.html](file:///Users/advaith/Soccer%20Automation/index.html), [style.css](file:///Users/advaith/Soccer%20Automation/style.css)