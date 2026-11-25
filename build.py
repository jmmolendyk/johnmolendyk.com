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

# Set True when the Lab entries have real content: adds Lab to the nav, footer and sitemap and lets search engines index it.
SHOW_LAB = True

NAV = [("/work/", "Work")] + ([("/lab/", "Lab")] if SHOW_LAB else []) + [("/approach/", "Approach"), ("/about/", "About"), ("/contact/", "Contact")]



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
    "person": [("circle-f", (11, 10.5, 4.4), W), ("path-f", "M3.5 27.5 C3.5 20.5 7 17.5 11 17.5 C15 17.5 18.5 20.5 18.5 27.5 Z", W),
               ("path-s", "M21.5 9 H29 M21.5 15 H29 M21.5 21 H29", W, .85, 1.8), ("circle-f", (25.5, 15, 2.5), A)],
    "people": [("circle-f", (7.5, 12.5, 3.2), W, .7), ("path-f", "M1.5 27 C1.5 21 4 18.5 7.5 18.5 C9.5 18.5 11 19.2 12 20.4 L12 27 Z", W, .7),
               ("circle-f", (24.5, 12.5, 3.2), W, .7), ("path-f", "M30.5 27 C30.5 21 28 18.5 24.5 18.5 C22.5 18.5 21 19.2 20 20.4 L20 27 Z", W, .7),
               ("circle-f", (16, 10.5, 4.6), A), ("path-f", "M7.5 29 C7.5 22 11 18.2 16 18.2 C21 18.2 24.5 22 24.5 29 Z", W)],
    "pen": [("path-s", "M8 7.5 L6 25 M24 7.5 L26 25", W, .6, 1.3),
            ("path-s", "M6 25 C7 9 25 9 26 25", W, 1, 2.8),
            ("rect", (3.9, 23, 4.2, 4.2), W), ("rect", (23.9, 23, 4.2, 4.2), W),
            ("circle-f", (8, 7.5, 2.4), A), ("circle-f", (24, 7.5, 2.4), A)],
}


def icon(name, cls=""):
    shapes = GLYPHS[name]
    body = "".join(_shape(s, True) for s in shapes) + "".join(_shape(s) for s in shapes)
    return '<span class="icon %s" aria-hidden="true"><svg viewBox="0 0 32 32" width="35" height="35">%s</svg></span>' % (cls, body)


