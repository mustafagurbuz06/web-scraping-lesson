# A first step in web scraping

In class, run `lesson.ipynb` from top to bottom. Each cell is one step. The last call follows every page and saves `books.csv`. Change `url`, `card`, and `fields` for another site.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

When you open the notebook, pick the Python inside `.venv` as the kernel.

The example site is [books.toscrape.com](https://books.toscrape.com/), published for scraping practice. Check that another site allows it before you run the same code there.
