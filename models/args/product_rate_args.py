from sqlalchemy import UniqueConstraint, CheckConstraint


# one user can rate one product only
rate_unique_user_product = (
    UniqueConstraint(
        "user_id",
        "product_id",
        name="unique_user_product_rate"
    ),
)



# rating must be between 1 and 5
rate_rating_range = (
    CheckConstraint(
        "rating >= 1 AND rating <= 5",
        name="check_rating_range"
    ),
)