def page(path, title, desc, body, current=""):
    nav = "".join(
        '<a href="%s"%s>%s</a>' % (h, ' aria-current="page"' if h == current else "", t) for h, t in NAV
    )
    lab_link = '<a href="/lab/">Lab</a>' if SHOW_LAB else ""
    noindex = '<meta name="robots" content="noindex">\n' if path.startswith("/lab/") and not SHOW_LAB else ""
    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#ffffff">
{noindex}<link rel="canonical" href="{SITE}{path}">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{SITE}{path}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<link rel="stylesheet" href="/assets/style.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header"><div class="wrap">
<a class="brand" href="/">John Molendyk</a>
<nav class="nav" aria-label="Main">{nav}<a class="nav-cta" href="{FLOWHAUS}" target="_blank" rel="noopener">Flowhaus.ai &#8599;</a></nav>
</div></header>
<main id="main">
{body}
</main>
<footer class="site-footer"><div class="wrap">
<div>&copy; 2026 John Molendyk</div>
<div class="foot-links"><a href="/work/">Work</a>{lab_link}<a href="/approach/">Approach</a><a href="/about/">About</a><a href="/contact/">Contact</a><a href="{LINKEDIN}">LinkedIn</a><a href="{FLOWHAUS}" target="_blank" rel="noopener">Flowhaus.ai</a></div>
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
        "tags": [("Governance", ""), ("Process", ""), ("Human-Centered", "d")],
        "card_stat": "<5 months",
        "card_stat_note": "delivered against an 18-month IT estimate",
        "summary": "Alongside a loan origination system (LOS) document compliance API implementation, I led the work to identify a controlled library of mortgage documentation. I implemented an IT-approved no-code solution with role-based access and basic mortgage scenarios to support audit functions. The application supported version control and let Operations view documents within their scope.",
        "stats": [
            ("<5 months", "against an 18-month IT estimate"),
            ("5,000+", "records audited and rationalized"),
            ("100%", "of in-scope documents validated and versioned"),
        ],
        "sections": [
            ("The situation",
             "<p>Audit findings highlighted an opportunity to bring more consistency to how mortgage documents were managed. Documents were stored across inboxes, personal drives and shared locations, which made it harder to confirm which version was current for a given state and loan type, and finding the right one often relied on experienced staff.</p>"),
            ("My role",
             "<p>I investigated the findings, led the cross-functional work with Operations, Legal and Compliance, and owned research, design and project delivery. I built the solution to enterprise IT standards and handed administration and development capability to internal teams so the bank could own it afterward.</p>"),
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
        "short": "Offline account balances",
        "title": "Maintaining wealth-management account balances offline through three migration weekends",
        "client": "Wells Fargo / Wachovia, wealth management",
        "years": "2010–2011",
        "role": "Senior Consultant / Product Owner",
        "tags": [("Delivery", ""), ("Governance", ""), ("Human-Centered", "d")],
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
             "<ul><li><strong>Set goals up front:</strong> accurate real-time balances to prevent overdrafts, minimal disruption for personal bankers, fraud prevention, and compliance with privacy, security and regulatory standards.</li>"
             "<li><strong>Discovered the real process.</strong> Interviews and surveys with personal bankers (who represented client needs), a journey map of migration pain points, current-state flows of compliance steps and business rules for wires, withdrawals and deposits, and analysis of past transactions and escalations.</li>"
             "<li><strong>Led design and development of an internal application</strong> for withdrawals and deposits against live balances, impacted-account lookup, and transaction review with the ability to pause updates.</li></ul>"),
            ("Outcome",
             "<p>The three weekends delivered no financial losses and no customer-reported disruption. Accounts were balanced with wire transactions at the end of every weekend, and surveys and interviews after the first weekend found the application worked well, with no findings that required changes. Personal bankers rated the experience 9.5.</p>"),
        ],
        "design": "The application was designed from current-state flows and tested with the bankers who would use it under weekend pressure. In a high-risk event, a tool that people can use correctly the first time is itself a control.",
    },
    {
        "slug": "healthcare-feedback-platform",
        "logo": ("alliance-healthcare", "Alliance Healthcare Services"),
        "short": "Digitizing customer feedback",
        "title": "Digitizing the customer experience: from mailed paper surveys to a scalable feedback platform",
        "client": "Alliance Healthcare Services",
        "years": "2015–2017",
        "role": "Technical Product Owner / Lead Product Designer",
        "tags": [("Process", ""), ("Delivery", ""), ("Human-Centered", "d")],
        "card_stat": "1,000+",
        "card_stat_note": "provider sites digitized for near real-time feedback",
        "summary": "Customer feedback depended on a 53-question paper survey mailed after the appointment, and the requests inside it moved through spreadsheets and email. We digitized it: a customer experience platform built on the Qualtrics API and Salesforce data, giving teams near real-time access to feedback.",
        "stats": [
            ("1,000+", "provider sites with branded digital surveys"),
            ("64%", "less time to log and manage each request"),
            ("100%", "of contact requests routed to operations within 24 hours"),
            ("86%", "of requests answered within 48 hours"),
        ],
        "sections": [
            ("The situation",
             "<p>A 53-question paper survey was mailed to participants after their appointment and arrived up to two weeks after service. Research found that over 70% of contact requests went unaddressed, lost to illegibility or timing. Teams tracked requests across email, spreadsheets and phone calls, staff spent up to 18 minutes logging a single request across several systems, and there was no scalable way to manage branding or devices for 1,000+ sites. The inconsistency also created compliance risk.</p>"),
            ("My role",
             "<p>As interim Product Owner across 15+ applications, I led the digital transformation, working with engineering, sales and operations through a phased approach.</p>"),
            ("What I did",
             "<ul><li><strong>Mapped before building.</strong> Interviews and shadowing across sales, customer experience and regional operations, then a sitemap of the full survey lifecycle that defined roles, data sources and system responsibilities.</li>"
             "<li><strong>Digitized the survey end to end.</strong> Built the platform with an API integration to Qualtrics and Salesforce data for near real-time access to customer feedback, with hardware and training delivered to client sites and technical administration of the Qualtrics survey platform.</li>"
             "<li><strong>Piloted first.</strong> A desktop pilot for program and operations admins proved the enrollment and request flows before the tablet and phone version for field teams.</li>"
             "<li><strong>Standardized the workflow.</strong> A platform for customer communications and hardware replacement requests, with device replacement tickets and history, contact requests that minimize free text, and API-driven enrollment of clients and sites with branding and metadata. Multiple teams moved off spreadsheets and email.</li></ul>"),
            ("Outcome",
             "<p>Time to document and manage a request dropped 64%, saving 13 minutes each, and every contact request now reached operations within 24 hours of service. Sites got self-service branded surveys, and survey data was shared across CX, operations, sales and compliance.</p>"),
        ],
        "quotes": {
            0: ("John\u2019s influence, creativity and resourcefulness regularly made the difference.", "Senior Manager, Project Development (ex-United Health Group)"),
            3: ("John has a great attention to detail and a unique ability to make complex topics easy to understand.", "Senior Manager, Project Development (ex-United Health Group)"),
        },
    },
    {
        "slug": "ai-voice-privacy-research",
        "logo": ("meta", "Meta"),
        "short": "AI voice, privacy and disclosure",
        "title": "Research behind AI voice features: privacy, disclosure and adoption",
        "client": "Meta / Reality Labs",
        "years": "2021–2023",
        "role": "Senior UX Researcher, AI / Voice",
        "tags": [("Governance", ""), ("Human-Centered", "d")],
        "card_stat": "30%",
        "card_stat_note": "new voice users estimated (based on internal testing)",
        "summary": "Adopting voice-driven messaging meant a spectrum of AI features, privacy disclosures and cross-platform applications. I led research that shaped adoption and roadmap decisions across product, privacy, legal and compliance.",
        "stats": [
            ("30%", "new voice users estimated (based on internal testing)"),
            ("1/3", "of high-priority roadmap driven by novel research findings"),
        ],
        "sections": [
            ("The situation",
             "<p>Voice messaging in VR for Facebook Messenger depended on speech-to-text and AI features. As part of the foundational research team, we focused on open questions around adoption and retention of voice users. The work improved the overall user experience by focusing on feature implementation and appropriate privacy messaging in disclaimer notices.</p>"),
            ("My role",
             "<p>I led the biannual research strategy across voice, speech-to-text, AI, AR/VR and smart communication experiences, partnering with product managers, designers, engineers, data scientists, and the Privacy, Legal and Compliance teams. I also coordinated governance for studies involving AI, voice and sensitive user data.</p>"),
            ("What I did",
             "<ul><li><strong>Tested disclosure with real users.</strong> Redesigned speech-to-text disclosures so they preserved regulatory intent while increasing user trust and first-time voice adoption.</li>"
             "<li><strong>Translated research into decisions.</strong> Connected findings to quarterly KPIs, roadmap priorities and longer-term strategy, and gave stakeholders direction on privacy and legal concerns.</li>"
             "<li><strong>Paired behavior with qualitative data</strong> to establish behavior-based benchmarks.</li>"
             "<li><strong>Made the work reusable.</strong> Contributed studies to research libraries; the findings became a reference for voice-based design in AR and wearables.</li></ul>"),
            ("Outcome",
             "<p>Research informed 12 of 21 high-priority initiatives for the second half of 2022. A single UI finding the team had not previously identified increased new voice usage by an estimated 30% in internal testing. The disclosure redesign showed that disclaimer language mattered more than originally thought and could be a driver of adoption. The studies became foundational for multiple voice-based design implementations.</p>"),
        ],
    },
]
_order = ["ai-voice-privacy-research", "wealth-migration-continuity", "healthcare-feedback-platform", "mortgage-document-governance"]
CASES.sort(key=lambda c: _order.index(c["slug"]))  # Meta first, then chronological: Work page, home and prev/next
HOME_CASES = list(CASES)
for i, c in enumerate(CASES):
    c["prev"] = CASES[i - 1] if i > 0 else None
    c["next"] = CASES[i + 1] if i < len(CASES) - 1 else None


