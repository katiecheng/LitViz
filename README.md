LITVIZ
======

A dynamic search and visualization tool for scientific research literature

Overview
-----------

When first entering a new area of academic study, newcomers often find that barriers to entry are quite high. A learner must quickly grasp – which literature is important to read? How has the field of research evolved over time? What is the scientific discourse among prominent authors in the domain?

LIT VIZ caters to these needs by presenting users with clear visualizations and responsive interactions. A user can input the title (or authors, or keywords) of a research paper that catches their interest, and the app will recursively search references to and from the selected paper to create a dynamic visualization of the historical literature from which this paper has grown, and the relevant “children” publications that have since been put to print. At a glance, users can immediately grasp how publications are linked, which have high impact, and how research topics have progressed with time. LIT VIZ aims to help users navigate a dense web of literature in a novel and intuitive way.


Technology Stack
-----------
- Python (Flask, SQLAlchemy, PyQuery, PDFMiner)
- PostgreSQL
- Jinja2
- Bash
- HTML/CSS
- JavaScript (jQuery, D3.js)




__Data Flow Diagram__:
![Alt text](/static/img/appflow.jpeg)


__Data Model Diagram__:
![Alt text](/static/img/datamodel.jpeg)
