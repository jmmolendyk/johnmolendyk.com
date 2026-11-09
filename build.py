#!/usr/bin/env python3
"""Builds the johnmolendyk.com static site. Usage: python3 build.py <output_dir>
Edit the content below, re-run, commit the output. No dependencies."""
import os
import sys

OUT = sys.argv[1] if len(sys.argv) > 1 else "."
SITE = "https://johnmolendyk.com"
CALENDLY = "https://calendly.com/johnmolendyk/1-1"
FLOWHAUS = "https://flowhaus.ai"
LINKEDIN = "https://www.linkedin.com/in/johnmolendyk"
FORM_KEY = "YOUR_WEB3FORMS_ACCESS_KEY"

NAV = [("/work/", "Work"), ("/approach/", "Approach"), ("/about/", "About"), ("/contact/", "Contact")]



# ---------------------------------------------------------------- icons
# Layered glyphs on a gradient tile: each shape gets a soft offset shadow for depth.
import math

W, A = "#ffffff", "#f2a516"


def _shape(sh, shadow=False):
    kind, geo, col = sh[0], sh[1], sh[2]
    op = sh[3] if len(sh) > 3 else 1
    sw = sh[4] if len(sh) > 4 else 2.4
    c = "#0a1d66" if shadow else col
    o = op * (0.32 if shadow else 1)
    tr = ' transform="translate(0 1.6)"' if shadow else ""
    if kind == "path-f":
        return '<path d="%s" fill="%s" fill-opacity="%s"%s/>' % (geo, c, o, tr)
    if kind == "path-s":
        return '<path d="%s" fill="none" stroke="%s" stroke-opacity="%s" stroke-width="%s" stroke-linecap="round" stroke-linejoin="round"%s/>' % (geo, c, o, sw, tr)
    if kind == "rect":
        x, y, w, h = geo
        return '<rect x="%s" y="%s" width="%s" height="%s" rx="1.8" fill="%s" fill-opacity="%s"%s/>' % (x, y, w, h, c, o, tr)
    if kind == "circle-f":
        cx, cy, r = geo
        return '<circle cx="%s" cy="%s" r="%s" fill="%s" fill-opacity="%s"%s/>' % (cx, cy, r, c, o, tr)
    if kind == "circle-s":
        cx, cy, r = geo
        return '<circle cx="%s" cy="%s" r="%s" fill="none" stroke="%s" stroke-opacity="%s" stroke-width="%s"%s/>' % (cx, cy, r, c, o, sw, tr)


def _teeth():
    out = []
    for k in range(8):
        a = math.radians(k * 45)
        x1, y1 = 16 + 9 * math.cos(a), 16 + 9 * math.sin(a)
        x2, y2 = 16 + 12.2 * math.cos(a), 16 + 12.2 * math.sin(a)
        out.append(("path-s", "M%.2f %.2f L%.2f %.2f" % (x1, y1, x2, y2), W, 1, 3.6))
    return out


GLYPHS = {
    "shield": [("path-f", "M16 3.5 L26 7.5 V15.5 C26 21.5 21.8 26 16 28.5 C10.2 26 6 21.5 6 15.5 V7.5 Z", W),
               ("path-s", "M11.3 16 L14.8 19.6 L21 12", A, 1, 2.9)],
    "flow": [("path-s", "M16 11 V15.5 M9 20.5 V15.5 H23 V20.5", W, .85, 2),
             ("rect", (11, 4.5, 10, 6.5), W), ("rect", (4, 20.5, 10, 7), W), ("rect", (18, 20.5, 10, 7), A)],
    "roadmap": [("rect", (4, 19, 6, 8), W), ("rect", (13, 14, 6, 13), W), ("rect", (22, 10, 6, 17), W),
                ("path-s", "M25 10 V3.8", W, 1, 1.7), ("path-f", "M25 3.6 L30.2 5.7 L25 7.8 Z", A)],
    "cog": [("circle-s", (16, 16, 6.6), W, 1, 3.4)] + _teeth() + [("circle-f", (16, 16, 2.5), A)],
    "layers": [("path-s", "M4 21 L16 27 L28 21", W, .75, 2.4), ("path-s", "M4 16 L16 22 L28 16", W, .9, 2.4),
               ("path-f", "M16 4.5 L28 10.5 L16 16.5 L4 10.5 Z", A)],
    "board": [("rect", (4, 5, 7, 7), W), ("rect", (4, 14.5, 7, 7), W), ("rect", (13, 5, 7, 11), W),
              ("rect", (13, 18.5, 7, 4.5), W, .7), ("rect", (22, 5, 7, 7), W, .7), ("rect", (22, 14.5, 7, 12), A)],
    "pen": [("path-s", "M8 7.5 L6 25 M24 7.5 L26 25", W, .6, 1.3),
            ("path-s", "M6 25 C7 9 25 9 26 25", W, 1, 2.8),
            ("rect", (3.9, 23, 4.2, 4.2), W), ("rect", (23.9, 23, 4.2, 4.2), W),
            ("circle-f", (8, 7.5, 2.4), A), ("circle-f", (24, 7.5, 2.4), A)],
}


