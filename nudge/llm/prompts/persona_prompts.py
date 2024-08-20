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
### Expert Psychologist Analysis for User Personality

As an expert psychologist, your task is to analyze and modify the user's persona based on their diary entries. Follow the detailed instructions below to ensure accurate and insightful results.

### Instructions:

**Modify Persona:**
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


### Context:

- **New Diary Entry:** {context}
- **Persona:** {persona}

{format_instructions}
"""