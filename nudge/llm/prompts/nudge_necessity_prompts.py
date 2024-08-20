depression_rate_template = """
### Expert Psychologist Analysis for User Personality and Depression Rate

As an expert psychologist, your task is to analyze the author's depression rate based on author's diary entry and persona. Follow the detailed instructions below to ensure accurate and insightful results.

### Instructions:
**Determine Depression Rate:**
   - Assess the author's depression rate on a scale of 0 to 1.
   - No need to explain the reasons for your modifications.
    
### Context:

- **Today Post:** {context}
- **Persona:** {persona}

{format_instructions}
"""

nudge_necessity_template = """
### Expert Psychologist Analysis for User Personality and Nudge Necessity

As an expert psychologist, your task is to analyze the author's nudge necessity based on author's post(diary) and persona. Follow the detailed instructions below to ensure accurate and insightful results.

### Instructions:
**Determine Nudge Necessity:**
   - If the user feels feelings of lack of guidance, fatigue, or anxiety, it is determined that a nudge is necessary.
   - No need to explain the reasons for your modifications.
   - Consider the recent posts to determine the nudge necessity and to understand the context of the user.
### Context:
- **Today Post:** {context}
- **Persona:** {persona}
- **Recent Posts:** {recent_posts}

{format_instructions}
"""