def icon(name):
    shapes = GLYPHS[name]
    body = "".join(_shape(s, True) for s in shapes) + "".join(_shape(s) for s in shapes)
    return '<span class="icon" aria-hidden="true"><svg viewBox="0 0 32 32" width="35" height="35">%s</svg></span>' % body


def page(path, title, desc, body, current=""):
    nav = "".join(
        '<a href="%s"%s>%s</a>' % (h, ' aria-current="page"' if h == current else "", t) for h, t in NAV
    )
    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#ffffff">
<link rel="canonical" href="{SITE}{path}">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{SITE}{path}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/style.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header"><div class="wrap">
<a class="brand" href="/">John Molendyk</a>
<nav class="nav" aria-label="Main">{nav}<a class="nav-cta" href="{FLOWHAUS}">Flowhaus.ai &#8599;</a></nav>
</div></header>
<main id="main">
{body}
</main>
<footer class="site-footer"><div class="wrap">
<div>&copy; 2026 John Molendyk</div>
<div class="foot-links"><a href="/work/">Work</a><a href="/approach/">Approach</a><a href="/about/">About</a><a href="/contact/">Contact</a><a href="{LINKEDIN}">LinkedIn</a><a href="{FLOWHAUS}">Flowhaus.ai</a></div>
</div></footer>
</body>
</html>
"""
    write(path, html)


def write(path, content):
    target = os.path.join(OUT, path.lstrip("/"))
    if path.endswith("/"):
        target = os.path.join(target, "index.html")
    os.makedirs(os.path.dirname(target), exist_ok=True)
    with open(target, "w", encoding="utf-8") as f:
        f.write(content)


# ---------------------------------------------------------------- case studies
CASES = [
    {
        "slug": "mortgage-document-governance",
        "logo": ("union-bank", "Union Bank"),
        "short": "Mortgage document governance",
        "title": "Bringing controls to mortgage document inventory",
        "client": "Union Bank, mortgage banking",
        "years": "2017–2018",
        "role": "Senior Consultant, Document Governance",
        "tags": [("Governance", ""), ("Audit response", ""), ("Process", ""), ("Design in context", "d")],
        "card_stat": "5,000+ → ~500",
        "card_stat_note": "records rationalized into controlled documents",
        "summary": "Audit findings exposed scattered, unversioned mortgage documents. I led the work to turn 5,000+ records into a controlled, role-based library the bank could defend to auditors.",
        "stats": [
            ("5,000+", "records audited and rationalized"),
            ("~90%", "fewer state-disclosure documents"),
            ("100%", "of in-scope documents validated and versioned"),
            ("<5 months", "against an 18-month IT estimate"),
        ],
        "sections": [
            ("The situation",
             "<p>Multi-state audit findings pointed at a basic problem: nobody could say which mortgage documents were authoritative. Documents lived in inboxes, personal drives and desktops. There was no version control, no way to verify that a document was current or matched a state and loan type, and finding the right one depended on long-tenured employees.</p>"),
            ("My role",
             "<p>I investigated the findings, led the cross-functional work with Operations, Legal and Compliance, and owned research, design and project delivery. I built the solution to enterprise IT standards rather than waiting in the IT queue, and handed administration and development capability to internal teams so the bank could own it afterward.</p>"),
            ("What I did",
             "<ul><li><strong>Audited the population.</strong> Reviewed 5,000+ records to find the real set of controlled documents, validating each finding with compliance, operations and administration.</li>"
             "<li><strong>Designed the control model.</strong> Role-based access by job and operational need; metadata for loan type, state applicability and version; a standard versioning schema with archiving so only current documents stay active.</li>"
             "<li><strong>Built it without code.</strong> Delivered the repository in SharePoint and InfoPath, including filtering by state, loan type and compliance role.</li>"
             "<li><strong>Modeled mortgage scenarios.</strong> Determined which documents are required for a given state, loan amount and other factors. The model supported internal and third-party audits.</li></ul>"),
            ("Outcome",
             "<p>Every in-scope document was validated and versioned, so only current documents entered loan processing. The inventory shrank by roughly 90%, retrieval got faster, and audit conversations got easier because the answer to “which version is authoritative?” was now a lookup instead of a debate. Administration moved to internal teams, which kept the controls alive after the project ended.</p>"),
        ],
        "design": "Stakeholder and site maps, wireframes and usability testing are why people followed the controls. A governance model that is hard to use gets worked around; this one was designed around how Operations and Compliance actually search for documents.",
    },
    {
        "slug": "wealth-migration-continuity",
        "logo": ("wells-fargo", "Wells Fargo"),
        "short": "Migration weekends with zero losses",
        "title": "Keeping wealth-management accounts transacting through three migration weekends",
        "client": "Wells Fargo / Wachovia, wealth management",
        "years": "2010–2011",
        "role": "Senior Consultant / Product Owner",
        "tags": [("Project delivery", ""), ("Risk & controls", ""), ("Data migration", ""), ("Design in context", "d")],
        "card_stat": "Zero",
        "card_stat_note": "financial losses across three data-migration weekends",
        "summary": "Core transaction systems went offline during a bank conversion, but wealth clients still expected to move large sums. I designed and led the continuity solution that kept balances accurate and fraud controls intact.",
        "stats": [
            ("0", "financial losses"),
            ("3", "migration weekends"),
            ("100%", "of accounts balanced after each weekend"),
            ("9.5", "satisfaction rating from personal bankers"),
        ],
        "sections": [
            ("The situation",
             "<p>During the data migration, the systems that manage transactions against account balances were offline and most customers lost access. Wealth-management clients were an exception: they expect to transact at any time, one bad experience could put millions in deposits at risk, and the outage was public, so fraud and IT-security teams were watching for active threats.</p>"),
            ("My role",
             "<p>I designed and led implementation of the transactional continuity solution and drove migration readiness, operational controls and execution across Wealth Management, Risk, Fraud, Compliance, IT, Data Administration and Operations, including controlled decommissioning after the conversion succeeded.</p>"),
            ("What I did",
             "<ul><li><strong>Set four goals up front:</strong> accurate real-time balances to prevent overdrafts, minimal disruption for personal bankers, fraud prevention, and compliance with privacy, security and regulatory standards.</li>"
             "<li><strong>Discovered the real process.</strong> Interviews and surveys with personal bankers (who represented client needs), a journey map of migration pain points, current-state flows of compliance steps and business rules for wires, withdrawals and deposits, and analysis of past transactions and escalations.</li>"
             "<li><strong>Built an internal application</strong> for withdrawals and deposits against live balances, impacted-account lookup, transaction review with the ability to pause updates, and weekend shift sign-ups so every shift was staffed with the right roles.</li></ul>"),
            ("Outcome",
             "<p>The three weekends delivered no financial losses and no customer-reported disruption. Accounts were balanced with wire transactions at the end of every weekend, and surveys and interviews after the first weekend found the application worked well, with no findings that required changes. Personal bankers rated the experience 9.5.</p>"),
        ],
        "design": "The application was designed from current-state flows and tested with the bankers who would use it under weekend pressure. In a high-risk event, a tool that people can use correctly the first time is itself a control.",
    },
    {
        "slug": "healthcare-feedback-platform",
        "logo": ("alliance-healthcare", "Alliance Healthcare Services"),
        "short": "Healthcare feedback and request platform",
        "title": "Replacing paper surveys with a scalable feedback and case-management platform",
        "client": "Alliance Healthcare Services",
        "years": "2015–2017",
        "role": "Technical Product Owner / Lead Product Designer",
        "tags": [("Process redesign", ""), ("Product delivery", ""), ("Compliance workflow", ""), ("Design in context", "d")],
        "card_stat": "1,000+",
        "card_stat_note": "provider sites moved off mailed paper surveys",
        "summary": "A 53-page mailed survey, spreadsheets and email were hiding the customer requests that mattered. I redesigned the process and delivered a digital platform across Qualtrics and Salesforce.",
        "stats": [
            ("1,000+", "provider sites with branded digital surveys"),
            ("64%", "less time to log and manage each request"),
            ("100%", "of contact requests routed to operations within 24 hours"),
            ("86%", "of requests answered within 48 hours"),
        ],
        "sections": [
            ("The situation",
             "<p>Paper surveys arrived 30+ days after service, and research found that over 70% of contact requests went unaddressed, lost to illegibility or timing. Teams tracked requests across email, spreadsheets and phone calls, staff spent up to 18 minutes logging a single request across several systems, and there was no scalable way to manage branding or devices for 1,000+ sites. The inconsistency also created compliance risk.</p>"),
            ("My role",
             "<p>As interim Product Owner across 15+ applications, I led the digital transformation, working with engineering, sales and operations through a phased approach. I also designed incident reporting and compliance case management for Compliance and Legal.</p>"),
            ("What I did",
             "<ul><li><strong>Mapped before building.</strong> Interviews and shadowing across sales, customer experience and regional operations, then a sitemap of the full survey lifecycle that defined roles, data sources and system responsibilities.</li>"
             "<li><strong>Piloted first.</strong> A desktop pilot for program and operations admins proved the enrollment and request flows before the tablet and phone version for field teams.</li>"
             "<li><strong>Standardized the workflow.</strong> Device replacement tickets with history, contact requests that minimize free text, and API-driven enrollment of clients and sites with branding and metadata.</li>"
             "<li><strong>Added assistive features</strong> for request identification, voice input and text rephrasing to cut documentation time in the field.</li></ul>"),
            ("Outcome",
             "<p>Time to document and manage a request dropped 64%, saving 13 minutes each, and every contact request now reached operations within 24 hours of service. Sites got self-service branded surveys, and survey data was shared across CX, operations, sales and compliance. Compliance and Legal also saw their incident-reporting cycle time cut by more than half.</p>"),
        ],
        "design": "Research, wireframes and pilot iterations drove adoption. The people closing requests were field teams on tablets and phones, so the process only worked once it fit their hands and their time.",
    },
    {
        "slug": "ai-voice-privacy-research",
        "logo": ("meta", "Meta"),
        "short": "AI voice, privacy and disclosure",
        "title": "Research behind AI voice features: privacy, disclosure and adoption",
        "client": "Meta / Reality Labs",
        "years": "2021–2023",
        "role": "Senior UX Researcher, AI / Voice",
        "tags": [("AI governance", ""), ("Privacy & disclosure", ""), ("Strategy", ""), ("Design in context", "d")],
        "card_stat": "30%",
        "card_stat_note": "more new voice users from one research-driven UI change",
        "summary": "Speech-to-text and AI features raise privacy and trust questions users notice immediately. I led research that shaped disclosure, adoption and roadmap decisions with Product, Privacy, Legal and Compliance.",
        "stats": [
            ("12 of 21", "high-priority H2 2022 initiatives informed by the research"),
            ("30%", "increase in new voice users from a single UI finding"),
            ("1/3", "of findings behind high-priority items were new to the team"),
        ],
        "sections": [
            ("The situation",
             "<p>Voice messaging in VR depended on speech-to-text and AI features, but the team had inconsistent design patterns, limited foundational research, and open questions about how first-time users perceive privacy and disclaimer notices. Adoption and retention of voice users were the commercial question; regulatory intent was the constraint.</p>"),
            ("My role",
             "<p>I led the biannual research strategy across voice, speech-to-text, AI, AR/VR and smart communication experiences, partnering with product managers, designers, engineers, data scientists, and the Privacy, Legal and Compliance teams. I also coordinated governance for studies involving AI, voice and sensitive user data.</p>"),
            ("What I did",
             "<ul><li><strong>Tested disclosure with real users.</strong> Redesigned speech-to-text disclosures so they preserved regulatory intent while increasing user trust and first-time voice adoption.</li>"
             "<li><strong>Translated research into decisions.</strong> Connected findings to quarterly KPIs, roadmap priorities and longer-term strategy, and gave stakeholders direction on privacy and legal concerns.</li>"
             "<li><strong>Paired behavior with qualitative data</strong> to establish behavior-based benchmarks.</li>"
             "<li><strong>Made the work reusable.</strong> Contributed studies to research libraries; the findings became a reference for voice-based design in AR and wearables.</li></ul>"),
            ("Outcome",
             "<p>Research informed 12 of 21 high-priority initiatives for the second half of 2022. A single UI finding the team had not previously identified increased new voice users by 30%, and the disclosure redesign showed that privacy transparency and adoption can move together.</p>"),
        ],
        "design": "This is the project where design research was the governance mechanism: the disclosure was the control, and testing it with users is how we knew it worked.",
    },
]
for i, c in enumerate(CASES):
    c["prev"] = CASES[i - 1] if i > 0 else None
    c["next"] = CASES[i + 1] if i < len(CASES) - 1 else None


def tags_html(tags):
    return '<div class="tags">' + "".join('<span class="%s">%s</span>' % (k, t) for t, k in tags) + "</div>"


def work_card(c):
    return f"""<a class="card work-card" href="/work/{c['slug']}/">
{tags_html(c['tags'])}
<h3>{c['short']}</h3>
<div class="stat">{c['card_stat']}<small>{c['card_stat_note']}</small></div>
<p class="muted">{c['client']}, {c['years']}</p>
<span class="more">Read the case &rarr;</span>
</a>"""


for c in CASES:
    stats = "".join('<div class="stat-box"><b>%s</b><span>%s</span></div>' % s for s in c["stats"])
    secs = "".join("<h2>%s</h2>%s" % s for s in c["sections"])
    nav_prev = '<a href="/work/%s/">&larr; %s</a>' % (c["prev"]["slug"], c["prev"]["short"]) if c["prev"] else '<a href="/work/">&larr; All work</a>'
    nav_next = '<a href="/work/%s/">%s &rarr;</a>' % (c["next"]["slug"], c["next"]["short"]) if c["next"] else '<a href="/work/">All work &rarr;</a>'
    lg, lg_alt = c["logo"]
    logo = '<img class="client-logo logo-%s" src="/assets/logos/%s.png" alt="%s logo">' % (lg, lg, lg_alt)
    body = f"""<section class="case-head"><div class="wrap">