def tags_html(tags):
    return '<div class="tags">' + "".join('<span class="%s">%s</span>' % (k, t) for t, k in tags) + "</div>"


CARD_CTX = {
    "ai-voice-privacy-research": "AI and voice features",
    "wealth-migration-continuity": "Wealth management, fraud, risk and compliance",
    "healthcare-feedback-platform": "Healthcare services",
    "mortgage-document-governance": "Mortgage banking",
}


def work_card(c):
    lg, lg_alt = c["logo"]
    return f"""<a class="card work-card" href="/work/{c['slug']}/">
<div class="card-logo"><img class="logo-{lg}" src="/assets/logos/{lg}.png" alt="{lg_alt} logo"></div>
{tags_html(c['tags'])}
<h3>{c['short']}</h3>
<div class="stat">{c['card_stat']}<small>{c['card_stat_note']}</small></div>
<p class="muted">{CARD_CTX[c['slug']]}</p>
<span class="more">Read the case &rarr;</span>
</a>"""


for c in CASES:
    stats = "".join('<div class="stat-box"><b>%s</b><span>%s</span></div>' % s for s in c["stats"])
    def quote(q):
        return '<blockquote class="quote"><p>\u201c%s\u201d</p><footer>%s</footer></blockquote>' % q
    qs = c.get("quotes", {})
    secs = ""
    for idx, sec in enumerate(c["sections"]):
        if idx in qs:
            secs += quote(qs[idx])
        secs += "<h2>%s</h2>%s" % sec
    nav_prev = '<a href="/work/%s/">&larr; %s</a>' % (c["prev"]["slug"], c["prev"]["short"]) if c["prev"] else '<a href="/work/">&larr; All work</a>'
    nav_next = '<a href="/work/%s/">%s &rarr;</a>' % (c["next"]["slug"], c["next"]["short"]) if c["next"] else '<a href="/work/">All work &rarr;</a>'
    lg, lg_alt = c["logo"]
    logo = '<img class="client-logo logo-%s" src="/assets/logos/%s.png" alt="%s logo">' % (lg, lg, lg_alt)
    design_html = ('<div class="callout amber"><h3>Where design mattered</h3><p>%s</p></div>' % c["design"]) if c.get("design") else ""
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
{design_html}
<div class="case-nav">{nav_prev}{nav_next}</div>
</div></div></section>"""
    page(
        "/work/%s/" % c["slug"],
        "%s | John Molendyk" % c["title"],
        c["summary"],
        body,
        "/work/",
    )

LAB = [
    {
        "slug": "email-automation",
        "name": "Email Automation",
        "fullname": "Email Automation Router and Analysis",
        "tile": "flow",
        "blurb": "Email routing and analysis",
        "tags": ["Client project", "Automation", "Email"],
        "summary": "A deployed AI-enabled email router for a small business that classifies incoming communications, identifies the appropriate owner, and assesses sentiment, urgency and business relevance. Configurable keywords support additional filtering based on the operational needs of the business.",
        "lede": "A deployed AI-enabled email router for a small business that classifies incoming communications, identifies the appropriate owner, and assesses sentiment, urgency and business relevance. Configurable keywords support additional filtering based on the operational needs of the business.",
        "links": "Client project. Additional details available upon request.",
        "lead_svg": ("email-automation-flow", "Email flow: Gmail to Zapier to the OpenAI API, then out to Gmail labels, HubSpot and Google Sheets", "Connected tools: Gmail, Zapier, the OpenAI API, HubSpot and Google Sheets."),
        "thumb": "thumb-email",
        "body": """<h2>What it is</h2>
<p>An email router that classifies each incoming message for sentiment, importance, urgency and topic, then sorts it so the right things surface at the right time. Zapier connects Gmail to the OpenAI API for analysis. Keywords update Gmail so messages are labeled and filtered, and the results are pushed to HubSpot and Google Sheets.</p>
<h2>Who it&rsquo;s for</h2>
<p>A small business owner who helps design and build high-end motorcycles and travels to multiple destinations throughout the year, staying for weeks and up to a month at a time. While on site, they need to stay focused on the work in front of them, with urgent items reaching them right away and everything else waiting until its time.</p>
<h2>How it works</h2>
<ol>
<li><strong>Email arrives.</strong> Zapier picks up each new message in Gmail.</li>
<li><strong>It&rsquo;s analyzed.</strong> The OpenAI API classifies sentiment, importance, urgency and topic.</li>
<li><strong>It&rsquo;s routed.</strong> Keywords update Gmail so messages are labeled and filtered, and urgent items stand out.</li>
<li><strong>It&rsquo;s recorded.</strong> Data is pushed to HubSpot and Google Sheets.</li>
</ol>
<h2>Result</h2>
<p>Email intake is low volume, at 50 to 100 messages a month, but the system lets my client focus on what they do best without worrying that something is being missed.</p>""",
    },
    {
        "slug": "insights",
        "thumb": "thumb-insight",
        "blurb": "AI governance research platform",
        "name": "Insight",
        "tags": ["Personal build", "AI governance", "Articles", "Knowledge center"],
        "summary": "An AI-powered research platform that collects, organizes and synthesizes news and articles about AI governance, helping turn a rapidly changing information landscape into actionable insights.",
        "what": "[Placeholder] Describe the app: a collection of AI governance articles presented under the Insights name. What can a visitor do with it?",
        "why": "[Placeholder] Why you built it and the gap it fills.",
        "how": "[Placeholder] How it was built: tools, the role AI played, what you decided versus what the AI drafted.",
        "links": "Personal project. Demonstration and additional details available upon request.",
        "lede": "An AI-powered news and research platform designed to make it easier to follow developments in AI governance, understand emerging trends and turn information into informed perspectives.",
        "stat": "2,500+ articles from 200+ active sources",
        "lead_img": ("insight-briefing", "Insight Daily Briefing: top stories, collection routes and source counts", "Daily Briefing"),
        "body": """<h2>What it is</h2>
