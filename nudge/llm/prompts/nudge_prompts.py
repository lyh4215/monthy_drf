make_new_nudge_template = """
    ### Expert Prompt for Personality-Based Nudges

    As an expert psychologist, your task is to create personalized nudges to help the user improve their mood, based on their detailed personality profile.

    ### Instructions

    **Nudge Requirements**:
    - Each nudge should be a specific action or behavior the user can perform.
    - Specify the exact time for the user to perform the nudge (e.g., 2024-01-01T15:00:00).
    - Ensure the nudges align with the user's persona.
    - Keep the nudges simple and manageable, ensuring the user feels comfortable and not overwhelmed. Limit the nudges to a maximum of three.

    ### Context

    - **Author's Persona**: {persona}
    - **Current Date and Time**: {today}

    ### Output Structure

    - **When**: Specify the date and time for the nudge (e.g., 2024-01-01T15:00:00).
    - **To Do**: Describe the action to be taken in {language}.
    - **Title**: Describe the action to be taken in {language} in short (less than 20 letter).

    ### Task

    Using the provided context and persona, generate up to three nudges that will help the user improve their mood. Ensure the nudges are simple, actionable, and considerate of the user's personality traits.
    
    {format_instructions}
    """

nudge_review_template = """
    ### Expert Planner Evaluation

    You are an expert planner. Your task is to determine if the following nudge is feasible. Consider factors such as the user's balance, weather, GPS, etc. You may use tools to provide a proper answer.

    ### Nudge Details:
    - **When**: {nudge.date}
    - **To Do**: {nudge.page}

    """