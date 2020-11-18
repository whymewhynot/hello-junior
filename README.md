# Hello Junior
Django project: IT job search website for junior specialists. Deployed to Heroku: https://hello-junior.herokuapp.com/

### Overview ###
* Backend: Django
* Frontend: [Jetapo Bootstrap Template](https://themeforest.net/item/jetapo-job-board-bootstrap-4-template/26745464)
* Auto updated content using [HeadHunter API](https://github.com/hhru/api) - `update_jobs_db.py`
* Newsletter using [Mailchimp API](https://mailchimp.com/developer/api/marketing/) `newsletter.py` and subscribers list update `update_subscribers.py`

### Django features ###
* ListView, DetailView
* Pagination
* Filtering system
* Custom user model
* Login, Logout, Registration, Password reset, Password change
* User's profile with search preferences and subscription/unsubscription
* Personal feed
* Favorites
* Pageview counters
* Login required content