<div class="case-top"><p class="eyebrow">Case study</p>{logo}</div>
<h1>{c['title']}</h1>
<p class="lede">{c['summary']}</p>
{tags_html(c['tags'])}
<div class="meta-row"><span><strong>Client</strong> {c['client']}</span><span><strong>When</strong> {c['years']}</span><span><strong>Role</strong> {c['role']}</span></div>
<div class="stats">{stats}</div>
</div></section>
<section style="padding-top:24px"><div class="wrap"><div class="prose">
{secs}
<div class="callout amber"><h3>Where design mattered</h3><p>{c['design']}</p></div>
<div class="case-nav">{nav_prev}{nav_next}</div>
</div></div></section>"""
    page(
        "/work/%s/" % c["slug"],
        "%s | John Molendyk" % c["title"],
        c["summary"],
        body,
        "/work/",
    )

# ---------------------------------------------------------------- home
home = f"""<section class="hero"><div class="wrap">
<p class="eyebrow">AI governance &middot; process &middot; delivery</p>
<h1>I help organizations put AI governance in place, and make it stick.</h1>
<p class="lede">Twenty years of delivering controls, processes and technology in financial services, healthcare and tech, now focused on governance that enables AI adoption instead of slowing it down.</p>
<div class="actions"><a class="btn" href="{CALENDLY}">Book a discovery call</a><a class="btn ghost" href="/work/">See the work</a></div>
<ul class="badges"><li>AIGP</li><li>ISO/IEC 42001 Lead Implementer (BSI)</li><li>CIPM</li><li>Six Sigma Black Belt</li><li>CSM &middot; CSPO</li></ul>
<p class="frameworks">Works with NIST AI RMF, ISO/IEC 42001, OECD AI Principles and privacy requirements.</p>
</div></section>

