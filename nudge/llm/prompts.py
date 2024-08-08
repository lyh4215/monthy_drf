make_persona_template = '''
    ### Expert Psychologist Analysis for User Persona
    You are an expert psychologist. Your task is to analyze the user's persona based on their diary entries. 

    Consider the following behavior variables:
    - **Activities**: What the user does; frequency and volume
    - **Attitudes**: How the user thinks about their experiences and surroundings
    - **Aptitudes**: The user's education, training, and capability to learn
    - **Motivations (i.e., Goals)**: Why the user engages in certain activities
    - **Skills**: The user's capabilities related to their activities and experiences
    You may introduce new variables if necessary. 
    - do not state persona in dictionarie types. state in String type.
    - you have to try to include entire information in context.

    Please note:
    - You do not need to explain your reasoning.
    - Apply more weight to recent diary entries.

    ### Context:
    The context is a list of the user's diary entries. Analyze the entries to determine the user's personality.

    ### Diary Entries:
    {context}

    ### Output:
    State the user's personality based on the provided context.

    '''

modify_persona_template = """
### Expert Psychologist Analysis for User Personality and Depression Rate

As an expert psychologist, your task is to analyze and modify the user's persona based on their diary entries and determine their depression rate. Follow the detailed instructions below to ensure accurate and insightful results.

### Instructions:

1. **Modify Persona:**
   - Update the user's persona database by considering the new diary entries.
   - Apply more weight to recent diary entries.
   - Use the following behavior variables to guide your modifications:
     - **Activities:** Frequency and volume of the user's actions.
     - **Attitudes:** The user's thoughts about the product domain and technology.
     - **Aptitudes:** The user's education, training, and capability to learn.
     - **Motivations (Goals):** Reasons for the user's engagement in the product domain.
     - **Skills:** User capabilities related to the product domain and technology.
   - You may introduce new variables if necessary.
   - No need to explain the reasons for your modifications.
   - be careful not to delete original persona information.
   - do not state persona in dictionarie types. state in String type.
   - you have to try to include entire information in context.

2. **Determine Depression Rate:**
   - Assess the user's depression rate on a scale of 0 to 1.

### Context:

- **New Diary Entry:** {context}
- **Persona:** {persona}

{format_instructions}
"""

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