# Posse_Porject1
Capstone Project 1

Posse:
"Carefully talk about what's on your mind and say what's on your mind"

A blog post webapp that analyses a users sentiment towards their discussed topics and allows other users to interact through a poll range of how much they agree with the post. It then provides users with analytics on that post and how the average user feels about that post. Users can also see how might other users interact with other posts.

Through sentiment analysis, any post users post get graded based on how the API analyses their text structure. The text analysis also provides us with the topics being discussed in each post. This allows us to take note of hwo this user may feel about this particular topic in that given post.

Users can also directly respond to posts via their own post to provide a greater emphasis on their thoughts about that particular post. If they feel comments may be more beneficial, that is an option as well. This direct response, can be found on the regular home page indicated with a response arrow, which users can interact with to directly take them to the post being responded to.

If a user is further intigued by a post, their is a 'more on this' option when viewing the full posts. This 'more' section shows other posts that may have mentioned the link, the post, or the topic that that post is tied to. This is so that users can explore what others may have to say about those posts' contents.

Posts that have garnered a substantial amount of interactions (poll responses + comments) are considered relevant posts. These relevant posts are then linked to other posts like it that share the same topics. These posts are then connected together and are presented in the homepage as 'joint-posts' as long as they are completely of opposite sentiments. This is so that posts that are clearly being discussed are not stand alone and the other side of the argument is readily available. The goal is that both sides of an argument, no matter the topic, is deserving of being heard. It is in hopes of having a more open and clearer view of social media.

----------------------------------------------------------------------------------------------------------------------------

Things not implemented but would want to work on later:
1. Follow system; fully understand how it works just did not thing it was an important function to do immediately.
2. Search bar; Allows searches of topics, users, etc.
3. Filter based on topics; View different posts based on topics. There are buttons on each user profile that shows their last discussed topics and that would be a great place to start.
----------------------------------------------------------------------------------------------------------------------------

API used:
----------------------------------------------------------------------------------------------------------------------------
MeaningCloud: (https://www.meaningcloud.com/, Sentiment Analysis)
  Note: There are only 100 requests per month
  
Link Preview: (https://api.linkpreview.net, Link Preview Generator)
  Note: There are only 100 requests per day
----------------------------------------------------------------------------------------------------------------------------

Tech Stack:
Python, HTML/JS/CSS, Jquery, AJAX, SQLAlchemy, PostgreSQL, Bootstrap, MeaningCloud API, LinkPreview API 