<section class="band"><div class="wrap">
<p class="eyebrow">What I do</p>
<h2>Governance that fits how the organization actually works</h2>
<div class="grid three" style="margin-top:28px">
<div class="card accent">{icon("shield")}<h3>AI governance</h3><p>Find the AI in use, assess risk and maturity, set up the operating model and controls, and prepare for regulation, then transition ownership to your team.</p></div>
<div class="card accent">{icon("flow")}<h3>Process and controls</h3><p>Fix the process first. Six Sigma discipline applied to audit findings, compliance workflows and decision rules so controls are lighter and actually followed.</p></div>
<div class="card accent">{icon("roadmap")}<h3>Project and product delivery</h3><p>From discovery to controlled deployment: roadmaps, vendors, migrations and adoption, delivered with Scrum and product practice.</p></div>
</div>
<p style="margin-top:28px">Organization-level engagements, including fractional AI governance, run through <a href="{FLOWHAUS}">Flowhaus.ai</a>.</p>
</div></section>

<section><div class="wrap">
<p class="eyebrow">Selected work</p>
<h2>Proof from regulated, high-stakes environments</h2>
<div class="grid two" style="margin-top:28px">{"".join(work_card(c) for c in CASES)}</div>
<p style="margin-top:24px"><a href="/work/">All case studies &rarr;</a></p>
</div></section>

