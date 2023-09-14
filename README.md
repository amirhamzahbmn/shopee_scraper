# Shopee_scraper

A simple script that scrapes product details from shopee based on 2 variables:
  - Keyword search terms
  - Number of pages 

The script opens up chrome to which it will then immediately go to the Shopee website. It will start to search based on what keywords you have inputted and then sort the products by sales. It will then go through each product tile one by one, if multiple pages were requested, it will keep going until the number of pages were met.

The following info is scraped:
  - Name
  - Initial cost
  - Item cost
  - Discount percentage
  - Item sales per month
  - Item location
  - Link

The data is then saved in a csd file in the same directory.

Note:
Script has been written and tested based only on the time it was made. Whatever changes they have made in the website would render this script obsolete. Even so, selenium as a whole is much slower than utilizing Requests or Shopee's API, which is conveniently done in my new Shopee_scraperv2 repo. Do check it out!
