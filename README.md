# RelevanceSearch
This is an assignment for Big Data Analysis course that calculate the relevant documents for searched query using AWS. Used CloudShell to write and debug python codes.

1. s3 buckets are:
  a. https://document-titles.s3.amazonaws.com/document-titles.csv
  b. https://tfidf-lab6.s3.amazonaws.com/tfidf.csv
  If is not feasible, csv files used are kept in data folder.
2. Import those two S3 data sources to create two DynamoDB tables, tfidf-5330 (keys are term, docid) and doctitle-lab6 to
hold the data. 
3. Created a Lambda function that incorporates your search code so it accepts a query string as input and produces HTML as output.
4. Created a file search.html that calls your Lambda functon and renders the HTML.