<section class="band"><div class="wrap">
<p class="eyebrow">The skill mix</p>
<h2>Four disciplines, one practitioner</h2>
<p class="lede">Most governance gaps sit between disciplines. Having all four in one person means fewer handoffs and controls that survive contact with the business.</p>
<div class="grid four" style="margin-top:28px">
<div class="card">{icon("cog")}<span class="tag">Process engineering</span><h3>Six Sigma Black Belt</h3><p>Remove waste and rework before adding controls or automation.</p></div>
<div class="card">{icon("layers")}<span class="tag">AI governance</span><h3>AIGP &middot; ISO 42001 &middot; CIPM</h3><p>Frameworks, risk, privacy and operating models.</p></div>
<div class="card">{icon("board")}<span class="tag">Product delivery</span><h3>CSM &middot; CSPO</h3><p>Roadmaps, vendors and delivery to sustainable operations.</p></div>
<div class="card design">{icon("pen")}<span class="tag">Human-centered design</span><h3>M.S., HCI + Design</h3><p>Makes governance usable, so people follow it instead of working around it.</p></div>
</div>
</div></section>

<section><div class="wrap">
<div class="callout"><h3>Optimize before automate</h3><p>Start with one system or issue, tailor governance to the organization, and expand once it works. <a href="/approach/">How I work &rarr;</a></p></div>
<div class="actions" style="margin-top:32px"><a class="btn" href="{CALENDLY}">Book a discovery call</a><a class="btn ghost" href="/contact/">Send a message</a></div>
</div></section>"""
page(
    "/",
    "John Molendyk | AI governance, process and delivery",
    "AI governance consultant and founder of Flowhaus.ai. 20+ years delivering controls, process and technology in financial services, healthcare and tech.",
    home,
)

# ---------------------------------------------------------------- work
work = f"""<section class="hero" style="padding-bottom:24px"><div class="wrap">
<p class="eyebrow">Work</p>
<h1>Governance, process and delivery in practice</h1>
<p class="lede">Four projects from banking, healthcare and big tech. Each began with a control, compliance or adoption problem and ended in something the organization could run on its own.</p>
</div></section>
<section style="padding-top:24px"><div class="wrap">
<div class="grid two">{"".join(work_card(c) for c in CASES)}</div>
<p class="note" style="margin-top:28px">These are past engagements from my work at the organizations named, not Flowhaus.ai client work.</p>
</div></section>"""
page("/work/", "Work | John Molendyk", "Case studies in AI and privacy governance, document controls, migration delivery and process redesign.", work, "/work/")

# ---------------------------------------------------------------- approach
approach = f"""<section class="hero" style="padding-bottom:24px"><div class="wrap">
<p class="eyebrow">Approach</p>
<h1>Optimize before automate. Govern so teams can move faster.</h1>
<p class="lede">The principle came from a Six Sigma engagement over twenty years ago and still holds for AI: fix the process, then add the technology, and keep the controls proportionate to the risk.</p>
</div></section>
<section style="padding-top:24px"><div class="wrap">
<ol class="steps">
<li><div><h3>See what exists</h3><p>Inventory current, planned and shadow AI, and the processes and data around it. You cannot govern what you cannot see.</p></div></li>
<li><div><h3>Right-size the governance</h3><p>Assess risk and maturity, then tailor policies, roles and controls to the organization instead of importing a canned framework.</p></div></li>
<li><div><h3>Pilot on one system or issue</h3><p>Prove the approach where it is cheapest to learn. Triggers for deeper assessment are defined here, not guessed.</p></div></li>
<li><div><h3>Expand gradually</h3><p>Roll out to the next system once the pilot shows controls that integrate with existing business and technology operations.</p></div></li>
<li><div><h3>Hand it over</h3><p>Transition ownership to your people, with monitoring and documentation that make audits and regulation routine.</p></div></li>
</ol>
</div></section>
<section class="band"><div class="wrap">
<div class="grid two">
<div class="card accent">{icon("shield")}<h3>Governance as enabler</h3><p>Good governance is how teams get to say yes to AI with confidence. Lightweight, proportionate controls let adoption move faster, because people know where the lines are.</p></div>
<div class="card design">{icon("pen")}<h3>Design as a capability</h3><p>A human-centered design background shows up in the details: disclosures users understand, workflows people follow, and controls that fit how work is done.</p></div>
</div>
<p style="margin-top:28px">For fractional AI governance and focused engagements, see <a href="{FLOWHAUS}">Flowhaus.ai</a>.</p>
<div class="actions"><a class="btn" href="{CALENDLY}">Book a discovery call</a></div>
</div></section>"""
page("/approach/", "Approach | John Molendyk", "Optimize before automate: a pilot-first, right-sized approach to AI governance and delivery.", approach, "/approach/")

# ---------------------------------------------------------------- about
about = f"""<section class="hero" style="padding-bottom:24px"><div class="wrap">
<p class="eyebrow">About</p>
<h1>Governance by someone who has built and run the systems</h1>
</div></section>
<section style="padding-top:24px"><div class="wrap"><div class="prose">
<p>I'm an independent AI governance consultant and the founder of <a href="{FLOWHAUS}">Flowhaus.ai</a>. For more than twenty years I have moved loosely defined business problems from discovery to controlled deployment and sustainable operations, working as a developer, business analyst, project manager, product owner and researcher in financial services, healthcare and technology.</p>
<p>That history is why I approach AI governance as an operating problem: audits, vendors, migrations, regulatory responses and rules-based decision systems all taught me what makes controls stick. Most recently I was a Senior UX Researcher at Meta, partnering with Privacy, Legal and Compliance on AI and voice features.</p>

