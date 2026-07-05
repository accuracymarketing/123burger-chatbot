import unittest

from restaurant_chatbot import answer_question


class RestaurantChatbotTests(unittest.TestCase):
    def test_answers_hours_question(self):
        answer = answer_question("What time do you close on Friday?")
        self.assertIn("Friday and Saturday", answer)
        self.assertIn("11:00 PM", answer)

    def test_answers_reservation_question(self):
        answer = answer_question("Can I book a table for 6?")
        self.assertIn("large groups", answer)
        self.assertIn("(+1) 919-679-7400", answer)

    def test_answers_dietary_question(self):
        answer = answer_question("Do you have vegan and gluten free food?")
        self.assertIn("dietary restrictions", answer)
        self.assertIn("allergies", answer)

    def test_answers_burger_prices(self):
        answer = answer_question("How much is a double cheeseburger combo?")
        self.assertIn("Double Cheeseburger", answer)
        self.assertIn("$14.99", answer)

    def test_chicken_does_not_trigger_greeting(self):
        answer = answer_question("Do you have chicken?")
        self.assertIn("Chicken Sandwich", answer)
        self.assertNotIn("Hello", answer)

    def test_unknown_question_lists_supported_topics(self):
        answer = answer_question("Do you sell branded candles?")
        self.assertIn("I am not completely sure", answer)
        self.assertIn("burger prices", answer)

    def test_goodbye_response(self):
        answer = answer_question("quit")
        self.assertIn("see you soon", answer)


if __name__ == "__main__":
    unittest.main()
