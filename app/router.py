from semantic_router import Route
from semantic_router.routers import SemanticRouter
from semantic_router.encoders import HuggingFaceEncoder

encoder = HuggingFaceEncoder(
    name="sentence-transformers/all-MiniLM-L6-v2"
)

faq = Route(
    name='faq',
    utterances=[
        # Return & defective
        "What is the return policy?",
        "How many days do I have to return a product?",
        "Can I return an item after 30 days?",
        "What if I receive a damaged product?",
        "My product is defective, what should I do?",
        "I got a broken item, can I get refund?",
        "Policy on damaged or wrong product?",

        # Payment & discount
        "Do you accept UPI?",
        "What payment options are there?",
        "Can I pay with cash on delivery?",
        "Is there discount for HDFC card?",
        "Any offer on credit cards?",

        # Tracking & orders
        "How to track my order?",
        "Where is my package?",
        "When will my order arrive?",
        "Can I cancel my order?",
        "How to modify my order?",
        # Refund & promo
        "How long for refund?",
        "When will I get my money back?",
        "How to apply promo code?",
        "Where to enter coupon?",

        # Shipping & sales
        "Do you ship internationally?",
        "Any ongoing sales?",
        "Are there current promotions?",
        "What deals are running?",
    ]
)

sql = Route(
    name='sql',
    utterances=[
        "Show me Puma shoes",
        "Nike running shoes under 5000",
        "Any shoes on discount?",
        "Cheap formal shoes size 9",
        "Puma sneakers with good rating",
        "Adidas t-shirts on sale",
        "List watches under 3000",
        "Red shoes for women",
        "Black Nike sneakers",
        "Products with more than 40% off",
    ]
)

router = SemanticRouter(routes=[faq, sql], encoder=encoder,auto_sync="local")

if __name__ == "__main__":
    print(router("What is your policy on defective product?").name)
    print(router("Pink Puma shoes in price range 5000 to 1000").name)