#  Project: sydney-rental-tracker

Each file provides the residential rental bond lodgements for each specific month of the year. The full data is available from January 2022 to September 2026, and the list grows as each month finishes. For this specific analysis, we will work on the January 2023 to September 2026 timeframe.

## Excel file document analysis:

 1. Each table has 5 headers (Lodgement Date, Postcode, Dwelling Type, Bedrooms, Weekly Rent).
 2. **Lodgement Date** is the date that the bond was lodged with Fair Trading.
 3. **Postcode** is the postcode of the rented premises address.
 4. **Dwelling Type** is the type of rented premise as provided by the agent of the landlord. Options are: (F) Flat/unit; (H) House; (T) Terrace/townhouse/semi-detached; (O) Other; (U) Unknown.
 5. **Bedrooms** is the number of bedrooms as provided by the agent or landlord. Options are: specific number; (U) unknown. A value of ‘0’ bedrooms may indicate a bedsitter or studio apartment or rented premises such as a garage or car space.
 6. **Weekly Rent** is the weekly paid amount.

| Column Header|Data type  |
|--|--|
|Lodgement Date|datetime64[US]  |
|Postcode|int64 |
|Dwelling Type|str |
|Bedrooms|str  |
|Weekly Rent|str  |



	 
