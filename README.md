# 🕸️ Scrapify

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/YonaniCodes/Scrapify/blob/main/notebooks/scrapify-demo.ipynb)

Scrapify is a lightweight and customizable Python web scraper for collecting data from websites with minimal setup. Ideal for quick scraping tasks, educational purposes, and rapid prototyping.

---

## 🚀 Features

- 🔍 Extract text, links, or custom elements from any public webpage
- 🧩 Easily extensible with custom parsing logic
- ✅ Works on Google Colab or locally
- 💾 Export scraped data to JSON

---

## 📦 Project Structure

## 📁 `notebooks/`

This folder contains Jupyter or Google Colab notebooks that:

- Demonstrate how to use the scraper
- Help debug or test the scraper in real time
- Serve as interactive tutorials

> ⚠️ These notebooks should **import from `src/`**, not contain the full logic themselves.

---

## 📁 `src/`

This is where your actual code lives. It should include:

- `scrapify.py`: your main scraper functions (modular, reusable)
- (Optional) `utils.py`: helper functions like `clean_text()`, `fetch_html()`
- (Optional) `parsers/`: separate logic for parsing different types of pages

> 🎯 Keeping logic in `src/` means your code can be easily tested, reused, and extended.

## Contributing

We welcome contributions from the community! To contribute:

1. Fork the repository.
2. Clone your forked repository to your local machine.
3. Create a new branch to work on your changes.
4. Make your changes and test them.
5. Push your changes to your forked repository.
6. Create a pull request describing the changes.