<p>Insight collects articles and organizes them into common-sense themes. It highlights specific sources and brings forward the articles most relevant to what I&rsquo;m working on now.</p>
<p>A daily briefing gives me a quick snapshot, where I can expand the categories I care about and collapse the rest.</p>
<p>I can search the full library of collected articles and, from within any article, start developing ideas for my own writing while the tool surfaces other articles and sources worth considering.</p>
<p>I can also manage my sources and create new categories for the article taxonomy.</p>
<figure class="shot"><img src="/assets/lab/insight-library.jpg" alt="Insight Library: collected articles organized by governance category, with search and filters" loading="lazy"><figcaption>Library: every collected article, organized by governance category.</figcaption></figure>
<figure class="shot"><img src="/assets/lab/insight-writing.jpg" alt="Insight Writing ideas: start from a perspective to test and build a research brief" loading="lazy"><figcaption>Writing ideas: start with a perspective to test and build a research brief from the evidence.</figcaption></figure>
<h2>Why I built it</h2>
<p>Staying current in a field as fast-moving as AI governance is nearly impossible, and the pace keeps increasing. New threats, technologies, solutions, regulations, standards and practices emerge constantly across multiple disciplines.</p>
<p>I built Insight to keep me focused on information from core sources on a regular basis, while exposing me to new sources without inundating me.</p>
<p>It goes beyond a list of bookmarks or a spreadsheet. AI parses newsletters and traverses my sources for me, so I get a consolidated perspective quickly and know there is one place where the material I care about most lives.</p>
<p>I can add individual articles or sources, or drop in a newsletter and have the articles and new sources collected. I can also see how each source performs and decide whether it is meeting my needs or should be removed.</p>
<h2>Approach</h2>
<p>Insight was developed through an iterative, AI-assisted process. I defined the product requirements, information architecture, taxonomy, collection workflow and editorial experience, and used AI coding tools to help implement and refine the application.</p>
<p>The design emphasizes source quality, relevance and traceability. Rather than treating AI-generated summaries as authoritative, the platform supports research and judgment while preserving access to the original sources.</p>
<p>The project continues to evolve as I explore more effective ways to use AI for information management, research and content development.</p>
<h2>Planned updates</h2>
<h3>Quality review and update</h3>
<p>Now that I have collected enough articles and sources, I&rsquo;ll work with AI to assess the quality of both. Some of the early collection was incomplete, though the articles themselves are relevant, so rebuilding the content around each article is key to keeping it searchable and relevant.</p>
<h3>Personalization</h3>
<p>I want to tell Insight what I&rsquo;m currently working on and focused on, so my daily briefing is as relevant as possible.</p>
<h3>Diverse storage</h3>
<p>A home for white papers, frameworks, standards and other knowledge beyond articles that I want considered in my own writing. That includes documents I create myself and my own published articles, kept for reference in future work.</p>
<h3>Writing center</h3>
<p>Grounding with RAG in my voice and writing style, so suggested drafts start closer to how I write. I also plan more control over article creation: length, variability, topics, number of sources, number and placement of quotes, citations in a couple of useful formats, and multiple versions when needed.</p>""",
    },
    {
        "slug": "ai-register",
        "thumb": "thumb-agent-register",
        "blurb": "AI agent governance workspace",
        "name": "Agent Register",
        "tags": ["Personal build", "AI governance", "Workspace"],
        "summary": "An AI governance prototype that helps teams describe their agents, establish ownership and give reviewers a clearer picture of how AI is being used across an organization.",
        "lede": "An AI governance prototype that helps teams describe their agents, establish ownership and give reviewers a clearer picture of how AI is being used across an organization.",
        "links": "Personal project under active development. A populated demonstration and walkthrough are available upon request. Feedback from governance professionals, business owners and technical teams is welcome.",
        "lead_img": ("ai-register-overview", "Agent Register governance view: agents organized by department with review status counts", "Organizational oversight: explore agent ownership by department and team, then drill into individual agents and their review status."),
        "body": """<h2>What it is</h2>
