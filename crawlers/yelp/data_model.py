from dataclasses import dataclass

@dataclass
class ReviewData:
    reviewer_name: str
    reviewe_location: str
    review_date: str
@dataclass
class MainPageData:
    name: str
    yelp_url: str
    rating: float
    number_of_reviews: int
    reviews : list[ReviewData]
