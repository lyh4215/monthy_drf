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