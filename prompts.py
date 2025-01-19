# Story generation prompts
STORY_ARCHITECT_TEMPLATE = """As a wise interpreter of the Bhagavad Gita, examine the theme '{theme}' \
and identify a pressing contemporary challenge that many people face today. \
Focus on a situation where modern life intersects with the eternal wisdom \
of the Gita. The challenge should:
1. Be a real-world situation that people commonly face today
2. Involve an ethical or spiritual dilemma that isn't easily solved
3. Mirror the depth of Arjuna's confusion in the Gita
4. Need guidance that the Gita's teachings could illuminate

Frame this in 2-3 sentences, emphasizing both the external situation \
and the internal struggle."""

CHARACTER_CREATOR_TEMPLATE = """For this modern situation: {core_story}
Create 3 essential characters that embody the dynamics found in the Bhagavad Gita:

1. A protagonist who, like Arjuna, faces a difficult choice and experiences confusion (dharma-sankata). \
They should be a relatable modern person dealing with real-world pressures.

2. A mentor figure who, like Krishna, can illuminate the situation through Gita's teachings. \
This should be someone who understands both modern life and timeless wisdom.

3. A supporting character who represents the worldly perspective and adds complexity to the situation.

For each character, describe:
- Their role in modern society
- Their internal conflicts
- Their perspective on the situation
- How they embody specific aspects of the Gita's teachings"""

PLOT_WEAVER_TEMPLATE = """Using this modern situation: {core_story}
And these characters: {characters}

Create a dynamic narrative that shows how the Bhagavad Gita's teachings can illuminate modern challenges. 
Structure it in these parts:

1. THE MODERN BATTLEFIELD (Setting & Conflict)
- Begin with an engaging scene that captures attention (avoid starting with desk/computer scenarios)
- Establish the contemporary situation through action or dialogue
- Show how modern pressures create confusion
- Highlight the parallel between this situation and Arjuna's dilemma

2. THE STRUGGLE (Initial Attempts)
- Show common worldly approaches to solving the problem
- Demonstrate why materialistic solutions fall short
- Reveal the deeper spiritual questions at play

3. GITA'S GUIDANCE (Wisdom Revealed)
- Introduce specific teachings from the Gita that apply to this situation
- Connect ancient wisdom to modern context
- Include relevant concepts such as:
  * Karma Yoga (selfless action)
  * Dharma (duty and righteousness)
  * Detachment from results
  * The eternal nature of the self

4. TRANSFORMATION (Resolution)
- Show how understanding the Gita's wisdom changes the perspective
- Demonstrate practical application of the teachings
- Reveal the universal truth within the particular situation"""

STYLIST_TEMPLATE = """Take this narrative: {narrative}

Transform it into a powerful story that bridges ancient wisdom and modern life. The story should:

1. AUTHENTICITY
- Maintain the philosophical depth of the Bhagavad Gita
- Include specific verses with their chapter and verse numbers
- Explain Sanskrit terms in accessible language

2. MODERN RELEVANCE
- Use contemporary language and diverse situations
- Open with a vivid scene that immediately draws readers in
- Make the wisdom practical and applicable
- Address real-world complexities

3. NARRATIVE STRUCTURE
- Begin in various settings (parks, cafes, workplaces, homes, etc.)
- Balance action, dialogue, and reflection
- Include meaningful conversations that echo Krishna-Arjuna dynamics
- Show both external events and internal transformation

4. WISDOM INTEGRATION
- Weave teachings naturally into the story
- Connect specific verses to modern challenges
- Show how eternal principles apply to temporary situations

Format the story with clear paragraphs, meaningful dialogue, and a length of 1500-2000 words. \
Include relevant verse references in (parentheses) where teachings are discussed."""

THEME_GENERATOR_TEMPLATE = """Generate exactly 5 moral themes from the Bhagavad Gita's teachings. \
Each theme must be on a new line and follow this exact format without any additional text:

'Theme Name (Sanskrit Term) - Brief one-sentence description'

Required format examples:
Duty (Karma Yoga) - The struggle of fulfilling one's responsibilities without attachment
Renunciation (Sanyasa Yoga) - A journey of letting go of worldly desires
Compassion (Karuna) - Acts of selfless love and kindness

Rules:
1. Each line must contain exactly one theme
2. Include the Sanskrit term in parentheses
3. Provide a clear, concise description after the hyphen
4. Do not add any additional text, numbers, or explanations
5. Do not use asterisks or other formatting

Generate 5 new themes now:""" 