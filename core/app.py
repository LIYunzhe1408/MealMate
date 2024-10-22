import yaml
from autogen import ConversableAgent
import sys
import os


def read_prompt(path):
    """
    Read all prompt from yaml file
    :param path: [string] Yaml file path
    :return: All prompt for agents
    """
    with open(path, 'r') as f:
        return yaml.safe_load(f)


# TODO Add interaction with database to check stock availability.
def check_availability(ingredients: list) -> list:
    """
    Check availability based on real-time stock.
    :param ingredients: [list] It should be a list of dict with name, quantity, and brand if applicable.
    :return: [list] Applicable list
    """
    print("========================================")
    print("Checking")

    for ingredient in ingredients:
        ingredient["availability"] = True

        # Check stock
        print(ingredient)

    return ingredients


def main(user_query, sys_msg):
    """
    Initiate chat workflow, return back applicable shopping list.
    :param user_query: [string]
    :param sys_msg: [dict] System message for agents.
    :return:
    """
    llm_config = {"config_list": [{"model": "gpt-4o-mini", "api_key": os.environ.get("OPENAI_API_KEY")}]}

    # Define customer manager to chat with customers and other staff.
    customer_manager = ConversableAgent(name="customer_manager_agent",
                                        system_message=sys_msg["customer_manager"],
                                        llm_config=llm_config)

    # Define chef de cuisine to break down recipe.
    chef_de_cuisine = ConversableAgent(name="chef_de_cuisine",
                                       system_message=sys_msg["chef_de_cuisine"],
                                       llm_config=llm_config,
                                       human_input_mode="NEVER",
                                       max_consecutive_auto_reply=1)

    # Define line cook to check ingredient availability.
    line_cook = ConversableAgent(name="line_cook",
                                 system_message=sys_msg["line_cook"],
                                 llm_config=llm_config,
                                 human_input_mode="NEVER",
                                 max_consecutive_auto_reply=1)

    line_cook.register_for_llm(name="check_availability",
                               description="Fetch ingredients availability for the recipe.")(check_availability)
    customer_manager.register_for_execution(name="check_availability")(check_availability)

    result = customer_manager.initiate_chats(
        [
            {
                "recipient": chef_de_cuisine,
                "message": user_query,
                "max_turns": 1,
                "summary_args": {
                    "summary_prompt": "Only keep ingredient list."},
            },
            {
                "recipient": line_cook,
                "message": "This is the recipe ingredient list, please check availability",
                "max_turns": 2,
                "summary_args": {
                    "summary_prompt": "Make the response as a jason file"},
            }
        ]
    )
    print(result[1].summary)
    return result


if __name__ == "__main__":
    prompt_path = "../assets/prompt.yaml"
    prompt_bank = read_prompt(prompt_path)

    try:
        query = sys.argv[1]
    except IndexError:
        query = prompt_bank["user_query"]

    main(query, prompt_bank["sys_msg"])
