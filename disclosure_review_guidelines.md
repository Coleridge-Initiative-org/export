# Disclosure Review Guidelines

This document contains all information regarding specific disclosure review guidelines
either imposed by the Coleridge Initiative or the data provider.

## Default

Every group needs to have at least 10 individuals (or entities)
- This includes:
  - Histogram bins
  - Dummy counts
  - Any numerical statistic
  - Scatterplots

No mean, median, quantiles
- This also pertains to boxplots
  - Solution: Use fuzzy quantiles

No code comments/code that reference specific data points


## Specific Agencies

Some agencies have their own guidelines for exporting statistics and visualizations
that we follow. The following guidelines replace the associated ones in the Default
section, but those not mentioned in the agency-specific sections are still required
for disclosure review.

Ex. No mean, median, quantiles for IRI data

### IRI (ERS - USDA)

Cannot release any unweighted data

Must have at least counts of at least three (unweighted) for any statistic or visualization you
wish to export of:
- Households
- Products
- Stores
- Brands
- Manufacturers

Must not have one that constitutes a share of at least 80% of the following:
- Product
- Store
- Brand
- Manufacturer


### NCSES-NSF

- Statistics and visualizations must also be based on at least 3 unique data points
at an institution level

### OLDA (OSU)

- Have to check for firm dominance (more than 80% of employees come from no more than 3 firms) if reporting on firm-based statistics.