<p>Agent Register brings business context and technical implementation into a shared governance workflow. Submitters begin with a simple user story: who will use the agent, what it will help them accomplish and why that outcome matters.</p>
<p>The intake then explores the platform, data sources, actions and human oversight involved. Questions adapt to how the agent is being built, allowing business teams to explain its purpose and technical owners to document its implementation.</p>
<p>The governance view organizes agents by department and business owner, with drill-downs into teams, submission statuses and individual records. Reviewers can identify missing information, request changes and record decisions. Indicators such as external data sharing, write access and human approval requirements help focus attention without assigning an automatic risk rating.</p>
<figure class="shot"><img src="/assets/lab/ai-register-drilldown.jpg" alt="Agent Register Finance drill-down showing subgroups, agents and submission statuses" loading="lazy"><figcaption>Drill-down: a department&rsquo;s subgroups, agents and submission statuses.</figcaption></figure>
<figure class="shot"><img src="/assets/lab/ai-register-review.jpg" alt="Agent Register review screen with platform and ownership details, review indicators and approval controls" loading="lazy"><figcaption>Informed review: examine data access, permitted actions and human approval requirements alongside technical details and governance decisions.</figcaption></figure>
<h2>Why I built it</h2>
<p>I built Agent Register to explore how governance can become part of the way teams create and deploy AI.</p>
<p>A useful review starts with a shared understanding of purpose, ownership, data and authority. Business users should be able to explain what they need in familiar language. Technical teams should be able to supply implementation details without asking the business owner to guess.</p>
<p>This project turns that idea into a working prototype. It gives me a practical way to test intake questions, review workflows and organizational views, and to explore how governance can provide useful guidance as AI adoption grows.</p>
<h2>How it was built</h2>
<p>I developed the prototype iteratively with AI-assisted coding. I defined the governance questions, ownership structure and review workflow, then used AI to help implement the interface, conditional forms and supporting logic. Each iteration added a specific capability, from user-story intake to technical review and departmental drill-downs.</p>
<p>The application uses HTML, CSS and JavaScript and is hosted as a private site. Records currently persist in the user&rsquo;s browser. The demonstration workspace contains 16 fictional agents across four departments, stored separately from other workspace records.</p>
<p>It is a working prototype for testing and feedback. Shared storage, authenticated roles and a production audit trail remain future work.</p>""",
    },
    {
        "slug": "personal-kanban",
        "thumb": "thumb-kanban",
        "blurb": "Personal planning tool",
        "name": "Personal Kanban Board",
        "tags": ["Personal build", "Productivity"],
        "summary": "A personal planning application I designed and built using AI-assisted development. It connects everyday tasks to personal values and priorities, exploring how thoughtful interface design can reduce cognitive load and support intentional action.",
        "lede": "A personal planning application I designed and built using AI-assisted development. It connects everyday tasks to personal values and priorities, exploring how thoughtful interface design can reduce cognitive load and support intentional action.",
        "links": "Personal project. Demonstration and additional details available upon request.",
        "lead_img": ("kanban-today", "Personal Kanban Board Today view showing a focused selection of five tasks from all three areas", "Today: a focused selection of tasks drawn from all three areas, retaining their categories and workflow status.", 785),
        "body": """<h2>What it is</h2>
<p>The board brings Personal, Professional and Home tasks into one view, with work moving through Backlog, Ready, In progress and Done. A separate Today view lets me choose a manageable set of tasks from any area without losing their place on the full board.</p>
<p>Each area has an editable values statement. Tasks can include notes, a definition of done and one small next step. A &ldquo;Needs clarity&rdquo; flag marks work that needs more thought or exploration before I know how to approach it. The board is available on my Mac and iPad, with tasks saved online.</p>
<figure class="shot" style="width:785px;max-width:calc(100vw - 48px)"><img src="/assets/lab/kanban-board.jpg" alt="Personal Kanban Board full board view: Personal, Professional and Home rows with Backlog, Ready, In progress and Done columns" loading="lazy"><figcaption>Full board: twelve cells organize Personal, Professional and Home tasks by status. Values statements connect each area to a broader intention, while &ldquo;Needs clarity&rdquo; flags identify tasks that need exploration.</figcaption></figure>
<p class="note">Both screenshots use fictitious demonstration tasks and the quote &ldquo;As I think, so I feel. As I feel, so I do. As I do, so I become.&rdquo;</p>
<h2>Why I built it</h2>
<p>I wanted a way to plan my day that recognized the relationship between my own needs, my work and my home. Personal comes first deliberately: taking care of myself helps me show up in the other areas of my life.</p>
<p>I also wanted to make unfamiliar work easier to approach. Naming what I don&rsquo;t yet understand, describing what done looks like and finding one small next step give me a practical way to move forward. The values statements and rotating quotes keep those daily choices connected to longer-term intentions.</p>
<h2>How it was built</h2>
<p>I directed the design and development through an iterative collaboration with ChatGPT and Codex. I defined the workflow, priorities, interactions and visual direction, and AI drafted and revised the implementation. Using the board between iterations helped me decide what to improve next.</p>
<p>The application uses React and TypeScript, with a Cloudflare Worker and D1 database for persistent storage, hosted through ChatGPT Sites. It includes responsive layouts, Calm and Energy themes, editable values and a personal quote collection. The current Calm palette draws from a watercolor my sister painted, with a frog and reed adapted into a floating illustration.</p>""",
    },
]

def thumb_html(e):
    if e.get("thumb"):
        return '<div class="card-thumb"><img src="/assets/lab/%s.jpg" alt="" loading="lazy"></div>' % e["thumb"]
    return '<div class="card-thumb tile">%s</div>' % icon(e["tile"])


lab_mini = "".join(
    f"""<a class="lab-mini" href="/lab/{e['slug']}/">
{thumb_html(e)}
<h3>{e['name']}</h3>
<p class="muted">{e['blurb']}</p>
</a>"""
    for e in LAB
)

# ---------------------------------------------------------------- home
home = f"""<section class="hero"><div class="wrap">
<p class="eyebrow">AI enablement &middot; process &middot; governance &middot; delivery</p>
<h1>I help teams make AI work, responsibly from day one.</h1>
<p class="lede">Twenty years of delivering technology and process within financial services, healthcare and big tech. I help organizations adopt AI in a sustainable and responsible way.</p>
<div class="actions"><a class="btn" href="{CALENDLY}">Book a discovery call</a><a class="btn ghost" href="/work/">See the work</a></div>
</div></section>

<section class="proof" aria-label="Experience"><div class="wrap">
<p class="proof-label">Where I&rsquo;ve been</p>
<ul class="proof-logos">
<li><img class="client-logo logo-meta" src="/assets/logos/meta.png" alt="Meta"></li>
<li><img class="client-logo logo-wells-fargo" src="/assets/logos/wells-fargo.png" alt="Wells Fargo"></li>
<li><img class="client-logo logo-union-bank" src="/assets/logos/union-bank.png" alt="Union Bank"></li>
<li><img class="client-logo logo-alliance-healthcare" src="/assets/logos/alliance-healthcare.png" alt="Alliance Healthcare Services"></li>
<li><img class="client-logo logo-b-braun" src="/assets/logos/b-braun.png" alt="B. Braun Medical"></li>
</ul>
<ul class="proof-industries"><li>Financial services</li><li>Mortgage</li><li>Healthcare</li><li>Medical devices</li><li>Technology</li></ul>
</div></section>