<h2>Credentials</h2>
<ul>
<li>AIGP, Artificial Intelligence Governance Professional</li>
<li>ISO/IEC 42001 Lead Implementer (BSI)</li>
<li>CIPM, Certified Information Privacy Manager</li>
<li>Six Sigma Black Belt</li>
<li>Certified ScrumMaster (CSM) and Certified Scrum Product Owner (CSPO)</li>
<li>M.S., Human-Computer Interaction &amp; Design, University of California, Irvine</li>
<li>B.A., Organizational Leadership</li>
</ul>

<h2>Experience</h2>
<ul>
<li><strong>Flowhaus.ai</strong>, Principal Consultant, AI Governance &amp; Advisory (2023&ndash;present)</li>
<li><strong>Meta / Reality Labs</strong>, Senior UX Researcher, AI / Voice (2021&ndash;2023)</li>
<li><strong>Union Bank</strong>, Senior Consultant, Document Governance (2017&ndash;2018)</li>
<li><strong>Alliance Healthcare Services</strong>, Technical Product Owner (2015&ndash;2017)</li>
<li><strong>Plaza Home Mortgage</strong>, Program Manager / LOS Product Owner (2012&ndash;2015)</li>
<li><strong>Wells Fargo / Wachovia</strong>, Senior Consultant / Product Owner (2010&ndash;2011)</li>
<li>Earlier: New Century Mortgage, H&amp;R Block, Lender Processing Services and others across mortgage and healthcare</li>
</ul>

