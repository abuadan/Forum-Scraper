# Forum-Scraper
A Very Ugly immplentation of a forum scraper using Scrapy the first spider is focused on BitcoinTalk
# Schema for scraping https://bitcointalk.org

## Profiles
profile data can be found using the [bitcointalk sitemap](https://bitcointalk.org/sitemap.php), Profiles contain the following;

- Name
- URL
- ID
- Profile_info
  - Number of posts started
  - Number of posts participated in 
  - Merit (reputation)
  - Position (Member/Admin)
  - Date Registered
  - Last Activate (Not sure if date of last post or last online) 
  - ICQ
  - AIM
  - MSN
  - YIM
  - Email
  - Website
  - Current Status (Online/Offline at time of viewing)
  - Skype
  - Gender
  - Age
  - Location
  - Local Time
  - Signature

```json
{
  "user_name:"string",
  "profile_url:"string",
  "profile_id":"int",
  "profile_object:[
                    all_data_in_profile_table
                    ]
}
```

##Post

Unlike profiles these are harder to get at, these posts contain the following;

- URL
- Board
- Topic
- Post
    - Author
        - user_name
        - position
        - activity
        - merit
        -signature
    - Post Title
    - Post/Message
    - Time
    - Count 
    - Signature
- Advert
    
```json
{
	"url":"string",
	"board":"string",
	"topic":"string",
	"topic_id:"integer",
	"posts":
	[
		{
		"user_name":"string",
		"position":"string",
		"merit":"string",
		"signature":"string",
		"post_title":"string",
		"post":"string",
		"post_count":"integer",
		"links_mentioned":"string",
		"images":"byte",
		"signature":"string"
		},
		{
		"user_name":"string",
		"position":"string",
		"merit":"string",
		"signature":"string",
		"post_title":"string",
		"post":"string",
		"Time":"date_time",
		"post_count":"integer",
		"links_mentioned":"string",
		"images":"byte",
		"signature":"integer"
		}
	]
	"post_page":"integer",
	"advert":"string",
	"post_language":"string"
}
```
 
This is still a work in progress and no garuntee on how well it will work.
