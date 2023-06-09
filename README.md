# HP Solve Final Submission by Gulafsha Ahmed

This is a solution to the HP Solve 2023, Round - II. 

## Table of contents

- [Overview](#overview)
  - [The challenge](#the-challenge)
  - [Screenshot](#screenshot)
  - [Links](#links)
- [My process](#my-process)
  - [Built with](#built-with)
  - [What I learned](#what-i-learned)
  - [Useful resources](#useful-resources)
- [Implementation Steps](#implementation-steps)
- [Author](#author)


## Overview

### The challenge

Understanding customer sentiments about products is of utmost priority for any product company including HP. Consumers are more vocal on social media platforms and express their feedback and experience about any product. HP too needs to know consumer sentiments first-hand so that it can make better products with great user experience and resolve customer issue faster. 
HP needs a one stop knowledge store, which can store reviews, suggestions, complaint and sentiments for all HP consumer printers/PC/laptop. This will help HP understand the consumers better and improve brand value and NPS score.

### Screenshot

![Sample Input](https://github.com/pyjamaSamm/HpSolve_Solution/assets/74822950/03f6d09f-b4b6-4ce5-a31c-1cf37fc6ea5a)
![Sample Output](https://github.com/pyjamaSamm/HpSolve_Solution/assets/74822950/fd39cb2a-4c41-4d54-a946-d8208772e6ff)


### Links

- Demonstration video: [Drive link](https://drive.google.com/drive/folders/1liWbFWzxck2sSO3rnE8uyRoebfeGYg7f)

## My process

### Built with

* Python 
* Libraries:
    * nltk
    * textBlob
    * flask
    * networkx
    * tweepy

My proposed solution involves:

* Data Collection
* Data Processing
* Text Classification
* Knowledge Graph Construction
* Web API Development

### What I learned

In this project, I have gained valuable insights into the practical implementation of APIs for data collection. I have acquired hands-on experience in utilizing natural language processing techniques to analyze textual data. Specifically, I have explored sentiment analysis and its significance in product development and improvement. Additionally, I have developed a knowledge graph that enhances the response capabilities for diverse queries. Throughout the project, I have also familiarized myself with various libraries and packages relevant to these tasks, expanding my toolkit for future projects.

### Useful resources

- [Hubspot blog](https://blog.hubspot.com/service/social-media-customer-feedback)
- [Google](https://support.google.com/knowledgepanel/answer/9787176?hl=en)
- [Twitter Developer Platform](https://developer.twitter.com/en)

## Implementation Steps

1. Create a Twitter developer's account and get the consumer key, consumer secret key, access token and access secret token.
2. Replace the respective values in the code.
3. Step 1 and 2 can be omitted for the purpose of demonstration. The program can be executed with dummy data which is already available in the code.
4. Copy the entire code in any IDE.
5. Install the necessary libraries.
6. Create a directory called 'templates' and add form.html. This directory is on the same level as the python program.
7. Run the python program. A development server gets launched.
8. Enter any query like "List all posts talking about wifi issues in printer model X or brand Y". The respective response will be displayed.

## Author
- LinkedIn - [Gulafsha Ahmed](https://www.linkedin.com/in/gulafshaahmed)
- Email - gulafsha1024ahmed@gmail.com
