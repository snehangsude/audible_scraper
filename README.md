# Audible Scraper
An [Audible.in](https://www.audible.in) webscraper to gather audiobooks data.

## Things to note about the customer scraper *(main.py)*
If you are going through the code, inside **Loop : 2** you may see a bit of handwritten customization of the code. 
That is cause of Audible redirects incorrectly under few sub-categories. Such as under any sub-category if `LGBTQ+` is present it redirects
to the `LGBTQ+` category and the category it was orginally under is ignored. 

It is recommended to check them prior to running the code as Audible.in is updated everyday.
Also, while running *Loop: 1* since it's recommended to use 3-5 pages at once instead of all as this makes sure that the program runs smoothly.

# Datset
#### You can find the dataset here: [Audiobooks Dataset](https://www.kaggle.com/datasets/snehangsude/audible-dataset)

# Data Cleaning
The Audiobooks dataset has two `.csv` files.
- audible_uncleaned.csv
- audible_cleaned.csv

If you are looking to use the uncleaned one to practice or wrangle the data based on your needs, [here's a notebook](https://snehangsude.github.io/xSpace/audible/dataa_wrangling/data_cleaning/tabular_data/2022/04/11/audible-cleaner.html)
that might help you get started. It covers from beginners to intermidiate.  

# Data Exploration
If you are rather interested to directly dive into the data and create exiciting data visulation, I've a [notebook here](https://snehangsude.github.io/xSpace/audible/data_analysis/data_visulization/tabular_data/matplotlib/seaborn/2022/04/11/audible-eda.html).
You can directly start with exploring the data, however make sure you are using the `audible_cleaned.csv` to start.