<section class="band"><div class="wrap">
<p class="eyebrow">What I do</p>
<h2>Enabling AI, responsibly from the start</h2>
<p class="lede">Putting AI to work safely takes organizational change: process, clear roles and decision rights, training, monitoring and ownership that your team can sustain.</p>
<figure class="model">
<ol class="model-steps">
<li class="mstep"><span class="mnum">01</span><div class="mart"><img src="/assets/step-process.png" alt="" width="270" height="122"></div><h3>Process Design</h3><p class="mkick">Integrate AI</p><p>Fix the process first, then build AI into workflows with clear roles, decisions and handoffs.</p><span class="mchip">Six Sigma Black Belt</span></li>
<li class="marrow" aria-hidden="true">&rarr;</li>
<li class="mstep center"><span class="mnum">02</span><div class="mart"><img src="/assets/step-human.png" alt="" width="265" height="149"></div><h3>Human-Centered</h3><p class="mkick">Enable oversight</p><p>Give people the tools, information and controls to oversee AI, and design governance they will actually follow.</p><span class="mchip">M.S. HCI + Design</span></li>
<li class="marrow" aria-hidden="true">&rarr;</li>
<li class="mstep"><span class="mnum">03</span><div class="mart"><img src="/assets/step-delivery.png" alt="" width="298" height="128"></div><h3>Product Delivery</h3><p class="mkick">Execute reliably</p><p>Take it from discovery to controlled deployment: roadmaps, vendors, migrations and adoption.</p><span class="mchip">CSM &middot; CSPO</span></li>
</ol>
<div class="mloop" aria-hidden="true"><span class="up"></span><span class="label">Continuous learning</span><span class="down"></span></div>
<div class="mbase"><div class="mpanel" aria-hidden="true"><svg viewBox="0 0 340 150" role="presentation">
<defs>
<linearGradient id="gv" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f7f9fd"/><stop offset="1" stop-color="#c7d4e7"/></linearGradient>
<linearGradient id="ga" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffd988"/><stop offset="1" stop-color="#f0a014"/></linearGradient>
<filter id="gb" x="-20%" y="-100%" width="140%" height="300%"><feGaussianBlur stdDeviation="5"/></filter>
</defs>
<ellipse cx="170" cy="138" rx="150" ry="8" fill="#17355f" opacity=".22" filter="url(#gb)"/>
<g stroke="#17355f" stroke-width="2.6" stroke-linejoin="round" stroke-linecap="round">
<rect x="20" y="100" width="80" height="28" rx="6" fill="url(#gv)"/><rect x="106" y="100" width="80" height="28" rx="6" fill="url(#gv)"/><rect x="192" y="100" width="80" height="28" rx="6" fill="url(#gv)"/>
<rect x="63" y="70" width="80" height="28" rx="6" fill="url(#gv)"/><rect x="149" y="70" width="80" height="28" rx="6" fill="url(#gv)"/>
<rect x="106" y="40" width="80" height="28" rx="6" fill="url(#ga)"/>
<path d="M304 66 L329 76 V98 C329 114 318 123 304 129 C290 123 279 114 279 98 V76 Z" fill="url(#gv)"/>
<path d="M293 97 L301 105 L317 86" fill="none" stroke="#f2a516" stroke-width="5.5"/>
</g>
<g stroke="#ffffff" stroke-width="2" stroke-linecap="round" opacity=".85"><path d="M28 105 H92 M114 105 H178 M200 105 H264 M71 75 H135 M157 75 H221 M114 45 H178" /></g>
</svg></div><div><h3>AI Governance <span>The foundation</span></h3><p>Establish the principles, accountability and guardrails for safe, ethical, responsible AI, owned by your team.</p><div class="mchips"><span class="mchip">AIGP</span><span class="mchip">ISO 42001 Lead Implementer</span><span class="mchip">CIPM</span></div></div></div>
</figure>
<div class="glue">
<h3>One voice across the whole organization</h3>
<p>AI adoption stalls in the gaps between teams. I work in those gaps, translating between functions so decisions get made with clarity and transparency.</p>
<ul class="glue-row"><li>Leadership</li><li>Legal</li><li>Compliance</li><li>IT</li><li>Business units</li></ul>
<div class="glue-bar" aria-hidden="true"></div>
<span class="glue-pill">One voice</span>
<blockquote class="quote glue-quote"><p>\u201cJohn has a great attention to detail and a unique ability to make complex topics easy to understand.\u201d</p><footer>Senior Manager, Project Development (ex-United Health Group), on the healthcare feedback platform</footer></blockquote>
</div>
<p style="margin-top:28px">Organization-level engagements, including fractional AI governance, run through <a href="{FLOWHAUS}" target="_blank" rel="noopener">Flowhaus.ai</a>.</p>
</div></section>

<section><div class="wrap">
<p class="eyebrow">Selected work</p>
<h2>Proof from regulated, high-stakes environments</h2>
<div class="grid two" style="margin-top:28px">{"".join(work_card(c) for c in HOME_CASES)}</div>
<p style="margin-top:24px"><a href="/work/">All case studies &rarr;</a></p>
</div></section>

<section class="band"><div class="wrap">
<div class="lab-strip">
<div class="lab-strip-head"><div><p class="eyebrow">From the Lab</p><h2>Apps I&rsquo;ve built with AI</h2></div><a href="/lab/">Explore the Lab &rarr;</a></div>
<div class="grid four lab-grid">{lab_mini}</div>
</div>
</div></section>

