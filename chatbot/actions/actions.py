# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormValidationAction, SlotSet

from actions.recommandation import lookup_item, cosine_explore, inventory

#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []


class ActionFetchRecommandation(Action):
    def name(self) -> Text:
        return "action_fetch_recommandation"

    def fetch_recommandation(self, user_message):
        # Fetch recommandation from database
        item = lookup_item(user_message)
        if item[0] is False:
            print("Item not found")
            print("Fetching recommandation...")
            recommandation = cosine_explore(user_message)
            return recommandation
        else:
            print("Item found")
            # print(f'Item: {item}')
            recommandation = cosine_explore(user_message)
            print(f"Recommandation: {recommandation} for user message: {user_message}")
            return recommandation

    def run(
        self, dispatcher, tracker, domain
    ):  # this method is called when the agent calls the action
        print("ActionFetchRecommandation is running")
        
        print(f"Slots are : {tracker.slots}")
        print(f'User dish: {tracker.slots["menu_item"]}')
        menu_item = tracker.slots["menu_item"].capitalize()
        
        top3_recommanded_items = self.fetch_recommandation(menu_item)
        print(f"Top 3 recommanded items: {top3_recommanded_items}")
        print("ActionFetchRecommandation done")
        print("--" * 20)
        
        return [
            SlotSet(
                "recommanded_items",
                (
                    top3_recommanded_items
                    if top3_recommanded_items
                    else "No recommandation found"
                ),
            )
        ]


class ActionSetUserChoice(Action):
    def name(self) -> Text:
        return "action_set_user_choice"

    # this method is called when the agent calls the action
    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:

        print("ActionSetUserChoice is running")
        print(f"Slots are : {tracker.slots}")
        user_message = tracker.latest_message.get("text")
        print(f"User message: {user_message}")
        print("--" * 20)

        # store the recommended items
        recommanded_items = tracker.slots["recommanded_items"]

        """ # utter the message to ask the user for his chosen item
        dispatched_message = f"Here are the top 3 recommanded items: {recommanded_items}. Please choose one of them"
        print(dispatched_message)
        dispatcher.utter_message(text=dispatched_message) 

        user_message = tracker.latest_message.get("text")
        print(f"User message: {user_message}")
        print("--" * 20)"""

        user_choice = user_message if user_message in recommanded_items else None

        # extract the chosen item from the user message and set it in the slot
        print(f"Extracted item {user_choice} from message {user_message}")
        print("ActionSetUserChoice done")
        print("--" * 20)
        return [
            SlotSet(
            "user_choice", 
            user_choice if user_choice else None
            )]


class ValidateHandleRecommandationForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_handle_recommandation_form"

    async def validate_user_choice(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        
        print("Action ValidateHandleRecommandationForm is running")
        print("Validating chosen item ...")
        print(f"Slots are : {tracker.slots}")
        user_message = tracker.latest_message.get("text")
        print(f"User message: {user_message}")
        print("--" * 20)

        # check if the slotted user_choice is correct
        user_choice = tracker.slots["user_choice"]
        print(f"Chosen item: {user_choice}")
        
        if user_choice and user_choice[0].islower():
            print("First letter of chosen item is lowercase")
            print("Slot value will be set to correct value")
            print("Action ValidateHandleRecommandationForm done")
            print("--" * 20)
            return {"user_choice": user_choice.capitalize()}
        else:
            print("First letter of chosen item is not lowercase")
            print("Slot value will be set to chosen item")
            print("Action ValidateHandleRecommandationForm done")
            print("--" * 20)
            return {"user_choice": user_choice}
        
 