<h2>Hands-on skills</h2>
<p>Python, SQL, JavaScript, HTML/CSS and APIs; research and design methods; data analysis and visualization; vendor management and roadmapping.</p>

<div class="actions"><a class="btn" href="{CALENDLY}">Book a discovery call</a><a class="btn ghost" href="{LINKEDIN}">LinkedIn</a></div>
</div></div></section>"""
page("/about/", "About | John Molendyk", "AI governance consultant, founder of Flowhaus.ai, with 20+ years delivering process and technology in regulated industries.", about, "/about/")

# ---------------------------------------------------------------- contact
contact = f"""<section class="hero" style="padding-bottom:24px"><div class="wrap">
<p class="eyebrow">Contact</p>
<h1>Let's talk about your project</h1>
<p class="lede">The quickest path is a 30-minute discovery call. Or send a note below and I will reply. I work remotely and on-site in or near Orange County, California.</p>
<div class="actions"><a class="btn" href="{CALENDLY}">Book a discovery call</a><a class="btn ghost" href="{LINKEDIN}">Connect on LinkedIn</a></div>
</div></section>
<section style="padding-top:24px"><div class="wrap">
<form action="https://api.web3forms.com/submit" method="POST">
<input type="hidden" name="access_key" value="{FORM_KEY}">
<input type="hidden" name="subject" value="Message from johnmolendyk.com">
<input type="checkbox" name="botcheck" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">
<label>Name<input type="text" name="name" required autocomplete="name"></label>
<label>Email<input type="email" name="email" required autocomplete="email"></label>
<label>Message<textarea name="message" required></textarea></label>
<button class="btn" type="submit">Send message</button>
</form>
<p class="note" style="margin-top:24px">Looking for organization-level AI governance? Start at <a href="{FLOWHAUS}">Flowhaus.ai</a>.</p>
</div></section>"""
page("/contact/", "Contact | John Molendyk", "Book a discovery call or send a message.", contact, "/contact/")

# ---------------------------------------------------------------- 404 and redirects of old Webflow URLs
page("/404.html", "Page not found | John Molendyk", "Page not found.",
     '<section class="hero"><div class="wrap"><h1>Page not found</h1><p class="lede">That page has moved or does not exist.</p><div class="actions"><a class="btn" href="/">Home</a><a class="btn ghost" href="/work/">Work</a></div></div></section>')

REDIRECTS = {
    "/qualtrics-api/": "/work/healthcare-feedback-platform/",
    "/offline-authorization/": "/work/wealth-migration-continuity/",
    "/doc-respository/": "/work/mortgage-document-governance/",
    "/meta-quest-ai/": "/work/ai-voice-privacy-research/",
    "/about-me/": "/about/",
}
for old, new in REDIRECTS.items():
    write(old, f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Redirecting&hellip;</title>
<link rel="canonical" href="{SITE}{new}"><meta http-equiv="refresh" content="0; url={new}"><meta name="robots" content="noindex">
</head><body><p>This page has moved to <a href="{new}">{new}</a>.</p></body></html>
""")

# ---------------------------------------------------------------- site files
urls = ["/", "/work/", "/approach/", "/about/", "/contact/"] + ["/work/%s/" % c["slug"] for c in CASES]
write("/sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
      + "".join("<url><loc>%s%s</loc></url>\n" % (SITE, u) for u in urls) + "</urlset>\n")
write("/robots.txt", "User-agent: *\nAllow: /\nSitemap: %s/sitemap.xml\n" % SITE)
write("/CNAME", "johnmolendyk.com\n")
write("/.nojekyll", "")
print("built", len(urls) + len(REDIRECTS) + 1, "pages into", OUT)
