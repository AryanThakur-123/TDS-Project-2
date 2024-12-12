# Data Analysis of Goodreads Books

## Overview

This analysis examines a dataset of 10,000 books from Goodreads, allowing us to extract insights into author popularity, book ratings, and publication years. The key columns analyzed include the title of the book, authors, publication year, average rating, ratings count, and the number of reviews.

## Key Insights

### Missing Values

- Several columns have missing values, most notably:
  - **ISBN**: 700 missing
  - **ISBN13**: 585 missing
  - **Original Title**: 585 missing
  - **Language Code**: 1084 missing
  - **Publication Year**: 21 missing
- These missing values may affect the analysis, so care needs to be taken in their treatment.

### Statistical Summary

- The average rating across all books is approximately **4.00**, indicating a generally high level of positivity among users. 
- The distribution of ratings (1-5 stars) shows a significant skew towards higher ratings, which is common in user-generated content:
   - Ratings of 5 stars have a mean of approximately **23,789**.
   - Ratings of 1 star are the least frequent, with a mean of only **1,345**.

Here’s a boxplot illustrating the distribution of ratings:

```python
import matplotlib.pyplot as plt
import seaborn as sns

# Sample data to demonstrate boxplot, assuming 'ratings_data' is a DataFrame with ratings columns
ratings_data = {
    'ratings_1': [1345, 1, 2, 3, 4, ...],
    'ratings_2': [3110, 30, 35, ...,],
    'ratings_3': [11475, 323, 350, ...],
    'ratings_4': [19965, 750, 800, ...],
    'ratings_5': [23789, 2200, 2500, ...],
}

sns.boxplot(data=ratings_data)
plt.title('Boxplot of Ratings Distribution')
plt.xlabel('Rating Categories')
plt.ylabel('Number of Ratings')
plt.show()
```

### Author Popularity

- The dataset contains **4664 unique authors**, with **Stephen King being the most frequently mentioned** author, appearing **60 times**.
- This popularity suggests that certain authors dominate the list, which could skew average ratings or influence user behavior in rating.

### Publication Year Trends

- The average original publication year is approximately **1982**, with a broad distribution:
  - The earliest publication year is **1750**, and the latest is **2017**.
- This suggests that the dataset includes both classic and contemporary literature.

A histogram showing the distribution of publication years:

```python
plt.hist(dataset['original_publication_year'].dropna(), bins=20, color='skyblue', edgecolor='black')
plt.title('Distribution of Original Publication Years')
plt.xlabel('Year')
plt.ylabel('Number of Books')
plt.show()
```

### Correlation Analysis

A correlation matrix reveals the relationships between various numerical features:

- There is a **strong positive correlation (0.995)** between `ratings_count` and `work_ratings_count`, indicating that more popular books (with more ratings) also tend to get more detailed reviews.
- Conversely, `ratings_count` shows a negative correlation with `books_count` (-0.324), which could imply that books with a higher count of books available by the same author or series might receive fewer ratings per individual book.

Here's a heatmap for easier visualization of these correlations:

```python
import seaborn as sns
import matplotlib.pyplot as plt

correlation_matrix = dataset.corr()
sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap='coolwarm')
plt.title('Correlation Matrix of Ratings and Attributes')
plt.show()
```

## Conclusion

This analysis highlights interesting trends in book ratings and authorship in the Goodreads dataset, revealing insights into reader preferences and behavior. Given the high average ratings and the popularity of certain authors, readers may tend to gravitate towards well-known titles, potentially limiting the exposure of newer or lesser-known books.

Future studies could explore the impact of genre on ratings or the effect of user reviews in driving book popularity. Additionally, addressing the missing values could improve the quality of insights drawn from this dataset.