<section><div class="wrap">
<div class="callout"><h3>Optimize then automate</h3><p>Start with one system or issue, tailor governance to the organization, and expand once it works. <a href="/approach/">How I work &rarr;</a></p></div>
<div class="actions" style="margin-top:32px"><a class="btn" href="{CALENDLY}">Book a discovery call</a><a class="btn ghost" href="/contact/">Send a message</a></div>
</div></section>"""
page(
    "/",
    "John Molendyk | AI enablement, process and delivery",
    "AI enablement and governance consultant, founder of Flowhaus.ai. 20+ years delivering process, controls and technology in financial services, healthcare and tech.",
    home,
)

# ---------------------------------------------------------------- work
work = f"""<section class="hero" style="padding-bottom:24px"><div class="wrap">
<p class="eyebrow">Work</p>
<h1>Enablement, process and delivery in practice</h1>
<p class="lede">Four projects from banking, healthcare and big tech. Each began with a control, compliance or adoption problem and ended in something the organization could run on its own.</p>
</div></section>
<section style="padding-top:24px"><div class="wrap">
<div class="grid two">{"".join(work_card(c) for c in CASES)}</div>
<p class="note" style="margin-top:28px">These are past engagements from my work at the organizations named, not Flowhaus.ai client work.</p>
</div></section>"""
page("/work/", "Work | John Molendyk", "Case studies in responsible AI adoption, privacy and document controls, migration delivery and process redesign.", work, "/work/")

# ---------------------------------------------------------------- approach
approach = f"""<section class="hero" style="padding-bottom:24px"><div class="wrap">
<p class="eyebrow">Approach</p>
<h1>Optimize then automate. Build governance in so teams can move faster.</h1>
<p class="lede">The principle came from a Six Sigma engagement over twenty years ago and still holds for AI: fix the process, then add the technology, and keep controls proportionate to the risk so teams can adopt AI with confidence.</p>
</div></section>
<section style="padding-top:24px"><div class="wrap">
<ol class="steps">
<li><div><h3>Define and measure</h3><p>Start by identifying the problem or opportunity. Understand what it is, what solving it means for the business, and how we&rsquo;ll measure success once it&rsquo;s in place.</p></div></li>
<li><div><h3>Optimize, then automate</h3><p>Fix the process first, then build the solution around the new needs and the technology available, including AI. Responsibility is built in from the start.</p></div></li>
<li><div><h3>Manage and improve</h3><p>Once it&rsquo;s live, we manage it against the measures set at the start, reviewing results and making small, iterative improvements.</p></div></li>
<li><div><h3>Hand over ownership</h3><p>Transfer the solution to its owner with the tools needed to maintain ownership, including documentation, training and a clear view of how it&rsquo;s performing.</p></div></li>
</ol>
</div></section>
<section class="band"><div class="wrap">
<div class="grid two">
<div class="card accent">{icon("shield")}<h3>Governance as enabler</h3><p>Good governance is how teams say yes to AI with confidence. Lightweight, proportionate controls speed adoption because people know where the lines are.</p></div>
<div class="card design">{icon("people")}<h3>Design to support adoption</h3><p>Human-centered design drives adoption by making expectations clear to everyone: disclosures people can read, workflows that feel intuitive and controls that fit the context.</p></div>
</div>
<p style="margin-top:28px">For fractional AI governance and focused engagements, see <a href="{FLOWHAUS}" target="_blank" rel="noopener">Flowhaus.ai</a>.</p>
<div class="actions"><a class="btn" href="{CALENDLY}">Book a discovery call</a></div>
</div></section>"""
page("/approach/", "Approach | John Molendyk", "Optimize then automate: a pilot-first, adaptive approach to enabling AI adoption with governance built in.", approach, "/approach/")

# ---------------------------------------------------------------- about
about = f"""<section class="hero" style="padding-bottom:24px"><div class="wrap">
<p class="eyebrow">About</p>
<h1>Enablement from someone who has built and run the systems</h1>
</div></section>
<section style="padding-top:24px"><div class="wrap"><div class="prose">
<p>I'm an independent AI enablement and governance consultant and the founder of <a href="{FLOWHAUS}" target="_blank" rel="noopener">Flowhaus.ai</a>. For more than twenty years I have moved loosely defined business problems from discovery to controlled deployment and sustainable operations, working as a developer, business analyst, project manager, product owner and researcher in financial services, healthcare and technology.</p>
<p>That history is why I approach AI adoption as an operating problem: audits, vendors, migrations, regulatory responses and rules-based decision systems all taught me what makes controls stick and adoption last. Most recently I was a Senior UX Researcher at Meta, partnering with Privacy, Legal and Compliance on AI and voice features.</p>

<h2>Credentials</h2>
<ul>
<li>AIGP, Artificial Intelligence Governance Professional</li>
<li>ISO/IEC 42001 Lead Implementer (BSI)</li>
<li>CIPM, Certified Information Privacy Manager</li>
<li>Six Sigma Black Belt</li>
<li>Certified ScrumMaster (CSM) and Certified Scrum Product Owner (CSPO)</li>
<li>M.S., Human-Computer Interaction &amp; Design, University of California, Irvine</li>
<li>B.A., Organizational Leadership, Chapman University, Orange, CA</li>
</ul>

<h2>Experience</h2>
<ul>
<li><strong>Flowhaus.ai</strong>, Principal Consultant, AI Governance &amp; Advisory (2023&ndash;present)</li>
<li><strong>Meta / Reality Labs</strong>, Senior UX Researcher, AI / Voice (2021&ndash;2023)</li>
<li><strong>Union Bank</strong>, Senior Consultant, Document Governance (2017&ndash;2018)</li>
<li><strong>Alliance Healthcare Services</strong>, Technical Product Owner (2015&ndash;2017)</li>
<li><strong>Plaza Home Mortgage</strong>, Program Manager / LOS Product Owner (2012&ndash;2015)</li>
<li><strong>B. Braun Medical</strong>, Senior Consultant, Safety Compliance (2011&ndash;2012)</li>
<li><strong>Wells Fargo / Wachovia</strong>, Senior Consultant / Product Owner (2010&ndash;2011)</li>
<li><strong>Independent consultant</strong>, small business management consulting (2008&ndash;2021)</li>
<li>Earlier: New Century Mortgage, H&amp;R Block and Lender Processing Services</li>
</ul>

<h2>Technical fluency</h2>
<p>My technical background spans software development, data analysis, systems integration and product delivery, built through close collaboration with engineering, data science, design and other stakeholders.</p>
<p>Today I bring that experience to an AI-assisted development practice, using tools such as Codex and Claude Code to accelerate development, test ideas and improve solutions iteratively.</p>
<p>I have worked with Python, SQL, JavaScript and HTML/CSS, and with automation and low-code tools including n8n, Zapier and Microsoft Power Platform.</p>

<div class="actions"><a class="btn" href="{CALENDLY}">Book a discovery call</a><a class="btn ghost" href="{LINKEDIN}">LinkedIn</a></div>
</div></div></section>"""
page("/about/", "About | John Molendyk", "AI enablement and governance consultant, founder of Flowhaus.ai, with 20+ years delivering process and technology in regulated industries.", about, "/about/")

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
<p class="note" style="margin-top:24px">Looking for organization-level AI governance? Start at <a href="{FLOWHAUS}" target="_blank" rel="noopener">Flowhaus.ai</a>.</p>
</div></section>"""
page("/contact/", "Contact | John Molendyk", "Book a discovery call or send a message.", contact, "/contact/")


# ---------------------------------------------------------------- lab


def lab_tags(tags):
    return '<div class="tags">' + "".join("<span>%s</span>" % t for t in tags) + "</div>"


lab_cards = "".join(
    f"""<a class="card work-card" href="/lab/{e['slug']}/">
{thumb_html(e)}
<h3>{e['name']}</h3>
<p class="muted">{e['summary']}</p>
{lab_tags(e['tags'])}
<span class="more">Details &rarr;</span>
</a>"""
    for e in LAB
)
page("/lab/", "Lab | John Molendyk", "Apps built with AI and governed by design: working examples of building AI responsibly.",
     f"""<section class="hero" style="padding-bottom:24px"><div class="wrap">
<p class="eyebrow">Lab</p>
<h1>Things I build and make</h1>
<p class="lede">Current projects built with modern AI tools: support tools, governance tools and personal projects.</p>
</div></section>
<section style="padding-top:24px"><div class="wrap"><div class="grid two">{lab_cards}</div>
<div class="prose" style="margin-top:48px"><h2>Technical fluency</h2>
<p>My technical background spans software development, data analysis, systems integration and product delivery, built through close collaboration with engineering, data science, design and other stakeholders.</p>
<p>Today I bring that experience to an AI-assisted development practice, using tools such as Codex and Claude Code to accelerate development, test ideas and improve solutions iteratively.</p>
<p>I have worked with Python, SQL, JavaScript and HTML/CSS, and with automation and low-code tools including n8n, Zapier and Microsoft Power Platform.</p></div>
<p class="note" style="margin-top:28px">For organization-level engagements and resources, see <a href="{FLOWHAUS}" target="_blank" rel="noopener">Flowhaus.ai</a>.</p></div></section>""",
     "/lab/")

for e in LAB:
    if e.get("body"):
        lab_stat = '<p class="lab-stat">%s</p>' % e["stat"] if e.get("stat") else ""
        li = e.get("lead_img")
        ls = e.get("lead_svg")
        lead_html = ('<section style="padding-top:8px"><div class="wrap">\n<figure class="shot lead" style="%s"><img src="/assets/lab/%s.jpg" alt="%s"><figcaption>%s</figcaption></figure>\n</div></section>' % (("max-width:%dpx" % li[3]) if len(li) > 3 else "", li[0], li[1], li[2])) if li else ""
        if ls:
            lead_html = '<section style="padding-top:8px"><div class="wrap">\n<figure class="shot lead"><img src="/assets/lab/%s.svg" alt="%s"><figcaption>%s</figcaption></figure>\n</div></section>' % ls
        page("/lab/%s/" % e["slug"], "%s | Lab | John Molendyk" % e["name"], e["lede"],
             f"""<section class="case-head"><div class="wrap">
<p class="eyebrow">Lab</p>
<h1>{e.get('fullname', e['name'])}</h1>
<p class="lede">{e['lede']}</p>
{lab_tags(e['tags'])}
{lab_stat}
</div></section>
{lead_html}
<section style="padding-top:24px"><div class="wrap"><div class="prose">
{e['body']}
<h2>Links</h2><p>{e['links']}</p>
<div class="case-nav"><a href="/lab/">&larr; Lab</a><a href="/contact/">Questions? Get in touch &rarr;</a></div>
</div></div></section>""", "/lab/")
        continue
    shots = "".join('<div class="shot-placeholder">Screenshot placeholder %d</div>' % i for i in (1, 2))
    page("/lab/%s/" % e["slug"], "%s | Lab | John Molendyk" % e["name"], e["summary"],
         f"""<section class="case-head"><div class="wrap">
<p class="eyebrow">Lab</p>
<h1>{e['name']}</h1>
<p class="lede">{e['summary']}</p>
{lab_tags(e['tags'])}
</div></section>
<section style="padding-top:24px"><div class="wrap"><div class="prose">
<h2>What it is</h2><p>{e['what']}</p>
<h2>Why I built it</h2><p>{e['why']}</p>
<div class="grid two" style="margin:28px 0">{shots}</div>
<h2>How it was built</h2><p>{e['how']}</p>
<h2>Links</h2><p>{e['links']}</p>
<div class="case-nav"><a href="/lab/">&larr; Lab</a><a href="/contact/">Questions? Get in touch &rarr;</a></div>
</div></div></section>""",
         "/lab/")

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
if SHOW_LAB:
    urls += ["/lab/"] + ["/lab/%s/" % e["slug"] for e in LAB]
write("/sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
      + "".join("<url><loc>%s%s</loc></url>\n" % (SITE, u) for u in urls) + "</urlset>\n")
write("/robots.txt", "User-agent: *\nAllow: /\nSitemap: %s/sitemap.xml\n" % SITE)
write("/CNAME", "johnmolendyk.com\n")
write("/.nojekyll", "")
print("built", len(urls) + len(REDIRECTS) + 1, "pages into", OUT)
